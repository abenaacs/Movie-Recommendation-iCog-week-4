from neo4j import GraphDatabase
from dotenv import load_dotenv
import pandas as pd
import os

# Load environment variables from .env file
load_dotenv()

# Neo4j connection details from environment variables
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Initialize Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# File paths
current_dir = os.getcwd()

# Load a sample of the dataset
chunk_size = 2000

input_metadata_path = os.path.join(current_dir, "./data/movies_metadata.csv")
rating_path = os.path.join(current_dir, "./data/ratings_small.csv")

# Load and process data
movies_df = pd.read_csv(input_metadata_path, nrows=chunk_size)
ratings_df = pd.read_csv(rating_path, nrows=chunk_size)

# Clean data (ensure IDs are strings for consistency)
movies_df["id"] = movies_df["id"].astype(str)
ratings_df["movieId"] = ratings_df["movieId"].astype(str)
ratings_df["userId"] = ratings_df["userId"].astype(str)


# Function to create Movie nodes
def create_movies(tx, movies):
    for _, row in movies.iterrows():
        tx.run(
            """
            MERGE (m:Movie {id: $id})
            SET m.title = $title, m.genres = $genres
            """,
            id=row["id"],
            title=row["title"],
            genres=row["genres"],
        )


# Function to create User nodes and RATED relationships
def create_ratings(tx, ratings):
    for _, row in ratings.iterrows():
        tx.run(
            """
            MERGE (u:User {id: $user_id})
            MERGE (m:Movie {id: $movie_id})
            MERGE (u)-[:RATED {rating: $rating}]->(m)
            """,
            user_id=row["userId"],
            movie_id=row["movieId"],
            rating=row["rating"],
        )


def create_similar_relationships_in_batches(session, batch_size=2000):
    """
    Create SIMILAR relationships between Movie nodes with the same genres in batches.
    """
    offset = 0
    while True:
        # Use batching to process chunks of nodes
        query = f"""
        MATCH (m1:Movie)
        WITH m1
        SKIP {offset} LIMIT {batch_size}
        MATCH (m2:Movie)
        WHERE m1.id <> m2.id AND m1.genres = m2.genres
        MERGE (m1)-[:SIMILAR]-(m2)
        """

        # Execute the query for the current batch
        result = session.run(query)

        # Check if the batch contains any nodes
        if result.peek() is None:  # No more data to process
            break

        # Move to the next batch
        offset += batch_size


# Load data into Neo4j
with driver.session() as session:
    session.execute_write(create_movies, movies_df[["id", "title", "genres"]])
    session.execute_write(create_ratings, ratings_df[["userId", "movieId", "rating"]])
    session.execute_write(create_similar_relationships_in_batches)


# Content-Based Filtering: Find similar movies by genres
def recommend_by_content(tx, movie_id):
    result = tx.run(
        """
        MATCH (m1:Movie {id: $movie_id})-[:SIMILAR]-(m2:Movie)
        RETURN m2.title AS recommendation, m2.genres AS genres
        ORDER BY m2.title
        LIMIT 5
        """,
        movie_id=movie_id,
    )
    return [record["recommendation"] for record in result]


# Collaborative Filtering: Find similar users and recommend their highly rated movies
def recommend_by_collaboration(tx, user_id):
    result = tx.run(
        """
        MATCH (u1:User {id: $user_id})-[:RATED]->(m:Movie)<-[:RATED]-(u2:User)
        WITH u1, u2, COUNT(*) AS shared_movies
        ORDER BY shared_movies DESC
        LIMIT 5
        MATCH (u2)-[:RATED]->(rec:Movie)
        WHERE NOT EXISTS {
            MATCH (u1)-[:RATED]->(rec)
        }
        RETURN rec.title AS recommendation
        LIMIT 5
        """,
        user_id=user_id,
    )
    return [record["recommendation"] for record in result]


# Recommendation System
def get_recommendations(user_id, movie_id):
    with driver.session() as session:
        # Try content-based filtering first
        recommendations = session.execute_read(recommend_by_content, movie_id)
        if recommendations:
            return recommendations

        # Fallback to collaborative filtering
        return session.execute_read(recommend_by_collaboration, user_id)


# Example usage
print("Recommendations:", get_recommendations(user_id="123", movie_id="652"))

# Close the Neo4j driver
driver.close()
