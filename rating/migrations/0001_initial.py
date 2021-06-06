# Generated by Django 3.2.4 on 2021-06-05 14:47

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovieRatings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
