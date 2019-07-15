from unittest import TestCase
import task3_2


class MyPerfectUnitTestClass(TestCase):

    def test_is_dividing_numbers(self):
        self.assertTrue(task3_2.is_dividing_number(128))
        self.assertTrue(task3_2.is_dividing_number(22))
        self.assertTrue(task3_2.is_dividing_number(15))
        self.assertTrue(task3_2.is_dividing_number(12))
        self.assertFalse(task3_2.is_dividing_number(10))
        self.assertFalse(task3_2.is_dividing_number(13))
        self.assertFalse(task3_2.is_dividing_number(14))
        self.assertFalse(task3_2.is_dividing_number(18))

    def test_main(self):
        self.assertEqual(task3_2.create_list(20, 22), [22])
        self.assertEqual(task3_2.create_list(7, 22), [7, 8, 9, 11, 12, 15, 22])
        self.assertEqual(task3_2.create_list(100, 118), [111, 112, 115])
