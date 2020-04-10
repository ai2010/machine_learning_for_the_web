# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('books_recsys_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('array', jsonfield.fields.JSONField(default=dict)),
                ('review', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='movierated',
            name='movie',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
