from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import (
    Page, NewsArticle, Event, Service, Issuance,
    Document, OfficeStructure, PartnerOffice
)
from .forms import ContactInquiryForm, FeedbackForm


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
        return NewsArticle.objects.filter(status='published').order_by('-published_date')


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
        return Event.objects.filter(status='published').order_by('start_datetime')


class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.filter(status='published').order_by('display_order')


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
    Office structure and organizational chart view.
    """
    structures = OfficeStructure.objects.filter(status='published').order_by('display_order')
    partners = PartnerOffice.objects.filter(is_active=True).order_by('display_order')
    context = {
        'structures': structures,
        'partners': partners,
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
