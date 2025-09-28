from fastapi import FastAPI, Path, HTTPException, Query
from typing import Annotated, Literal
from pydantic import BaseModel, EmailStr, Field, computed_field
from fastapi.responses import JSONResponse
import json

app = FastAPI()

# Pydantic Object for creating pateint ...
class Patient(BaseModel):
    
    id : Annotated[str, Field(...,description='Patient Id')]
    name : Annotated[str, Field(...,description='Patient Name')]
    age : Annotated[int, Field(...,gt=0,lt=150,description='Patient Age')]
    height : Annotated[float, Field(...,description='Patient Height')]
    weight : Annotated[float, Field(...,description='Patient Weight')]
    gender : Annotated[Literal['Male', 'Female','Other'], Field(...,description='Patient Gender')]
    email : Annotated[EmailStr, Field(...,description='Patient Email')]
    address : Annotated[str, Field(...,description='Patient Address')]
    phone : Annotated[str, Field(...,description='Patient mobile number')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi 
    
    
    
    
    

# Utility Function for patients detail 
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

# Utility Function to save the patient data ...
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

# View all patients.....
@app.get('/')
def view():
    data = load_data()
    return data


# View a specific patients by their ID ...
@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(...,description='ID of the patient in the DB',example='2')):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=400, detail='Patient not found')



# Sort the Patients with their [ Height, Weight, bmi ] .....
@app.get('/sort')
def sort_patient(sort_by: str = Query(...,description='Sort patient by height,weight & bmi'),order: str = Query('asc',description = 'sort in asc or desc order')):
    
    valid_fields = ['height','weight','bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400 ,detail=f'Invalid fields select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400 ,detail='Invalide order select between asc & desc')
    
    sort_order = True if order =='desc' else False
    data = load_data()

    
    sorted_data = sorted(data.values(),key = lambda x:x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data


# Create a Patient ...

@app.post('/create-patient')
def create(patient: Patient):
    
    data = load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists.')
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    save_data(data)
    return JSONResponse(status_code=201,content='Patient created')
        




