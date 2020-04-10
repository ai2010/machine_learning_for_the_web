# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('books_recsys_app', '0003_moviereview_ndim'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='movierated',
            name='user',
            field=models.ForeignKey(related_name='ratedmovies', on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
