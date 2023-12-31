from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from ..models import Folder, Note, TodoList, Task
from .long_test_strings import note_content, encrypted_name, encrypted_name_limit_exceeded, encrypted_name_corrupted

from datetime import datetime, date, timedelta


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
        folder.save()
        self.assertIsInstance(folder, Folder)
        self.assertEqual(folder.name, self.name)

    def test_create_folder_nested(self):
        folder1 = Folder.objects.create(name=self.name, account=self.account)
        folder1.save()
        folder2 = Folder.objects.create(name=self.name, account=self.account, parent=folder1)
        folder2.save()
        self.assertIsInstance(folder2, Folder)
        self.assertEqual(folder2.parent, folder1)

    def test_create_folder_inactive_account(self):
        self.account.is_active = False
        self.account.save()
        with self.assertRaises(ValidationError):
            folder = Folder.objects.create(name=self.name, account=self.account)
            folder.save()

    def test_create_folder_name_empty(self):
        with self.assertRaises(ValidationError):
            folder = Folder.objects.create(name='', account=self.account)
            folder.save()

    def test_create_folder_name_limit_exceeded(self):
        with self.assertRaises(ValidationError):
            folder = Folder.objects.create(name=self.name_limit_exceeded, account=self.account)
            folder.save()

    def test_create_folder_name_corrupted(self):
        with self.assertRaises(ValidationError):
            folder = Folder.objects.create(name=self.name_corrupted, account=self.account)
            folder.save()

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
        self.folder.save()

        # name
        self.name = encrypted_name
        self.name_limit_exceeded = encrypted_name_limit_exceeded
        self.name_corrupted = encrypted_name_corrupted

        # content
        self.content = note_content

    def test_create_note(self):
        note = Note.objects.create(name=self.name, content=self.content, folder=self.folder)
        note.save()
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
        with self.assertRaises(ValidationError):
            note = Note.objects.create(name=self.name, content=self.content, folder=None)
            note.save()

    def test_create_note_name_empty(self):
        with self.assertRaises(ValidationError):
            note = Note.objects.create(name='', content=self.content, folder=self.folder)
            note.save()

    def test_create_note_name_limit_exceeded(self):
        with self.assertRaises(ValidationError):
            note = Note.objects.create(name=self.name_limit_exceeded, content=self.content, folder=self.folder)
            note.save()

    def test_create_note_name_corrupted(self):
        with self.assertRaises(ValidationError):
            note = Note.objects.create(name=self.name_corrupted, content=self.content, folder=self.folder)
            note.save()

    def test_create_note_content_empty(self):
        note = Note.objects.create(name=self.name, content='', folder=self.folder)
        note.save()
        self.assertIsInstance(note, Note)
        self.assertEqual(note.content, '')

    def test_create_note_content_corrupted(self):
        with self.assertRaises(ValidationError):
            note = Note.objects.create(name=self.name_corrupted, content=self.content, folder=self.folder)
            note.save()

    def test_update_note_date_updated(self):
        note = Note.objects.create(name=self.name, content=self.content, folder=self.folder)
        note.save()
        note.content = ''
        note.save()
        self.assertNotEqual(note.date_created, note.date_updated)


