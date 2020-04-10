# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addressesapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='mobilephone',
        ),
    ]
