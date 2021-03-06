# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-07 19:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('causes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cie10',
            fields=[
                ('clave', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=500)),
                ('cies', models.CharField(default=b'CIE10', editable=False, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Cie10Caps',
            fields=[
                ('capitulo', models.CharField(max_length=6, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Cie9MC',
            fields=[
                ('clave', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=500)),
                ('cies', models.CharField(default=b'CIE9', editable=False, max_length=5)),
                ('causes', models.ManyToManyField(related_name='cie9_causes', to='causes.Causes')),
            ],
        ),
        migrations.AddField(
            model_name='cie10',
            name='capitulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cies.Cie10Caps'),
        ),
        migrations.AddField(
            model_name='cie10',
            name='causes',
            field=models.ManyToManyField(related_name='cie10_causes', to='causes.Causes'),
        ),
    ]
