from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Optional,Annotated



class Patient(BaseModel):
    name: str
    email:EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com','icici.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @field_validator('age',mode ='after')
    @classmethod
    def validate(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 to 100 in between')

    # if Validation depend on more then one validator
    @mod_


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
    'age': 30,
    'weight': 47.9,
    'married': False,
    'allergies': [],
    'contact_details': {
        'email': 'abc@gmail.com',
        'Phone': '+91 6398579183',
    },
}
patient1 = Patient(**patient_info)

updated_patient_data(patient1)