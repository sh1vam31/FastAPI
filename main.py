from fastapi import FastAPI, Path, HTTPException, Query           # Import FastAPI class
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


# Path Parameters
# Define an endpoint to get patient details by patient ID
@app.get('/patient/{patient_id}')
# path parameter with description and example , when we open docs it will show description and example
# the ... in Path(...) indicates that this parameter is required
def get_Patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
#  Load patient data from the JSON file
    data = load_data()
#  Search for the patient with the given ID
    if patient_id in data:
        return data[patient_id]
    else:
        #return {"error": "Patient not found"}
 # Problem ---> when we search for a patient id that does not exist in the data , it returns "Patient not found" , but the status code is 200 OK , which is not appropriate for an error response., so we will fix it by returning a 404 status code for not found errors.
        raise HTTPException(status_code=404, detail="Patient not found")
# HTTPException is used to raise HTTP errors with specific status codes and messages.



# Query Parameters
@app.get('/sort')
def sorted_patients(sort_by: str = Query(..., description="Sort on the basis of Height , Weigth , BMI") , order: str = Query('asc', description="Sort in asc and desc order")):

    valid_fileds = ['height', 'weight', 'bmi']
    if sort_by not in valid_fileds:
        raise HTTPException(status_code=400, detail= f"Invalid sort_by field. Must be one of {valid_fileds}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")
    
    data = load_data()

    sort_order = False if order == 'asc' else True

    sorted_data = sorted(data.values() , key=lambda x: x.get(sort_by, 0) , reverse=sort_order)

    return sorted_data
    

    