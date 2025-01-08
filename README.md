# Movie Recommendation System

This repository implements a **Movie Recommendation System** using Neo4j and Python. The system provides recommendations based on two approaches:

1. **Content-Based Filtering**: Finds movies similar to a given movie based on shared genres.
2. **Collaborative Filtering**: Suggests movies based on user behavior and ratings.

---

## Features

- **Data Loading**: Reads movie metadata and user ratings from CSV files.
- **Neo4j Integration**: Stores movies, users, and their relationships in a Neo4j graph database.
- **Recommendation System**:
  - Content-based recommendations by matching genres.
  - Collaborative filtering recommendations by finding similar users.
- **Secure Credentials**: Uses a `.env` file to manage sensitive information securely.

---

## Repository Structure

```plaintext
Movie-Recommendation-iCog-week-4/
├── data/
│   ├── movies_metadata.csv          # Sample movie metadata
│   ├── ratings_small.csv            # Sample user ratings
├── script.py                        # Main Python script
├── .env                             # Environment variables (not included in repo)
├── .gitignore                       # Git ignore file
└── README.md                        # This file
```

---

## Requirements

- Python 3.7+
- Neo4j Community or Enterprise Edition

### Python Packages

- `neo4j`
- `pandas`
- `python-dotenv`

Install the required packages using:

```bash
pip install -r requirements.txt
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/abenaacs/Movie-Recommendation-iCog-week-4.git
cd Movie-Recommendation-iCog-week-4
```

### 2. Set Up Neo4j

- Install Neo4j from [Neo4j Downloads](https://neo4j.com/download/).
- Start your Neo4j database and access the Neo4j Browser at `http://localhost:7474`.
- Set up the default username (`neo4j`) and password.

### 3. Add the `.env` File

Create a `.env` file in the root directory with the following content:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password_here
```

Replace `your_password_here` with your Neo4j password.

### 4. Add the Data Files

Place your datasets (`movies_metadata.csv` and `ratings_small.csv`) in the `data/` directory.

---

## How to Run the Script

1. Ensure Neo4j is running locally.
2. Run the Python script:

```bash
python script.py
```

3. The script will:
   - Load data into Neo4j.
   - Create `SIMILAR` relationships for movies with the same genres.
   - Generate recommendations based on content or collaboration.

---

## Example Usage

The `get_recommendations` function combines content-based and collaborative filtering.

```python
print("Recommendations:", get_recommendations(user_id="3", movie_id="652"))
```

- **Input**: `user_id="3"`, `movie_id="652"`
- **Output**: List of recommended movie titles.

---

## Security Note

To secure your credentials:

1. Store them in the `.env` file.
2. Add `.env` to `.gitignore` to prevent exposing sensitive information in your repository.

---

## Future Improvements

- Expand the dataset for more robust recommendations.
- Use advanced collaborative filtering techniques (e.g., matrix factorization).
- Add a web interface for user interaction.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

Developed by [Abenezer Nigussie](https://github.com/abenaacs).

---

## Acknowledgments

- [Neo4j](https://neo4j.com/) for the graph database.
- [The Kaggel site](https://www.kaggle.com/code/rounakbanik/movie-recommender-systems/input) for the dataset.
- iCog Labs for Week 4 training and support.
