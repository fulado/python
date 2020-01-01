from django.db import models

# Create your models here.


# 权限表
# 1-企业, 2-支队, 3-交管局
class Authority(models.Model):
    name = models.CharField(max_length=50, unique=True)


# 状态表
class Status(models.Model):
    status_content = models.CharField(max_length=50, null=True, blank=True)     # 状态描述


# 支队表
class Department(models.Model):
    dept_name = models.CharField(max_length=50, null=True, blank=True)     # 支队名称
    dept_address = models.CharField(max_length=200, null=True, blank=True)  # 支队名称
    dept_phone = models.CharField(max_length=50, null=True, blank=True)  # 支队名称


# 用户表
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)                     # 帐号
    password = models.CharField(max_length=50)                                  # 密码
    authority = models.IntegerField(default=1, null=True, blank=True)           # 权限，1-企业，2-支队，3-交管局
    phone = models.CharField(max_length=20, null=True, blank=True)  # 手机号码
    dept = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)  # 用户所属支队
    person_name = models.CharField(max_length=50, null=True, blank=True)                     # 姓名
    person_id = models.CharField(max_length=50, null=True, blank=True)  # 警号
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL, default=71)   # 用户状态，71-正常，72-冻结
    reason = models.CharField(max_length=200, null=True, blank=True)  # 审核不通过/冻结原因


# 企业信息
class Enterprise(models.Model):
    enterprise_name = models.CharField(max_length=200, null=True, blank=True)                     # 企业名称
    enterprise_owner = models.CharField(max_length=200, null=True, blank=True)  # 法人
    enterprise_code = models.CharField(max_length=50, null=True, blank=True)  # 统一社会信用代码
    enterprise_type = models.ForeignKey(Status, related_name='enterprise_type_code', null=True, blank=True,
                                        on_delete=models.SET_NULL)      # 企业类型，41-自有车辆企业，42-租赁公司
    contact_person = models.CharField(max_length=200, null=True, blank=True)  # 联系人
    phone = models.CharField(max_length=50, null=True, blank=True)  # 联系方式
    business_license = models.CharField(max_length=200, null=True, blank=True)                     # 营业执照
    id_card_front = models.CharField(max_length=200, null=True, blank=True)  # 营业执照
    id_card_back = models.CharField(max_length=200, null=True, blank=True)  # 营业执照
    rent_contract = models.CharField(max_length=200, null=True, blank=True)  # 营业执照
    enterprise_status = models.ForeignKey(Status, related_name='enterprise_status_code', null=True, blank=True,
                                          on_delete=models.SET_NULL)      # 站点状态，1-未提交，2-待审核，3-正常，4-审核不通过， 5-冻结
    enterprise_reason = models.CharField(max_length=200, null=True, blank=True)  # 不通过、冻结原因
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # 企业所属用户
    dept = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)  # 企业所属支队


# 行政区信息
class Area(models.Model):
    area_code = models.CharField(max_length=50, unique=True)
    area_name = models.CharField(max_length=50, null=True, blank=True)


# 道路信息
class Road(models.Model):
    road_name = models.CharField(max_length=200, null=True, blank=True)  # 站点名称
    road_area = models.ForeignKey(Area, null=True, blank=True, on_delete=models.SET_NULL)  # 所属区域


# 方向信息
class Direction(models.Model):
    direction_name = models.CharField(max_length=200, null=True, blank=True)  # 方向名称
    direction_road = models.ForeignKey(Road, null=True, blank=True, on_delete=models.SET_NULL)  # 所属道路


# 站点信息
class Station(models.Model):
    # station_name = models.CharField(max_length=200, null=True, blank=True)                     # 站点名称
    # station_area = models.ForeignKey(Area, null=True, blank=True)  # 区域
    # station_road = models.ForeignKey(Road, null=True, blank=True)  # 道路
    # station_direction = models.ForeignKey(Direction, null=True, blank=True)  # 方向
    # station_position = models.CharField(max_length=200, null=True, blank=True)  # 位置

    station_name = models.CharField(max_length=50, null=True, blank=True)  # 站点名称
    station_position = models.CharField(max_length=200, null=True, blank=True)  # 具体位置
    station_direction = models.CharField(max_length=50, null=True, blank=True)  # 站点方向
    station_road = models.CharField(max_length=100, null=True, blank=True)  # 道路
    station_area = models.CharField(max_length=50, null=True, blank=True)  # 区域

    station_status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)  # 站点状态，31-运行，32-停运，33-未启动
    station_cnt = models.IntegerField(default=0)     # 站点使用次数


