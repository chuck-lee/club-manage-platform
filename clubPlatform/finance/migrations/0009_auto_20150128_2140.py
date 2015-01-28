# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0008_auto_20150128_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='category',
        ),
        migrations.AlterField(
            model_name='budget',
            name='subCategory',
            field=models.ForeignKey(to='finance.SubCategory', verbose_name='目', default=1),
            preserve_default=False,
        ),
    ]
