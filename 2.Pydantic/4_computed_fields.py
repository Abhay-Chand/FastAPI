# Computed fields - interview revision notes
#
# 1. @computed_field exposes a derived property as part of the Pydantic model
#    representation and serialization output.
# 2. Combine it with @property: @property defines normal Python access, while
#    @computed_field tells Pydantic to include the result in model_dump() and
#    model_dump_json(). Keep @computed_field above @property.
# 3. A computed field is not normally accepted as input and is calculated from
#    source fields. Here BMI is derived from weight in kilograms and height in
#    meters using BMI = weight / height squared.
# 4. Computed fields are recalculated when accessed, so do not use them for
#    stored state or expensive work without considering the cost.
# 5. They are useful for response schemas: API clients receive useful derived
#    values without duplicating business logic in every endpoint.
# 6. Interview distinction: Field stores validated input; computed_field exposes
#    a value derived from validated model state.

from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated



class Patient(BaseModel):
    # Weight is stored in kilograms and height is stored in meters.
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
        # BMI is derived data, so it is not supplied in patient_info.
        bmi = round(self.weight/(self.height**2),2)
        return bmi

def updated_patient_data(patient: Patient):

    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.allergies)
    print(patient.weight)
    # Accessing the property calculates the current BMI from model values.
    print('BMI : ', patient.bmi)
    print('updated')
# Input contains source fields only; bmi will be computed automatically.
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

# computed_field is included when serializing the model, but it is not a normal
# stored input field. Interview question: when should you use it? For cheap,
# deterministic values derived from validated fields, such as BMI or full_name.