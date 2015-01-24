# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_auto_20150120_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='date',
        ),
        migrations.AddField(
            model_name='budget',
            name='year',
            field=models.IntegerField(default=2014),
            preserve_default=False,
        ),
    ]
