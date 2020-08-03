from django.test import TestCase
from .dao import UserDao


# Create your tests here.
class AppTestCase(TestCase):
    def setUp(self):
        print('=' * 20)

    def tearDown(self):
        print('*' * 20)
