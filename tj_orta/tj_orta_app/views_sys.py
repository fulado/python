from django.http import HttpResponseRedirect
from .models import Backup1, Vehicle, SysStatus, User
from tj_orta import settings
import os


# 定时任务, 每月1日0点, 初始化系统:
# 保存上月车辆申请状态(id, 号牌, 审核状态, 未通过原因, 通行证id, 车辆提交审核时间, 环保局审核时间, 交管局审核时间)
# 修改系统状态为可以提交车辆审核
# 保存通行证文件到备份目录, 删除certification目录中的全部通行证图片文件
# 全部车辆状态修改为1-未提交, 清空数据库中如下列的内容: 未通过原因(reason), 通行证保存路径(file_name), 通行证id(cert_id)
# 所有用户的已提交车辆数量归零
def init_sys():
    # 清空备份数据库
    Backup1.objects.all().delete()

    # 备份上月车辆审核状态
    truck_list = Vehicle.objects.all()
    backup_list = []
    for truck in truck_list:
        backup = Backup1()
        backup.number = truck.number
        backup.status_id = truck.status_id
        backup.reason = truck.reason
        backup.cert_id = truck.cert_id
        backup.submit_time = truck.submit_time
        backup.hbj_time = truck.hbj_time
        backup.jgj_time = truck.jgj_time
        backup.file_name = truck.file_name
        backup.enterprise_id = truck.enterprise_id
        backup_list.append(backup)

    Backup1.objects.bulk_create(backup_list)

    # 保存通行证文件到备份目录, 删除certification目录中的全部通行证图片文件
    # 1 修改certification目录名为certification_backup
    # 1.1 判断certification_backup目录是否存在
    old_path = r'%s/certification' % settings.FILE_DIR
    new_path = r'%s/certification_backup' % settings.FILE_DIR
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

    # 修改系统状态为可以提交车辆审核
    sys_status = SysStatus.objects.get(id=1)
    sys_status.allow_submit = True
    sys_status.save()

    # 初始化全部车辆状态为未提交
    Vehicle.objects.all().update(status_id=1)

    # 清除数据库中如下列的内容: 未通过原因(reason), 通行证保存路径(file_name), 通行证id(cert_id)
    Vehicle.objects.all().update(reason=None)
    Vehicle.objects.all().update(file_name=None)
    Vehicle.objects.all().update(cert_id=None)

    # 所有用户的已提交车辆数量归零
    User.objects.all().update(applied_number=0)

    print('System initial complete.')


# 定时任务, 每月26日0点, 修改系统状态为不能提交车辆审核
def forbid_submit():
    sys_status = SysStatus.objects.get(id=1)
    sys_status.allow_submit = False
    sys_status.save()
    print('submit is forbidden!')


# 允许提交申请
def permit_submit():
    sys_status = SysStatus.objects.get(id=1)
    sys_status.allow_submit = True
    sys_status.save()
    print('submit is permitted!')


# 重置系统请求
def init_sys_request(request):
    init_sys()

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)


# 禁止提交请求
def forbid_submit_request(request):
    forbid_submit()

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)


# 允许提交请求
def permit_submit_request(request):
    permit_submit()

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)
