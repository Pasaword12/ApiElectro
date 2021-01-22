# Generated by Django 3.1.5 on 2021-01-12 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ordentrabajo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordentrabajo',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='ordentrabajo',
            name='autor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='autorAsignado', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ordentrabajo',
            name='id',
            field=models.AutoField(db_index=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ordentrabajo',
            name='rut',
            field=models.CharField(db_index=True, max_length=30),
        ),
    ]
