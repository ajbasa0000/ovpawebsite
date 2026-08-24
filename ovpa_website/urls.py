"""
URL configuration for ovpa_website project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cms import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('cms.dashboard_urls')),
    
    # Homepage
    path('', views.homepage, name='home'),
    
    # Pages (About, Mandate, Mission, Vision, etc.)
    path('about/', views.page_view, {'slug': 'about'}, name='about_direct'),
    path('page/<slug:slug>/', views.page_view, name='page'),
    
    # News & Updates Hub
    path('news-updates/', views.news_updates_hub, name='news_updates_hub'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('events/', views.EventListView.as_view(), name='events'),
    
    # Resources Hub
    path('resources/', views.resources_hub, name='resources_hub'),
    path('resources/services/', views.ServiceListView.as_view(), name='services'),
    path('resources/services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('resources/issuances/', views.IssuanceListView.as_view(), name='issuances'),
    path('resources/documents/', views.DocumentListView.as_view(), name='documents'),
    path('resources/media-gallery/', views.media_gallery, name='media_gallery'),
    path('resources/statistics/', views.statistics_dashboard, name='statistics'),
    path('resources/faqs/', views.faq_view, name='faqs'),
    
    # Office Structure & Sub-Offices
    path('office/', views.office_structure, name='office_structure'),
    path('office/cash-office/', views.cash_office_landing, name='cash_office_landing'),
    path('office/cash-office/search/', views.cash_office_check_search, name='cash_office_check_search'),
    path('office/cash-office/verify-pin/', views.cash_office_verify_pin, name='cash_office_verify_pin'),
    path('office/<slug:office_code>/', views.office_detail, name='office_detail'),
    
    # Hub Views
    path('careers/', views.careers_view, name='careers'),
    path('projects/', views.projects_view, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('programs/', views.programs_view, name='programs'),
    
    # Contact & Feedback
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

