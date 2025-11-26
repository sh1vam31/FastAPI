from fastapi import FastAPI, Path, HTTPException, Query           # Import FastAPI class
import json
from fastapi.responses import JSONResponse       # Import JSONResponse for custom JSON responses
from typing import Annotated, Literal   # Import Annotated and Literal for type annotations
from pydantic import BaseModel, Field, computed_field      # Import BaseModel from Pydantic for data validation and Field for giving extra information about the fields and computed_field for computed properties

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
    


# Pydantic Models
class Patient(BaseModel):

    id: Annotated[str , Field(..., description="Unique identifier for the patient", example="P005")] 
    name: Annotated[str, Field(..., description="Full name of the patient", example="John Doe")]
    city: Annotated[int, Field(..., description="City of the patient")]
    age: Annotated[int, Field(..., gt=0, lt=120,  description="Age of the patient", example=30 )]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description="Gender of a Patient")]
    height: Annotated[float, Field(... , description="Height of the patient in mtrs")]
    weight: Annotated[float , Field(... , description="Weight of the patient in kgs")]

# Compute the BMI
@computed_field         # This tells Pydantic that this field (BMI) is computed, not stored.
@property               # This allows you to access bmi like a normal attribute
def bmi(self) -> float:         # self means the current patient object
    bmi = round(self.weight / (self.height ** 2), 2)
    return bmi

# Compute the verdict based on BMI
@computed_field
@property
def verdict(self) -> str:

    if self.bmi < 18.5:
        return "Underweight"
    elif 18.5 <= self.bmi < 24.9:
        return "Normal weight"
    elif 25 <= self.bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"
    

# Define an endpoint to add a new patient
@app.post('/create')
def create_patient(patient: Patient):       # this patient is of type Patient model
    
    # load existing patient data
    data = load_data()

    # Check if patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    
    # Add new patient to the data
    data[patient.id]  = patient.model_dump(exclude=['id'])    # Convert Pydantic model to dictionary and Add new patient data to existing data

    # Save updated data back to the JSON 
    def save_data(data):
        with open('patients.json', 'w') as file:
            json.dump(data, file)           # Dump data to JSON file

    save_data(data)


    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)




    