function verify() {
  value = $('#certifycode')[0].value
  if(value=="")
    alert("Please enter a valid certify code")
  else
    window.location = window.location + '/check/' + value

}
function addValue(obj){
  icon=obj.getElementsByTagName('i')[0]
  if(icon.className.includes('value_add_icon')){
    icon.innerText = 'check_circle'
    icon.classList.remove('value_add_icon')
    icon.classList.add('value_check_icon')
  }
  else {
    icon.innerText = 'add_circle'
    icon.classList.add('value_add_icon')
    icon.classList.remove('value_check_icon')
  }
}