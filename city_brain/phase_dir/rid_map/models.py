from django.db import models

# Create your models here.


# ods_signal_froad_info_scats 客户路口进口道定义表
class CustFroad(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 进口道id, scat_id + road_id
    cust_signal_id = models.CharField(max_length=20, null=True, blank=True)  # 信号机编号或id
    cust_froad_id = models.CharField(max_length=10, null=True, blank=True)  # 进口序号
    cust_froad_name = models.CharField(max_length=50, null=True, blank=True)  # 进口道的名称，比如xxx路西进口
    cust_froad_lane_num = models.IntegerField(default=0, null=True, blank=True)  # 进口道车道数
    cust_froad_angle = models.IntegerField(default=None, null=True, blank=True)  # 进口道角度（相对于西方向，顺时针）
    cust_troad_lane_num = models.IntegerField(default=0, null=True, blank=True)  # 出口道车道数
    staff_street_type = models.CharField(max_length=10, null=True, blank=True)  # 行人过街线类型
    center_div_type = models.CharField(max_length=10, null=True, blank=True)  # 中央分割带类型
    lane_func_def = models.CharField(max_length=50, null=True, blank=True)  # 车道功能划分，即左至右分别为哪一条车道
    up_cust_signal_id = models.CharField(max_length=20, null=True, blank=True)  # 信号机编号或id
    dt = models.CharField(max_length=20, null=True, blank=True)  # 日期：yyyymmdd
    adcode = models.CharField(max_length=20, null=True, blank=True)  # 城市编码


# dwd_tfc_rltn_wide_inter_rid 路口进口道的rid信息
class InterRid(models.Model):
    inter_id = models.CharField(max_length=50, null=True, blank=True)  # 路口ID
    inter_name = models.CharField(max_length=50, null=True, blank=True)  # (当前版本可能有空值)路口name
    is_corner = models.IntegerField(default=0, null=True, blank=True)  # 是否为综合路口 1是 0非
    is_signlight = models.IntegerField(default=0, null=True, blank=True)  # 是否为信号灯路口 1表示路口 0表示非路口
    rid = models.CharField(max_length=50, primary_key=True)  # rid
    ft_type_no = models.IntegerField(default=0, null=True, blank=True)  # 进出口编号 1:进口道 2: 出口道
    rid_len = models.FloatField(default=0, null=True, blank=True)  # rid长度
    rid_lnglat_seq = models.CharField(max_length=500, null=True, blank=True)  # rid经纬度串, 第一经纬度串表示起点
    rid_name = models.CharField(max_length=50, null=True, blank=True)  # 进口rid名称
    rid_angle = models.FloatField(default=0, null=True, blank=True)  # 起点路口→终点路口连直线，相对于正北，顺时针方向的角度
    rid_dir_4_no = models.IntegerField(default=0, null=True, blank=True)  # 基于rid方向的序号
    rid_dir_8_no = models.IntegerField(default=0, null=True, blank=True)  # 基于rid方向的序号
    rid_road_level = models.IntegerField(default=0, null=True, blank=True)  # 道路等级
    rid_type_no = models.IntegerField(default=0, null=True, blank=True)  # 1-主路, 2-辅路, 3-独立右转路段, 4-独立左转路段,
    # 5-高架/高速上匝道, 6-高架/高速下匝道, 7-高速与高速连接路段, 8-隧道, 9-虚拟路段, 10-出口, 11-入口, 12-引路
    rid_pass_type_no = models.IntegerField(default=0, null=True, blank=True)  # -1 暂无数据,1：机动车,2：非机动车,3：机非混合,4：行人
    rid_overlap = models.IntegerField(default=0, null=True, blank=True)  # 是否立体重叠道路，。-1：未调查 1：为立体重叠道路，2：不是立体重叠道路
    rid_median = models.IntegerField(default=0, null=True, blank=True)  # 是否有隔离带,只要有一段link有隔离带，整个路段就认为有;-1：未调查,1：有物理隔离带,2：有法律隔离带,3：无隔离带
    rid_walkway = models.IntegerField(default=0, null=True, blank=True)  # 是否有人行道，-1：未调查 1：有人行道 2：无人行道
    ft_angle = models.FloatField(default=0, null=True, blank=True)  # 取进、出口道rid第一个和第二个经纬度点，计算第一个点到第二个点相对于正北方向的角度，作为进、出口道进入和离开路口的角度
    ft_dir_4_no = models.IntegerField(default=0, null=True, blank=True)  # 进、出口道进入路口相对于正北方向的角度的4方向编码，进口角度的8方向编码，使用ft_angle计算
    ft_dir_8_no = models.IntegerField(default=0, null=True, blank=True)  # 进、出口道进入路口相对于正北方向的角度的8方向编码，进口角度的8方向编码，使用ft_angle计算
    data_version = models.CharField(max_length=20, null=True, blank=True)  # 版本信息 如20180331：yyyymmdd
    adcode = models.CharField(max_length=20, null=True, blank=True)  # 城市编码


# dwd_tfc_rltn_wide_inter_rid 路口出口道的rid信息
class InterOutRid(models.Model):
    inter_id = models.CharField(max_length=50, null=True, blank=True)  # 路口ID
    inter_name = models.CharField(max_length=50, null=True, blank=True)  # (当前版本可能有空值)路口name
    is_corner = models.IntegerField(default=0, null=True, blank=True)  # 是否为综合路口 1是 0非
    is_signlight = models.IntegerField(default=0, null=True, blank=True)  # 是否为信号灯路口 1表示路口 0表示非路口
    rid = models.CharField(max_length=50, primary_key=True)  # rid
    ft_type_no = models.IntegerField(default=0, null=True, blank=True)  # 进出口编号 1:进口道 2: 出口道
    rid_len = models.FloatField(default=0, null=True, blank=True)  # rid长度
    rid_lnglat_seq = models.CharField(max_length=500, null=True, blank=True)  # rid经纬度串, 第一经纬度串表示起点
    rid_name = models.CharField(max_length=50, null=True, blank=True)  # 进口rid名称
    rid_angle = models.FloatField(default=0, null=True, blank=True)  # 起点路口→终点路口连直线，相对于正北，顺时针方向的角度
    rid_dir_4_no = models.IntegerField(default=0, null=True, blank=True)  # 基于rid方向的序号
    rid_dir_8_no = models.IntegerField(default=0, null=True, blank=True)  # 基于rid方向的序号
    rid_road_level = models.IntegerField(default=0, null=True, blank=True)  # 道路等级
    rid_type_no = models.IntegerField(default=0, null=True, blank=True)  # 1-主路, 2-辅路, 3-独立右转路段, 4-独立左转路段,
    # 5-高架/高速上匝道, 6-高架/高速下匝道, 7-高速与高速连接路段, 8-隧道, 9-虚拟路段, 10-出口, 11-入口, 12-引路
    rid_pass_type_no = models.IntegerField(default=0, null=True, blank=True)  # -1 暂无数据,1：机动车,2：非机动车,3：机非混合,4：行人
    rid_overlap = models.IntegerField(default=0, null=True, blank=True)  # 是否立体重叠道路，。-1：未调查 1：为立体重叠道路，2：不是立体重叠道路
    rid_median = models.IntegerField(default=0, null=True, blank=True)  # 是否有隔离带,只要有一段link有隔离带，整个路段就认为有;-1：未调查,1：有物理隔离带,2：有法律隔离带,3：无隔离带
    rid_walkway = models.IntegerField(default=0, null=True, blank=True)  # 是否有人行道，-1：未调查 1：有人行道 2：无人行道
    ft_angle = models.FloatField(default=0, null=True, blank=True)  # 取进、出口道rid第一个和第二个经纬度点，计算第一个点到第二个点相对于正北方向的角度，作为进、出口道进入和离开路口的角度
    ft_dir_4_no = models.IntegerField(default=0, null=True, blank=True)  # 进、出口道进入路口相对于正北方向的角度的4方向编码，进口角度的8方向编码，使用ft_angle计算
    ft_dir_8_no = models.IntegerField(default=0, null=True, blank=True)  # 进、出口道进入路口相对于正北方向的角度的8方向编码，进口角度的8方向编码，使用ft_angle计算
    data_version = models.CharField(max_length=20, null=True, blank=True)  # 版本信息 如20180331：yyyymmdd
    adcode = models.CharField(max_length=20, null=True, blank=True)  # 城市编码


# 电科进口道与rid对应关系
class RoadRidMap(models.Model):
    inter_id = models.CharField(max_length=20, null=True, blank=True)  # 高德路口ID
    road = models.ForeignKey(CustFroad, on_delete=models.DO_NOTHING)
    rid = models.ForeignKey(InterRid, on_delete=models.DO_NOTHING)
    cust_signal_id = models.CharField(max_length=20, null=True, blank=True)  # 信号机编号或id
    cust_froad_id = models.CharField(max_length=10, null=True, blank=True)  # 进口序号


# 电科进口道与出口到rid对应关系
class RoadOutRidMap(models.Model):
    inter_id = models.CharField(max_length=20, null=True, blank=True)  # 高德路口ID
    road = models.ForeignKey(CustFroad, on_delete=models.DO_NOTHING)
    rid = models.ForeignKey(InterOutRid, on_delete=models.DO_NOTHING)
    cust_signal_id = models.CharField(max_length=20, null=True, blank=True)  # 信号机编号或id
    cust_froad_id = models.CharField(max_length=10, null=True, blank=True)  # 进口序号


# 客户信号机id与大脑路口id对应关系
class CustSignalInterMap(models.Model):
    cust_inter_id = models.CharField(max_length=20, null=True, blank=True)  # 信号机编号或id
    cust_inter_name = models.CharField(max_length=50, null=True, blank=True)  # 客户路口名称
    inter_id = models.CharField(max_length=20, null=True, blank=True)  # 高德路口ID
    inter_name = models.CharField(max_length=50, null=True, blank=True)  # 高德路口名称
    is_valid = models.CharField(max_length=5, null=True, blank=True)  # 是否有效
    gmt_invalid = models.CharField(max_length=20, null=True, blank=True)  # 失效时间
    area_code = models.CharField(max_length=20, null=True, blank=True)  # 行政区域编码
    grid_id = models.CharField(max_length=20, null=True, blank=True)  # 管辖区域编码


# 客户信号机相位阶段与灯组关系
class PhaseLightRelation(models.Model):
    cust_signal_id = models.CharField(max_length=20, null=True, blank=True)  # 信号机编号或id
    phase_name = models.CharField(max_length=20, null=True, blank=True)  # 相位阶段
    lightset_id_list = models.CharField(max_length=50, null=True, blank=True)  # 本相位对应的灯组ID列表
    dt = models.CharField(max_length=20, null=True, blank=True)  # 日期：yyyymmdd
    adcode = models.CharField(max_length=20, null=True, blank=True)  # 城市编码


# 信号机灯组（灯组代表了一组通行方向）定义
class LightRoadRelation(models.Model):
    cust_signal_id = models.CharField(max_length=20, null=True, blank=True)  # 信号机编号或id
    lightset_id = models.CharField(max_length=20, null=True, blank=True)  # 相位阶段
    lightset_content = models.CharField(max_length=50, null=True, blank=True)  # 本相位对应的灯组ID列表
    dt = models.CharField(max_length=20, null=True, blank=True)  # 日期：yyyymmdd
    adcode = models.CharField(max_length=20, null=True, blank=True)  # 城市编码







