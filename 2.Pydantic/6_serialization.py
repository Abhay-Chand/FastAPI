# Serialization - interview revision notes
#
# 1. Serialization converts a Pydantic model into a transport format such as a
#    dict or JSON. Deserialization parses external data into a typed model.
# 2. model_dump() returns a Python dictionary. Nested BaseModel values are also
#    converted to dictionaries, making the result suitable for application code.
# 3. model_dump_json() returns a JSON string, useful when a JSON payload is
#    explicitly required. It is different from model_dump(), which returns dict.
# 4. exclude=['name'] removes selected fields from the output. include can be
#    used to keep only selected fields. Nested selections use mappings such as
#    exclude={'address': {'state'}}.
# 5. exclude_unset=True removes fields that were not supplied by the caller.
#    In this example, the default gender is omitted because it was not input.
# 6. Other useful options include exclude_none=True, exclude_defaults=True,
#    by_alias=True, and round_trip=True depending on the API contract.
# 7. Interview distinction: model_dump is for Python data; model_dump_json is
#    for JSON text. FastAPI normally handles response serialization for you.

from pydantic import BaseModel

class Address(BaseModel):
    # Nested models are recursively converted during serialization.
    city:str
    state:str
    pin:str
class Patient(BaseModel):
    # gender has a default, which lets us demonstrate exclude_unset=True.
    name: str
    gender: str = 'Male'
    age: int
    address: Address

# Build and validate the nested Address first.
address_dict = {'city':'Tanakpur','state':'Uttarakhand','pin':'262309'}
address1 = Address(**address_dict)

# gender is intentionally omitted, so Pydantic applies the default 'Male'.
patient_dict = {'name':'abhay chand','age':35,'address':address1}

patient1 = Patient(**patient_dict)

# model_dump returns a Python dict. This first result excludes name.
temp = patient1.model_dump(exclude=['name'])
# This assignment replaces temp; only explicitly supplied fields remain.
temp = patient1.model_dump(exclude_unset=True)


print(temp)
print(type(temp))

# model_dump_json returns JSON text, not a Python dictionary.
temp1 = patient1.model_dump_json()

print(temp1)
print(type(temp1))

# Serialization is used when sending model data to an API client or database.
# Interview distinction: model_dump() gives Python data; model_dump_json() gives
# a JSON string. Useful options include include, exclude_none, by_alias, and
# exclude_defaults. Deserialization in Pydantic is model creation from input.