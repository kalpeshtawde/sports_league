# Generated by Django 3.2.11 on 2022-03-10 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0007_auto_20220310_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='city',
            field=models.CharField(blank=True, db_index=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='country',
            field=models.CharField(blank=True, db_index=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='name',
            field=models.CharField(db_index=True, max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='state',
            field=models.CharField(blank=True, db_index=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='status',
            field=models.CharField(choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')], default='ongoing', max_length=256),
        ),
        migrations.AlterField(
            model_name='leagueapplication',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=256),
        ),
        migrations.AlterField(
            model_name='match',
            name='format',
            field=models.CharField(choices=[('single', 'Single'), ('double', 'Double'), ('mix_double', 'Mix Double')], default='single', max_length=256),
        ),
        migrations.AlterField(
            model_name='match',
            name='match_status',
            field=models.CharField(choices=[('completed', 'Completed'), ('draw', 'Draw'), ('cancelled', 'Cancelled'), ('pending', 'Pending')], db_index=True, default='single', max_length=256),
        ),
        migrations.AlterField(
            model_name='matchrequest',
            name='format',
            field=models.CharField(choices=[('single', 'Single'), ('double', 'Double'), ('mix_double', 'Mix Double')], default='single', max_length=256),
        ),
    ]
