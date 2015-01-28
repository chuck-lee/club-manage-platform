# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_auto_20150124_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(verbose_name='名稱', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='payee',
            name='name',
            field=models.CharField(verbose_name='名稱', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payee',
            field=models.ForeignKey(blank=True, null=True, to='finance.Payee', verbose_name='關係人'),
            preserve_default=True,
        ),
    ]
