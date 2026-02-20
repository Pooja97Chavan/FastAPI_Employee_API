from fastapi import FastAPI, HTTPException
from schema import Employee
import json
import os

app = FastAPI()

FILE_NAME = "employees_data.json"


# Helper function to read data safely
def read_data():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r", encoding="utf-8-sig") as f:
        return json.load(f)


# Helper function to write data
def write_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


# Get All Employees
@app.get("/all_employees")
def getAllEmployees():
    return read_data()


# Get Employee by ID
@app.get("/get_employee/{id}")
def get_employee(id: int):
    db = read_data()
    if str(id) not in db:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db[str(id)]


# Add Employee
@app.post("/add_employee")
def addEmployee(obj: Employee):
    db = read_data()

    if str(obj.id) in db:
        raise HTTPException(status_code=400, detail="Employee already exists")

    db[str(obj.id)] = {
        "Name": obj.name,
        "Department": obj.department,
        "Salary": obj.salary,
        "Is Active": obj.is_active
    }

    write_data(db)
    return {"message": "Employee added successfully", "data": db[str(obj.id)]}


# Update Employee
@app.put("/update_employee/{id}")
def updateEmployee(id: int, obj: Employee):
    db = read_data()

    if str(id) not in db:
        raise HTTPException(status_code=404, detail="Employee not found")

    db[str(id)] = {
        "Name": obj.name,
        "Department": obj.department,
        "Salary": obj.salary,
        "Is Active": obj.is_active
    }

    write_data(db)
    return {"message": "Employee updated successfully", "data": db[str(id)]}


# Delete Employee
@app.delete("/delete_employee/{id}")
def deleteEmployee(id: int):
    db = read_data()

    if str(id) not in db:
        raise HTTPException(status_code=404, detail="Employee not found")

    record = db.pop(str(id))
    write_data(db)

    return {"message": "Employee deleted successfully", "deleted_data": record}

