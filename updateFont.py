def getFont(fontName):
  if(fontName == "Arial"):
    return "./static/assets/fonts/arial.ttf"
  elif(fontName == "Calibri"):
    return "./static/assets/fonts/Calibri 400.ttf"
  elif(fontName == "Gabriela"):
    return "./static/assets/fonts/Gabriela-Regular.ttf"
  elif(fontName == "Georgia"):
    return "./static/assets/fonts/georgia.ttf"
  elif(fontName == "Italianno"):
    return "./static/assets/fonts/Italianno-Regular.ttf"
  elif(fontName == "Lato"):
    return "./static/assets/fonts/Lato-Regular.ttf"
  elif(fontName == "Dynalight"):
    return "./static/assets/fonts/Dynalight-Regular.ttf"
  elif(fontName == "Farsan"):
    return "./static/assets/fonts/Farsan-Regular.ttf"
  elif(fontName == "Oswald"):
    return "./static/assets/fonts/Oswald-Regular.ttf"
  elif(fontName == "Raleway"):
    return "./static/assets/fonts/Raleway-Regular.ttf"
  elif(fontName == "Roboto"):
    return "./static/assets/fonts/Roboto-Regular.ttf"
  elif(fontName == "Merriweather Sans"):
    return "./static/assets/fonts/MerriweatherSans-Regular.ttf"
  elif(fontName == "Acme"):
    return "./static/assets/fonts/Acme-Regular.ttf"
  elif(fontName == "Ubuntu"):
    return "./static/assets/fonts/Ubuntu-Title.ttf"
  elif(fontName == "Paytone One"):
    return "./static/assets/fonts/PaytoneOne-Regular.ttf"
  elif(fontName == "Verdana"):
    return "./static/assets/fonts/VERDANA.ttf"
  elif(fontName == "Notable"):
    return "./static/assets/fonts/Notable-Regular.ttf"
  elif(fontName == "bold"):
    return "./static/assets/fonts/theboldfont.ttf"
  elif(fontName == "Montserrat"):
    return "./static/assets/fonts/Montserrat-Regular.ttf"
  elif(fontName == "Pattaya"):
    return "./static/assets/fonts/Pattaya-Regular.ttf"
  else:
    return "./static/assets/fonts/arial.ttf"



def updateFont(font):
  #get font url from name
  fontName = getFont(font["name"])
  #update font name with url
  font["name"] = fontName

  #updating font size from str to int
  font["size"] = int(font["size"])
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

  #update color from hex to tuple
  font["color"] = colorTuple
  
  return font