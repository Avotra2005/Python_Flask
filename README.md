# Flask Bootstrap Login & Dashboard Web App

## Installation and Local Setup

Follow these exact steps to clone, configure, and execute this web interface locally on your machine.

### Prerequisites
Make sure you have **Python 3.x** installed on your system.

### Set Up Your Project Folder
Navigate to your project container directory inside your terminal:

```bash



## Configure Your Isolated Python Environment (venv)
>>python -m venv .venv
>>source .venv\bin\activate


## Install Package Dependencies
>>pip install -r requirements.txt 

## run App
>>python app.py
----------------------------------Docker INTEGRATION--------------------------------------------------
### Add create docker
>>docker build -t mon-app-flask .

## lance docker
>>docker -d -p 80:5000 --name flask-app-container  mon-app-flask
// open browser and open http://localhost:80

## stop container
docker stop flask-app-container