# 路线信息
class Route(models.Model):
    route_name = models.CharField(max_length=200, null=True, blank=True)                     # 路线名称
    route_station = models.ManyToManyField(Station, null=True, blank=True)   # 路线关联站点
    route_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)     # 路线所属用户
    route_status = models.IntegerField(default=1, null=True, blank=True)      # 站点状态，1-临时添加，2-临时删除，3-正式生效
    # is_temp = models.BooleanField(default=True)      # 是否临时添加


# 路线站点
# class RouteStation(models.Model):
#     route = models.ForeignKey(Route, null=True, blank=True, on_delete=models.SET_NULL)   # 路线
#     station = models.ForeignKey(Station, null=True, blank=True, on_delete=models.SET_NULL)   # 站点


# 车辆信息
class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=50, null=True, blank=True)     # 车牌号
    vehicle_type = models.ForeignKey(Status, related_name='vehicle_type_code', null=True, blank=True,
                                     on_delete=models.SET_NULL)      # 站点状态，21-中型车，22-大型车
    engine_code = models.CharField(max_length=50, null=True, blank=True)    # 发动机号
    vehicle_owner = models.CharField(max_length=200, null=True, blank=True)     # 所有人
    register_date = models.DateTimeField(null=True, blank=True)     # 注册日期
    vehicle_belong = models.ForeignKey(Status, related_name='vehicle_belong_code', null=True, blank=True,
                                       on_delete=models.SET_NULL)      # 车辆所属，11-自有车辆，22-租赁车辆
    vehicle_status = models.ForeignKey(Status, related_name='vehicle_status_code', null=True, blank=True,
                                       on_delete=models.SET_NULL)  # 车辆状态，1-未审核，2-待审核，3-审核通过，4-未通过，5-冻结
    vehicle_reason = models.CharField(max_length=200, null=True, blank=True)  # 审核不通过/冻结原因
    vehicle_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # 车辆所属用户
    mark_cnt = models.IntegerField(default=0, null=True, blank=True)      # 被标记数量
    unlock_content = models.CharField(max_length=200, null=True, blank=True)  # 解冻说明
    unlock_file = models.CharField(max_length=200, null=True, blank=True)  # 解冻说明文件


# 通行证信息
class Permission(models.Model):
    permission_vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)  # 车辆
    permission_route = models.ForeignKey(Route, null=True, blank=True, on_delete=models.SET_NULL)  # 路线
    permission_status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)  # 通行证状态，51-可用，52-不可用
    permission_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # 通行证用户
    start_date = models.DateTimeField(null=True, blank=True)  # 开始时间
    end_date = models.DateTimeField(null=True, blank=True)   # 结束时间
    permission_id = models.CharField(max_length=50, null=True, blank=True)  # 通行证编号


# 通行证统计
class Statistic(models.Model):
    sta_enterprise = models.ForeignKey(Enterprise, null=True, blank=True, on_delete=models.SET_NULL)  # 企业
    sta_date = models.DateTimeField(null=True, blank=True)  # 统计日期
    permission_count = models.IntegerField(default=0)     # 通行证数量
    download_count = models.IntegerField(default=0)     # 下载次数


# 车辆标记
class Mark(models.Model):
    mark_time = models.DateTimeField(null=True, blank=True)   # 标记时间
    mark_position = models.CharField(max_length=200, null=True, blank=True)  # 标记地点
    mark_reason = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)  # 标记原因，61-违规，62-其它
    mark_content = models.CharField(max_length=200, null=True, blank=True)  # 标记内容
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)  # 标记车辆
    dept = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)  # 标记支队
































