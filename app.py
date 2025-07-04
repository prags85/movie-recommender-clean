import streamlit as st
import pickle
import os
import requests

# --- Download similarity.pkl from Dropbox ---
def download_similarity_file():
    url = "https://www.dropbox.com/scl/fi/bgivig39srrubbyn2w3ma/similarity.pkl?rlkey=xeww2dhab6fhz4z8qndqqoo5m&st=zx2mqfql&dl=1"
    r = requests.get(url)
    with open("similarity.pkl", "wb") as f:
        f.write(r.content)

# --- Only download if file not present ---
if not os.path.exists("similarity.pkl"):
    download_similarity_file()

# --- Load data ---
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Recommendation function ---
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommended_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies_df.iloc[i[0]].title for i in recommended_indices]

# --- Streamlit UI ---
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    '🎥 Select a movie to get recommendations:',
    movies_df['title'].values
)

if st.button('Recommend'):
    st.subheader("Top 5 Recommendations:")
    recommendations = recommend(selected_movie_name)
    for movie in recommendations:
        st.write("✅", movie)
