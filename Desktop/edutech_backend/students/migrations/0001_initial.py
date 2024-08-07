# Generated by Django 3.2.25 on 2024-05-26 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uniqueId', models.CharField(max_length=50, unique=True)),
                ('admNumber', models.CharField(max_length=255)),
                ('schoolCode', models.CharField(max_length=50)),
                ('firstName', models.CharField(max_length=255)),
                ('middleName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('studentGender', models.CharField(max_length=255)),
                ('deleteFlag', models.CharField(default='N', max_length=1)),
                ('transferFlag', models.CharField(default='N', max_length=1)),
                ('dob', models.DateField()),
                ('dateOfAdmission', models.DateField()),
                ('healthStatus', models.CharField(max_length=255)),
                ('grade', models.IntegerField()),
                ('stream', models.IntegerField()),
                ('schoolStatus', models.CharField(max_length=255)),
                ('dormitory', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=1)),
                ('parentID', models.IntegerField()),
                ('schoolID', models.IntegerField()),
                ('urls', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='StudentAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='students.students')),
            ],
        ),
    ]
