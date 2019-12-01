# Generated by Django 2.1 on 2019-12-01 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('npb', '0013_auto_20191201_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eights', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='eights', to='npb.Player')),
                ('fifth', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fifth', to='npb.Player')),
                ('first', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='first', to='npb.Player')),
                ('fourth', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fourth', to='npb.Player')),
                ('match_result', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='npb.MatchResult')),
                ('nineth', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='nineth', to='npb.Player')),
                ('second', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='second', to='npb.Player')),
                ('seventh', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='seventh', to='npb.Player')),
                ('sixth', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sixth', to='npb.Player')),
                ('third', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='third', to='npb.Player')),
            ],
        ),
    ]
