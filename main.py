from fastapi import FastAPI

app = FastAPI()

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


