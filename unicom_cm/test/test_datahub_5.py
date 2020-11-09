import time
import random

from collections import OrderedDict
from server.utils import xml_construct


def create_send_data(tmp_plan_dict):
    for cross_id, plan_list in tmp_plan_dict.items():

        split_time_list_element = OrderedDict()
        split_time_list = []

        end_time = '0'

        is_cancel_cmd = False

        for plan in plan_list:
            split_time_element = OrderedDict()
            stage_no = plan.get('stage_no')
            split_time = plan.get('split_time')

            if stage_no == 0 and split_time == 0:
                is_cancel_cmd = True
            else:
                split_time_element['StageNo'] = stage_no
                split_time_element['Green'] = split_time

                split_time_list.append(split_time_element)

                end_time = plan.get('end_time', '0')

        if is_cancel_cmd:
            temp_plan_param_element = OrderedDict()
            temp_plan_param_element['CrossID'] = cross_id
            temp_plan_param_element['Type'] = '1'
            temp_plan_param_element['Entrance'] = '8'
            temp_plan_param_element['Exit'] = '8'

            object_element = OrderedDict()
            object_element['UnlockFlowDirection'] = temp_plan_param_element
        else:
            split_time_list_element['SplitTime'] = split_time_list

            temp_plan_param_element = OrderedDict()
            temp_plan_param_element['CrossID'] = cross_id
            temp_plan_param_element['CoordStageNo'] = '0'
            temp_plan_param_element['OffSet'] = '0'
            temp_plan_param_element['EndTime'] = end_time
            temp_plan_param_element['SplitTimeList'] = split_time_list_element

            object_element = OrderedDict()
            object_element['TempPlanParam'] = temp_plan_param_element

        object_element['@order'] = '6'
        object_element['@name'] = 'Set'

        operation_element = OrderedDict()
        operation_element['Operation'] = object_element

        send_data_dict = operation_element

        seq = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '000%d%d%d' % (random.randint(0, 9),
                                                                               random.randint(0, 9),
                                                                               random.randint(0, 9))

        send_data_xml = xml_construct(send_data_dict, seq, 'token', 'REQUEST')

        # print(send_data_xml)


if __name__ == '__main__':
    tmp_plan_dict = {'123': []}
    tmp_plan_dict['123'].append({'stage_no': 1, 'split_time': 12})

    create_send_data(tmp_plan_dict)


























