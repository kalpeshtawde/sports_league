# Generated by Django 3.2.11 on 2022-03-21 02:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0009_auto_20220313_0317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('street', models.CharField(db_index=True, max_length=255, unique=True)),
                ('city', models.CharField(db_index=True, max_length=255, unique=True)),
                ('state', models.CharField(db_index=True, max_length=255, unique=True)),
                ('zip', models.CharField(db_index=True, max_length=255, unique=True)),
                ('type', models.CharField(db_index=True, max_length=255, unique=True)),
            ],
        ),
    ]
