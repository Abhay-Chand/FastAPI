from fastapi import FastAPI, Path, HTTPException
import json
app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

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