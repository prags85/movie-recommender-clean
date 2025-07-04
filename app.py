import streamlit as st
import pickle
import os
import requests

# Download similarity.pkl from Google Drive if missing
def download_file_from_google_drive(url, output_path):
    response = requests.get(url)
    with open(output_path, 'wb') as f:
        f.write(response.content)

if not os.path.exists("similarity.pkl"):
    gdrive_url = "https://drive.google.com/uc?export=download&id=1tNuObdTqK5-EdtdkN-0e2IiuZ3TTPNdv"
    download_file_from_google_drive(gdrive_url, "similarity.pkl")

# Load data
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommended_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies_df.iloc[i[0]].title for i in recommended_indices]
    return recommended_movies

# UI
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
