import streamlit as st
import pickle
import os
import gdown  # New import

# --- Download from Google Drive using gdown ---
def download_similarity_file():
    if not os.path.exists("similarity.pkl"):
        file_id = "1tNuObdTqK5-EdtdkN-0e2IiuZ3TTPNdv"
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, "similarity.pkl", quiet=False)

# --- Call download before loading ---
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
