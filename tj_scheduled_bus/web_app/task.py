"""
定时任务
"""

from .models import Permission, PermissionThisMonth
from tj_scheduled_bus import settings

import os


# 定时任务, 每月1日0点, 初始化系统:
# 保存上月车通行证信息
# 保存通行证文件到备份目录, 删除certification目录中的全部通行证图片文件
def permission_backup():
    # 清空备份数据库
    PermissionThisMonth.objects.all().delete()

    # 备份上月车辆审核状态
    permission_list = Permission.objects.all()
    backup_list = []
    for permission_info in permission_list:
        if permission_info.permission_status_id == 51:
            backup_info = PermissionThisMonth()

            backup_info.permission_vehicle = permission_info.permission_vehicle
            backup_info.permission_route = permission_info.permission_route
            backup_info.permission_status = permission_info.permission_status
            backup_info.permission_user = permission_info.permission_user
            backup_info.start_date = permission_info.start_date
            backup_info.end_date = permission_info.end_date
            backup_info.permission_id = permission_info.permission_id
        else:
            continue

        backup_list.append(backup_info)

    PermissionThisMonth.objects.bulk_create(backup_list)

    # 保存通行证文件到备份目录, 删除certification目录中的全部通行证图片文件
    # 1 修改certification目录名为certification_backup
    # 1.1 判断certification_backup目录是否存在
    old_path = r'%s/certification' % settings.FILE_DIR
    new_path = r'%s/certification_this_month' % settings.FILE_DIR

    if os.path.exists(new_path):
        # 删除目录
        for f in os.listdir(new_path):
            f_path = r'%s/%s' % (new_path, f)
            os.remove(f_path)
        os.rmdir(new_path)
    # 1.2 修改certification目录名为certification_backup
    os.rename(old_path, new_path)

    # 2 创建certification目录
    os.mkdir(old_path)

    # 重置下月通行证表中的数据
    # 通行证状态改为未申请-53
    # 开始时间、结束时间、通行证id设置为空值
    Permission.objects.all().update(permission_status=53, start_date=None, end_date=None, permission_id=None)

    print('permission backup complete.')
































