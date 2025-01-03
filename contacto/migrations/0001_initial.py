# Generated by Django 3.1.5 on 2021-01-12 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('correo', models.EmailField(max_length=255)),
                ('nombrecompleto', models.CharField(max_length=255)),
                ('telefono', models.IntegerField()),
                ('observaciones', models.TextField()),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
