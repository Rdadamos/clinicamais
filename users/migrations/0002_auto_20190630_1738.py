# Generated by Django 2.2.2 on 2019-06-30 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendant',
            name='shift',
            field=models.CharField(choices=[('I', 'Integral'), ('M', 'Manhã'), ('T', 'Tarde')], default='I', max_length=1),
        ),
    ]
