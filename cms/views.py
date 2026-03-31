from django.shortcuts import render
from django.db import models
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import (
    Page, NewsArticle, Event, Service, Issuance,
    Document, OfficeStructure, PartnerOffice, MediaGallery, Project, StaffMember
)
from .forms import ContactInquiryForm, FeedbackForm
from django.shortcuts import get_object_or_404


def homepage(request):
    """
    Homepage view with featured content.
    """
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
        'admin_staff': staff_members.filter(is_top_management=False),
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
    # Assuming we might want to vary content eventually, for now using slugs or titles
    office_map = {
        'sspmo': 'System Supply and Property Management Office',
        'shrdo': 'System Human Resources Development Office',
        'sco': 'System Cash Office'
    }
    title = office_map.get(office_code.lower(), 'Office Detail')
    return render(request, 'cms/office_detail.html', {'title': title, 'office_code': office_code})


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
