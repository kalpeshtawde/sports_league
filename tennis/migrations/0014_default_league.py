# Generated by Django 3.2.11 on 2022-04-18 00:25

from django.conf import settings
from django.db import migrations


def default_league(apps, schema_editor):
    League = apps.get_model("tennis", "League")
    league = League(name='Not Applicable')
    league.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tennis', '0013_rename_userquery_userenquiry'),
    ]

    operations = [
        migrations.RunPython(default_league),
    ]
