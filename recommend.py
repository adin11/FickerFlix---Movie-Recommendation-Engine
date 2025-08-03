import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import ast
import joblib

def load_data():
    print("Loading Data...")
    df = pd.read_csv('all_movie_data.csv')
    print(f"Rows and columns of the data {df.shape}")
    print(df.head(3))
    return df

# Function for pre-processig the data
def pre_process_data(df):
    print("Pre-processing the data...")
    df = df.dropna(subset=['title'])
    df = df.drop_duplicates(subset=['title'])
    
    df['year'] = pd.to_datetime(df['year']).dt.year
    df['year'] = df['year'].astype(str)

    df['genres']= df['genres'].apply(ast.literal_eval)
    df['cast']= df['cast'].apply(ast.literal_eval)

    df['genres_str'] = df['genres'].apply(lambda x: ' '.join(x))
    df['cast_str']   = df['cast'].apply(lambda x: ' '.join(x))  
    df['all_text']   = df['year']+ ' ' + df['overview'] + ' ' + df['genres_str'] + ' ' + df['cast_str'] + ' ' + df['director'] + ' ' + df['original_language']
    
    print(df.head(3))
    return df

# Function for vectorizing and scaling.
def vectorize_scaling(df):
    vectorizer = TfidfVectorizer(stop_words='english')
    print("Converting to tfidf matrix")
    tfidf_matrix = vectorizer.fit_transform(df['all_text'])
    print(tfidf_matrix.shape)
    
    return tfidf_matrix

# Function for recommending movies
def recommend(df,movie_name,tfidf_matrix,top_n):
    if movie_name in df['title'].values:
        index = df[df['title']==movie_name].index[0]
        distances = cosine_similarity(tfidf_matrix[index], tfidf_matrix).flatten()
        sorted_distances = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:top_n+1]
        
        print(f"Here are your suggested movies for {movie_name} ")
        for i in sorted_distances:
            print(df.iloc[i[0]].title)

    else:
        print("Movie not found")


# Main fucntion
def main():
    df = load_data()
    df = pre_process_data(df)
    tfidf_matrix = vectorize_scaling(df)
    recommend(df,'3 Idiots',tfidf_matrix,5)

    df.to_csv('processed_movies.csv',index=False)
    joblib.dump(tfidf_matrix, "tfidf_matrix.pkl")
    print("✅ Saved all components successfully.")

if __name__ == "__main__":
    main()



