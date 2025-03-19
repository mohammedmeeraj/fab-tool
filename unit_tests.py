import unittest
from ui_views.fabrication_dashboard import convert_to_hours_return_float
class TestFunctions(unittest.TestCase):
    def test_calculate_time(self):
        result = convert_to_hours_return_float("2.7")
        self.assertEqual(result, 2.42)

if __name__=="__main__":
    unittest.main()