# Generated by Django 4.2 on 2023-05-09 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Teachers', '0010_alter_examscore_classes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='user',
        ),
    ]
