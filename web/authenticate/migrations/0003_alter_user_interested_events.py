# Generated by Django 3.2.7 on 2021-10-25 14:53
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happenings', '0006_auto_20211016_1539'),

        ('authenticate', '0002_user_swiped_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='interested_events',
            field=models.ManyToManyField(blank=True, to='happenings.Schedule'),
        ),
    ]
