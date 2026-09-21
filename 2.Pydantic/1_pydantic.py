# Pydantic basics - interview revision notes
#
# 1. BaseModel is the foundation for Pydantic schemas. It validates input,
#    converts compatible types, applies defaults, and exposes clean attributes.
# 2. Type annotations define the contract: str, int, float, bool, List, Dict,
#    Optional, EmailStr, and AnyUrl are all validated when Patient is created.
# 3. EmailStr and AnyUrl perform format validation. EmailStr needs the optional
#    email-validator package installed in the active Python environment.
# 4. Field adds constraints and schema metadata. gt=0 means strictly greater
#    than zero; lt=120 means strictly less than 120; max_length limits a value.
# 5. Annotated[Type, Field(...)] keeps the type and its validation metadata
#    together. It is especially useful for FastAPI/OpenAPI documentation.
# 6. Optional[T] means None is allowed; it does not automatically mean the
#    field may be omitted. Give the field a default (usually None) to omit it.
# 7. Patient(**patient_info) validates the dictionary and creates a Patient
#    object. Invalid input raises pydantic.ValidationError.
# 8. Interview answer: Pydantic validates at the application boundary, so
#    downstream code can work with trusted, typed data instead of raw dicts.

from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List,Dict,Optional,Annotated

# These imports provide reusable types and validation metadata. In a FastAPI
# project, the same Pydantic model can validate request bodies and document API
# fields automatically.

class Patient(BaseModel):
    # BaseModel converts this class into a validated schema and data object.

    # Annotated keeps the Python type and Field constraints together.
    name : Annotated[str, Field(max_length=50, title='Name of the Patient',description='Give the name of the patient in less than 50 char', examples=['Nitish','Amit'])]
    # EmailStr rejects values that are not valid email addresses.
    email : EmailStr
    # AnyUrl validates the URL format, including its scheme.
    linkedin_url : AnyUrl
    # gt and lt are strict numeric boundaries: 0 < age < 120.
    age : int = Field(gt=0, lt=120)
    # The patient's weight must be greater than zero.
    weight: Annotated[float, Field(gt=0)]
    # The default allows this optional value to be omitted.
    married: Annotated[bool, Field(default=None,description='Is the patient married or not ')]
    # Optional means None is accepted; max_length limits the list to 10 items.
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=10)]
    # Optional nested dictionary; None is used when contact details are absent.
    contact_details : Optional[Dict[str,str]] = None

def insert_patient_data(patient: Patient):
    # The function receives validated data, so attribute access is predictable.

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
    # A type annotation documents that callers must provide a Patient object.

    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print('updated')
   
# Raw input normally comes from a request, JSON body, or database record.
patient_info = {'name':'abhay','email':'abhaychand639@gmail.com','linkedin_url':'https://www.linkedin.com/in/abhay-chand/','age':30,'weight': 47.9,'contact_details':{'email':'abc@gmail.com','Phone':'+91 6398579183'}}

# ** unpacks dictionary keys into model fields and triggers validation.
patient1 = Patient(**patient_info)

# If validation had failed, execution would stop before this function call.
insert_patient_data(patient1)

# Remember: annotations describe data, Field adds constraints, and BaseModel
# turns untrusted input into a validated object. Interview question: why use
# Pydantic instead of a plain dict? It centralizes validation and clear errors.