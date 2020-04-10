# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_id', models.IntegerField(null=True)),
                ('to_id', models.IntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(default=b'', verbose_name='url', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='Name')),
                ('depth', models.IntegerField(default=-1, null=True)),
                ('html', models.TextField(default=b'', verbose_name='html', blank=True)),
                ('old_rank', models.IntegerField(default=-1, null=True)),
                ('new_rank', models.IntegerField(default=-1, null=True)),
                ('content', models.TextField(default=b'', verbose_name='content', blank=True)),
                ('sentiment', models.IntegerField(default=100, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