class TestTodoListModel(TestCase):
    def setUp(self):
        # account setup
        email = 'test@TeSt.com'
        password = 'password123'
        username = 'testname'
        account = get_user_model().objects.create_user(email=email, username=username, password=password)
        account.is_active = True
        account.save()

        # folder
        name = encrypted_name
        self.folder = Folder.objects.create(name=name, account=account)
        self.folder.save()

        # todo list name
        self.name = encrypted_name
        self.name_limit_exceeded = encrypted_name_limit_exceeded
        self.name_corrupted = encrypted_name_corrupted
        
        # todo list priority
        self.priority = 'h'
        self.priority_alt = 'm'
        self.priority_wrong_letter = 'a'
        self.priority_wrong_type = 1
        self.priority_wrong_length = 'mm'

        # todo list due_date
        self.due_date = date(2024, 10, 9)

    def test_create_todo_list(self):
        todo_list = TodoList(name=self.name, priority=self.priority, folder=self.folder)
        todo_list.save()
        self.assertIsInstance(todo_list, TodoList)
        self.assertEqual(todo_list.name, self.name)
        self.assertEqual(todo_list.priority, self.priority)
        self.assertIsInstance(todo_list.date_created, datetime)
        self.assertIsInstance(todo_list.date_updated, datetime)
        self.assertEqual(todo_list.folder_id, self.folder.id)

    def test_create_todo_list_add_duedate(self):
        todo_list = TodoList(name=self.name, priority=self.priority, due_date=self.due_date, folder=self.folder)
        todo_list.save()
        self.assertIsInstance(todo_list, TodoList)
        self.assertEqual(todo_list.due_date, self.due_date)
        
    def test_create_note_no_folder(self):
        with self.assertRaises(ValidationError):
            todo_list = TodoList(name=self.name, priority=self.priority)
            todo_list.save()

    def test_create_note_name_empty(self):
        with self.assertRaises(ValidationError):
            todo_list = TodoList(name='', priority=self.priority, folder=self.folder)
            todo_list.save()

    def test_create_note_name_limit_exceeded(self):
        with self.assertRaises(ValidationError):
            todo_list = TodoList(name=self.name_limit_exceeded, priority=self.priority, folder=self.folder)
            todo_list.save()

    def test_create_note_name_corrupted(self):
        with self.assertRaises(ValidationError):
            todo_list = TodoList(name=self.name_corrupted, priority=self.priority, folder=self.folder)
            todo_list.save()

    def test_create_note_no_priority(self):
        todo_list = TodoList(name=self.name, folder=self.folder)
        todo_list.save()
        self.assertIsInstance(todo_list, TodoList)
        self.assertEqual(todo_list.priority, 'n')

    def test_create_note_wrong_priority(self):
        with self.assertRaises(ValidationError):
            todo_list = TodoList(name=self.name, priority=self.priority_wrong_letter, folder=self.folder)
            todo_list.save()

        with self.assertRaises(ValidationError):
            todo_list = TodoList(name=self.name, priority=self.priority_wrong_type, folder=self.folder)
            todo_list.save()

        with self.assertRaises(ValidationError):
            todo_list = TodoList(name=self.name, priority=self.priority_wrong_length, folder=self.folder)
            todo_list.save()

    def test_update_todo_list_date_updated(self):
        todo_list = TodoList.objects.create(name=self.name, priority=self.priority, folder=self.folder)
        todo_list.save()
        todo_list.priority = self.priority_alt
        todo_list.save()
        self.assertNotEqual(todo_list.date_created, todo_list.date_updated)


