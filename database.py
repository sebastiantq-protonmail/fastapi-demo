from peewee import * # Es un ORM para manejar los datos
from config import *

database = MySQLDatabase( # En realidad se puede utilizar cualquier base de datos
    DATABASE,
    user = USER,
    password = PASSWORD,
    port = 3306
)

# Modelo que almacena la información de los estudiantes
class Student(Model):
    id = PrimaryKeyField(unique=True)
    cc = IntegerField(unique=True)
    email = CharField(unique=True)
    name = TextField()
    last_name = TextField(null=True)

    def __str__(self):
        return self.id

    class Meta:
        database = database
        table_name = "students"

# Modelo que almacena las credenciales de las cuentas de los estudiantes
class Account(Model):
    student = ForeignKeyField(Student, to_field="id")
    username = CharField(max_length=20, unique=True)
    password = CharField()

    def __str__(self):
        return self.student

    class Meta:
        database = database
        table_name = "accounts"

# Modelo que almacena los cursos dictados
class Course(Model):
    name = CharField(unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        database = database
        table_name = "courses"

# Modelo que relaciona estudiantes con cursos
class StudentCourse(Model):
    student_id = ForeignKeyField(Student, to_field="id")
    course_id = ForeignKeyField(Course, to_field="id")
    
    def __str__(self):
        return self.student_id

    class Meta:
        database = database
        table_name = "studentcourse"

# Modelo que relaciona notas con un estudiante matriculado en un curso
class Calification(Model):
    student_course_id = ForeignKeyField(StudentCourse, to_field="id")
    calification = FloatField()
    
    def __str__(self):
        return self.calification

    class Meta:
        database = database
        table_name = "califications"