import streamlit as st
import pickle
import pandas as pd
import requests

movie_dict = pickle.load(open('movies_dict.pkl','rb'))
movie_list = pd.DataFrame(movie_dict)
movie = movie_list['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))


def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp{{
        background-image: url("https://repository-images.githubusercontent.com/275336521/20d38e00-6634-11eb-9d1f-6a5232d0f84f");
        background-attachment: fixed;
        background-size:cover;
        opacity:0.6;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_url()

def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=925b2767e64a79c6adb854ec54f84e70&language=en-US'.format(movie_id)
    response =requests.get(url)
    data = response.json()
    return 'https://image.tmdb.org/t/p/original'+data['poster_path']

def recommend(movie_name):
    movie_index = movie_list[movie_list['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    matching_movie = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    movies_list =[]
    recommended_movies_poster =[]

    for i in matching_movie:
        id =movie_list.iloc[i[0]].movie_id
        print(id)
        movies_list.append(movie_list.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(id))
    return movies_list,recommended_movies_poster



st.title("Movie Recommender System")


selected_movie_name = st.selectbox("What is the name of movie that you like?",
    (movie))

print(selected_movie_name)
if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])