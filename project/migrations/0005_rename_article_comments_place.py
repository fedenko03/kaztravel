# Generated by Django 4.0.3 on 2022-05-20 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='article',
            new_name='place',
        ),
    ]
