# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20150124_0037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='subCategory',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='type',
        ),
        migrations.AddField(
            model_name='transaction',
            name='budget',
            field=models.ForeignKey(default=1, verbose_name='預算', to='finance.Budget'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='budget',
            name='amount',
            field=models.IntegerField(verbose_name='金額'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.ForeignKey(verbose_name='科', to='finance.Category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='budget',
            name='subCategory',
            field=models.ForeignKey(null=True, verbose_name='目', blank=True, to='finance.SubCategory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='budget',
            name='type',
            field=models.IntegerField(choices=[(-1, '支出'), (1, '收入')], default=-1, verbose_name='收支'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='budget',
            name='year',
            field=models.IntegerField(verbose_name='年度'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, verbose_name='名稱'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='payee',
            name='name',
            field=models.CharField(max_length=200, verbose_name='名稱'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(verbose_name='科', to='finance.Category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=200, verbose_name='名稱'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.IntegerField(verbose_name='金額'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='comment',
            field=models.CharField(null=True, blank=True, max_length=200, verbose_name='附註'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(verbose_name='日期'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='documentSerial',
            field=models.CharField(null=True, blank=True, max_length=200, verbose_name='票據編號'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payee',
            field=models.ForeignKey(null=True, verbose_name='對象', blank=True, to='finance.Payee'),
            preserve_default=True,
        ),
    ]
