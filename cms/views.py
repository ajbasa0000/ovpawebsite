from django.shortcuts import render
from django.db import models
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import (
    Page, NewsArticle, Event, Service, Issuance,
    Document, OfficeStructure, PartnerOffice, MediaGallery, Project, StaffMember, ClaimableCheck, CashOfficePage
)
from .forms import ContactInquiryForm, FeedbackForm
from django.shortcuts import get_object_or_404


def homepage(request):
    """
    Homepage view with comprehensive featured sections.
    """
    from .models import Service, PartnerOffice
    context = {
        'featured_news': NewsArticle.objects.filter(
            status='published',
            is_featured=True
        ).order_by('-published_date')[:3],
        'upcoming_events': Event.objects.filter(
            status='published'
        ).order_by('start_datetime')[:3],
        'latest_issuances': Issuance.objects.filter(
            status='published'
        ).order_by('-issuance_date')[:5],
        'featured_services': Service.objects.filter(
            status='published'
        ).order_by('display_order', 'title')[:6],
        'partner_offices': PartnerOffice.objects.filter(
            status='published',
            is_active=True
        ).order_by('name')[:6],
    }
    return render(request, 'index.html', context)


def page_view(request, slug):
    """
    Generic page view for About, Mandate, Mission, Vision, etc.
    """
    page = Page.objects.filter(slug=slug, status='published').first()
    if not page:
        return render(request, '404.html', status=404)
    return render(request, 'page.html', {'page': page})


class NewsListView(ListView):
    model = NewsArticle
    template_name = 'news/news_list.html'
    context_object_name = 'news_articles'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = NewsArticle.objects.filter(status='published').order_by('-published_date')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                models.Q(title__icontains=q) | 
                models.Q(content__icontains=q)
            )
        return queryset


class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = 'news/news_detail.html'
    context_object_name = 'article'
    
    def get_queryset(self):
        return NewsArticle.objects.filter(status='published')


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Event.objects.filter(status='published').order_by('start_datetime')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                models.Q(title__icontains=q) | 
                models.Q(description__icontains=q) |
                models.Q(location__icontains=q)
            )
        return queryset


class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        queryset = Service.objects.filter(status='published').order_by('display_order')
        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(service_category=category)
            
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                models.Q(title__icontains=q) | 
                models.Q(description__icontains=q)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    
    def get_queryset(self):
        return Service.objects.filter(status='published')


class IssuanceListView(ListView):
    model = Issuance
    template_name = 'issuances/issuance_list.html'
    context_object_name = 'issuances'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Issuance.objects.filter(status='published').order_by('-issuance_date')
        issuance_type = self.request.GET.get('type')
        if issuance_type:
            queryset = queryset.filter(issuance_type=issuance_type)
        
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                models.Q(title__icontains=q) | 
                models.Q(issuance_number__icontains=q)
            )
        return queryset


class DocumentListView(ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Document.objects.filter(status='published').order_by('-created_at')
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(tags__icontains=search)
        return queryset


def office_structure(request):
    """
    Office structure and organizational chart view with keyword search and staff directory.
    """
    q = request.GET.get('q')
    structures = OfficeStructure.objects.filter(status='published').order_by('display_order')
    partners = PartnerOffice.objects.filter(is_active=True).order_by('display_order')
    
    # Staff Directory
    staff_members = StaffMember.objects.filter(is_active=True, status='published').order_by('display_order')
    
    if q:
        structures = structures.filter(
            models.Q(title__icontains=q) | 
            models.Q(description__icontains=q)
        )
        partners = partners.filter(
            models.Q(name__icontains=q) | 
            models.Q(description__icontains=q)
        )
        staff_members = staff_members.filter(
            models.Q(name__icontains=q) |
            models.Q(position__icontains=q) |
            models.Q(unit__icontains=q)
        )
        
    context = {
        'structures': structures,
        'partners': partners,
        'executive_staff': staff_members.filter(is_top_management=True),
        'qms_staff': staff_members.filter(is_top_management=False, unit='OVPA-Quality Management System'),
        'admin_staff': staff_members.filter(is_top_management=False).exclude(unit='OVPA-Quality Management System'),
        'search_query': q,
    }
    return render(request, 'office/structure.html', context)


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactInquiryForm
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thank you for your inquiry. We will respond as soon as possible.')
        return super().form_valid(form)


class FeedbackView(FormView):
    template_name = 'feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('feedback')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thank you for your feedback!')
        return super().form_valid(form)
def news_updates_hub(request):
    """
    Combined hub for News and Events.
    """
    news = NewsArticle.objects.filter(status='published').order_by('-published_date')[:6]
    events = Event.objects.filter(status='published').order_by('start_datetime')[:6]
    return render(request, 'cms/news_updates_hub.html', {
        'news': news,
        'events': events
    })


def resources_hub(request):
    """
    Main landing for all resources.
    """
    return render(request, 'cms/resources_hub.html')


def media_gallery(request):
    """
    Media Gallery with photos and descriptions from the dedicated model.
    """
    items = MediaGallery.objects.filter(status='published').order_by('-published_date')
    return render(request, 'cms/media_gallery.html', {'items': items})


def statistics_dashboard(request):
    """
    Dashboard-like statistics view.
    """
    return render(request, 'cms/statistics.html')


def faq_view(request):
    """
    Frequently Asked Questions.
    """
    return render(request, 'cms/faqs.html')


