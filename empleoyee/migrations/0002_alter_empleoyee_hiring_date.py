# Generated by Django 3.2.8 on 2022-05-20 13:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleoyee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleoyee',
            name='hiring_date',
            field=models.TextField(default=datetime.date(2022, 5, 20)),
        ),
    ]
