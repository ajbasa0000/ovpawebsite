from django.contrib import admin
from .models import (
    Page, OfficeStructure, PartnerOffice, Service,
    Issuance, NewsArticle, Event, Document,
    ContactInquiry, Feedback, MediaGallery, Project, ProjectImage
)


# Customize admin site branding
admin.site.site_header = 'OVPA Website Administration'
admin.site.site_title = 'OVPA Admin'
admin.site.index_title = 'Content Management System'


class BaseAdmin(admin.ModelAdmin):
    """
    Base admin class with common configurations.
    """
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_delete_permission(self, request, obj=None):
        # Only super admins can delete
        return request.user.is_superuser or (hasattr(request.user, 'is_super_admin') and request.user.is_super_admin())


@admin.register(Page)
class PageAdmin(BaseAdmin):
    list_display = ['title', 'slug', 'status', 'created_by', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'meta_description')
        }),
        ('Publishing', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OfficeStructure)
class OfficeStructureAdmin(BaseAdmin):
    list_display = ['title', 'display_order', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'org_chart_image', 'display_order')
        }),
        ('Publishing', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PartnerOffice)
class PartnerOfficeAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_order', 'is_active', 'website_url']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Information', {
            'fields': ('name', 'description', 'logo', 'website_url')
        }),
        ('Display', {
            'fields': ('display_order', 'is_active')
        }),
    )


@admin.register(Service)
class ServiceAdmin(BaseAdmin):
    list_display = ['title', 'display_order', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'description', 'requirements', 'process', 'icon', 'display_order')
        }),
        ('Publishing', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Issuance)
class IssuanceAdmin(BaseAdmin):
    list_display = ['issuance_number', 'title', 'issuance_type', 'issuance_date', 'status']
    list_filter = ['issuance_type', 'status', 'issuance_date']
    search_fields = ['issuance_number', 'title', 'content']
    date_hierarchy = 'issuance_date'
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Issuance Information', {
            'fields': ('issuance_number', 'title', 'issuance_type', 'issuance_date')
        }),
        ('Content', {
            'fields': ('content', 'attachment')
        }),
        ('Publishing', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NewsArticle)
class NewsArticleAdmin(BaseAdmin):
    list_display = ['title', 'published_date', 'is_featured', 'status', 'created_by']
    list_filter = ['status', 'is_featured', 'published_date']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('status', 'published_date', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'remove_featured']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Mark selected as featured"
    
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
    remove_featured.short_description = "Remove featured status"


@admin.register(Event)
class EventAdmin(BaseAdmin):
    list_display = ['title', 'start_datetime', 'end_datetime', 'event_type', 'status']
    list_filter = ['event_type', 'status', 'start_datetime']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start_datetime'
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'event_type', 'location')
        }),
        ('Schedule', {
            'fields': ('start_datetime', 'end_datetime')
        }),
        ('Publishing', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Document)
class DocumentAdmin(BaseAdmin):
    list_display = ['title', 'category', 'download_count', 'status', 'uploaded_by', 'created_at']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['title', 'description', 'tags']
    readonly_fields = ['download_count', 'created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'description', 'document_file', 'category', 'tags')
        }),
        ('Publishing', {
            'fields': ('status',)
        }),
        ('Statistics', {
            'fields': ('download_count',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at', 'is_resolved']
    list_filter = ['is_resolved', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'submitted_at']
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Inquiry Details', {
            'fields': ('name', 'email', 'subject', 'message', 'submitted_at')
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolved_by')
        }),
    )
    
    actions = ['mark_resolved']
    
    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True, resolved_by=request.user)
    mark_resolved.short_description = "Mark selected inquiries as resolved"
    
    def has_add_permission(self, request):
        # Contact inquiries are submitted via form, not created in admin
        return False


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'rating', 'submitted_at', 'is_reviewed']
    list_filter = ['rating', 'is_reviewed', 'submitted_at']
    search_fields = ['name', 'email', 'feedback']
    readonly_fields = ['name', 'email', 'feedback', 'rating', 'submitted_at']
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Feedback Details', {
            'fields': ('name', 'email', 'feedback', 'rating', 'submitted_at')
        }),
        ('Review Status', {
            'fields': ('is_reviewed',)
        }),
    )
    
    actions = ['mark_reviewed']
    
    def mark_reviewed(self, request, queryset):
        queryset.update(is_reviewed=True)
    mark_reviewed.short_description = "Mark selected feedback as reviewed"
    
    def has_add_permission(self, request):
        # Feedback is submitted via form, not created in admin
        return False


@admin.register(MediaGallery)
class MediaGalleryAdmin(BaseAdmin):
    list_display = ['title', 'published_date', 'status', 'created_by']
    list_filter = ['status', 'published_date', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'published_date'
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Gallery Item Details', {
            'fields': ('title', 'description', 'image_file', 'published_date')
        }),
        ('Publishing', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption')


@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    inlines = [ProjectImageInline]
    list_display = ['title', 'category', 'status', 'created_at', 'created_by']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'category', 'excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
