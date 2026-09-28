# Field validators - interview revision notes
#
# 1. @field_validator targets one or more fields and runs custom validation
#    during Pydantic model creation.
# 2. The validator must be a class method in this style: @field_validator(...)
#    followed by @classmethod. It receives the class and the field value.
# 3. Return the value to keep it. Returning a changed value transforms data;
#    raising ValueError creates a normal Pydantic validation error.
# 4. mode='after' runs after Pydantic's built-in type conversion and validation.
#    mode='before' runs on raw input and is useful for preprocessing strings,
#    but the validator must then handle untrusted input types carefully.
# 5. This example validates an email domain, uppercases the name, and checks
#    that age is between 0 and 100. Multiple validators can target one model.
# 6. Field validators are best for rules involving one field. Use
#    @model_validator when a rule depends on multiple fields.
# 7. Interview distinction: validation checks correctness; transformation
#    changes the value returned by the model, such as name.upper().

from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    # Every field below gets Pydantic's normal type validation first.
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
        # This custom rule runs for the email field during model creation.
        valid_domains = ['hdfc.com','icici.com']
        # EmailStr has already checked the basic email shape.
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            # ValueError is converted into a Pydantic ValidationError.
            raise ValueError('Not a valid domain')

        # Returning the value keeps it in the model unchanged.
        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        # A validator can also normalize data, not only reject it.
        return value.upper()

    @field_validator('age',mode ='after')
    @classmethod
    def validate(cls, value):
        # mode='after' receives the value after Pydantic converts it to int.
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 to 100 in between')

def updated_patient_data(patient: Patient):
    # The name is already uppercase because transform_name ran at creation.

    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.allergies)
    print(patient.weight)
    print('updated')
# This input demonstrates all three custom validators.
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
# Patient creation runs built-in validation and then the custom validators.
patient1 = Patient(**patient_info)

updated_patient_data(patient1)

# Remember: use field_validator for one-field rules. Use mode='before' to
# normalize raw input and mode='after' for already-typed values. Interview
# question: what must a successful validator do? Return the accepted value.