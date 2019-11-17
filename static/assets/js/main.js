function verify() {
  value = $('#certifycode')[0].value
  if(value=="")
    alert("Please enter a valid certify code")
  else
    window.location = window.location + '/check/' + value

}