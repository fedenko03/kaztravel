# Generated by Django 4.0.3 on 2022-04-26 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_places_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='pic',
            field=models.ImageField(upload_to='static/images/places'),
        ),
    ]
