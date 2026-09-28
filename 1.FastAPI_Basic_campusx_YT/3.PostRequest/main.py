from fastapi import FastAPI, Path, HTTPException,Query
from fastapi.responses import JSONResponse
from typing import Annotated,Literal
from pydantic import BaseModel,Field,computed_field
from pathlib import Path as FilePath
import json

app = FastAPI()
# Keep the shared data file in the project root, next to the other examples.
DATA_FILE = FilePath(__file__).parent.parent / 'patients.json'

class Patient(BaseModel):

    id: Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name: Annotated[str,Field(...,description='Name of the Patient',examples=['Abhay'])]
    city: Annotated[str,Field(...,description='Name of the City',examples=['Noida'])]
    age: Annotated[int,Field(...,gt=0,lt=120,description='Age of the Patient')]
    gender: Annotated[Literal['Male','Female','Others'],Field(...,description='Gender of the Patient')]
    height: Annotated[float,Field(...,gt=0,description='Height of the Patient in Meters')]
    weight: Annotated[float,Field(...,gt=0,description='Weight of the Patient in Kg')]
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25 :
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

def load_data():
    with DATA_FILE.open('r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with DATA_FILE.open('w') as f:
        json.dump(data,f)

@app.get("/") # / means home endpoint
# uvicorn main:app  --> we can access the page but if we do any chances then we have to restart the server 
# uvivorn main:app --> we can access the page and at the same time update without reloading it 
def read_root():
    return{"Message": "Hello guys"}

@app.get("/greet")
def greet():
    return{"Message":"Hello all"}

@app.get("/greet/{name}")
# if you want to send data dynamically through the url then have to create path parameter
def greet_name(name:str, age:int):
    return {"Message":f"hello {name} and i am {age} year old"}

@app.get('/about')
def about():
    return {'message':'A fully fucntional appi to manage your project records'}
@app.get('/view')
def view():
    data = load_data()

    return data
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(...,description='ID of the patient in the DB',example='P002')):
    # load all the patient
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='sort in the basis of height , weight or bmi'),
                  order:str = Query('asc',description='sort in asc or desc order')):
    valid_fields = ['height','weight','bmi']

    if sort_by not in valid_fields :
        raise HTTPException(status_code=400,detail= f'Invalid field select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f'Invalid order select between asc and desc')

    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    #load exisiting data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient Already exists')
    

    #new patient add to the database
    data[patient.id]=patient.model_dump(exclude=['id'])

    #save into the json file
    save_data(data)


    return JSONResponse(status_code=201, content={'message':'patient created successfully'})