def office_detail(request, office_code):
    """
    Detailed view for sub-offices (SSPMO, SHRDO, SCO).
    """
    if office_code.lower() in ('sco', 'cash-office', 'cash_office'):
        return cash_office_landing(request)

    office_map = {
        'sspmo': 'System Supply and Property Management Office',
        'shrdo': 'System Human Resources Development Office',
    }
    title = office_map.get(office_code.lower(), 'Office Detail')
    return render(request, 'cms/office_detail.html', {'title': title, 'office_code': office_code})


def cash_office_landing(request):
    """
    Dedicated landing page for the System Cash Office (SCO) featuring supplier check status lookup.
    """
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    
    sco_page = CashOfficePage.get_solo()
    all_published = ClaimableCheck.objects.filter(status='published')
    
    searched_checks = None
    if query or status_filter:
        searched_checks = all_published
        if query:
            searched_checks = searched_checks.filter(
                models.Q(payee_name__icontains=query) |
                models.Q(voucher_number__icontains=query) |
                models.Q(check_number__icontains=query)
            )
        if status_filter:
            searched_checks = searched_checks.filter(claim_status=status_filter)
        searched_checks = searched_checks.order_by('-check_date')[:50]
        
    recent_ready_checks = all_published.filter(claim_status='ready').order_by('-check_date')[:8]
    
    stats_summary = {
        'ready_count': all_published.filter(claim_status='ready').count(),
        'processing_count': all_published.filter(claim_status='processing').count(),
        'released_count': all_published.filter(claim_status='released').count(),
    }
    
    context = {
        'title': sco_page.hero_title or 'System Cash Office',
        'sco_page': sco_page,
        'query': query,
        'status_filter': status_filter,
        'searched_checks': searched_checks,
        'recent_ready_checks': recent_ready_checks,
        'stats_summary': stats_summary,
    }
    return render(request, 'cms/cash_office.html', context)


def cash_office_check_search(request):
    """
    JSON API endpoint for real-time supplier check lookup.
    """
    from django.http import JsonResponse
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return JsonResponse({'results': [], 'message': 'Please enter at least 2 characters to search.'})
        
    checks = ClaimableCheck.objects.filter(
        status='published'
    ).filter(
        models.Q(payee_name__icontains=query) |
        models.Q(voucher_number__icontains=query) |
        models.Q(check_number__icontains=query)
    ).order_by('-check_date')[:25]
    
    results = []
    for c in checks:
        results.append({
            'id': c.id,
            'payee_name': c.payee_name,
            'voucher_number': c.voucher_number,
            'check_number': c.check_number or 'Pending',
            'amount': '₱ ••••••••',
            'check_date': c.check_date.strftime('%B %d, %Y') if c.check_date else '',
            'claim_status': c.claim_status,
            'claim_status_display': c.get_claim_status_display(),
            'date_released': c.date_released.strftime('%B %d, %Y') if c.date_released else None,
            'claiming_requirements': 'Protected by Security PIN',
            'remarks': '',
        })
        
    return JsonResponse({'results': results, 'count': len(results)})


def cash_office_verify_pin(request):
    """
    JSON API endpoint to verify supplier PIN code and return unlocked check details.
    """
    from django.http import JsonResponse
    import json

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            check_id = data.get('check_id')
            input_pin = str(data.get('pin_code', '')).strip()
        except Exception:
            check_id = request.POST.get('check_id')
            input_pin = str(request.POST.get('pin_code', '')).strip()
    else:
        check_id = request.GET.get('check_id')
        input_pin = str(request.GET.get('pin_code', '')).strip()

    if not check_id or not input_pin:
        return JsonResponse({'success': False, 'message': 'Check ID and 6-digit PIN are required.'}, status=400)

    try:
        check = ClaimableCheck.objects.get(pk=check_id, status='published')
    except ClaimableCheck.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Check record not found.'}, status=404)

    if str(check.pin_code).strip() != input_pin:
        return JsonResponse({'success': False, 'message': 'Incorrect Security PIN. Please check your 6-digit access code or contact the Cash Office.'}, status=403)

    return JsonResponse({
        'success': True,
        'data': {
            'id': check.id,
            'payee_name': check.payee_name,
            'voucher_number': check.voucher_number,
            'check_number': check.check_number or 'Pending Assignment',
            'amount': f"₱{check.amount:,.2f}",
            'check_date': check.check_date.strftime('%B %d, %Y') if check.check_date else '',
            'claim_status': check.claim_status,
            'claim_status_display': check.get_claim_status_display(),
            'date_released': check.date_released.strftime('%B %d, %Y') if check.date_released else 'Not yet released',
            'claiming_requirements': check.claiming_requirements,
            'remarks': check.remarks or 'None',
        }
    })


def careers_view(request):
    return render(request, 'cms/hub_page.html', {'title': 'Careers', 'content': 'Join our team at the UP System.'})


def projects_view(request):
    projects = Project.objects.filter(status='published')
    
    # Group projects by category
    projects_by_category = {}
    for project in projects:
        cat_name = project.get_category_display()
        if cat_name not in projects_by_category:
            projects_by_category[cat_name] = []
        projects_by_category[cat_name].append(project)
        
    return render(request, 'cms/projects_hub.html', {
        'title': 'Projects & Initiatives',
        'projects_by_category': projects_by_category
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, status='published')
    return render(request, 'cms/project_detail.html', {'project': project})


def programs_view(request):
    return render(request, 'cms/hub_page.html', {'title': 'Programs', 'content': 'Learn about our strategic programs.'})
