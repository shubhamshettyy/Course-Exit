# Generated by Django 2.2.6 on 2020-07-10 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20200707_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
    ]
