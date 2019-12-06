# Certify 
Certify helps creating multiple certificates (Upto 1000 at a time) that are using a same template but differ in data. It also provides an authentication feature to verify authenticity of certificate by providing it a unique Certify Code

## How to Contribute


### Cloning project
`git clone https://github.com/kbhutani0001/Certify`

### Entering project and creating directories

`cd Certify`

As of now, for image database, Certify uses file system and for user data it uses MongoDB (Mlab)
The URI for Mlab instance is not provided here. For now, keep the Certify verification on edit page as checked off to avoid errors with MongoDB

To create folders for temp data run following commands

`mkdir static/temp/data static/temp/download static/verified/images`


### Setting up Virtual environment

Note: You can skip installing virtual environment if you want. Jump to step 3 if you want to install packages globally

1. To create a virtual environment, do
`virtualenv ven`

2. Activate virtual environment
`source venv/bin/activate`

3. Installing dependencies 
`pip install -r requirements.txt`

### Running the project

`python app.py`

This will run a http server at http://127.0.0.1:5000/
