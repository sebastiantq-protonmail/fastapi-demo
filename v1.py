from fastapi import APIRouter, HTTPException

from database import *
from schemas import *

v1 = APIRouter()

@v1.get("/")
async def index(): # Las peticiones son asincronas en FastAPI
    return "API funcionando correctamente"

@v1.post("/register")
async def createStudent(register: RegisterRequestModel):
    student = Student.create(
        cc = register.cc,
        email = register.email,
        name = register.name,
        last_name = register.last_name
    )
    
    account = Account.create(
        student_id = student.id,
        username = register.username,
        password = register.password
    )

    return register

@v1.get("/student/{id}")
async def getStudent(id: int):
    student = Student.select() \
                     .where(Student.id == id) \
                     .first()

    if student:
        return RegisterReponseModel(id = student.id,
                                    cc = student.cc,
                                    name = student.name,
                                    last_name = student.last_name,
                                    email = student.email)
    else:
        return HTTPException(404, "Estudiante no encontrado")

@v1.get("/students/{course_id}")
async def getStudentsFromCourse(course_id: int):
    students = StudentCourse.select(Student, Course.name) \
                            .join(Student, on=(StudentCourse.student_id == Student.id)) \
                            .join(Course, on=(StudentCourse.course_id == Course.id)) \
                            .where(StudentCourse.course_id == course_id)

    data = {}

    for i, student in enumerate(students):
        data[i] = student

    if students:
        return data
    else:
        return HTTPException(204, "El curso no cuenta con estudiantes")

@v1.post("/course")
async def addCourse(course: CourseRequestModel):
    course = Course.create(
        name = course.name
    )

    return course

@v1.post("/matriculate")
async def matriculateStudent(request: StudentCourseRequestModel):
    studentcourse = StudentCourse.create(
        student_id = request.student_id,
        course_id = request.course_id
    )

    return studentcourse

@v1.delete("/desmatriculate/{student_id}/{course_id}")
async def desmatriculateStudent(student_id: int, course_id: int):
    query = StudentCourse.delete() \
                         .where(StudentCourse.student_id == student_id, StudentCourse.course_id == course_id) \
                         .execute()
    
    if query:
        return "Estudiante desmatriculado con exito"
    else:
        return HTTPException(404, "El estudiante no se encontraba matriculado")
    

@v1.post("/calification")
async def setStudentCourseCalification(request: CalificationRequestModel):
    calificationRecord = Calification.create(
        student_course_id = request.student_course_id,
        calification = request.calification
    )

    return calificationRecord

@v1.get("/califications/{student_id}")
async def getStudentCalifications(student_id: int):
    califications = Calification.select() \
                                .join(StudentCourse, on=(Calification.student_course_id == StudentCourse.id)) \
                                .where(StudentCourse.student_id == student_id)

    data = {}

    for i, calification in enumerate(califications):
        data[i] = calification

    if califications:
        return data
    else:
        return HTTPException(204, "El estudiante no cuenta con calificaciones")

@v1.put("/calification/{calification_id}/{calification}")
async def updateCalification(calification_id: int, calification: float):
    query = Calification.update(calification = calification) \
                        .where(Calification.id == calification_id) \
                        .execute()

    if query:
        return "Calificación actualizada"
    else:
        return HTTPException(404, "No se ha encontrado la calificación")