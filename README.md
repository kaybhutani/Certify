# Certify 
Certify helps creating multiple certificates (Upto 1000 at a time) that are using a same template but differ in data. It also provides an authentication feature to verify authenticity of certificate by providing it a unique Certify Code

## How to Contribute


### Cloning project
`git clone https://github.com/kbhutani0001/Certify`

### Entering project and creating directories

`cd Certify`

As of now, for verified certificate image database (`static/verified/images`), Certify uses file system and for user data it uses MongoDB (Mlab)


### Setting up Virtual environment

Note: You can skip installing virtual environment if you want. Jump to step 3 if you want to install packages globally

1. To create a virtual environment, do
`virtualenv ven`

2. Activate virtual environment
`source ven/bin/activate`

3. Installing dependencies 
`pip3 install -r requirements.txt`

### Running the project

`python3 app.py`

This will run a http server at http://127.0.0.1:5000/