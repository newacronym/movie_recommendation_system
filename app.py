import pickle
import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

API_KEY = os.getenv('TMDB_API_KEY')


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    if movie not in movies['title'].values:
        st.error('Movie not found in the database. Please try another one.')
        return [], []
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies_dict = pickle.load(open('model/movie_dict.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

movies = pd.DataFrame(movies_dict)

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)

    columns = st.columns(5)
    for idx, col in enumerate(columns):
        if idx < len(recommended_movie_names):
            with col:
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx])