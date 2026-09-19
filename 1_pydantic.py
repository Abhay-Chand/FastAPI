from pydantic import BaseModel, EmailStr, AnyUrl ,Field
from typing import List,Dict,Optional,Annotated
class Patient(BaseModel):


    name : str = Annotated(Field(max_length=50))
    email : EmailStr
    linkedin_url : AnyUrl
    age : int = Field(gt=0, lt=120)
    weight: float = Field(gt=0)
    married: bool = False
    allergies: Optional[List[str]] = Field(max_length=10)
    contact_details : Optional[Dict[str,str]] = None

def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.email)
    print(patient.linkedin_url)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)

    print('inserted')

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print('updated')
   
patient_info = {'name':'abhay','email':'abhaychand639@gmail.com','linkedin_url':'https://www.linkedin.com/in/abhay-chand/','age':30,'weight': 47.9,'contact_details':{'email':'abc@gmail.com','Phone':'+91 6398579183'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)