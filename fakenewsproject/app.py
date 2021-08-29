#Importing the Libraries
from flask.json import jsonify
import numpy as np
from flask import Flask, request,render_template
from flask_cors import CORS,cross_origin
import os
#from sklearn.externals import joblib
import pickle
import flask
import os
import newspaper
from newspaper import Article
import urllib
#Loading Flask and assigning the model variable
app = Flask(__name__)
CORS(app)
app=flask.Flask(__name__,template_folder='html')

with open('model.pickle', 'rb') as handle:
	model = pickle.load(handle)

@app.route('/')
def main():
    return render_template('main.html')

#Receiving the input url from the user and using Web Scrapping to extract the news content
@app.route('/predict',methods=['GET','POST'])
@cross_origin()
def predict():
    url =request.json['link']
    if(not url):
        return flask.jsonify(err = 'Invalid URL')
    if(url):
        url = urllib.parse.unquote(url)
        article = Article(str(url))
        article.download()
        article.parse()
        article.nlp()
        news = article.summary
        #Passing the news article to the model and returing whether it is Fake or Real
        pred = model.predict([news])
        isFake = pred[0] == 'FAKE'
        return flask.jsonify(isFake = isFake)

if __name__=="__main__":
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)