# Generated by Django 2.1 on 2019-11-30 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('npb', '0006_auto_20191130_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='HitterStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daritsu', models.FloatField(default=0.0)),
                ('shiai', models.FloatField(default=0.0)),
                ('dasekisuu', models.FloatField(default=0.0)),
                ('dasuu', models.FloatField(default=0.0)),
                ('annda', models.FloatField(default=0.0)),
                ('honnruida', models.FloatField(default=0.0)),
                ('datenn', models.FloatField(default=0.0)),
                ('tokutenn', models.FloatField(default=0.0)),
                ('niruida', models.FloatField(default=0.0)),
                ('sannruida', models.FloatField(default=0.0)),
                ('ruida', models.FloatField(default=0.0)),
                ('tourui_fail', models.FloatField(default=0.0)),
                ('tourui', models.FloatField(default=0.0)),
                ('sikyuu', models.FloatField(default=0.0)),
                ('deadball', models.FloatField(default=0.0)),
                ('sannshinn', models.FloatField(default=0.0)),
                ('gida', models.FloatField(default=0.0)),
                ('heisatsuda', models.FloatField(default=0.0)),
                ('shutsuruiritsu', models.FloatField(default=0.0)),
                ('tyuodaritsu', models.FloatField(default=0.0)),
                ('ops', models.FloatField(default=0.0)),
                ('rc', models.FloatField(default=0.0)),
                ('no1', models.FloatField(default=0.0)),
                ('gpa', models.FloatField(default=0.0)),
                ('rc27', models.FloatField(default=0.0)),
                ('isop', models.FloatField(default=0.0)),
                ('isod', models.FloatField(default=0.0)),
                ('xr', models.FloatField(default=0.0)),
                ('xr27', models.FloatField(default=0.0)),
                ('babip', models.FloatField(default=0.0)),
                ('seca', models.FloatField(default=0.0)),
                ('ta', models.FloatField(default=0.0)),
                ('psn', models.FloatField(default=0.0)),
                ('bbk', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='PitcherStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bougyoritsu', models.FloatField(default=0.0)),
                ('shiai', models.FloatField(default=0.0)),
                ('shouri', models.FloatField(default=0.0)),
                ('haiboku', models.FloatField(default=0.0)),
                ('save', models.FloatField(default=0.0)),
                ('hold', models.FloatField(default=0.0)),
                ('shouritsu', models.FloatField(default=0.0)),
                ('dasha', models.FloatField(default=0.0)),
                ('toukyuukai', models.FloatField(default=0.0)),
                ('hidaritsu', models.FloatField(default=0.0)),
                ('hihonnruida', models.FloatField(default=0.0)),
                ('sikyuu', models.FloatField(default=0.0)),
                ('deadball', models.FloatField(default=0.0)),
                ('datsusannshinn', models.FloatField(default=0.0)),
                ('shitten', models.FloatField(default=0.0)),
                ('jisekitenn', models.FloatField(default=0.0)),
                ('whip', models.FloatField(default=0.0)),
                ('dips', models.FloatField(default=0.0)),
                ('hp', models.FloatField(default=0.0)),
                ('kanntou', models.FloatField(default=0.0)),
                ('kannpuu', models.FloatField(default=0.0)),
                ('mushikyuu', models.FloatField(default=0.0)),
                ('kbb', models.FloatField(default=0.0)),
                ('dfr', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AlterField(
            model_name='player',
            name='no',
            field=models.CharField(default='999', max_length=15),
        ),
        migrations.AddField(
            model_name='pitcherstats',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='npb.Player'),
        ),
        migrations.AddField(
            model_name='hitterstats',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='npb.Player'),
        ),
    ]
