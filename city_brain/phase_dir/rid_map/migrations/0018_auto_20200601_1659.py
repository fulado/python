# Generated by Django 3.0.5 on 2020-06-01 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rid_map', '0017_auto_20200601_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phasefroadftridmap',
            name='ft_rid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rid_map.InterFTRid'),
        ),
    ]
