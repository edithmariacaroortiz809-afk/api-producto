from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title = "Mi Student API",
    description = "Mini API para gestionar estudiantes",
    version = "1.0.0"
)

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    program: str = Field(..., min_length=5, description="Nombre completo del estudiante")
    active: bool

class Student(StudentCreate):
    id: int

students = [
    {
        "id": 1,
        "name": "Santiago Rodríguez",
        "email": "santiago.rodriguez@gmail.com",
        "program": "Ingeniería de Sistemas",
        "active": True
    },
    {
        "id": 2,
        "name": "Valentina Gómez",
        "email": "valentina.gomez@gmail.com",
        "program": "Administración de Empresas",
        "active": True
    },
    {
        "id": 3,
        "name": "Juan Esteban Martínez",
        "email": "juan.martinez@gmail.com",
        "program": "Derecho",
        "active": False
    },
    {
        "id": 4,
        "name": "Camila Herrera",
        "email": "camila.herrera@gmail.com",
        "program": "Medicina",
        "active": True
    },
    {
        "id": 5,
        "name": "Andrés Felipe Torres",
        "email": "andres.torres@gmail.com",
        "program": "Arquitectura",
        "active": True
    }
]

@app.get("/")
def home():
    return {
        "message" : "Bienvenido a mi API estudiantes",
        "endpoints" : [
            "GET /students/{id}", "Obtener estudiantes por su ID",
            "POST /students", "Crear a un nuevo estudiante",
            "GET /students?active=true", "Ver estudiantes activos",
            "GET /students?active=false", "Ver estudiantes no activos",
        ]
    }

@app.get("/students/{student_id}", response_model=Student)
def get_student_by_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Estudiante no encontrado")

@app.post("/students", response_model=Student, status_code = status.HTTP_201_CREATED)
def create_student(student_data: StudentCreate):
    new_id = len(students) + 1
    new_student = {
        "id": new_id,
        "name": student_data.name,
        "email": student_data.email,
        "program": student_data.program,
        "active": student_data.active
    }
    students.append(new_student)
    return new_student

@app.get("/students", response_model=list[Student])
def get_students(active: bool = None):
    if active is None:
        return students
    return [student for student in students if student["active"] == active]