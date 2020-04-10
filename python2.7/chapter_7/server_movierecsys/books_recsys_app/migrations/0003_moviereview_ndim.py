# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_recsys_app', '0002_auto_20160228_0240'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviereview',
            name='ndim',
            field=models.IntegerField(default=300),
            preserve_default=True,
        ),
    ]
