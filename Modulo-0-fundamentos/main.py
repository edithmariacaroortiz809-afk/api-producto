from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List


app = FastAPI()


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {"message": "Bienvenido a la API"}


# =========================
# MODELOS
# =========================

class Student(BaseModel):
    id: int
    name: str
    email: EmailStr
    program: str
    active: bool


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    program: str
    active: bool


# =========================
# BASE DE DATOS TEMPORAL
# =========================

students = [
    {
        "id": 1,
        "name": "Laura Gómez",
        "email": "laura.gomez@email.com",
        "program": "Análisis y Desarrollo de Software",
        "active": True
    },
    {
        "id": 2,
        "name": "Andrés Martínez",
        "email": "andres.martinez@email.com",
        "program": "Producción Multimedia",
        "active": False
    },
    {
        "id": 3,
        "name": "Carlos Pérez",
        "email": "carlos.perez@email.com",
        "program": "Gestión de Redes de Datos",
        "active": True
    },
    {
        "id": 4,
        "name": "Mariana Rodríguez",
        "email": "mariana.rodriguez@email.com",
        "program": "Análisis y Desarrollo de Software",
        "active": True
    },
    {
        "id": 5,
        "name": "Juan Esteban López",
        "email": "juan.lopez@email.com",
        "program": "Producción Multimedia",
        "active": False
    }
]


# =========================
# GET STUDENT BY ID
# =========================

@app.get("/students/{id}", response_model=Student)
def get_student(id: int):

    for student in students:
        if student["id"] == id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


# =========================
# CREATE STUDENT
# =========================

@app.post(
    "/students",
    response_model=Student,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: StudentCreate):

    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "email": student.email,
        "program": student.program,
        "active": student.active
    }

    students.append(new_student)

    return new_student


# =========================
# FILTER STUDENTS
# =========================

@app.get("/students", response_model=List[Student])
def get_students(active: bool):

    filtered_students = []

    for student in students:
        if student["active"] == active:
            filtered_students.append(student)

    return filtered_students