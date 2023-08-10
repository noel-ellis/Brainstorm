from django.test import TestCase
from django.db.utils import IntegrityError, DataError
from django.core.exceptions import ValidationError

from .models import Tag

class TestTagModel(TestCase):
    def setUp(self):
        self.name = 'tag1'
        self.name_limit_exceeded = 'a'* 256
        self.name_starts_w_spaces = '     a'
        self.name_ends_w_spaces = 'a    '
        self.name_all_spaces = '    '

    def test_create_tag(self):
        tag = Tag.objects.create(name=self.name)
        self.assertIsInstance(tag, Tag)
        self.assertEqual(tag.name, self.name)

    def test_duplicate_names_constraint(self):
        Tag.objects.create(name=self.name)
        with self.assertRaisesMessage(IntegrityError, 'duplicate key value violates unique constraint "core_tag_name_key"'):
            Tag.objects.create(name=self.name)

    def test_char_limit_constraint(self):
        with self.assertRaisesMessage(DataError, "value too long for type character varying(30)"):
            tag = Tag.objects.create(name=self.name_limit_exceeded)
            tag.full_clean()

    def test_empty_string_tag(self):
        with self.assertRaisesMessage(ValidationError, "{'name': ['This field cannot be blank.']}"):
            tag = Tag.objects.create(name='')
            tag.full_clean()

    def test_all_spaces_tag(self):
        with self.assertRaisesMessage(ValidationError, "Tag cannot be empty or contain whitespaces at the ends"):
            tag = Tag.objects.create(name=self.name_all_spaces)
            tag.full_clean()

    def test_start_spaces_tag(self):
        with self.assertRaisesMessage(ValidationError, "Tag cannot be empty or contain whitespaces at the ends"):
            tag = Tag.objects.create(name=self.name_starts_w_spaces)
            tag.full_clean()
    
    def test_end_spaces_tag(self):
        with self.assertRaisesMessage(ValidationError, "Tag cannot be empty or contain whitespaces at the ends"):
            tag = Tag.objects.create(name=self.name_ends_w_spaces)
            tag.full_clean()

        
class TestFolderModel(TestCase):
    def test_folders(self):
        pass


class TestNoteModel(TestCase):
    def test_notes(self):
        pass


class TestTodoListModel(TestCase):
    def test_todo_lists(self):
        pass


class TestTaskModel(TestCase):
    def test_tasks(self):
        pass

