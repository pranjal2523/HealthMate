# Generated by Django 3.0.3 on 2023-05-15 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_auto_20230515_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='patimage',
            field=models.ImageField(default='media/default.png', upload_to='media/'),
        ),
    ]
