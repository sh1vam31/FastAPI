from fastapi import FastAPI             # Import FastAPI class
import json

app = FastAPI()             # Create an Object of FastAPI

@app.get("/")                # Define a GET endpoint at the root URL
def hello():                
    return {"massage": "Hello from FastAPI!"}

@app.get("/about")
def about():
    return{"massage": "This is the About Page"}


def load_data():
    with open('patients.json' , 'r') as file:
        data = json.load(file)
    return data

@app.get('/view')
def view_patients():
    Patient_data = load_data()
    return Patient_data