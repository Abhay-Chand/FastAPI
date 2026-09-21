from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated



class Patient(BaseModel):
    name: str
    email:EmailStr
    age: int
    weight: float   # in kg
    married: bool 
    height: float  # meters
    allergies: List[str]
    contact_details: Dict[str,str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
def updated_patient_data(patient: Patient):

    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.allergies)
    print(patient.weight)
    print('BMI : ', patient.bmi)
    print('updated')
patient_info = {
    'name': 'abhay',
    'email': 'abhaychand639@icici.com',
    'age': 67,
    'weight': 47.9,
    'height' : 1.72,
    'married': False,
    'allergies': [],
    'contact_details': {
        'email': 'abc@gmail.com',
        'Phone': '+91 6398579183',
        'emergency':'+91 9627093874',
    },
}
patient1 = Patient(**patient_info)

updated_patient_data(patient1)