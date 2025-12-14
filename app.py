from fastapi import FastAPI, Path, HTTPException, Query

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
app = FastAPI()

# '''
#   "P001": {
#     "name": "Ananya Sharma",
#     "city": "Mumbai",
#     "age": 20,
#     "gender": "Female",
#     "height": 1.65,
#     "weight": 90.0,
#     "bmi": 33.0,
#     "verdict": "obese"
#   }
# '''

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Enter Your Id', examples=['P004','P002'])]
    name: Annotated[str, Field(..., description="Enter your name",max_length=50)]
    city: Annotated[str, Field(...,description="Enter your city",max_length=30, )]
    gender: Annotated[Literal['male', 'female','others'], Field(..., description='Patient Gender')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = self.weight/self.height**2
        return bmi
    
    @computed_field
    @property
    def verdict(self)->float:
        verdict=''
        if self.bmi<18.5:
            verdict = 'underweight'
        elif self.bmi>=18.5 and self.bmi<24.9:
            verdict='normal'
        elif self.bmi>=25 and self.bmi<29.9:
            verdict='overweight'
        else:
            verdict='obese'
        return verdict

class PatientUpdate(BaseModel):
    name: Annotated[str, Field(default=None, description="Enter your name",max_length=50)]
    city: Annotated[str, Field(default=None,description="Enter your city",max_length=30, )]
    gender: Annotated[Literal['male', 'female','others'], Field(default=None, description='Patient Gender')]
    age: Annotated[int, Field(default=None, gt=0, lt=120, description='Age of the patient')]
    height: Annotated[float, Field(default=None, gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(default=None, gt=0, description='Weight of the patient in kgs')]

    


def load_data():
    with open(r'data\patientdetails.json', 'r') as f:
        data=json.load(f)

    return data

def save_data(data):
    with open(r'C:\Users\hp\OneDrive\Desktop\MY\fastapitutorials\data\patientdetails.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient Management System"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records."}


@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description='This is a patient id.' ,example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    
    else:
        raise HTTPException(status_code=400, detail='Patient ID not found.')
    
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str= Query('asc', description='sort in asc or desc')):

    valid_fields=['height', 'weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid Field Select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc') 
    
    data= load_data()

    sort_order= True if order=='desc' else False
    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    data=load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    data[patient.id]=patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'New Patient created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info=data[patient_id]
    patient_upadate_dict=patient_update.model_dump(exclude_unset=True)

    for key, value in patient_upadate_dict.items():
        existing_patient_info[key]=value
    
    existing_patient_info['id']=patient_id
    updated_patient_info_obj=Patient(**existing_patient_info)
    data[patient_id]=updated_patient_info_obj.model_dump(exclude='id')

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Patient Updated!'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Patient deleted sucessfully'
    ''})

    

    
