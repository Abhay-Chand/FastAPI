# Nested models - interview revision notes
#
# 1. A Pydantic model can use another BaseModel as a field type. Patient.address
#    is therefore an Address object, not an unvalidated generic dictionary.
# 2. Nested models organize related data, improve readability, and make models
#    reusable across endpoints, for example Address in Patient and Hospital.
# 3. Pydantic recursively validates nested input. Both an Address instance and
#    a compatible dictionary can be supplied for the address field.
# 4. Access nested data with patient.address.city. This gives typed, explicit
#    access instead of repeated dictionary lookups such as data['address'].
# 5. Validation errors include the nested path, for example address.city, which
#    makes bad API input easier to diagnose.
# 6. Interview answer: nested schemas model real domain composition and let one
#    validation framework enforce rules at every level of the object graph.

from pydantic import BaseModel

class Address(BaseModel):
    # Address owns address-specific validation and can be reused elsewhere.
    city:str
    state:str
    pin:str
class Patient(BaseModel):
    # The Address annotation creates a nested model relationship.
    name: str
    gender: str
    age: int
    address: Address

# A dictionary can be validated into an Address model using ** unpacking.
address_dict = {'city':'Tanakpur','state':'Uttarakhand','pin':'262309'}
address1 = Address(**address_dict)

# The patient receives an Address instance, not a loose nested dictionary.
patient_dict = {'name':'abhay chand','gender':'male','age':35,'address':address1}

patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.name)
print(patient1.address.city)
print(patient1.address.pin)

# Pydantic also accepts a compatible dictionary directly in the address field
# and recursively creates Address for you.

# Remember: nested models improve organization, reuse, readability, and
# validation. Interview question: what happens if pin is an integer? Pydantic
# validates the nested field according to Address's declared type.