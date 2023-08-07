from django.test import TestCase


class TestModels(TestCase):
    def account_success(self):
        self.assertEqual(1, 1)

    def folders(self):
        self.assertEqual(2, 3)

    def notes(self):
        pass

    def todo_lists(self):
        pass

    def test_tasks(self):
        pass
