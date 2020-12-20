# Generated by Django 3.1.4 on 2020-12-13 11:10

from django.db import migrations

def add_category_names(apps, schema_editor):
    Category = apps.get_model('vlapi', 'Category')

    culture = Category(name='culture')
    interviews = Category(name='interviews')
    pixels = Category(name='pixels')

    Category.objects.bulk_create([culture, interviews, pixels])


class Migration(migrations.Migration):

    dependencies = [
        ('vlapi', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_category_names)
    ]
