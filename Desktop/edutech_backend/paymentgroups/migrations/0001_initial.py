# Generated by Django 3.2.25 on 2024-05-26 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGroups',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('status', models.IntegerField(default=1)),
                ('dateCreated', models.DateField(auto_now_add=True)),
            ],
        ),
    ]