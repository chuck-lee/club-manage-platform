# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.IntegerField(choices=[(-1, 'Expense'), (1, 'Income')], default=-1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payee',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.ForeignKey(to='finance.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.IntegerField(choices=[(-1, 'Expense'), (1, 'Income')], default=-1)),
                ('amount', models.IntegerField()),
                ('comment', models.CharField(max_length=200)),
                ('category', models.ForeignKey(to='finance.Category')),
                ('payee', models.ForeignKey(to='finance.Payee')),
                ('subCategory', models.ForeignKey(to='finance.SubCategory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='budget',
            name='category',
            field=models.ForeignKey(to='finance.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='budget',
            name='subCategory',
            field=models.ForeignKey(to='finance.SubCategory'),
            preserve_default=True,
        ),
    ]
