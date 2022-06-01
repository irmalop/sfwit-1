import imp
from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator 

# Create your models here.
class ApplicantVideo(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    video= models.URLField('video', blank=True, null=True)
    def __str__(self): 
        return self.user.email
    class Meta:
        db_table='applicant_video'
SEX = (
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('Prefiero no decirlo', 'Prefiero no decirlo'),
)
MARITAL_STATUS = (
        ('Soltero', 'Soltero'),
        ('Casado', 'Casado'),
        ('Viudo', 'Viudo'),
        ('Divorciado', 'Divorciado'),
        ('Union libre', 'Union libre'),
        ('Prefiero no decirlo', 'Prefiero no decirlo'),
)
class PersonalData(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='data')
    name = models.CharField(max_length=40, null = False, verbose_name='Nombre')
    fathers_surname = models.CharField(max_length=40, null = False, verbose_name='Apellido paterno')
    mothers_surname = models.CharField(max_length=40, null = False, verbose_name='Apellido materno')
    sexo = models.CharField(max_length=20, choices=SEX, default='Hombre', verbose_name='Sexo')
    birth_date = models.DateField(null=False, blank=True, verbose_name='Fecha de nacimiento')
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS, default='Soltero', verbose_name='Estado civil')
    age = models.IntegerField(null=True, validators=[MinValueValidator(18), MaxValueValidator(80)], verbose_name='Edad')
    email = models.EmailField(max_length=100, verbose_name='Correo')
    state = models.CharField(max_length=50, verbose_name='Estado de residencia')
    municipality = models.CharField(max_length=50,  verbose_name='Municipio de residencia')
    def __str__(self): 
        return self.user.email
    class Meta:
        db_table='personal_data'
LEVEL = (
        ('Curso', 'Curso'),
        ('Certificacion', 'Certificacion'),
        ('Carrera técnica', 'Carrera técnica'),
        ('Universidad', 'Universidad'),
        ('Maestria', 'Maestria'),
        ('Doctorado', 'Doctorado'),
)
STATUS = (
        ('Finalizado', 'Finalizado'),
        ('Trunco', 'Trunco'),
        ('En curso', 'En curso'),
)
class AcademicData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='academic')
    # user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='academic')
    level = models.CharField(max_length=30, choices=LEVEL, default='Curso', verbose_name='Nivel')
    name = models.CharField(max_length=50, null = False, verbose_name='Nombre')
    institution = models.CharField(max_length=50, null = False, verbose_name='Institución')
    duration = models.CharField(max_length=50, null = False, verbose_name='Duración')
    status = models.CharField(max_length=20, choices=STATUS, default='Finalizado', verbose_name='Estatus')
    def __str__(self): 
        return self.user.email
    class Meta:
        db_table='academic_data'
# class Role(models.Model):
#     name = models.CharField(max_length=32, verbose_name='Rol')
#     class Meta:
#         db_table='role'
# class Area(models.Model):
#     name = models.CharField(max_length=32, verbose_name='Area')
#     role = models.ManyToManyField(Role)
#     class Meta:
#         db_table='area'
# MODALITY = (
#         ('Home office', 'Home office'),
#         ('Presencial', 'Presencial'),
#         ('Hibrido', 'Hibrido'),
# )
# TYPE_JOB = (
#         ('Medio tiempo','Medio tiempo'),
#         ('Tiempo completo','Tiempo completo'),
# )
# class InterestProfile(models.Model):
#     user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='interest')
#     area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
#     role = models.ManyToManyField(Role)
#     modality = models.CharField(max_length=50, choices=MODALITY,  default='Presencial', verbose_name='Modalidad')
#     type_job = models.CharField(max_length=20, choices=TYPE_JOB, default='Tiempo completo', verbose_name='Tipo de trabajo')
#     def __str__(self): 
#         return self.user.email
#     class Meta:
#         db_table='interest'