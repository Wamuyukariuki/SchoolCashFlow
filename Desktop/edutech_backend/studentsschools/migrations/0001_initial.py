# Generated by Django 3.2.25 on 2024-05-26 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schools', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentsSchools',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dateCreated', models.DateField(auto_now_add=True)),
                ('schoolID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.schools')),
                ('studentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.students')),
            ],
        ),
    ]
