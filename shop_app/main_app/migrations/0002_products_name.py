# Generated by Django 4.0.2 on 2022-02-03 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='name',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
