# Generated by Django 2.1 on 2019-12-01 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('npb', '0008_auto_20191201_1747'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pitcherstats',
            old_name='dfr',
            new_name='datsusannshinnritsu',
        ),
        migrations.AddField(
            model_name='pitcherstats',
            name='hidr',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='pitcherstats',
            name='pfr',
            field=models.FloatField(default=0.0),
        ),
    ]
