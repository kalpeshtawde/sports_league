# Generated by Django 4.0.1 on 2022-01-31 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchrequest',
            name='match_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
