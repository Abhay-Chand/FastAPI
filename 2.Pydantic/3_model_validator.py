# Model validators - interview revision notes
#
# 1. @model_validator validates the complete model rather than one field.
#    Use it when a rule depends on two or more values together.
# 2. mode='after' runs after all individual fields have been parsed and
#    validated, so the validator can safely inspect typed model attributes.
# 3. An after model validator receives the model instance. Return that same
#    instance, or a modified instance, when validation succeeds.
# 4. Raising ValueError stops model creation and Pydantic wraps the message in
#    a ValidationError. In this example, older patients need an emergency key.
# 5. mode='before' receives raw input, normally a dict, before field parsing.
#    It is useful for normalizing input but requires defensive type checks.
# 6. Field validator versus model validator: field rules are local; model rules
#    express cross-field invariants such as password confirmation or date order.
# 7. Interview answer: model validation enforces business rules that cannot be
#    represented by a single field type or constraint.

from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator
from typing import List,Dict,Optional,Annotated



class Patient(BaseModel):
    # These fields are individually valid, but the business rule below uses
    # age and contact_details together.
    name: str
    email:EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str,str]


    # if Validation depend on more then one validator
    @model_validator(mode='after')
    def validate_emergency_contact(self):
        # mode='after' gives access to the fully validated Patient instance.
        if self.age > 60 and 'emergency' not in self.contact_details:
            # The entire model is rejected when the cross-field rule fails.
            raise ValueError('Patients older than 60 must have an emergency contact.')
        # An after model validator must return the model instance.
        return self

def updated_patient_data(patient: Patient):

    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.allergies)
    print(patient.weight)
    print('updated')
# This case passes because an elderly patient has an emergency contact.
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
# Patient(**patient_info) runs field validation first, then model validation.
patient1 = Patient(**patient_info)

updated_patient_data(patient1)

# Try removing 'emergency' to see ValidationError. Remember: field_validator
# handles one field; model_validator enforces relationships between fields.
# Interview example: password and password_confirmation should match.