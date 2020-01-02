import pandas as pd
from PIL import Image, ImageFont, ImageDraw
import sys
from hashids import Hashids
from datetime import datetime, date
import time
import threading
import os
import pymongo
import gridfs
import shutil
import config


def retrieve_image_from_database(img_id):
    # get an image based on it's 'certify code'
    client = pymongo.MongoClient(config.MONGODB_URI, connectTimeoutMS=30000)
    database = client.certify
    fs = gridfs.GridFS(database)
    if fs.exists(img_id):
        retrieved_img = fs.get(img_id).read()
        verified_img_file = open('./static/verified/images/' + img_id + '.jpg', 'wb')
        verified_img_file.write(retrieved_img)
        img_location = 'verified/images/' + img_id + '.jpg'
        return True
    else:
        return False


def add_to_image_database(image, img_id):
    # Saves a given image to the database with the 'certify code' as its ID
    client = pymongo.MongoClient(config.MONGODB_URI, connectTimeoutMS=30000)
    database = client.certify
    fs = gridfs.GridFS(database)
    fs.put(image, _id=img_id)


def addToDatabase(listData):
    client = pymongo.MongoClient(config.MONGODB_URI, connectTimeoutMS=30000)
    #database certify
    database = client.certify
    #collection userData in Certify
    collection = database["userData"]
    #inserting full list as many documents
    collection.insert_many(listData)


class Create:
    #defining variables
    def __init__(self, template, spreadsheet, values, font, certify, ts):
        self.template = template
        self.spreadsheet = spreadsheet
        self.values = values
        self.font = font
        self.certify = certify
        self.ts = ts

    def resizeFontValues(self):
      img = Image.open(self.template).convert('RGB')
      width, height = img.size
      heightNew = 500
      ratio = height/heightNew

      for coor in self.values:
        self.values[coor] = [int((self.values[coor][0])*ratio),  int((self.values[coor][1])*ratio) ]

      self.font["size"]=int((self.font["size"])*ratio)

      if self.certify["verify"] == True:
        self.certify["coordinates"]=[  int((self.certify["coordinates"][0])*ratio),int((self.certify["coordinates"][1])*ratio)  ]


    def generate(self):
        try:
            data=pd.read_csv(self.spreadsheet)
        except:
            data=pd.read_excel(self.spreadsheet)
            data.fillna("")

        #updating data
        print(self.values, self.font, self.certify)
        self.resizeFontValues()
        print(self.values, self.font, self.certify)
        #getting max no. of rows
        count = max(list(data.count()))

        #update data with certify code if user checked it
        datanew = self.addUnique(data,count)

        #create directory for files
        path = './static/temp/download/download_' + str(self.ts)
        os.mkdir(path)
        os.mkdir(path + '/images')

        #generating certificate
        self.imageProcessing(datanew,count)

        #remove folder after creating zip
        shutil.rmtree(path)

    def imageProcessing(self,data,count):

        for i in range(0,count):
            #opening image and canvas
            img = Image.open(self.template).convert('RGB')

            #opening canvas
            draw = ImageDraw.Draw(img)

            #k for iterating through values{} index
            for j,k in zip(self.values,range(0,len(self.values))):
                fontSize = self.font['size']
                if(j=='Certify'):
                    fontSize=int(fontSize/1.5)
                #get font for that element
                fontName = ImageFont.truetype(self.font['name'], fontSize)

                #center align
                h,w=draw.textsize(data[j][i])
                if (j=='College' or j=='Position'):
                    draw.text([self.values[j][0]+31.5*3-(h/2)*3,self.values[j][1]], data[j][i],font=fontName, fill=self.font['color'])
                elif(j=='Event'):
                    if (h>48):
                        draw.text([self.values[j][0]+23*6-(h/2)*6,self.values[j][1]], data[j][i],font=fontName, fill=self.font['color'])
                    else:
                        draw.text([self.values[j][0]+23*3-(h/2)*3,self.values[j][1]], data[j][i],font=fontName, fill=self.font['color'])
                else:
                    draw.text([self.values[j][0]+24*6-(h/2)*6,self.values[j][1]], data[j][i],font=fontName, fill=self.font['color'])

            #save image separately
            #also save in database --> verified folder if verification is checked
            if(self.certify['verify']):
                # img.save('./static/verified/images/' + data["Certify"][i] +'.jpg')
                # compresses image (x is set to 500 and aspect ration is preserved through the 'img_size_on_y' variable)
                img_size_on_y = int(500 * img.size[1] / img.size[0])
                downsized_img = img.resize((500, img_size_on_y), Image.LANCZOS)
                downsized_img.save('./static/verified/images/' + data["Certify"][i] + '_downsized' + '.jpg')
                database_image = open('./static/verified/images/' + data["Certify"][i] + '_downsized' +'.jpg', 'rb')
                background_thread = threading.Thread(target=add_to_image_database,
                                                     args=(database_image, data["Certify"][i]))
                background_thread.start()

            
            #save for downloading
            folder = './static/temp/download/download_' + str(self.ts)
            img.save(folder + '/images/' + str(i) + '.jpg')
        

        #save dataframe as spreadsheet
        data.to_csv(folder + '/data.csv', header=False, index=False)
        shutil.make_archive(folder , 'zip', folder)

    #generate unique id based on timestamp and salt
    def unique(self):
        #generating hashid, specifying salt and alphabets available
        hashids = Hashids(salt = "certify to create certificates", alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvyxyz1234567890")

        #generating unique id based on time stamp before and after decimal
        uniqueId = hashids.encode(int(datetime.today().timestamp()))[-3:] + hashids.encode(int(str(datetime.today().timestamp()).split('.')[1]))

        return uniqueId

    #add unique id to data frame if certify verification is True
    def addUnique(self,data,count):
        if(self.certify["verify"]==True):
            uIds=[]
            #creating dataframe copy
            data = data.copy()

            #generate unique id for all values
            for i in range(0,count):
                uIds.append(self.unique())

            #append column to dataframe
            data['Certify'] = uIds

            #creating empty list for database data
            listData = []

            #iterating through unique id array and 0 to count in same loop
            for i,n in zip(uIds,range(0,count)):
                #adding unique id to dictionary
                dictData = {}
                #making dict for values corresponding to certify code
                dictData[i] = {}
                #iterating through values
                for j in self.values:
                    #adding value and its data
                    dictData[i][j] = data[j][n]
                dictData[i]["Generated on"] = date.today().strftime("%d/%m/%Y")
                listData.append(dictData)
            addToDatabase(listData)
            #adding certify to value
            self.values["Certify"]=self.certify["coordinates"]



        #return new data frame
        return data