class TestTaskModel(TestCase):
    def setUp(self):
        # account setup
        email = 'test@TeSt.com'
        password = 'password123'
        username = 'testname'
        account = get_user_model().objects.create_user(email=email, username=username, password=password)
        account.is_active = True
        account.save()

        # folder
        self.name = encrypted_name
        folder = Folder.objects.create(name=self.name, account=account)
        folder.save()

        # todo list
        priority = 'h'
        self.todo_list = TodoList(name=self.name, priority=priority, folder=folder)
        self.todo_list.save()

        # note
        content = note_content
        self.note = Note.objects.create(name=self.name, content=content, folder=folder)
        self.note.save()

        # task wrong names
        self.name_limit_exceeded = encrypted_name_limit_exceeded
        self.name_corrupted = encrypted_name_corrupted

        # task priority
        self.priority = 'm'
        self.priority_alt = 'l'
        self.priority_wrong_letter = 'a'
        self.priority_wrong_type = 1
        self.priority_wrong_length = 'mm'

        # task due date
        self.due_date = date(2025, 12, 4)

        # task date closed
        self.date_closed = date(2020, 10, 10)
        self.date_closed_today = date.today()
        self.wrong_date_closed = date.today() + timedelta(days = 1)

    def test_create_task(self):
        task = Task.objects.create(name=self.name, priority = self.priority, todo_list=self.todo_list)
        task.save()
        self.assertIsInstance(task, Task)
        self.assertEqual(task.name, self.name)
        self.assertEqual(task.priority, self.priority)
        self.assertEqual(task.todo_list, self.todo_list)
        self.assertIsInstance(task.date_created, datetime)
        self.assertEqual(task.failed, False)
        self.assertEqual(task.due_date, None)
        self.assertEqual(task.date_closed, None)
        self.assertEqual(task.parent_task, None)
        self.assertEqual(task.note, None)

    def test_create_task_name_empty(self):
        with self.assertRaises(ValidationError):
            task = Task(name='', priority = self.priority, todo_list=self.todo_list)
            task.save()

    def test_create_task_name_limit_exceeded(self):
        with self.assertRaises(ValidationError):
            task = Task(name=self.name_limit_exceeded, priority = self.priority, todo_list=self.todo_list)
            task.save()

    def test_create_task_name_corrupted(self):
        with self.assertRaises(ValidationError):
            task = Task(name=self.name_corrupted, priority = self.priority, todo_list=self.todo_list)
            task.save()

    def test_create_task_wrong_priority(self):
        with self.assertRaises(ValidationError):
            task = Task(name=self.name, priority=self.priority_wrong_letter, todo_list=self.todo_list)
            task.save()

        with self.assertRaises(ValidationError):
            task = Task(name=self.name, priority=self.priority_wrong_type, todo_list=self.todo_list)
            task.save()

        with self.assertRaises(ValidationError):
            task = Task(name=self.name, priority=self.priority_wrong_length, todo_list=self.todo_list)
            task.save()

    def test_create_task_nested(self):
        parent_task = Task.objects.create(name=self.name, priority = self.priority, todo_list=self.todo_list)
        parent_task.save()
        task = Task.objects.create(name=self.name, priority = self.priority, todo_list=self.todo_list, parent_task=parent_task)
        task.save()
        self.assertIsInstance(task, Task)
        self.assertEqual(task.parent_task, parent_task)

    def test_create_task_attached_note(self):
        task = Task.objects.create(name=self.name, priority = self.priority, todo_list=self.todo_list, note=self.note)
        task.save()
        self.assertIsInstance(task, Task)
        self.assertEqual(task.note, self.note)

    def test_update_task_date_closed(self):
        # create a task
        task = Task.objects.create(name=self.name, priority = self.priority, todo_list=self.todo_list)
        task.save()
        self.assertEqual(task.date_closed, None)

        # close the task (past day)
        task.date_closed = self.date_closed
        task.save()
        self.assertEqual(task.date_closed, self.date_closed)

        # close the task (today)
        task.date_closed = self.date_closed_today
        task.save()
        self.assertEqual(task.date_closed, self.date_closed_today)

    # ValidationError: date closed is in the future
    def test_update_task_wrong_date_closed(self):
        task = Task.objects.create(name=self.name, priority = self.priority, todo_list=self.todo_list)
        task.save()
        self.assertEqual(task.date_closed, None)
        with self.assertRaises(ValidationError):
            task.date_closed = self.wrong_date_closed
            task.save()

    def test_update_task_mark_failed(self):
        # create a task
        task = Task.objects.create(name=self.name, priority = self.priority, todo_list=self.todo_list)
        task.save()
        self.assertEqual(task.date_closed, None)

        # close the task
        task.date_closed = self.date_closed
        task.save()
        self.assertEqual(task.date_closed, self.date_closed)

        # mark as failed
        task.failed = True
        task.save() 
        self.assertEqual(task.failed, True)

    def test_update_task_mark_failed_while_open(self):
        # create a task
        task = Task.objects.create(name=self.name, priority=self.priority, todo_list=self.todo_list)
        task.save()
        self.assertEqual(task.date_closed, None)

        # mark as failed
        with self.assertRaises(ValidationError):
            task.failed = True
            task.save() 

    def test_update_task_remove_date_closed(self):
        # create a task
        task = Task.objects.create(name=self.name, priority = self.priority, todo_list=self.todo_list)
        task.save()
        self.assertEqual(task.date_closed, None)

        # close the task
        task.date_closed = self.date_closed
        task.save()
        self.assertEqual(task.date_closed, self.date_closed)

        # mark as failed
        task.failed = True
        task.save() 

        # open the task again
        with self.assertRaises(ValidationError):
            task.date_closed = None
            task.save()

    def test_create_task_due_date(self):
        task = Task.objects.create(name=self.name, todo_list=self.todo_list, due_date=self.due_date)
        task.save()
        self.assertIsInstance(task, Task)
