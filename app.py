#importing files
from flask import Flask,render_template,request,redirect,url_for,send_from_directory,jsonify,abort
import os
import generate
import glob


values = {
                "Name": [550, 830],
                "College": [650,970],
                "Position": [1250, 1120],
                "Competetion": [550, 1260]
}

#app name
app=Flask(__name__)


#app route for main page
@app.route('/', methods=['GET', 'POST'])
def home():
  	if request.method == 'GET':
		  return render_template("index.html")


#app route for verify page
@app.route('/verify', methods=['GET', 'POST'])
def verify():
  	if request.method == 'GET':
		  return render_template("verify.html")


#app route for verify check page
@app.route('/verify/check/<certifycode>', methods=['GET', 'POST'])
def verifycheck(certifycode):
  arr = glob.glob("static/temp/img/" + certifycode + ".*")
  #check if arr is not empty (means a file with same name exists)
  if arr:
    
    #take first image
    #split image path and get the end file name
    image = arr[0].split('/')[-1]

    #getting image path in flask template
    image_url = url_for('static',filename='temp/img/'+ image)
    print(image_url)
    #return template and sending image url as parameter
    return render_template("verified.html", image_url=image_url)
  else:
    return render_template("notverified.html")


#app route for create edit page
@app.route('/create/edit', methods=['GET', 'POST'])
def create_edit():
  	if request.method == 'GET':
		  return render_template("create_edit.html",values=values)


#app route for create api
@app.route('/create/api', methods=['POST'])
def create_api():
  if request.method == 'POST':
    json = request.get_json()
    values = json['values']
    font = json['font']
    certify = json['certify']
    print(json)
    return "Success!"









if(__name__=='__main__'):
	app.run(debug=True,use_reloader=True)
