# Generated by Django 3.2.11 on 2022-03-20 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
