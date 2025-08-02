# 🎬 Flicker-Flix: Personalized Movie Recommendation System
> **🔗 Live App:** [Add your Railway URL here]
---
## 📌 Project Overview

This is a **content-based movie recommendation system** designed to assist users to watch similar movies based on thier cinema taste. Unlike many similar projects that rely on static or limited datasets, this project uses **self-scraped 1 lakh+ movie metadata** to provide **highly adaptable and accurate recommendations**.

It features a clean and simple **Streamlit UI**, allowing users to search for any movie and receive personalized recommendations based on content similarity — not ratings or user behavior.

---

## 📽️ Video Overview
<!-- Embed or link a demo walkthrough video here -->
**(Coming soon)**

---

## 🧠 Technical Details

This project uses a **Content-Based Filtering** technique. Here's how it works:

1. **Data Collection & Cleaning**:  
   - Movie metadata scraped from TMDb, IMDb, etc.
   - Includes genres, keywords, cast, crew, and overviews.

2. **Metadata Tag Creation**:  
   - Combined relevant features into a single `tag` column.
   - Cleaned and normalized text (e.g., lowercase, stemming, removing spaces).

3. **Vectorization & Similarity Calculation**:  
   - Used **CountVectorizer** to convert `tag` text into a numerical matrix.
   - Calculated **cosine similarity** between movies based on tag vectors.
   - Stored similarity scores and movie metadata into a serialized `.pkl` file for faster loading.

4. **Recommendation Logic**:  
   - User selects a movie from the dropdown.
   - The app fetches the top N most similar movies from the precomputed similarity matrix.
   - Poster images are fetched dynamically using the TMDb API.

---

## 📁 Repository Contents

| File/Folder | Description |
|-------------|-------------|
| `app.py` | Main Streamlit script for UI and recommendation logic |
| `processes_movies.pkl` | Processed movie metadata with tags |
| `final_matrix.pkl` | Precomputed cosine similarity matrix |
| `recommend.py` | Script for re-training the recommender on new data for re-producibility |
| `all_scraper` | Script used to scrape latest movie data |
| `README.md` | You’re reading it! |

---

## 🛠️ Tech Stack

- **Python**
- **Pandas**, **NumPy**
- **Scikit-learn** (CountVectorizer, Cosine Similarity)
- **Streamlit** (Frontend & UI)
- **TMDb API** (for fetching movie posters)
- **Pickle** (for serialized fast-loading models)

---

## 🚀 Running the Project Locally

```bash
# Clone the repository
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
