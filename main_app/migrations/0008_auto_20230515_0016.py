# Generated by Django 3.0.3 on 2023-05-15 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20200118_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='docimage',
            field=models.ImageField(default=False, upload_to='Doctor'),
        ),
        migrations.AddField(
            model_name='patient',
            name='patimage',
            field=models.ImageField(default=True, upload_to='Patient'),
        ),
    ]
