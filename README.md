# 🎬 Flicker-Flix: Personalized Movie Recommendation System
### 🔗 Live App:[FlickerFlix](https://flickerflix.streamlit.app/)

---
## 📌 Project Overview

This is a **content-based movie recommendation system** designed to assist users to watch similar movies based on their cinema taste. Unlike many similar projects that rely on static or limited datasets, this project uses **self-scraped 2 lakh+ movie metadata** from TMDB API to provide **highly adaptable and accurate recommendations**.

This is an **End-to-End** Project where we web-scraped the data using `requests` module, applied pre-processing techniques like lemmatization using `Nltk`module and calculated cosine similairty using tf-idf matrix.

## How this system is different from other recommendation sytems❓
Most existing recommendation systems available use the pre-existing old kaggle dataset, whereas in this project we used our own custom self scraped movie meta-data which consists of more up-to-date data. Instead of countvectorizer we used tf-idf vectorizer which uses a slighlty efficient approach and assigns more weight to words with less frequency. We applied lemmatization rather than stemming to keep the base words grammar perfect


---
## 📽️ Video Overview

https://github.com/user-attachments/assets/9b85a021-401a-4c01-93ba-3f2e34f34e48

---

## 🧠 Technical Details

This project uses a **Content-Based Filtering** technique. Here's how it works:

1. **Data Collection & Cleaning**:  
   - 2lakh Movie metadata scraped from TMDB Api.
   - Includes genres, keywords, cast, crew, and overviews.

2. **Metadata Tag Creation**:  
   - Combined relevant features into a single `all_text` column.
   - Cleaned and normalized text (e.g., lowercase, stemming, removing spaces).

3. **NLTK Pre-processing**:
   - Used NLTK library to perfrom lemmatization, lowercasing and stopwards removal
   - Removed the stopwords from the combined text

4. **Vectorization & Similarity Calculation**:  
   - Used **TF-IDF** to convert `all_text` column into a numerical matrix.
   - Calculated **cosine similarity** between movies based on tag vectors.
   - Stored similarity scores and movie metadata into a serialized `.npz` file for faster loading.

5. **Recommendation Logic**:  
   - User searches from a movie.
   - The app fetches the top N most similar movies from the precomputed similarity matrix.
   - Displays the recommended movies on the screen

---

## 📁 Repository Contents

| File/Folder | Description |
|-------------|-------------|
| `app.py` | Main Streamlit script for UI and recommendation logic |
| `processes_movies.csv` | Our self-scraped dataset |
| `tfidf matrix.npz` | Precomputed tf-idf similarity matrix |
| `recommend.py` | Script for re-training the recommender on new data for re-producibility |
| `all_scraper` | Script used to scrape latest movie data |


---

## 🛠️ Tech Stack

- **Python**
- **Pandas**, **NumPy**
- **Scikit-learn** (TFIDF Vectorizer, Cosine Similarity)
- **SciPy** (for serializing the tfidf matrix in npz format)
- **Streamlit** (Frontend & UI)
- **TMDb API** (for fetching movie metadata)
- **Streamlit Community Cloud** (for quick deployment)
- **Uptime Robot** (For pinging the /heathcheck endpoint to avoid cold start)

---

## Future Improvements
1. Add user authentication on the site and save the user performance history.
2. Train a collaborative system using user-user or item-item data.
3. Build a hybrid system which recommends similar movies based on both **Content as well as collaborative filtering.**

---

## Running the Project Locally

1. Clone the repository
2. Navigate to the current directory
3. Run the app.py file using `streamlit run app.py`
