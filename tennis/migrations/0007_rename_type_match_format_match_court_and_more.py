# Generated by Django 4.0.1 on 2022-01-17 23:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tennis', '0006_auto_20211015_0341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='type',
            new_name='format',
        ),
        migrations.AddField(
            model_name='match',
            name='court',
            field=models.CharField(blank=True, db_index=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='match_status',
            field=models.CharField(choices=[('completed', 'Completed'), ('draw', 'Draw'), ('cancelled', 'Cancelled'), ('pending', 'Pending')], db_index=True, default='single', max_length=64),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner_one',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wone', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MatchRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('format', models.CharField(choices=[('single', 'Single'), ('double', 'Double'), ('mix_double', 'Mix Double')], db_index=True, default='single', max_length=64)),
                ('court', models.CharField(blank=True, db_index=True, max_length=2000, null=True)),
                ('match_time', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiry_at', models.DateTimeField(auto_now_add=True)),
                ('accepted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('league', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tennis.league')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]