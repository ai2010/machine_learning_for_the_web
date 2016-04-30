# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20151010_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='new_rank',
            field=models.FloatField(default=-1, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='old_rank',
            field=models.FloatField(default=-1, null=True),
            preserve_default=True,
        ),
    ]
