# Generated by Django 2.1 on 2019-12-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('npb', '0016_auto_20191201_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchresult',
            name='year',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
