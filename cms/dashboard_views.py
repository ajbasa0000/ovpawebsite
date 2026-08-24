from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.apps import apps
from django import forms
from .decorators import content_manager_required
from .models import Page, StaffMember, NewsArticle, Event, Service, Issuance, Document, PartnerOffice, MediaGallery, Project, Feedback, ContactInquiry, ClaimableCheck, CashOfficePage

# --- Dashboard Home ---

@login_required
@content_manager_required
def dashboard_home(request):
    from .models import AdvisoryTicker
    stats = {
        'pages': Page.objects.count(),
        'staff': StaffMember.objects.count(),
        'news': NewsArticle.objects.count(),
        'advisories': AdvisoryTicker.objects.count(),
        'checks': ClaimableCheck.objects.count(),
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
    from .models import AdvisoryTicker
    model_map = {
        'pages': (Page, ['title', 'slug', 'status', 'updated_at']),
        'staff': (StaffMember, ['name', 'position', 'unit', 'is_active']),
        'news': (NewsArticle, ['title', 'published_date', 'status']),
        'advisories': (AdvisoryTicker, ['text', 'category', 'is_active', 'status']),
        'events': (Event, ['title', 'start_datetime', 'event_type', 'status']),
        'services': (Service, ['title', 'service_category', 'display_order', 'status']),
        'issuances': (Issuance, ['issuance_number', 'title', 'issuance_type', 'status']),
        'documents': (Document, ['title', 'category', 'status']),
        'partners': (PartnerOffice, ['name', 'is_active', 'status']),
        'gallery': (MediaGallery, ['title', 'published_date', 'status']),
        'projects': (Project, ['title', 'category', 'status']),
        'inquiries': (ContactInquiry, ['name', 'subject', 'is_resolved', 'created_at']),
        'feedback': (Feedback, ['name', 'rating', 'is_reviewed', 'created_at']),
        'claimable_checks': (ClaimableCheck, ['payee_name', 'voucher_number', 'check_number', 'amount', 'pin_code', 'claim_status', 'status']),
        'cash_office_page': (CashOfficePage, ['hero_title', 'cashier_hours', 'office_location', 'contact_email', 'status']),
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


# --- Centralized Categorized Page Manager Hub ---

@login_required
@content_manager_required
def page_manager_hub(request):
    """
    Centralized Categorized Page Manager Hub in CMD grouping dynamic pages, office portals, and resource hubs.
    """
    ovpa_pages = Page.objects.all().order_by('title')
    sco_page = CashOfficePage.get_solo()
    
    categories = [
        {
            'id': 'ovpa_core',
            'name': 'OVPA Core Pages',
            'icon': 'fa-building-columns',
            'badge_color': '#7b1113',
            'description': 'Standard dynamic content pages (About Us, Quality Policy, Mandate, Careers, etc.)',
            'pages': [
                {
                    'title': page.title,
                    'type': 'Dynamic Page',
                    'slug': page.slug,
                    'status': page.status,
                    'updated_at': page.updated_at,
                    'edit_url': reverse('module_edit', kwargs={'model_name': 'pages', 'pk': page.pk}),
                    'delete_url': reverse('module_delete', kwargs={'model_name': 'pages', 'pk': page.pk}),
                    'public_url': f"/page/{page.slug}/",
                } for page in ovpa_pages
            ]
        },
        {
            'id': 'office_units',
            'name': 'Constituent & Office Portals',
            'icon': 'fa-landmark-flag',
            'badge_color': '#0284c7',
            'description': 'Specialized landing pages and portals for system offices and constituent units',
            'pages': [
                {
                    'title': 'System Cash Office (SCO) Landing Page',
                    'type': 'Structured Office Portal',
                    'slug': 'cash-office',
                    'status': sco_page.status if hasattr(sco_page, 'status') else 'published',
                    'updated_at': sco_page.updated_at if hasattr(sco_page, 'updated_at') else None,
                    'edit_url': reverse('module_edit', kwargs={'model_name': 'cash_office_page', 'pk': sco_page.pk}),
                    'delete_url': None,
                    'public_url': '/office/cash-office/',
                },
                {
                    'title': 'Constituent Offices Directory',
                    'type': 'Directory Page',
                    'slug': 'office',
                    'status': 'published',
                    'updated_at': None,
                    'edit_url': reverse('module_list', kwargs={'model_name': 'partners'}),
                    'delete_url': None,
                    'public_url': '/office/',
                },
            ]
        },
        {
            'id': 'institutional_portals',
            'name': 'Institutional Portals',
            'icon': 'fa-layer-group',
            'badge_color': '#059669',
            'description': 'Operational listing directories for projects, staff, services, and partnerships',
            'pages': [
                {
                    'title': 'Major Projects & Programs Directory',
                    'type': 'Listing Portal',
                    'slug': 'projects',
                    'status': 'published',
                    'updated_at': None,
                    'edit_url': reverse('module_list', kwargs={'model_name': 'projects'}),
                    'delete_url': None,
                    'public_url': '/projects/',
                },
                {
                    'title': 'OVPA Staff Directory',
                    'type': 'Directory Portal',
                    'slug': 'staff',
                    'status': 'published',
                    'updated_at': None,
                    'edit_url': reverse('module_list', kwargs={'model_name': 'staff'}),
                    'delete_url': None,
                    'public_url': '/staff/',
                },
                {
                    'title': 'Programs & Services Directory',
                    'type': 'Directory Portal',
                    'slug': 'programs',
                    'status': 'published',
                    'updated_at': None,
                    'edit_url': reverse('module_list', kwargs={'model_name': 'services'}),
                    'delete_url': None,
                    'public_url': '/programs/',
                },
            ]
        },
        {
            'id': 'resource_hubs',
            'name': 'Resource & Media Hubs',
            'icon': 'fa-folder-open',
            'badge_color': '#d97706',
            'description': 'Public document downloads, official issuances, advisories, and media galleries',
            'pages': [
                {
                    'title': 'Document & Policy Downloads Hub',
                    'type': 'Resource Hub',
                    'slug': 'documents',
                    'status': 'published',
                    'updated_at': None,
                    'edit_url': reverse('module_list', kwargs={'model_name': 'documents'}),
                    'delete_url': None,
                    'public_url': '/resources/documents/',
                },
                {
                    'title': 'Official Issuances Center',
                    'type': 'Resource Hub',
                    'slug': 'issuances',
                    'status': 'published',
                    'updated_at': None,
                    'edit_url': reverse('module_list', kwargs={'model_name': 'issuances'}),
                    'delete_url': None,
                    'public_url': '/resources/issuances/',
                },
                {
                    'title': 'OVPA Media Gallery',
                    'type': 'Media Hub',
                    'slug': 'media',
                    'status': 'published',
                    'updated_at': None,
                    'edit_url': reverse('module_list', kwargs={'model_name': 'gallery'}),
                    'delete_url': None,
                    'public_url': '/media/',
                },
            ]
        }
    ]
    
    total_pages_count = sum(len(cat['pages']) for cat in categories)
    
    context = {
        'categories': categories,
        'total_pages_count': total_pages_count,
        'ovpa_pages_count': len(ovpa_pages),
    }
    return render(request, 'dashboard/page_manager.html', context)

