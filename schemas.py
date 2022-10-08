from typing import Optional # Para hacer los campos del modelo opcionales
from pydantic import BaseModel, root_validator, validator

# IMPORTANTE
#
# El siguiente es el único modelo que contiene validaciones por el hecho de ser una demo

class RegisterRequestModel(BaseModel):
    cc: int
    name: str
    last_name: Optional[str] = None # Ejemplo de uno de los campos opcionales
    username: str
    email: str
    password: str
    password_confirmation: str

    """ Esto en caso tal de que CC fuera str

    @validator("cc")
    def cc_not_contains_spaces(cls, value):
        if " " in value:
            raise ValueError("La cedula contiene espacios")

        return value

    @validator("cc")
    def cc_is_numeric(cls, value):
        if not value.isnumeric():
            raise ValueError("La cedula contiene caracteres no numericos")

        return value
        
    """

    @validator("name")
    def name_contains_only_letters(cls, value):
        if not value.isalpha():
            raise ValueError("El nombre debe contener solo letras")

        return value
        
    @validator("last_name")
    def lastname_contains_only_letters(cls, value):
        if value and not value.isalpha():
            raise ValueError("El apellido debe contener solo letras")

        return value
        
    @validator("username")
    def username_not_containts_spaces(cls, value):
        if " " in value:
            raise ValueError("El nombre de usuario no debe contener espacios")

        return value

    @validator("email")
    def email_is_valid(cls, value):
        if False:
            raise ValueError("El email es invalido")

        return value

    @root_validator
    def passwords_match(cls, values):
        if values.get("password") != values.get("password_confirmation"):
            raise ValueError("Las contraseñas no coinciden")

        return values

# IMPORTANTE
#
# Además tambien, este es el único modelo creado para dar una respuesta

class RegisterReponseModel(BaseModel):
    id: int
    cc: int
    name: str
    last_name: Optional[str] = None # Puede que no haya registrado apellidos
    email: str

# Modelo de request para agregar curso
class CourseRequestModel(BaseModel):
    name: str

# Modelo de request para matricular un estudiante a un curso
class StudentCourseRequestModel(BaseModel):
    student_id: int
    course_id: int

class CalificationRequestModel(BaseModel):
    student_course_id: int
    calification: float
