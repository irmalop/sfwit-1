# Generated by Django 4.0.3 on 2022-06-01 09:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Nombre')),
                ('fathers_surname', models.CharField(max_length=40, verbose_name='Apellido paterno')),
                ('mothers_surname', models.CharField(max_length=40, verbose_name='Apellido materno')),
                ('sexo', models.CharField(choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Prefiero no decirlo', 'Prefiero no decirlo')], default='Hombre', max_length=20, verbose_name='Sexo')),
                ('birth_date', models.DateField(blank=True, verbose_name='Fecha de nacimiento')),
                ('marital_status', models.CharField(choices=[('Soltero', 'Soltero'), ('Casado', 'Casado'), ('Viudo', 'Viudo'), ('Divorciado', 'Divorciado'), ('Union libre', 'Union libre'), ('Prefiero no decirlo', 'Prefiero no decirlo')], default='Soltero', max_length=20, verbose_name='Estado civil')),
                ('age', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(80)], verbose_name='Edad')),
                ('email', models.EmailField(max_length=100, verbose_name='Correo')),
                ('state', models.CharField(max_length=50, verbose_name='Estado de residencia')),
                ('municipality', models.CharField(max_length=50, verbose_name='Municipio de residencia')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='data', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'personal_data',
            },
        ),
        migrations.CreateModel(
            name='ApplicantVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.URLField(blank=True, null=True, verbose_name='video')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'applicant_video',
            },
        ),
        migrations.CreateModel(
            name='AcademicData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('Curso', 'Curso'), ('Certificacion', 'Certificacion'), ('Carrera t??cnica', 'Carrera t??cnica'), ('Universidad', 'Universidad'), ('Maestria', 'Maestria'), ('Doctorado', 'Doctorado')], default='Curso', max_length=30, verbose_name='Nivel')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('institution', models.CharField(max_length=50, verbose_name='Instituci??n')),
                ('duration', models.CharField(max_length=50, verbose_name='Duraci??n')),
                ('status', models.CharField(choices=[('Finalizado', 'Finalizado'), ('Trunco', 'Trunco'), ('En curso', 'En curso')], default='Finalizado', max_length=20, verbose_name='Estatus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'academic_data',
            },
        ),
    ]
