# Generated by Django 3.2.7 on 2021-10-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happenings', '0002_event_host'),
        ('authenticate', '0003_rename_interests_user_interested_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='interested_events',
            field=models.ManyToManyField(related_name='users', to='happenings.Schedule'),
        ),
    ]
