from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated
class Patient(BaseModel):
        name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give you name in less than 50 words', examples=['Nitish','Amit'])]
        email: EmailStr
        linkedin_url: AnyUrl
        age: int = Field(gt=0, lt=100)
        weight: float
        height: float
        married: Annotated[bool, Field(default=None, description='You married status here in True or False')]

        allergies: Annotated[Optional[str], Field(default=None, description='Mention your allergies in list format')]

        contact_details: Dict[str,str]

        @field_validator('email', mode='before') # Pydantic do type coersion. To type coersion se phele agr field_validator lagana hai to mode='before' agr field_validator baad me lagana hai to mode='after'.>        @classmethod
        def email_validator(cls, value):
            valid_domains=['hdfc.com','icici.com']
            domain_name=value.split('@')[-1]

            if domain_name not in valid_domains:
                raise ValueError('Not a valid domain')
            return value

        @model_validator(mode='after')
        def validate_emergency_contact(self):
              if self.age>60 and 'emergency' not in self.contact_details:
                    raise ValueError('Patient older than 60 must have an emergency contact.')

    # Use model_validator when:

        #Validation depends on multiple fields together.

        #One field logically conflicts with another.

        #You want to apply final transformations/cleaning after validation.     

        @computed_field
        @property
        def bmi(self)->float:
              bmi=round(self.weight/self.height**2, 2)  
              return bmi
        
        

patient_info={'name':'nitish','age':20, 'weight': 76.4,'height':1.7,'email':'aman@hdfc.com', 'married': True, 'contact_details':{'email':'rajattsharma87077@hdfc.com', 'mobile_number': '8707786096'},
              'linkedin_url':'https://www.linkedin.com/in/shrmarajat/'}

patient_1= Patient(**patient_info)

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.contact_details)
    print(patient.allergies)
    print(patient_1.bmi)

insert_patient_data(patient_1)





## We can also make nested Pydantic Models 