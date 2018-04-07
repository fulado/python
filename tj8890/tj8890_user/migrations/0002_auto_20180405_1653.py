# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tj8890_user', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Authority',
        ),
        migrations.DeleteModel(
            name='Duty',
        ),
    ]
