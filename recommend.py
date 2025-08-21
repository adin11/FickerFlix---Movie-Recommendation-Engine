import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import save_npz
import ast
import nltk

# Download required NLTK resources
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Function for loading the data
def load_data():
    print("Loading Data...")
    df = pd.read_csv('processed_movies.csv')
    print(f"Rows and columns of the data {df.shape}")
    print(df.head(3))
    return df

# Function for pre processing the metadata
def pre_process_data(df):
    print("Pre-processing the data...")
    df = df.dropna(subset=['title'])
    df = df.drop_duplicates(subset=['title'])

    df['year'] = pd.to_datetime(df['year']).dt.year
    df['year'] = df['year'].astype(str)

    df['genres'] = df['genres'].apply(ast.literal_eval)
    df['cast'] = df['cast'].apply(ast.literal_eval)

    df['genres_str'] = df['genres'].apply(lambda x: ' '.join(x))
    df['cast_str'] = df['cast'].apply(lambda x: ' '.join(x))

    df['all_text'] = (
        df['year'] + ' ' + 
        df['overview'] + ' ' + 
        df['genres_str'] + ' ' + 
        df['cast_str'] + ' ' + 
        df['director'] + ' ' + 
        df['original_language']
    )
    print(df.head(3))
    return df

# Function for NLTK pre-processing
def apply_nltk_preprocessing(df):
    print("Applying NLTK Preprocessing...")
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    def clean_text(text):
        tokens = word_tokenize(text.lower())                # tokenize + lowercase
        tokens = [t for t in tokens if t.isalpha()]         # keep only words (remove punctuation/numbers)
        tokens = [t for t in tokens if t not in stop_words] # remove stopwords
        tokens = [lemmatizer.lemmatize(t) for t in tokens]  # lemmatization
        return ' '.join(tokens)

    df['all_text'] = df['all_text'].apply(clean_text)
    print(df['all_text'].head(3))
    return df

# Function for tf-idf Vectorization
def vectorize_scaling(df):
    vectorizer = TfidfVectorizer()
    print("Converting to tfidf matrix")
    tfidf_matrix = vectorizer.fit_transform(df['all_text'])
    print(tfidf_matrix.shape)
    return tfidf_matrix

# Function for generating recommendations
def recommend(df, movie_name, tfidf_matrix, top_n):
    if movie_name in df['title'].values:
        index = df[df['title'] == movie_name].index[0]
        distances = cosine_similarity(tfidf_matrix[index], tfidf_matrix).flatten()
        sorted_distances = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:top_n+1]
        print(f"Here are your suggested movies for {movie_name}:")
        for i in sorted_distances:
            print(df.iloc[i[0]].title)
    else:
        print("Movie not found")

# Main funtion for Binding all the logic
def main():
    df = load_data()
    df = pre_process_data(df)
    df = apply_nltk_preprocessing(df)   
    tfidf_matrix = vectorize_scaling(df)
    recommend(df, '3 Idiots', tfidf_matrix, 5)
    save_npz("tfidf_matrix1.npz", tfidf_matrix)
    print("✅ Saved all components successfully.")

if __name__ == "__main__":
    main()
