# Generated by Django 4.1 on 2023-01-10 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropsuggestion',
            name='area',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
