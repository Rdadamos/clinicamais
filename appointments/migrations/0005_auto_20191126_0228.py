# Generated by Django 2.2.7 on 2019-11-26 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190630_1923'),
        ('appointments', '0004_auto_20191125_1451'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='doctorschedule',
            unique_together={('doctor', 'day', 'hour')},
        ),
    ]
