# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchTerm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=255, verbose_name='search')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Links',
            new_name='Link',
        ),
        migrations.AddField(
            model_name='page',
            name='searchterm',
            field=models.ForeignKey(related_name='pages', blank=True, to='pages.SearchTerm', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=255, verbose_name='name'),
            preserve_default=True,
        ),
    ]
