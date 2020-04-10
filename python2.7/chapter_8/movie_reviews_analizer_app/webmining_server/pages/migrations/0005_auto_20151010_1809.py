# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_link_searchterm'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='review',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='new_rank',
            field=models.IntegerField(default=1, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='old_rank',
            field=models.IntegerField(default=1, null=True),
            preserve_default=True,
        ),
    ]
