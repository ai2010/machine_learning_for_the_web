# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_searchterm_num_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='searchterm',
            field=models.ForeignKey(related_name='links', blank=True, to='pages.SearchTerm', null=True),
            preserve_default=True,
        ),
    ]
