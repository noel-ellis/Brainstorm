from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.mail import send_mail
    

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.clean_fields()
        user.save(using=self._db)

        user.email_user(subject='Brainstorm Account', message=f'Your Brainstorm username: {username}')
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=150, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.email
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
