import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import ast
import joblib


def load_data():
    df = pd.read_csv('movies_data.csv',index_col=0)
    print(f"Rows and columns of the data {df.shape}")
    return df

# Function for pre-processig the data
def pre_process_data(df):
    print("Pre-processing the data...")
    df = df.dropna(subset=['title'])
    df = df.drop_duplicates(subset=['title'])
    
    df['release_date'] = pd.to_datetime(df['release_date'],errors='coerce').dt.year

    df['genres']= df['genres'].apply(ast.literal_eval)
    df['cast']= df['cast'].apply(ast.literal_eval)

    df['genres_str']   = df['genres'].apply(lambda x: ' '.join(x))
    df['cast_str']     = df['cast'].apply(lambda x: ' '.join(x))  
    df['all_text'] = df['overview'] + ' ' + df['genres_str'] + ' ' + df['cast_str'] + ' ' + df['director'] + ' ' + df['original_language']

    return df

# Function for vectorizing and scaling.
def vectorize_scaling(df):
    vectorizer = TfidfVectorizer(stop_words='english')
    print("Converting to tfidf matrix")
    tfidf_matrix = vectorizer.fit_transform(df['all_text'])
    print(tfidf_matrix.shape)
    
    numeric_features = ['release_date','runtime','popularity']
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(df[numeric_features])
    
    final_matrix = hstack([tfidf_matrix, scaled_features]).tocsr()
    
    return final_matrix

# Function for recommending movies
def recommend(df,movie_name,final_matrix,top_n):
    if movie_name in df['title'].values:
        index = df[df['title']==movie_name].index[0]
        distances = cosine_similarity(final_matrix[index], final_matrix).flatten()
        sorted_distances = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:top_n+1]
        
        print("Here are your suggested movies")
        for i in sorted_distances:
            print(df.iloc[i[0]].title)
    else:
        print("Movie not found")

# Main fucntion
def main():
    df = load_data()
    df = pre_process_data(df)
    final_matrix = vectorize_scaling(df)
    recommend(df,'Home Alone',final_matrix,5)

    # df.to_pickle("processed_movies.pkl")
    # joblib.dump(final_matrix, "final_matrix.pkl")
    # print("Saved all components successfully.")

if __name__ == "__main__":
    main()


























