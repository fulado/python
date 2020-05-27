# Generated by Django 3.0.5 on 2020-05-26 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rid_map', '0013_lightroadrelation_phaselightrelation'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterFTRid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inter_id', models.CharField(blank=True, max_length=20, null=True)),
                ('inter_name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_signlight', models.IntegerField(blank=True, default=0, null=True)),
                ('is_corner', models.IntegerField(blank=True, default=0, null=True)),
                ('ftrid_len', models.FloatField(blank=True, default=0, null=True)),
                ('f_rid', models.CharField(blank=True, max_length=50, null=True)),
                ('f_rid_name', models.CharField(blank=True, max_length=50, null=True)),
                ('f_rid_angle', models.FloatField(blank=True, default=0, null=True)),
                ('f_rid_dir_8_no', models.IntegerField(blank=True, default=0, null=True)),
                ('f_rid_dir_4_no', models.IntegerField(blank=True, default=0, null=True)),
                ('f_angle', models.FloatField(blank=True, default=0, null=True)),
                ('f_dir_8_no', models.IntegerField(blank=True, default=0, null=True)),
                ('f_dir_4_no', models.IntegerField(blank=True, default=0, null=True)),
                ('f_road_level', models.IntegerField(blank=True, default=0, null=True)),
                ('f_rid_type_no', models.IntegerField(blank=True, default=0, null=True)),
                ('f_pass_type_no', models.IntegerField(blank=True, default=0, null=True)),
                ('f_overlap', models.IntegerField(blank=True, default=0, null=True)),
                ('f_median', models.IntegerField(blank=True, default=0, null=True)),
                ('f_walkway', models.IntegerField(blank=True, default=0, null=True)),
                ('f_fork', models.IntegerField(blank=True, default=0, null=True)),
                ('f_rid_length', models.FloatField(blank=True, default=0, null=True)),
                ('f_rid_lnglat_seq', models.CharField(blank=True, max_length=255, null=True)),
                ('f_lane_cnt', models.IntegerField(blank=True, default=0, null=True)),
                ('f_road_name', models.CharField(blank=True, max_length=50, null=True)),
                ('t_rid', models.CharField(blank=True, max_length=50, null=True)),
                ('t_rid_name', models.CharField(blank=True, max_length=50, null=True)),
                ('t_rid_angle', models.FloatField(blank=True, default=0, null=True)),
                ('t_rid_dir_8_no', models.IntegerField(blank=True, default=0, null=True)),
                ('t_rid_dir_4_no', models.IntegerField(blank=True, default=0, null=True)),
                ('t_angle', models.FloatField(blank=True, default=0, null=True)),
                ('t_dir_8_no', models.IntegerField(blank=True, default=0, null=True)),
                ('t_dir_4_no', models.IntegerField(blank=True, default=0, null=True)),
                ('t_road_level', models.IntegerField(blank=True, default=0, null=True)),
                ('t_rid_type_no', models.IntegerField(blank=True, default=0, null=True)),
                ('t_pass_type_no', models.IntegerField(blank=True, default=0, null=True)),
                ('t_overlap', models.IntegerField(blank=True, default=0, null=True)),
                ('t_median', models.IntegerField(blank=True, default=0, null=True)),
                ('t_walkway', models.IntegerField(blank=True, default=0, null=True)),
                ('t_fork', models.IntegerField(blank=True, default=0, null=True)),
                ('t_rid_length', models.FloatField(blank=True, default=0, null=True)),
                ('t_rid_lnglat_seq', models.CharField(blank=True, max_length=255, null=True)),
                ('t_lane_cnt', models.IntegerField(blank=True, default=0, null=True)),
                ('t_road_name', models.CharField(blank=True, max_length=50, null=True)),
                ('turn_dir_no', models.CharField(blank=True, max_length=10, null=True)),
                ('data_version', models.CharField(blank=True, max_length=20, null=True)),
                ('adcode', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
