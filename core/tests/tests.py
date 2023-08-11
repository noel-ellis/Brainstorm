from django.test import TestCase
from django.db.utils import DataError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from ..models import Folder
from .long_test_strings import encrypted_name, encrypted_name_limit_exceeded, encrypted_name_corrupted


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
        self.name = encrypted_name

        # wrong data: name
        self.name_limit_exceeded = encrypted_name_limit_exceeded
        self.name_corrupted = encrypted_name_corrupted

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

