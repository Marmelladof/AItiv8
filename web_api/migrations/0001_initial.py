# Generated by Django 4.1 on 2023-01-10 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CropSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apple', models.FloatField()),
                ('banana', models.FloatField()),
                ('blackgram', models.FloatField()),
                ('chickpea', models.FloatField()),
                ('coconut', models.FloatField()),
                ('coffee', models.FloatField()),
                ('cotton', models.FloatField()),
                ('grapes', models.FloatField()),
                ('jute', models.FloatField()),
                ('kidneybeans', models.FloatField()),
                ('lentil', models.FloatField()),
                ('maize', models.FloatField()),
                ('mango', models.FloatField()),
                ('mothbeans', models.FloatField()),
                ('mungbean', models.FloatField()),
                ('muskmelon', models.FloatField()),
                ('orange', models.FloatField()),
                ('papaya', models.FloatField()),
                ('pigeonpeas', models.FloatField()),
                ('pomegranate', models.FloatField()),
                ('rice', models.FloatField()),
                ('watermelon', models.FloatField()),
            ],
        ),
    ]
