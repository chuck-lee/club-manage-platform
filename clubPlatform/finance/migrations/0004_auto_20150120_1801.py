# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20150120_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='subCategory',
            field=models.ForeignKey(to='finance.SubCategory', null=True),
            preserve_default=True,
        ),
    ]
