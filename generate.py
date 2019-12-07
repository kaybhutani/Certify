import pandas as pd
from PIL import Image, ImageFont, ImageDraw
import sys
from hashids import Hashids
from datetime import datetime, date
import time
import os
import pymongo
import shutil
import config
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
                
                # center allign text 
                w, h = draw.textsize(data[j][i])
                #draw on image
                draw.text([self.values[j][0]-(w/2),self.values[j][1]], data[j][i],font=fontName, fill=self.font['color'])
            
            #save image separately
            #also save in database --> verified folder if verification is checked 
            if(self.certify['verify']):
                img.save('./static/verified/images/' + data["Certify"][i] +'.jpg')
            
            #save for downloading
            folder = './static/temp/download/download_' + str(self.ts)
            img.save( folder + '/images/' + str(i)  +'.jpg')
        
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
            self.addToDatabase(listData)
            #adding certify to value
            self.values["Certify"]=self.certify["coordinates"]
            
            
            
        #return new data frame
        return data
    def addToDatabase(self,listData):
        client = pymongo.MongoClient(config.MONGODB_URI, connectTimeoutMS=30000)
        #database certify
        database = client.certify
        #collection userData in Certify
        collection = database["userData"]
        #inserting full list as many documents
        collection.insert_many(listData)
        
        