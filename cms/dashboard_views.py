from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.apps import apps
from django import forms
from .decorators import content_manager_required
from .models import Page, StaffMember, NewsArticle, Event, Service, Issuance, Document, PartnerOffice, MediaGallery, Project, Feedback, ContactInquiry

# --- Dashboard Home ---

@login_required
@content_manager_required
def dashboard_home(request):
    stats = {
        'pages': Page.objects.count(),
        'staff': StaffMember.objects.count(),
        'news': NewsArticle.objects.count(),
        'services': Service.objects.count(),
    }
    recent_pages = Page.objects.order_by('-updated_at')[:5]
    recent_staff = StaffMember.objects.order_by('-updated_at')[:5]
    
    return render(request, 'dashboard/home.html', {
        'stats': stats,
        'recent_pages': recent_pages,
        'recent_staff': recent_staff,
    })


# --- Generic Module Controller (Token Saving & Efficient) ---

def get_module_config(model_name):
    """
    Returns the model and its configuration for the dashboard.
    """
    model_map = {
        'pages': (Page, ['title', 'slug', 'status', 'updated_at']),
        'staff': (StaffMember, ['name', 'position', 'unit', 'is_active']),
        'news': (NewsArticle, ['title', 'published_date', 'status']),
        'events': (Event, ['title', 'start_datetime', 'event_type', 'status']),
        'services': (Service, ['title', 'service_category', 'display_order', 'status']),
        'issuances': (Issuance, ['issuance_number', 'title', 'issuance_type', 'status']),
        'documents': (Document, ['title', 'category', 'status']),
        'partners': (PartnerOffice, ['name', 'is_active', 'status']),
        'gallery': (MediaGallery, ['title', 'published_date', 'status']),
        'projects': (Project, ['title', 'category', 'status']),
        'inquiries': (ContactInquiry, ['name', 'subject', 'is_resolved', 'created_at']),
        'feedback': (Feedback, ['name', 'rating', 'is_reviewed', 'created_at']),
    }
    return model_map.get(model_name.lower())

@login_required
@content_manager_required
def module_list(request, model_name):
    config = get_module_config(model_name)
    if not config:
        return redirect('dashboard_home')
    
    model, field_names = config
    items = model.objects.all()
    
    # Pre-format headers (replace underscores with spaces)
    headers = [f.replace('_', ' ').title() for f in field_names]
    
    # Pre-format rows so template needs zero custom tags
    rows = []
    for item in items:
        cells = []
        for i, f in enumerate(field_names):
            val = getattr(item, f, '')
            display_method = getattr(item, f'get_{f}_display', None)
            
            if f == 'status':
                cells.append({'type': 'status', 'raw': item.status, 'display': item.get_status_display()})
            elif f in ('is_active', 'is_resolved', 'is_reviewed'):
                cells.append({'type': 'bool', 'value': bool(val)})
            elif display_method:
                cells.append({'type': 'text', 'value': display_method(), 'bold': i == 0})
            elif callable(val):
                cells.append({'type': 'text', 'value': val(), 'bold': i == 0})
            else:
                cells.append({'type': 'text', 'value': val, 'bold': i == 0})
        rows.append({'pk': item.pk, 'cells': cells})
    
    return render(request, 'dashboard/module_list.html', {
        'rows': rows,
        'model_name': model_name,
        'verbose_name': model._meta.verbose_name_plural,
        'headers': headers,
        'col_count': len(field_names) + 1,
    })

@login_required
@content_manager_required
def module_edit(request, model_name, pk=None):
    config = get_module_config(model_name)
    if not config:
        return redirect('dashboard_home')
        
    model, _ = config
    instance = get_object_or_404(model, pk=pk) if pk else model()
    
    # Dynamic Form Creation
    class DynamicForm(forms.ModelForm):
        class Meta:
            model = instance.__class__
            exclude = ['is_deleted', 'deleted_at', 'created_by']
            
    if request.method == 'POST':
        form = DynamicForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            if not pk:
                obj.created_by = request.user
            obj.save()
            messages.success(request, f"{model._meta.verbose_name} saved successfully.")
            return redirect('module_list', model_name=model_name)
    else:
        form = DynamicForm(instance=instance)
        
    return render(request, 'dashboard/module_form.html', {
        'form': form,
        'model_name': model_name,
        'verbose_name': model._meta.verbose_name,
        'instance': instance,
        'title': f"{'Edit' if pk else 'Add'} {model._meta.verbose_name}"
    })

@login_required
@content_manager_required
def module_delete(request, model_name, pk):
    config = get_module_config(model_name)
    if not config:
        return redirect('dashboard_home')
        
    model, _ = config
    item = get_object_or_404(model, pk=pk)
    
    if request.method == 'POST':
        item.delete() # Soft delete
        messages.warning(request, f"{model._meta.verbose_name} moved to Recycle Bin.")
        return redirect('module_list', model_name=model_name)
        
    return render(request, 'dashboard/confirm_delete.html', {'item': item, 'type': model._meta.verbose_name})


# --- Super Admin Tools (Recycle Bin) ---

@login_required
def recycle_bin(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    # Dynamically find all soft-deleted items
    deleted_items = []
    cms_models = apps.get_app_config('cms').get_models()
    for model in cms_models:
        if hasattr(model, 'all_objects'):
            items = model.all_objects.filter(is_deleted=True)
            for item in items:
                deleted_items.append({
                    'obj': item,
                    'type': model._meta.verbose_name,
                    'model_key': model.__name__.lower() # We'll map this for restore
                })
    
    return render(request, 'dashboard/recycle_bin.html', {'deleted_items': deleted_items})

@login_required
def restore_item(request, model_class, pk):
    if not request.user.is_superuser:
        raise PermissionDenied
        
    model = apps.get_model('cms', model_class)
    item = get_object_or_404(model.all_objects, pk=pk)
    item.restore()
    messages.success(request, f"Item restored successfully.")
    return redirect('recycle_bin')
