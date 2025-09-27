from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    
    name: str = Field(max_length = 50)
    age: int = Field(gt= 0)
    email: EmailStr
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: bool = False
    allergies:Annotated[Optional[List[str]], Field(default= None, max_length=10, Description = 'Diseases.? ')] 
    contact_detail: Dict[str, str] = None
    

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        
        if model.age > 60 and 'emergency' not in model.contact_detail:
            raise('Add Emergencycontact number')
        return model
    
    
    
def insert_patient(patient: Patient):
    print('Name: ',patient.name)
    print('Age: ',patient.age)
    print('Married: ',patient.married)
    print('Email: ', patient.email)
    print('Allergies: ',patient.allergies)
    print('Contact Details: ',patient.contact_detail)
    print('inserted')
    

patient_detial = { 'name': 'David', 'email': 'abc@gmail.com','age':330, 'weight':58.20, 'married':False,'contact_detail':{'mob':'469465651'}}    

patient1 = Patient(**patient_detial)

insert_patient(patient1)