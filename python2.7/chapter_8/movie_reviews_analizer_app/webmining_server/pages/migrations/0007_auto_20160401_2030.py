# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20160401_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='new_rank',
            field=models.FloatField(default=1, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='old_rank',
            field=models.FloatField(default=0, null=True),
            preserve_default=True,
        ),
    ]
