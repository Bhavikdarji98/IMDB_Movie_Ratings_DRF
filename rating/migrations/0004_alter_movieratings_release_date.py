# Generated by Django 3.2.4 on 2021-06-05 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0003_alter_movieratings_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieratings',
            name='release_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
