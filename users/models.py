from django.db.models import CASCADE
import re
from django.db import models
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Criação de um model de User personalizado
class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=15, unique=True,
                                help_text=_('Required. 15 characters or fewer. Letters, \
                    numbers and @/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(
                                        re.compile('^[\w.@+-]+$'),
                                        _('Enter a valid username.'),
                                        _('invalid'))])
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. \
                    Unselect this instead of deleting account.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    first_login = models.BooleanField(default=True)
    is_trusty = models.BooleanField(_('trusty'), default=False,
                                    help_text=_('Designates whether this user has confirmed his account.'))
    current_organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.username


# Termino da criação do model de User personalizado


class Organization(models.Model):
    name = models.CharField(max_length=105)
    created_by = models.ForeignKey(User, on_delete=CASCADE, related_name='created_organization')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Membership(models.Model):  # Aqui define a função do usuario na equipe
    ROLES = [
        ('owner', 'Dono'),
        ('admin', 'Administrador'),
        ('collaborator', 'Colaborador'),
    ]

    user = models.ForeignKey(User, on_delete=CASCADE, related_name='funcoes')
    organization = models.ForeignKey(Organization, on_delete=CASCADE, related_name='membros')
    role = models.CharField(max_length=20, choices=ROLES, default='collaborator')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'organization')
        verbose_name_plural = "Members of Orgs"

    def __str__(self):
        return f'{self.role} {self.user.username} de {self.organization.name}'
