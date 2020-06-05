from django.test import TestCase
from .models import PhaseLightRelation

import itertools


# Create your tests here.

class ModelTest(TestCase):

    def test_get_phase_plan_list(self):

        cust_signal_id = '1300'
        phsase_light_list = PhaseLightRelation.objects.filter(cust_signal_id=cust_signal_id)

        phase_content = ''

        for phase_light in phsase_light_list:
            if phase_light.phase_name in phase_content:
                continue
            else:
                phase_content += phase_light.phase_name

        phase_plane_list = []
        phase_plan_id = 1
        for i in range(1, len(phase_content) + 1):
            phase_comb = itertools.combinations(phase_content, i)

            for j in phase_comb:
                phase_plan_dict = {'phase_plan_id': phase_plan_id, 'phase_content': j}
                phase_plane_list.append(phase_plan_dict)

                phase_plan_id += 1

        print(phase_plane_list)


