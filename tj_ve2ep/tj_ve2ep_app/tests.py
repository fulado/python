from django.test import TestCase

# Create your tests here.

# import cx_Oracle
#
# # connect oracle database
# db = cx_Oracle.connect('yjhctxz/yjhctxz@192.168.188.94:1521/oracle.orcl')
#
# # create cursor
# cursor = db.cursor()
#
# # execute sql
# cursor.execute('select HPHM from TB_CAR_DATA')
#
# # fetch data
# data = cursor.fetchone()
#
# print('Database HPHM:%s' % data)
#
# # close cursor and oracle
# cursor.close()
# db.close()

import os
import django
from tj_ve2ep_app.models import TbCarData

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")  # project_name 项目名称
django.setup()

truck_count = TbCarData.objects.all().count()

print(truck_count)
