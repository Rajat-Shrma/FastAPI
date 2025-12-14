# def insert_patient_data(name, age):
#     print(name)
#     print(age)
#     print('inserted into database')


# insert_patient_data('nitish', 'thirty') 
# No type Validation

# def insert_patient_data(name: str, age: int): #Type Hinting do not produce errors
#     print(name)
#     print(age)
#     print('inserted into database')

# insert_patient_data('nitish', 'thirty') 
#No Error


def insert_patient_data(name: str, age: int): #Type Hinting do not produce errors
    if type(name)==str and type(age)==int:
        print(name)
        print(age)
        print('inserted into database')

# insert_patient_data('nitish', 'thirty') #error
# insert_patient_data('nitish', 30)
# But not Scalable
# Jahan jahan yeh variable use honge wahan wahan condition lagani padegi

### TYPE VALIDATION TO HOGYA 
### AB DATA VALIDATION

def insert_patient_data(name: str, age: int): #Type Hinting do not produce errors
    if type(name)==str and type(age)==int:
        if age<0:
            print(name)
            print(age)
            print('inserted into database')

# This also not scalable