# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_budget_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='documentSerial',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='comment',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payee',
            field=models.ForeignKey(to='finance.Payee', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='subCategory',
            field=models.ForeignKey(to='finance.SubCategory', null=True),
            preserve_default=True,
        ),
    ]
