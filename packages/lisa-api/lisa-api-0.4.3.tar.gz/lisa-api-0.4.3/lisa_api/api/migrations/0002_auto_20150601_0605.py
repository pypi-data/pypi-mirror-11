# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plugin',
            name='enabled',
        ),
        migrations.AlterField(
            model_name='plugin',
            name='version',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
