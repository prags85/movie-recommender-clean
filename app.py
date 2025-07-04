import streamlit as st
import pickle
import os
import requests

# --- Utility to download from Google Drive ---
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# --- Download similarity.pkl if missing ---
if not os.path.exists("similarity.pkl"):
    file_id = "1tNuObdTqK5-EdtdkN-0e2IiuZ3TTPNdv"  # Your Google Drive file ID
    download_file_from_google_drive(file_id, "similarity.pkl")

# --- Load data ---
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Recommendation function ---
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommended_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies_df.iloc[i[0]].title for i in recommended_indices]
    return recommended_movies

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
