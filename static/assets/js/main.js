function verify() {
  value = $('#certifycode')[0].value
  if(value=="")
    alert("Please enter a valid certify code")
  else
    window.location = window.location + '/check/' + value

}

function downloadFiles() {
  const downloadTimeStamp = window.location.href.split('?')[1]
  window.location.href = `/download?${downloadTimeStamp}`
}

function changeSize(obj){
  elements=$(".draggable")
  for(var i =0; i<elements.length;i++)
{
text=elements[i].getElementsByClassName("valuePara")[0]
text.style.fontSize=`${obj.value}px`
}
}


function addValue(obj){
  icon=obj.getElementsByTagName('i')[0]
  if(icon.className.includes('value_add_icon')){
    icon.innerText = 'check_circle'
    icon.classList.remove('value_add_icon')
    icon.classList.add('value_check_icon')

    valueName = obj.innerText.replace('check_circle','')
    templateElement = $(`#template_${valueName}`)[0]
    templateElement.style.display="inline-table"

  }
  else {
    icon.innerText = 'add_circle'
    icon.classList.add('value_add_icon')
    icon.classList.remove('value_check_icon')

    valueName = obj.innerText.replace('add_circle','')
    templateElement = $(`#template_${valueName}`)[0]
    templateElement.style.display="none"
  }
}

function addCertifyToTemplate(){
  checkbox=$('#certifyVerification')[0]
  if(checkbox.checked==true){
    element = $('#template_certify')[0]
    element.style.display="inline-table"
    fontsize = Math.floor($('#fontSize')[0].value)/2
    element.style.fontSize = `${fontsize}px`

}
  else
  $('#template_certify')[0].style.display="none"
}

function generate() {
  document.getElementsByClassName('create_edit_loading')[0].style.display = "block"
  var values = {}
  var valuesarr = $('.value_check_icon')
  for(var i =0; i<valuesarr.length;i++)
  {
    //the text contains icon name as text too, replacing it with ''    
    valueName = (valuesarr[i].parentElement.innerText).replace(valuesarr[i].innerText, '')
   
    //getting coordinates
    coordinates = getCoordinates(valueName)

    //adding value to dictionary
    values[valueName] =  [coordinates["x"],coordinates["y"]]
  }
  
  //getting font data: name,size and color

  var fontName = $('#fontName')[0].value
  var fontSize = $('#fontSize')[0].value
  var fontColor = $('#fontColor')[0].value

  var font = {
    "name": fontName,
    "size": fontSize,
    "color": fontColor
  }

  var certifyVerification = $('#certifyVerification')[0].checked
  var certifyValue = {"verify": certifyVerification}
  if(certifyVerification) {
    // sample data coordinates
    certifyCoordinates = getCoordinates("certify")
    certifyValue["coordinates"] = [certifyCoordinates["x"],certifyCoordinates["y"]]
    
  }

  var json = {
    "values": values,
    "font": font,
    "certify": certifyValue
  }
  loc = window.location.href
  ts = loc.split('=')[1]

apiRequest(json, ts)
}

  function apiRequest(json, ts) {

    $.ajax(
    { url: '/create/api?=' + ts.toString(),
      data: JSON.stringify({json: json,
      ts: ts}),
      contentType: 'application/json',
      type: 'POST',
      success: function(data, status){
      window.location.href = `/create/thankyou?ts=${data}`
      }
      });

  }


function getCoordinates(valueName) {
  
  //returning dict with x and y coordinates
  valueNewName = `template_${valueName}`
  innerDiv = $(`#${valueNewName}`)[0].getElementsByClassName("draggable")[0]
  console.log("Checkpoint2")
  innerDivX=innerDiv.offsetLeft
  innerDivY=innerDiv.offsetTop
  certiImg = $('.edit_certificate_div')[0]
  certiImgX = certiImg.offsetLeft
  certiImgY = certiImg.offsetTop

  fontsize = $('.draggable')[0].getElementsByClassName("valuePara")[0].style.fontSize
  fontsize = parseInt(fontsize.replace("px", ""))
  console.log(fontsize)
  xpos = innerDivX- certiImgX
  //subtracting font length from y axis
  ypos = innerDivY-certiImgY
  //Testing
  /*console.log({"x": innerDivX-certiImgX,
  "y": innerDivY-certiImgY})*/
  return {"x": xpos,
          "y": ypos - fontsize}
  
}
