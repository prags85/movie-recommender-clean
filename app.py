import streamlit as st
import pickle
import os
import gdown

# --- Download similarity.pkl from Google Drive if not present ---
def download_similarity_file():
    file_id = "1tNuObdTqK5-EdtdkN-0e2IiuZ3TTPNdv"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "similarity.pkl", quiet=False)

if not os.path.exists("similarity.pkl"):
    download_similarity_file()

# --- Load local movies.pkl ---
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Recommendation function ---
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
