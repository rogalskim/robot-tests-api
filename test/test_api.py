import unittest

from api import Query


class QueryTests(unittest.TestCase):
    def test_returns_correct_string_representation(self):
        test_query = Query(key="query_key", value="query_value")
        expected_string_representation = "query_key=query_value"
        self.assertEqual(test_query.text(), expected_string_representation)


if __name__ == '__main__':
    unittest.main()
