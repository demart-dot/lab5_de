import unittest
import os
import shutil
from job import MetalPriceJob

class TestMetalPriceJob(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.getcwd(), 'test_raw')
        os.makedirs(self.test_dir, exist_ok=True)
        self.job = MetalPriceJob(raw_dir=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_run(self):
        date = "2024-10-25"
        feature = "Gold"
        result_files = self.job.run(date, feature)
        expected_file = os.path.join(self.test_dir, feature, date, f"{date}.json")

        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual([str(result_files[0])], [str(expected_file)])  # Приведення до рядка

if __name__ == '__main__':
    unittest.main()