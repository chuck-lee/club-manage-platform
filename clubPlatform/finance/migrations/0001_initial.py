# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('year', models.IntegerField(verbose_name='年度')),
                ('type', models.IntegerField(choices=[(-1, '支出'), (1, '收入')], verbose_name='收支', default=-1)),
                ('amount', models.IntegerField(verbose_name='金額')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, verbose_name='名稱', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='名稱', max_length=200)),
                ('category', models.ForeignKey(to='finance.Category', verbose_name='科')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField(verbose_name='日期')),
                ('documentSerial', models.CharField(blank=True, verbose_name='票據編號', max_length=200, null=True)),
                ('amount', models.IntegerField(verbose_name='金額')),
                ('comment', models.CharField(blank=True, verbose_name='附註', max_length=200, null=True)),
                ('approveBy', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='核可人', null=True, blank=True, related_name='approveBy')),
                ('budget', models.ForeignKey(to='finance.Budget', verbose_name='預算')),
                ('payee', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='關係人', null=True, blank=True, related_name='payee')),
                ('submitBy', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='申請人', related_name='submitBy')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='budget',
            name='subCategory',
            field=models.ForeignKey(to='finance.SubCategory', verbose_name='目'),
            preserve_default=True,
        ),
    ]
