from django.test import TestCase
from django.db.utils import IntegrityError, DataError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Folder


class TestFolderModel(TestCase):
    def setUp(self):
        # account setup
        email = 'test@TeSt.com'
        password = 'password123'
        username = 'testname'
        self.account = get_user_model().objects.create_user(email=email, username=username, password=password)
        self.account.is_active = True
        self.account.save()

        # folder
        self.name = 'U2FsdGVkX18C1wjGTYc2PhdDPDAGkgnROcChQfGfCtakYN2ZYFahO/TKxyZbC0dpo7MSgsA+L5Ze2PlV6Zxbfhecjewjr2nmmW7I5uy/KQU5vBbWO2EQVa7JpcgCQtRCimfHqsqRRpMC48IfGAd7tjdgTVl99mSYiyZPuqaMU9MIiST5szSKEJoE+cAA2Gt3Av0ghO/IkFqQ9C3RovZbuNvsL/1oY8AsY0d+IWJGtx17mWGISJyOd3YHUJpufAd2'

        # wrong data: name
        self.name_limit_exceeded = 'U2FsdGVkX18QVsZIUai5qWu06W5oBCJCdBedpXYy9ckPvWRNIB1h8ZU5NwT7Ca+Hk+Zo7p4RKfrcks5yqp9mcNWg6/NHi0gUB8cpuUvjIHK1AYmYu4YrXvOb4HbO+la5ei/UE1JDFC/Ck+HYiOL3mCD5BH6j4J3S71j1a3p61IbZZv4amKWxZ+r5X9234yCcMjxf77KQbBq00oRCP+8e2rV1eB27T7hg2exXSSinMWEG/8Qm50W33V/UPvzFAsMtt'
        self.name_corrupted = 'U2FsdGVkX18C1wjGTYc2PhdDPD[AGkgnROcChQfGfCtakYN2ZYFahO/TKxyZbC0dpo7MSgsA+L5Ze2PlV6Zxbfhecjewjr2nmmW7I5uy/KQU5vBbWO2EQVa7JpcgCQtRCimfHqsqRRpMC48IfGAd7tjdgTVl99mSYiyZPuqaMU9MIiST5szSKEJE+cAA2Gt3Av0ghO/IkFqQ9C3RovZbuNvsL/1oY8AsY0d+IWJGtx17mWGISJyOd3YHUJpufAd2'


    def test_create_folder(self):
        folder = Folder.objects.create(name=self.name, account=self.account)
        self.assertIsInstance(folder, Folder)
        self.assertEqual(folder.name, self.name)

    def test_create_folder_nested(self):
        folder1 = Folder.objects.create(name=self.name, account=self.account)
        folder2 = Folder.objects.create(name=self.name, account=self.account, parent=folder1)
        self.assertIsInstance(folder2, Folder)
        self.assertEqual(folder2.parent, folder1)

    def test_create_folder_inactive_account(self):
        self.account.is_active = False
        self.account.save()
        with self.assertRaises(ValidationError):
            folder = Folder.objects.create(name=self.name, account=self.account)
            folder.full_clean()

    def test_create_folder_name_empty(self):
        with self.assertRaises(ValidationError):
            folder = Folder.objects.create(name='', account=self.account)
            folder.full_clean()

    def test_create_folder_name_limit_exceeded(self):
        with self.assertRaises(DataError):
            Folder.objects.create(name=self.name_limit_exceeded, account=self.account)

    def test_create_folder_name_corrupted(self):
        with self.assertRaises(ValidationError):
            folder = Folder.objects.create(name=self.name_corrupted, account=self.account)
            folder.full_clean()

class TestNoteModel(TestCase):
    def test_notes(self):
        pass


class TestTodoListModel(TestCase):
    def test_todo_lists(self):
        pass


class TestTaskModel(TestCase):
    def test_tasks(self):
        pass

