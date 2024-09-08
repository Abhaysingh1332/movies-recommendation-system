# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=1d382ea7511c28d3a9835f500b7b8598&language=en-US'.format(movie_id),timeout=10)
#     data = response.json()
#     print(data)
#     return "https://image.tmdb.org/t/p/w500" + data['poster_path']
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#
#         recommended_movies.append(movies.iloc[i[0]].title)
#         # fetech poster from API
#         recommended_movies_posters.append(fetch_poster(movie_id))
#
#     return recommended_movies,recommended_movies_posters
#
# movie_dict = pickle.load(open('movie_dict.pkl','rb'))
# movies = pd.DataFrame(movie_dict)
#
# similarity = pickle.load(open('similarity.pkl','rb'))
#
# st.title('Movie recommender system')
#
# selected_movie_name = st.selectbox(
# 'how would you like to contacted?',
# movies['title'].values)
#
# if st.button('recommend'):
#     names, posters = recommend(selected_movie_name)
#     # for i in recommendations:
#     #     st.write(i)
#     col1, col2, col3,col4,col5 = st.beta_columns(5)
#     with col1:
#         st.text(names[0])
#         st.image(posters[0])
#     with col2:
#         st.text(names[1])
#         st.image(posters[1])
#     with col3:
#         st.text(names[2])
#         st.image(posters[2])
#     with col4:
#         st.text(names[3])
#         st.image(posters[3])
#     with col5:
#         st.text(names[4])
#         st.image(posters[4])
import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch the movie poster
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=1d382ea7511c28d3a9835f500b7b8598&language=en-US',
            timeout=20)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        # Log the response for debugging
        st.write(data)  # Comment this out once you're sure the API returns the right data

        # Ensure the poster path is correct and not None
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w780" + data['poster_path']  # Higher resolution image
        else:
            return "https://via.placeholder.com/500"  # Fallback for movies without posters
    except requests.exceptions.Timeout:
        return "https://via.placeholder.com/500"  # Return a placeholder image on timeout
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return "https://via.placeholder.com/500"  # Return a placeholder image on other errors


# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Load the movie data and similarity matrix
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

# Dropdown menu to select a movie
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

# Recommend button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display recommendations and posters
    cols = st.columns(5)  # Updated to use st.columns

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])



