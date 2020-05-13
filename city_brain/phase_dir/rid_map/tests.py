import sys
import os
import django


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phase_dir.phase_dir.settings')
django.setup()


from django.test import TestCase
from .models import PhaseLightRelation, LightRoadRelation

# Create your tests here.


# 测试
def test_phase():
    cust_signal_id = 2722
    phase_light_list = PhaseLightRelation.objects.get(cust_singal_id=cust_signal_id)

    for phase_light_info in phase_light_list:
        print(phase_light_info.phase_name)


if __name__ == '__main__':
    test_phase()
