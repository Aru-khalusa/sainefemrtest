# Generated by Django 4.0.1 on 2022-01-24 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hmsApp', '0004_alter_patientbio_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdiagnoses',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmsApp.patientvitals'),
        ),
    ]
