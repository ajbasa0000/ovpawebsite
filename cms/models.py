from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField


class SoftDeleteManager(models.Manager):
    """
    Manager that filters out soft-deleted items by default.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class AllObjectsManager(models.Manager):
    """
    Manager to retrieve all objects, including soft-deleted ones.
    """
    def get_queryset(self):
        return super().get_queryset()


class BaseModel(models.Model):
    """
    Abstract base model with common fields for all CMS content.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='published',
        help_text='Content status in the publishing workflow'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created'
    )
    
    is_deleted = models.BooleanField(
        default=False,
        help_text='If checked, content is archived and hidden from the public site.'
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()
    
    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, *args, **kwargs):
        """
        Soft delete the object.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """
        Restore a soft-deleted object.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def hard_delete(self, *args, **kwargs):
        """
        Permanently delete the object.
        """
        super().delete(*args, **kwargs)


class Page(BaseModel):
    """
    Dynamic pages for About, Mandate, Mission, Vision, Values & Policy, etc.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = RichTextField()
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text='SEO meta description (160 characters max)'
    )
    
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class OfficeStructure(BaseModel):
    """
    Office structure and organizational chart information.
    """
    title = models.CharField(max_length=200)
    description = RichTextField()
    org_chart_image = models.ImageField(
        upload_to='org_charts/',
        blank=True,
        null=True,
        help_text='Upload organizational chart image'
    )
    display_order = models.IntegerField(default=0, help_text='Order of display (lower numbers first)')
    
    class Meta:
        verbose_name = 'Office Structure'
        verbose_name_plural = 'Office Structures'
        ordering = ['display_order', 'title']
    
    def __str__(self):
        return self.title


class PartnerOffice(BaseModel):
    """
    Partner agencies and offices.
    """
    name = models.CharField(max_length=200)
    description = RichTextField(blank=True)
    logo = models.ImageField(upload_to='partner_logos/', blank=True, null=True)
    website_url = models.URLField(blank=True, help_text='Partner office website URL')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Partner Office'
        verbose_name_plural = 'Partner Offices'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class Service(BaseModel):
    """
    Services offered by the office.
    """
    SERVICE_CATEGORIES = [
        ('internal', 'Internal Services'),
        ('external', 'External Services'),
    ]
    TRANSACTION_TYPES = [
        ('simple', 'Simple Transaction'),
        ('complex', 'Complex Transaction'),
        ('highly_technical', 'Highly Technical Transaction'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    service_category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES, default='internal')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='simple')
    duration = models.CharField(max_length=100, blank=True, help_text='Expected processing time (e.g., 20 minutes)')
    description = RichTextField()
    where_to_secure = models.CharField(max_length=200, blank=True, help_text='Office or Unit where the service is secured')
    who_may_avail = models.CharField(max_length=300, blank=True, help_text='Target constituents (e.g., UP System Employees)')
    classification = models.CharField(max_length=50, blank=True, default='G2G', help_text='Classification (e.g., G2G, G2C)')
    requirements = RichTextField(blank=True, help_text='Requirements to avail this service')
    process = RichTextField(blank=True, help_text='Step-by-step process')
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='Font Awesome icon class (e.g., fa-file-alt)'
    )
    display_order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['display_order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Issuance(BaseModel):
    """
    Memos, circulars, and official issuances.
    """
    ISSUANCE_TYPES = [
        ('memo', 'Memorandum'),
        ('circular', 'Circular'),
        ('order', 'Order'),
        ('resolution', 'Resolution'),
    ]
    
    title = models.CharField(max_length=300)
    issuance_number = models.CharField(max_length=50, unique=True, help_text='e.g., MEMO-2026-001')
    issuance_type = models.CharField(max_length=20, choices=ISSUANCE_TYPES, default='memo')
    content = RichTextField()
    attachment = models.FileField(
        upload_to='issuances/',
        blank=True,
        null=True,
        help_text='PDF or document file'
    )
    issuance_date = models.DateField()
    
    class Meta:
        verbose_name = 'Issuance'
        verbose_name_plural = 'Issuances'
        ordering = ['-issuance_date', '-created_at']
    
    def __str__(self):
        return f"{self.issuance_number} - {self.title}"


class NewsArticle(BaseModel):
    """
    News and advisories.
    """
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, help_text='Brief summary for listings')
    content = RichTextField()
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(
        default=False,
        help_text='Featured articles appear on homepage'
    )
    
    class Meta:
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
        ordering = ['-published_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Event(BaseModel):
    """
    Calendar events.
    """
    EVENT_TYPES = [
        ('meeting', 'Meeting'),
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = RichTextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='meeting')
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['start_datetime']
    
    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%Y-%m-%d')}"


class Document(BaseModel):
    """
    Document repository with categorization.
    """
    CATEGORY_CHOICES = [
        ('forms', 'Forms'),
        ('policies', 'Policies'),
        ('reports', 'Reports'),
        ('guidelines', 'Guidelines'),
        ('templates', 'Templates'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document_file = models.FileField(upload_to='documents/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text='Comma-separated tags for search'
    )
    download_count = models.IntegerField(default=0, editable=False)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents'
    )
    
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def increment_download_count(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])


class ContactInquiry(BaseModel):
    """
    Contact form submissions.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_inquiries'
    )
    
    class Meta:
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class Feedback(BaseModel):
    """
    Feedback form submissions.
    """
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    feedback = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback from {self.name or 'Anonymous'} - {self.created_at.strftime('%Y-%m-%d') if self.created_at else 'No Date'}"


class MediaGallery(BaseModel):
    """
    Independent repository for the Media Gallery.
    """
    title = models.CharField(max_length=200, help_text="Short title for the image.")
    description = models.TextField(blank=True, help_text="Context or descriptive caption for the image.")
    image_file = models.ImageField(upload_to='media_gallery/')
    published_date = models.DateField(help_text="Date the event or subject occurred.")
    
    class Meta:
        verbose_name = 'Media Gallery Item'
        verbose_name_plural = 'Media Gallery Items'
        ordering = ['-published_date', '-created_at']
    
    def __str__(self):
        return self.title


class Project(BaseModel):
    """
    Dedicated model for major initiatives and projects.
    """
    CATEGORY_CHOICES = [
        ('sspmo', 'SSPMO'),
        ('shrdo', 'SHRDO'),
        ('sco', 'SCO'),
        ('ovpa-qms', 'OVPA-QMS'),
        ('special', 'Special Projects'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='special')
    excerpt = models.TextField(help_text="Short summary for the project card.")
    content = RichTextField(help_text="Full article content and design.")
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectImage(BaseModel):
    """
    Separate database for images associated with a Project.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'
        ordering = ['created_at']
        
    def __str__(self):
        return f"Image for {self.project.title}"


class StaffMember(BaseModel):
    """
    Personnel and staff directory for the office.
    """
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    is_top_management = models.BooleanField(
        default=False, 
        help_text="Highlights the member in the Executive Leadership section."
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'
        ordering = ['display_order', 'name']
        
    def __str__(self):
        return f"{self.name} - {self.position}"
