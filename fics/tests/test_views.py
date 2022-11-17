from test_plus.test import TestCase


class FicsViewsTests(TestCase):
    def test_index_200(self):
        """
        GET /
        """
        self.get_check_200("/")
