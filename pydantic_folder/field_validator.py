from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    
    name: str = Field(max_length = 50)
    age: int = Field(gt= 0)
    email: EmailStr
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: bool = False
    allergies:Annotated[Optional[List[str]], Field(default= None, max_length=10, Description = 'Diseases.? ')] 
    contact_detail: Dict[str, str] = None
    
    
def insert_patient(patient: Patient):
    print('Name: ',patient.name)
    print('Age: ',patient.age)
    print('Married: ',patient.married)
    print('Email: ', patient.email)
    print('Allergies: ',patient.allergies)
    print('Contact Details: ',patient.contact_detail)
    print('inserted')
    

patient_detial = { 'name': 'David', 'email': 'abc@gmail.com','age':30, 'weight':58.20, 'married':False}    

patient1 = Patient(**patient_detial)

insert_patient(patient1)