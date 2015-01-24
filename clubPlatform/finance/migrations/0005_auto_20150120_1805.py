# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_auto_20150120_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='subCategory',
            field=models.ForeignKey(null=True, blank=True, to='finance.SubCategory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='comment',
            field=models.CharField(null=True, max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='documentSerial',
            field=models.CharField(null=True, max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payee',
            field=models.ForeignKey(null=True, blank=True, to='finance.Payee'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='subCategory',
            field=models.ForeignKey(null=True, blank=True, to='finance.SubCategory'),
            preserve_default=True,
        ),
    ]
