# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_searchterm_num_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='searchterm',
            field=models.ForeignKey(related_name='links', on_delete=models.CASCADE,blank=True, to='pages.SearchTerm', null=True),
            preserve_default=True,
        ),
    ]
