#importing modules
from flask import Flask,render_template,request,redirect,url_for,send_from_directory,jsonify,abort,send_file
import os
from generate import Create
import glob
from datetime import datetime
import pymongo
import config
import time
import shutil
import pandas as pd

#specifing temp data
valuetemp = {
                "Name": [550, 830],
                "College": [650,970],
                "Position": [1250, 1120],
                "Event": [550, 1260]
}
fonttemp={
    "name": 'arial.ttf',
    "size": 65,
    "color": (0,0,0)
}
certifytemp = {"verify": True,
           "coordinates": [30,1730]}

#app name
app=Flask(__name__)


def searchCertifyCode(code):
  client = pymongo.MongoClient(config.MONGODB_URI, connectTimeoutMS=30000)
  db = client.certify
  col = db["userData"]
  userData={}
  for i in col.find({}):
    currentCertifyCode = list(i.keys())[1]
    if(currentCertifyCode==code):
      userData = i[currentCertifyCode]
  return userData
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
  arr = glob.glob("static/verified/images/" + certifycode + ".*")
  #check if arr is not empty (means a file with same name exists)
  if arr:
    
    #take first image
    #split image path and get the end file name
    image = arr[0].split('/')[-1]

    #getting image path in flask template
    image_url = url_for('static',filename='verified/images/'+ image)
    
    #look for certify id and return data
    verifiedUserData = searchCertifyCode(certifycode)

    #return template and sending image url as parameter
    return render_template("verified.html", image_url=image_url, userData=verifiedUserData)
  else:
    return render_template("notverified.html")


#app route for create upload page
@app.route('/create', methods=['GET', 'POST'])
def create_upload():
  if request.method == 'GET':
    return render_template("create_upload.html",values=valuetemp)
  elif request.method == 'POST':
    spreadsheet = request.files['spreadsheet']
    template = request.files['template']
    ts = int(datetime.today().timestamp())
    
    #create directory for files
    path = './static/temp/data/data_' + str(ts)
    os.mkdir(path)
    spreadsheet.save(path + '/' + "data.csv")
    template.save(path + '/' + "template.jpg")
    return redirect("/create/edit?ts=" + str(ts))

#app route for create edit page
@app.route('/create/edit', methods=['GET', 'POST'])
def create_edit():
  if request.method == 'GET':
    try:
      ts = request.args.get('ts')
      print(ts)
    except:
      ts=""
      print("Couldnt get ts")
    #url of folder with data
    path = path = './static/temp/data/data_' + str(ts)
    
    #url for data spreadsheet
    spreadsheet = path + "/data.csv"
    
    #reading dataframe
    data = pd.read_csv(spreadsheet)
    
    #making list of all columns
    valuesTemp=list(data.columns)
    
    #url for certificate to display
    templateImg = '../static/temp/data/data_' + str(ts) + "/template.jpg"

    return render_template("create_edit.html",values=valuesTemp, template=templateImg)


#app route for create api
@app.route('/create/api', methods=['POST'])
def create_api():
  if request.method == 'POST':
    #getting api request data
    json = request.get_json()
    try:
      print("Got ts")
      print(json["ts"])
      ts = json["ts"]
    except:
      ts=""
      print("Couldnt get ts")

    #print json data to check
    print(json["json"])
    json = json["json"]

    #getting values
    values = json['values']
    font = json['font']
    certify = json['certify']
    #get color as it will be in hex
    colorTemp = font["color"]

    #get color for RGB, # R G B
    colorRed = colorTemp[1:3]
    colorGreen = colorTemp[3:5]
    colorBlue = colorTemp[5:7]

    #convert all colors from hex(base 16) to decimal int
    colorRed = int(colorRed, 16)
    colorGreen = int(colorGreen, 16)
    colorBlue = int(colorBlue, 16)
    
    #making tuple of color
    colorTuple = (colorRed, colorGreen, colorBlue)

    #testing purpose
    fonttemp["color"] = colorTuple

    #url of folder with data
    path = path = './static/temp/data/data_' + str(ts)
    
    #url for data spreadsheet
    spreadsheet = path + "/data.csv"

    #url for template image
    template = path + "/template.jpg"

    create = Create(template=template, spreadsheet=spreadsheet, values=valuetemp, font=fonttemp, certify=certify,ts=ts)
    print("Creating files....")
    create.generate()
    print("Created files successfully!")
    #delete teplate data
    shutil.rmtree(path)
    return str(ts)

#app route for thankyou page
@app.route('/create/thankyou', methods=['GET', 'POST'])
def create_thankyou():
  if request.method == 'GET':
    try:
      ts = request.args.get('ts')
      print(ts)
    except:
      ts=""
      print("Couldnt get ts")
    return render_template("create_download.html", ts=ts)



#app route for download page, redirects direct to file
@app.route('/download', methods=['GET', 'POST'])
def create_download():
  if request.method == 'GET':
    try:
      ts = request.args.get('ts')
      print(ts)
    except:
      ts=""
      print("Couldnt get ts")
    return send_file(("static/temp/download/download_" + ts + ".zip"), attachment_filename=("download_"+ts) , as_attachment=True)





if(__name__=='__main__'):
	app.run(debug=True,use_reloader=True)
