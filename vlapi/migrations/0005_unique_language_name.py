# Generated by Django 3.1.4 on 2021-02-21 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vlapi', '0004_populate_languages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=2, unique=True),
        ),
    ]
