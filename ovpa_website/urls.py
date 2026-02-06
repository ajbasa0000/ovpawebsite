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
    
    # Homepage
    path('', views.homepage, name='home'),
    
    # Pages (About, Mandate, Mission, Vision, etc.)
    path('page/<slug:slug>/', views.page_view, name='page'),
    
    # News & Advisories
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    
    # Events
    path('events/', views.EventListView.as_view(), name='events'),
    
    # Services
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    
    # Issuances
    path('issuances/', views.IssuanceListView.as_view(), name='issuances'),
    
    # Documents
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    
    # Office Structure
    path('office/', views.office_structure, name='office_structure'),
    
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

