from django.test import TestCase
from django.db.utils import DataError, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from ..models import Folder, Note
from .long_test_strings import note_content, encrypted_name, encrypted_name_limit_exceeded, encrypted_name_corrupted

from datetime import datetime


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
    def setUp(self):
        # account setup
        email = 'test@TeSt.com'
        password = 'password123'
        username = 'testname'
        account = get_user_model().objects.create_user(email=email, username=username, password=password)
        account.is_active = True
        account.save()

        # folder setup
        folder_name = encrypted_name
        self.folder = Folder.objects.create(name=folder_name, account=account)

        # name
        self.name = encrypted_name
        self.name_limit_exceeded = encrypted_name_limit_exceeded
        self.name_corrupted = encrypted_name_corrupted

        # content
        self.content = note_content

    def test_create_note(self):
        note = Note.objects.create(name=self.name, content=self.content, folder=self.folder)
        self.assertIsInstance(note, Note)
        self.assertEqual(note.name, self.name)
        self.assertEqual(note.content, self.content)
        self.assertEqual(note.folder, self.folder)
        self.assertEqual(note.pinned, False)
        self.assertIsInstance(note.date_created, datetime)
        self.assertIsInstance(note.date_created, datetime)

    def test_pin_note(self):
        note = Note.objects.create(name=self.name, content=self.content, folder=self.folder)
        note.save()
        note.pinned = True
        note.save()
        self.assertEqual(note.pinned, True)

    def test_create_note_no_folder(self):
        with self.assertRaises(IntegrityError):
            folder = Note.objects.create(name=self.name, content=self.content, folder=None)
            folder.full_clean()

    def test_create_note_name_empty(self):
        with self.assertRaises(ValidationError):
            folder = Note.objects.create(name='', content=self.content, folder=self.folder)
            folder.full_clean()

    def test_create_note_name_limit_exceeded(self):
        with self.assertRaises(DataError):
            Note.objects.create(name=self.name_limit_exceeded, content=self.content, folder=self.folder)

    def test_create_note_name_corrupted(self):
        with self.assertRaises(ValidationError):
            folder = Note.objects.create(name=self.name_corrupted, content=self.content, folder=self.folder)
            folder.full_clean()

    def test_create_note_content_empty(self):
        note = Note.objects.create(name=self.name, content='', folder=self.folder)
        self.assertIsInstance(note, Note)
        self.assertEqual(note.content, '')

    def test_create_note_content_corrupted(self):
        with self.assertRaises(ValidationError):
            folder = Note.objects.create(name=self.name_corrupted, content=self.content, folder=self.folder)
            folder.full_clean()

    def test_update_note_date_updated(self):
        note = Note.objects.create(name=self.name, content=self.content, folder=self.folder)
        note.save()
        note.content = ''
        note.save()
        self.assertNotEqual(note.date_created, note.date_updated)


class TestTodoListModel(TestCase):
    def test_todo_lists(self):
        pass


class TestTaskModel(TestCase):
    def test_tasks(self):
        pass

