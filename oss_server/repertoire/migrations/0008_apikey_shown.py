# Generated by Django 3.0.5 on 2020-04-10 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repertoire', '0007_auto_20200410_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='shown',
            field=models.BooleanField(default=False, verbose_name='Wether the user has seen the API-Key'),
        ),
    ]
