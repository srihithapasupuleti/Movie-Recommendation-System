"""
Routes and views for the flask application.
"""
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
# libraries for making count matrix and similarity matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from FlaskWebProject4 import app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
# define a function that creates similarity matrix
# if it doesn't exist
def create_sim():
    data = pd.read_csv('C:/Users/12499/Desktop/AI algorithm/tmdb_movies.csv')
    # creating a count matrix
  
    tfidf = TfidfVectorizer(stop_words='english')

    #Replace NaN with an empty string
    data['overview'] = data['overview'].fillna('')

    #Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(data['overview'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    return data,cosine_sim


# defining a function that recommends 10 most similar movies
def rcmd(m):
  
    # check if data and sim are already assigned
    try:
        data.head()
        print(data.head())
        sim.shape
    except:
        data,sim = create_sim()
        print()
        if m not in data['title'].unique():
            return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
        else:
            i = data.loc[data['title']==m].index[0]
      
            # fetching the row containing similarity scores of the movie
            # from similarity matrix and enumerate it
            lst = list(enumerate(sim[i]))
             # sorting this list in decreasing order based on the similarity score
            lst = sorted(lst, key = lambda x:x[1] ,reverse=True)

            # taking top 1- movie scores
            # not taking the first index since it is the same movie
            lst = lst[1:11]

            # making an empty list that will containg all 10 movie recommendations
            l = []
            for i in range(len(lst)):
                a = lst[i][0]
                l.append(data['title'][a])
            return l


@app.route("/")
def home():
    #console.WriteLine('hi')
    return render_template('home.html')
    

@app.route("/recommend")
def recommend():
    movie = request.args.get('movie')
    r = rcmd(movie)
    movie = movie.upper()
    print(r)
    if type(r)==type('string'):
        return render_template('recommend.html',movie=movie,r=r,t='s')
    else:
        return render_template('recommend.html',movie=movie,r=r,t='l')



