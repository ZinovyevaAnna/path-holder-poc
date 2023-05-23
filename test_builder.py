from unittest import TestCase
from builder import *


class Test(TestCase):
    def test_check_reachability_between_packages(self):
        remove_all()

        append_info_from_path('A', 'B', ['A.m1', 'A.m2', 'A.m3', 'A.m4', 'B.m1'])
        append_info_from_path('A', 'C', ['A.m1', 'A.m2', 'A.m3', 'C.m1'])
        append_info_from_path('A', 'B', ['A.m2', 'A.m4', 'B.m2'])
        append_info_from_path('B', 'C', ['B.m1', 'B.m2', 'B.m3', 'C.m2'])

        self.assertTrue(check_reachability_between_packages('A', 'C'))
