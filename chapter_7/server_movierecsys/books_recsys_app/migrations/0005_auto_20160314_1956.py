# -*- coding: utf-8 -*-


from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books_recsys_app', '0004_auto_20160310_2115'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('array', jsonfield.fields.JSONField(default=dict)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='movierated',
            name='movieindx',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movierated',
            name='user',
            field=models.ForeignKey(related_name='ratedmovies', on_delete=models.CASCADE, to='books_recsys_app.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movierated',
            name='value',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
