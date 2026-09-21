from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator
from typing import List,Dict,Optional,Annotated



class Patient(BaseModel):
    name: str
    email:EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str,str]


    # if Validation depend on more then one validator
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact.')
        return model
def updated_patient_data(patient: Patient):

    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.allergies)
    print(patient.weight)
    print('updated')
patient_info = {
    'name': 'abhay',
    'email': 'abhaychand639@icici.com',
    'age': 67,
    'weight': 47.9,
    'married': False,
    'allergies': [],
    'contact_details': {
        'email': 'abc@gmail.com',
        'Phone': '+91 6398579183',
        'emergency':'+91 9627093874'
    },
}
patient1 = Patient(**patient_info)

updated_patient_data(patient1)