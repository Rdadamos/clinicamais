# Generated by Django 2.2.7 on 2019-11-28 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0005_auto_20191126_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='canceled',
            field=models.BooleanField(default=False),
        ),
    ]
