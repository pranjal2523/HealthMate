# Generated by Django 3.0.3 on 2023-05-15 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_auto_20230515_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='patimage',
            field=models.ImageField(default='media/Patient/default.png', upload_to='C:\\Users\\pranj\\Final-year-project\\Disease-Prediction-using-Django\\Disease-Prediction-using-Django-and-machine-learning-master\\media/Patient/'),
        ),
    ]
