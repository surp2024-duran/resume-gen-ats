import unittest
import sys
import os
from tqdm import tqdm
from colorama import init, Fore, Style
from datetime import datetime, timedelta
from dotenv import load_dotenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.mongo_util import MongoUtil
init(autoreset=True)
load_dotenv()

class TestMongoUtil(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mongo_util = MongoUtil()
        cls.test_db = cls.mongo_util.db
        cls.test_collection_name = "test-collection"
        cls.test_collection = cls.test_db[cls.test_collection_name]

    def setUp(self):
        self.test_data = {
            "resume_text": "Test Resume Text",
            "job_description": "Test Job Description",
            "generated_resume": "Generated Resume Text",
            "prompt": "Test Prompt"
        }

    def tearDown(self):
        self.test_collection.delete_many({})

    @classmethod
    def tearDownClass(cls):
        cls.test_db.drop_collection(cls.test_collection_name)
        cls.mongo_util.close_connection()

    def test_get_or_create_collection(self):
        expected = self.test_collection_name
        actual = self.mongo_util.get_or_create_collection(self.test_collection_name).name
        print(f"{Fore.GREEN}Expected: {expected}, Actual: {actual}")
        self.assertEqual(expected, actual)

    # def test_fetch_documents(self):
    #     self.test_collection.insert_one(self.test_data)
    #     expected = [self.test_data]
    #     actual = list(self.mongo_util.fetch_documents(self.test_collection))
    #     for doc in actual:
    #         doc.pop('_id', None)  # Remove _id for comparison
    #     print(f"{Fore.BLUE}Expected: {expected}, Actual: {actual}")
    #     self.assertEqual(expected, actual)

    def test_insert_document(self):
        expected = {**self.test_data}
        self.mongo_util.insert_document(self.test_collection, self.test_data)
        actual = self.test_collection.find_one({"resume_text": "Test Resume Text"})
        actual.pop('_id', None) 
        print(f"{Fore.YELLOW}Expected: {expected}, Actual: {actual}")
        self.assertEqual(expected, actual)

    def test_get_next_day_collection_name(self):
        next_day = datetime.utcnow() + timedelta(days=1)
        expected = next_day.strftime('%B-%d-resumes').lower()
        actual = self.mongo_util.get_next_day_collection_name()
        print(f"{Fore.CYAN}Expected: {expected}, Actual: {actual}")
        self.assertEqual(expected, actual)

    def test_get_previous_day_collection_name(self):
        previous_day = datetime.utcnow() - timedelta(days=1)
        expected = previous_day.strftime('%B-%d-resumes').lower()
        actual = self.mongo_util.get_previous_day_collection().name
        print(f"{Fore.MAGENTA}Expected: {expected}, Actual: {actual}")
        self.assertEqual(expected, actual)

    # def test_insert_and_fetch_documents(self):
    #     for i in range(5):
    #         self.mongo_util.insert_document(self.test_collection, {**self.test_data, "extra_field": i})
    #     expected = [{**self.test_data, "extra_field": i} for i in range(5)]
    #     actual = list(self.mongo_util.fetch_documents(self.test_collection))
    #     for doc in actual:
    #         doc.pop('_id', None)  # Remove _id for comparison
    #     print(f"{Fore.LIGHTGREEN_EX}Expected: {expected}, Actual: {actual}")
    #     self.assertEqual(expected, actual)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMongoUtil)
    runner = unittest.TextTestRunner(verbosity=2)
    for _ in tqdm(iter(runner.run(suite)), total=suite.countTestCases()):
        pass
