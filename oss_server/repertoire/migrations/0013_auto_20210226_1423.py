# Generated by Django 3.1.7 on 2021-02-26 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repertoire', '0012_auto_20210226_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='artist',
            field=models.ManyToManyField(blank=True, to='repertoire.Artist', verbose_name='From Artist'),
        ),
    ]
