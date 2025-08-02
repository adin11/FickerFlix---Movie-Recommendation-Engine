import requests
import time
import pandas as pd

# API details
api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNmQ1ZDZlODFiMDE3MmY4NDczOGU5OTFmYjVhYzQ5YiIsIm5iZiI6MTc1Mzc4OTg2NS4xNzIsInN1YiI6IjY4ODhiNWE5MmU0ODk0N2FkZmY3OTgzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.x-3lqPDeBUuN6dIw-pdz7CYZVjAWasqLJHFttA6C-xA"
api_key = 'your_api_key'

# Function for extracting movie and cast details details
def get_movie_details(movie_id):

    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits'
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()

        if ( data.get('title') and 
            data.get('genres') and 
            data.get('overview') and 
            data.get('release_date') and 
            data.get('runtime') > 30
        ):
        
            movie_data = {
                    'movie_id': movie_id,
                    'title': data.get('title'),
                    'genre': [ genre['name'] for genre in data.get('genres', [])],
                    'release_date': data.get('release_date'),
                    'runtime': data.get('runtime'),
                    'overview': data.get('overview'),
                    'vote_average': data.get('vote_average'),
                    'vote_count': data.get('vote_count'),
                    'popularity': data.get('popularity'),
                    'original_language': data.get('original_language'),
                    'cast': [member['name'] for member in data.get('credits', {}).get('cast', [])[:3]],  # top 3 cast
                    'director': next((crew['name'] for crew in data.get('credits', {}).get('crew', []) if crew['job'] == 'Director'), None)
                }
            
            print(f"✅ Added movie {movie_id} : title {movie_data['title']} ")
            return movie_data

    else:
        print(f"❌ Error {res.status_code} for movie_id {movie_id}")
        return None


# Main function 
def main():
    all_data = []   # List for appending the data in each iteration for each movie.
    movie_ids = range(1,10)

    for movie_id in movie_ids:     
            movie_data = get_movie_details(movie_id)
            if movie_data:
                all_data.append(movie_data)
            time.sleep(0.2)    
    
    # After appending convert to csv
    df = pd.DataFrame(all_data)
    df.to_csv('data.csv',index=False)


if __name__ == "__main__":
    main()

















