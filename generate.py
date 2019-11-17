import pandas as pd
from PIL import Image, ImageFont, ImageDraw
import sys
from pymongo import MongoClient

##testing data
template = "certi.jpg"
data = "data.csv"
values = {
                "Name": [550, 830],
                "College": [650,970],
                "Position": [1250, 1120],
                "Competetion": [550, 1260]
}
size=[80,75,75,75]

try:
	client = MongoClient(config.MONGODB_URI, connectTimeoutMS=30000)
except:
  print("Some error ocurred while connecting to database")


class Create:
    def __init__(self, template, spreadsheet, values, size, font='arial.ttf'):
        self.template = template
        self.spreadsheet = spreadsheet
        self.values = values
        self.font = font
        self.size = size
    
    def printf(self):
        print(self.template,self.data)
    def generate(self):
        try:
            data=pd.read_csv(self.spreadsheet)
        except:
            data=pd.read_excel(self.spreadsheet)
        data.fillna("")
        
        #getting no. of rows
        count = data.count()[0]
        
        for i in range(0,count):
            #opening image and canvas
            img = Image.open(template).convert('RGB')
            draw = ImageDraw.Draw(img)
            
            #iterating all values
            iterator_main_loop=0
            
            for j in values:
                
                #get font for that element
                font = ImageFont.truetype(self.font, size[iterator_main_loop])
                
                #draw on image
                draw.text(values[j], data[j][i],font=font, fill=(255,0,255,255),align='center')
                
                #main iterator increment
                iterator_main_loop+=1
            
            #save image separately
            img.save('new/' + str(i)+'.jpg')
