#importing files
from flask import Flask,render_template,request,redirect,url_for,send_from_directory,jsonify,abort
import os
import generate

#app name
app=Flask(__name__)


#app route for main page
@app.route('/', methods=['GET', 'POST'])
def home():
  	if request.method == 'GET':
		  return render_template("index.html")