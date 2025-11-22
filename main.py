from fastapi import FastAPI             # Import FastAPI class

app = FastAPI()             # Create an Object of FastAPI

@app.get("/")                # Define a GET endpoint at the root URL
def hello():                
    return {"massage": "Hello from FastAPI!"}

@app.get("/about")
def about():
    return{"massage": "This is the About Page"}