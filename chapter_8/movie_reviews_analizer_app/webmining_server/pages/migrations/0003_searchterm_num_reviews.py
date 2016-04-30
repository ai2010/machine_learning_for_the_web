# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20151004_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchterm',
            name='num_reviews',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
