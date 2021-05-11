from monitor.tools import get_data_from_odps_by_sql, get_odps
import xlwt
import os
import time


def data_monitor(o, devc_type_no):
    """
    信号机实时数据断流监视
    :param o: odps
    :param devc_type_no: 设备类型编号: 7-信号机, 10-雷达, 9-复合检测器, 1-线圈
    :return: 当天信号机断流路口列表
    """

    if devc_type_no == 7:
        sql = """
            select t1.cust_signal_id, t2.inter_id, t2.inter_name from dwd_tfc_rltn_custsignal_inter_city_brain t1 
            join dim_signaloptim_inter_info_city_brain t2 on t1.inter_id=t2.inter_id
            where t1.cust_signal_id not in 
            (select distinct cust_signal_id from ods_rt_phase_oper_allinfo_collect_scats where dt=to_char(getdate(), 'yyyymmdd')) 
            and t1.area_code='310104' and t1.cust_signal_id not in ('xh01', 'xh02')
            order by cust_signal_id;
             """
    elif devc_type_no == 10:
        sql = """
                select DISTINCT t1.cust_devc_id as radar_id, t3.cust_devc_id as scats_id, t2.inter_name from dwd_tfc_rltn_devc_lane_qianxun_xuhui t1
                join jj_znafaqglxt2.dwd_tfc_bas_rdnet_inter_info t2 on t1.inter_id=t2.inter_id
                join dwd_tfc_rltn_devc_lane_qianxun_xuhui t3 on t1.inter_id=t3.inter_id and t3.qx_type_no='7' and t3.cust_devc_id not in ('xh01', 'xh02')
                where t1.qx_type_no='12' and t1.cust_devc_id not in (
                    select DISTINCT radar_id from ods_rt_radar_lane_parameter_image_dianke
                    where dt=to_char(getdate(), 'yyyymmdd') and radar_id like '310104%'
                )
                order by radar_id;
            """
    elif devc_type_no == 9:
        sql = """
            select DISTINCT t1.cust_devc_id as dmdm, t3.cust_devc_id as scats_id, t2.inter_name from dwd_tfc_rltn_devc_lane_qianxun_xuhui t1
            join jj_znafaqglxt2.dwd_tfc_bas_rdnet_inter_info t2 on t1.inter_id=t2.inter_id
            join dwd_tfc_rltn_devc_lane_qianxun_xuhui t3 on t1.inter_id=t3.inter_id and t3.qx_type_no='7' and t3.cust_devc_id not in ('xh01', 'xh02')
            where t1.qx_type_no='10' and t1.cust_devc_id not in (
                select DISTINCT dmdm from ods_rt_bynt_vhc_dianke
                where dt=to_char(getdate(), 'yyyymmdd') and dmdm like '310104%'
            )
            order by dmdm;
        """
    elif devc_type_no == 1:
        sql = """
            select t2.cust_devc_id, split_part(t1.devc_id, '_', 3) as scats_id, t1.devc_name from dwd_tfc_bas_devc_coil_info_city_brain t1
            join dwd_tfc_rltn_custdevc_devc_city_brain t2 on t1.devc_id=t2.devc_id
            where t1.devc_id like '310104%' and t2.cust_devc_id not in (
                select distinct substr(detector_id, 3) as detector_id from ods_rt_detector_5miflow_collect_scats where dt=to_char(getdate(), 'yyyymmdd'))
            order by cust_devc_id;
        """
    else:
        return []

    return get_data_from_odps_by_sql(o, sql)


def get_workbook():
    return xlwt.Workbook()


def write_data_to_xlsx(data_list, devc_type_no, wb):
    """
    把缺失的数据输出到excel文件
    :param data_list: 缺失数据列表
    :param devc_type_no: 设备类型编码
    :param wb: workbook
    :return:
    """
    # 创建sheet, 配置相应表头
    if devc_type_no == 1:
        ws = wb.add_sheet('线圈')
        title = ['detector_id', 'scats_id', 'inter_name']
    elif devc_type_no == 7:
        ws = wb.add_sheet('信号机')
        title = ['scats_id', 'inter_id', 'inter_name']
    elif devc_type_no == 9:
        ws = wb.add_sheet('复合检测器')
        title = ['dmdm', 'scats_id', 'inter_name']
    elif devc_type_no == 10:
        ws = wb.add_sheet('雷达')
        title = ['radar_id', 'scats_id', 'inter_name']
    else:
        return False

    # 写入表头
    for i in range(0, len(title)):
        ws.write(0, i, title[i])

    # 写入数据
    i = 1
    for data in data_list:
        for j in range(0, len(data)):
            ws.write(i, j, data[j][1])
        i += 1

    return True


def save_excel(wb):
    """
    保存excel文件
    :param wb: workbook 对象
    :return:
    """
    file_path = 'd:/data_monitor'
    file_name = '数据断流_' + time.strftime('%Y%m%d_%H%M.xls', time.localtime())
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    wb.save(file_path + '/' + file_name)


def main():
    access_id = 'wJGLPrjEt3GCgB2h'
    access_key = 'SJcsN7acOaCsaAYicrX0iU8l72x9GZ'
    project_name = 'jj_znjt'
    endpoint = 'http://15.74.19.77/api'

    o = get_odps(access_id, access_key, project_name, endpoint)

    wb = get_workbook()

    for devc_type_no in (7, 9, 10, 1):
        data_list = data_monitor(o, devc_type_no)
        write_data_to_xlsx(data_list, devc_type_no, wb)

    save_excel(wb)

    print('今日断流设备清单已保存在D:\data_monitor目录下, 请查看')


if __name__ == '__main__':
    main()
