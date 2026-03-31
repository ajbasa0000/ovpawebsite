from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cms.models import (
    Page, StaffMember, NewsArticle, Event, Service, 
    Project, Issuance, Document, MediaGallery
)

class Command(BaseCommand):
    help = 'Setup the Staff Content Manager role and permissions'

    def handle(self, *args, **kwargs):
        group_name = 'Staff Content Manager'
        group, created = Group.objects.get_or_create(name=group_name)
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Group already exists: {group_name}'))

        # List of models that content managers can manage
        models = [
            Page, StaffMember, NewsArticle, Event, Service, 
            Project, Issuance, Document, MediaGallery
        ]
        
        permissions_count = 0
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            # Standard CRUD permissions
            actions = ['view', 'add', 'change']
            for action in actions:
                codename = f'{action}_{model._meta.model_name}'
                try:
                    permission = Permission.objects.get(content_type=content_type, codename=codename)
                    group.permissions.add(permission)
                    permissions_count += 1
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission not found: {codename}'))

        group.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully assigned {permissions_count} permissions to {group_name}'))
