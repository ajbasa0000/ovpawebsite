from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based permissions for CMS management.
    """
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('content_admin', 'Content Admin'),
        ('content_editor', 'Content Editor'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='content_editor',
        help_text='User role determines permissions in the CMS'
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_super_admin(self):
        return self.role == 'super_admin' or self.is_superuser
    
    def is_content_admin(self):
        return self.role in ['super_admin', 'content_admin'] or self.is_superuser
    
    def can_publish(self):
        """Content editors cannot publish, only admins can"""
        return self.is_content_admin()
