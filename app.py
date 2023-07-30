# Import all the required libraries
import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch poster from given movie Id


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# This function will show the movies which are similar to given movie and returns a list of movie titles and posters

def recommend(movie, k):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:1+k]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Load the data and take out the list of different movie in database
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open("similairty.pkl", 'rb'))
movie_list = movies['title'].values


# Showcase the header and input elements
st.header('Movie Recommender System')
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
k = st.slider('How many recommendations do you want?', 1, 10, 1)


# Show case the recommended movies
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie, k)
    col = st.columns(k)
    count = 0
    for i in col:
        with i:
            st.text(recommended_movie_names[count])
            st.image(recommended_movie_posters[count])
            count = count + 1
