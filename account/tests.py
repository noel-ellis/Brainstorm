from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


class TestAccountModel(TestCase):
    def setUp(self):
        self.email = 'test@TeSt.com'
        self.email2 = 'test2@TeSt.com'
        self.limit_exceeded_email = 'a'*255 + '@test.com'
        self.wrong_format_email = 'aftest@@'
        self.password = 'password123'
        self.username = 'testname'
        self.limit_exceeded_username = 'a'*151
        self.account = get_user_model()

    def test_create_account_success(self):
        account = self.account.objects.create_user(email=self.email, username=self.username, password=self.password)
        self.assertEqual(account.email, self.email.lower())
        self.assertEqual(account.username, self.username)
        self.assertEqual(account.last_login, None)

    def test_supercreate_account_success(self):
        account = self.account.objects.create_superuser(email=self.email, username=self.username, password=self.password)
        self.assertEqual(account.email, self.email.lower())
        self.assertEqual(account.username, self.username)
        self.assertEqual(account.last_login, None)

    def test_superaccount_is_active(self):
        account = self.account.objects.create_superuser(email=self.email, username=self.username, password=self.password)
        self.assertEqual(account.is_active, True)

    def test_account_is_inactive(self):
        account = self.account.objects.create_user(email=self.email2, username=self.username, password=self.password)
        self.assertEqual(account.is_active, False)

    def test_account_no_duplicate_emails(self):
        self.account.objects.create_superuser(email=self.email, username=self.username, password=self.password)
        with self.assertRaisesMessage(IntegrityError, 'duplicate key value violates unique constraint "account_account_email_key"'):
            self.account.objects.create_user(email=self.email, username=self.username, password=self.password)

    def test_account_email_character_limit_exceeded(self):
        with self.assertRaisesMessage(ValidationError, "{'email': ['Ensure this value has at most 255 characters (it has "+str(len(self.limit_exceeded_email))+").']}"):
            self.account.objects.create_user(email=self.limit_exceeded_email, username=self.username, password=self.password)

    def test_account_email_wrong_format(self):
        with self.assertRaisesMessage(ValidationError, "{'email': ['Enter a valid email address.']}"):
            self.account.objects.create_user(email=self.wrong_format_email, username=self.username, password=self.password)

    def test_account_password_is_hashed(self):
        account = self.account.objects.create_user(email=self.email, username=self.username, password=self.password)
        self.assertNotEqual(account.password, self.password)

    def test_account_username_character_limit_exceeded(self):
        with self.assertRaisesMessage(ValidationError, "{'username': ['Ensure this value has at most 150 characters (it has "+str(len(self.limit_exceeded_username))+").']}"):
            self.account.objects.create_user(email=self.email, username=self.limit_exceeded_username, password=self.password)

    def test_account_no_email(self):
        with self.assertRaisesMessage(ValueError, "Users must have an email address"):
            self.account.objects.create_user(email='', username=self.username, password=self.password)

    def test_account_no_username(self):
        with self.assertRaisesMessage(ValueError, "Users must have an username"):
            self.account.objects.create_user(email=self.email, username='', password=self.password)

    def test_account_no_password(self):
        with self.assertRaisesMessage(ValueError, "Users must have a password"):
            self.account.objects.create_user(email=self.email, username=self.username, password='')

class TestEmail(TestCase):
    def test_smtp_config(self):
        flag = send_mail(
            "Subject",
            "Message",
            'testing.brainstorm@gmail.com',
            ["testing.brainstorm@gmail.com"],
            fail_silently=False,
        )
        self.assertEqual(flag, 1)
