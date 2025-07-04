import streamlit as st
import pickle
import os
import requests

# --- Download similarity.pkl from Dropbox ---
def download_similarity_file():
    url = "https://www.dropbox.com/s/bgivig39srrubbyn2w3ma/similarity.pkl?dl=1"
    r = requests.get(url)
    with open("similarity.pkl", "wb") as f:
        f.write(r.content)

# --- Only download if not already present ---
if not os.path.exists("similarity.pkl"):
    download_similarity_file()

# --- Load data ---
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Recommendation logic ---
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    top_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies_df.iloc[i[0]].title for i in top_indices]

# --- Streamlit UI ---
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    '🎥 Select a movie to get recommendations:',
    movies_df['title'].values
)

if st.button('Recommend'):
    st.subheader("Top 5 Recommendations:")
    for movie in recommend(selected_movie_name):
        st.write("✅", movie)
