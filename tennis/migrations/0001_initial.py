# Generated by Django 3.2.8 on 2021-10-09 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=64)),
                ('city', models.CharField(db_index=True, max_length=64)),
                ('state', models.CharField(db_index=True, max_length=64)),
                ('country', models.CharField(db_index=True, max_length=64)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('level', models.FloatField(blank=True, help_text='Level of the league', null=True)),
                ('description', models.CharField(blank=True, db_index=True, max_length=2000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('players', models.ManyToManyField(blank=True, related_name='leagueplayer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('single', 'Single'), ('double', 'Double'), ('mix_double', 'Mix Double')], db_index=True, default='single', max_length=64)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('league', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tennis.league')),
                ('player_four', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pfour', to=settings.AUTH_USER_MODEL)),
                ('player_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pone', to=settings.AUTH_USER_MODEL)),
                ('player_three', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pthree', to=settings.AUTH_USER_MODEL)),
                ('player_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ptwo', to=settings.AUTH_USER_MODEL)),
                ('winner_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wone', to=settings.AUTH_USER_MODEL)),
                ('winner_two', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wtwo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]