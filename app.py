import streamlit as st
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# Page configuration
st.set_page_config(
    page_title="Flicker Flix",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    
    .main-title {
        text-align: center;
        color: #ffffff;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease-in-out infinite;
    }
    .main-subtitle{
            text-align: center;
        color: #ffffff;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease-in-out infinite;
            }
            

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #b3b3b3;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    .movie-result {
        background: #1e2329;
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-left: 4px solid #4ecdc4;
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
    }
    
    .movie-result:hover {
        transform: translateX(5px);
        border-left-color: #ff6b6b;
    }
    
    .section-title {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .social-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
    }
    
    .social-link {
        display: inline-block;
        padding: 0.8rem;
        background: linear-gradient(45deg, #4ecdc4, #45b7d1);
        border-radius: 50%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-decoration: none;
    }
    .footer {
        margin-top: 4rem;
        padding: 2rem;
        text-align: center;
        border-top: 1px solid #333;
        background: #1a1a1a;
    }
    
    .footer-title {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .social-link:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.4);
    }
    
    .error-message {
        background: #2d1b1b;
        color: #ff6b6b;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ff6b6b;
        margin: 1rem 0;
        text-align: center;
    }
    
    .success-header {
        color: #4ecdc4;
        font-size: 1.8rem;
        font-weight: 600;
        text-align: center;
        margin: 2rem 0 1rem 0;
    }
      
    .support-section {
        margin: 2rem 0 1rem 0;
        text-align: center;
    }

    .support-text {
        color: #b3b3b3;
        font-size: 1rem;
        margin-bottom: 1rem;
    }      

</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_resources():
    df = pd.read_csv("processed_movies.csv")
    tfidf_matrix = joblib.load("tfidf_matrix.pkl")
    return df, tfidf_matrix

def recommend_movies(df, tfidf_matrix, movie_name, top_n=5):
    if movie_name in df['title'].values:
        index = df[df['title'] == movie_name].index[0]
        distances = cosine_similarity(tfidf_matrix[index], tfidf_matrix).flatten()
        sorted_distances = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:top_n+1]
        recommended = [df.iloc[i[0]]['title'] for i in sorted_distances]
        return recommended
    else:
        return []

# Load data
df, tfidf_matrix = load_resources()

# Header
st.markdown("""
<h1 class="main-title">Flicker Flix:</h1>
<h3 class="main-subtitle">Your Personalized Movie Recommendation Engine</h3>
<p class="subtitle">Discover your next favorite movie based on your cinema taste </p>
""", unsafe_allow_html=True)

# Number of recommendations slider
st.markdown('<div class="slider-container">', unsafe_allow_html=True)
num_recommendations = st.slider(
    "Number of recommendations:",
    min_value=3,
    max_value=10,
    value=1,
    help="Choose how many movies to recommend"
)
st.markdown('</div>', unsafe_allow_html=True)

# Movie search
st.markdown('<p class="section-title">🎬 Find Your Movie</p>', unsafe_allow_html=True)

# Create form for Enter key functionality
with st.form(key='movie_form'):
    selected_movie = st.text_input(
        "Movie name",
        placeholder="Type exact movie name (e.g., Interstellar, The Dark Knight, Inception...)",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.form_submit_button(
            "🎯 Get Recommendations",
            use_container_width=True,
            type="primary"
        )

st.markdown('</div>', unsafe_allow_html=True)

# Handle recommendations
if submit_button and selected_movie:
    with st.spinner("🔄 Finding perfect matches..."):
        recommendations = recommend_movies(df, tfidf_matrix, selected_movie.strip(), num_recommendations)
    
    if recommendations:
        st.markdown(f'<h2 class="success-header">🎭 Movies Similar to "{selected_movie}"</h2>', unsafe_allow_html=True)
        
        for i, movie in enumerate(recommendations, start=1):
            st.markdown(f"""
            <div class="movie-result">
                {i}. {movie}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="error-message">
            ⚠️ Movie not found in our database. Please check the spelling and try again.
        </div>
        """, unsafe_allow_html=True)

elif submit_button and not selected_movie:
    st.markdown("""
    <div class="error-message">
        🎬 Please enter a movie name to get recommendations!
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="support-section">
        <p class="support-text">☕ Enjoying Flicker Flix? Support the project!</p>
        <a href="https://buymeacoffee.com/adinraja" target="_blank" class="coffee-button">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="margin-right: 8px; vertical-align: middle;">
            <path d="M20.216 6.415l-.132-.666c-.119-.598-.388-1.163-.766-1.688a4.436 4.436 0 0 0-1.348-1.137c-.314-.162-.654-.1-.87.15-.216.25-.1.666.15.87.398.33.717.711.951 1.137.234.426.394.888.479 1.364l.132.696c.119.598.388 1.163.766 1.688.378.525.856.942 1.348 1.137.314.162.654.1.87-.15.216-.25.1-.666-.15-.87-.398-.33-.717-.711-.951-1.137-.234-.426-.394-.888-.479-1.364zM12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
            <path d="M12 6c-3.309 0-6 2.691-6 6s2.691 6 6 6 6-2.691 6-6-2.691-6-6-6-2.691-6-6-6zm0 10c-2.206 0-4-1.794-4-4s1.794-4 4-4 4 1.794 4 4-1.794 4-4 4z"/>
            </svg>
            Buy Me a Coffee
        </a>
    </div>
    <p class="footer-title"> A Project by ~  Adin Raja✌️</p>
    <div class="social-links">
        <a href="https://github.com/adin11" target="_blank" class="social-link">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
        </a>
        <a href="https://www.linkedin.com/in/adinraja78/" target="_blank" class="social-link">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
        </a>
        <a href="https://twitter.com/adinraja" target="_blank" class="social-link">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
            </svg>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)