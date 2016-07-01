# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('books_recsys_app', '0008_userprofile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='arrayratedmoviesindxs',
            field=jsonfield.fields.JSONField(default=dict),
            preserve_default=True,
        ),
    ]
