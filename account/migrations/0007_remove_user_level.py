# Generated by Django 3.2.11 on 2022-04-09 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_user_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='level',
        ),
    ]
