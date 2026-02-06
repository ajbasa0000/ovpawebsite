# OVPA Website - Government CMS

Office of the Vice President for Administration - University of the Philippines System

## Overview

This is a production-ready government office website built with Django 5.0, featuring a comprehensive Content Management System (CMS) designed for non-technical staff. The system includes role-based permissions, audit logging, and a clean, accessible government-appropriate design.

## Features

### CMS Modules
- **Homepage** - Hero section with featured content
- **Pages** - About, Mandate, Mission, Vision, Values & Policy
- **Office Structure** - Organizational chart and hierarchy
- **Partner Offices** - Partner agencies and offices
- **Services** - Services listing with detailed information
- **Issuances** - Memos, circulars, orders, and resolutions
- **News & Advisories** - News articles with featured images
- **Events Calendar** - Upcoming events and activities
- **Document Repository** - Categorized documents with search
- **Contact Form** - Public inquiry submission
- **Feedback Form** - User feedback collection

### User Roles
- **Super Admin** - Full system access
- **Content Admin** - Can publish and manage all content
- **Content Editor** - Can create and edit content (requires admin approval to publish)

### Technical Features
- Django 5.0 with PostgreSQL/SQLite support
- Rich text editing with CKEditor
- Role-based permissions
- Draft/Review/Publish workflow
- Audit logging
- Responsive design
- WCAG 2.1 AA accessibility
- Security-first configuration

## Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

For local development, the default SQLite configuration in `.env` works out of the box.

3. **Run migrations:**
```bash
python manage.py migrate
```

4. **Create superuser:**
```bash
python manage.py createsuperuser
```

5. **Run development server:**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` for the public site and `http://localhost:8000/admin` for the admin panel.

## Usage

### Admin Panel

Access the admin panel at `/admin` with your superuser credentials.

#### Creating Content

1. **Pages** (About, Mandate, etc.):
   - Go to CMS → Pages
   - Click "Add Page"
   - Enter title (slug auto-generates)
   - Add content using the rich text editor
   - Set status to "Published"
   - Save

2. **News Articles**:
   - Go to CMS → News Articles
   - Add title, excerpt, content
   - Upload featured image (optional)
   - Set published date
   - Mark as featured for homepage display
   - Set status to "Published"

3. **Services**:
   - Go to CMS → Services
   - Add title, description, requirements, process
   - Set display order
   - Set status to "Published"

4. **Issuances**:
   - Go to CMS → Issuances
   - Add issuance number, title, type
   - Add content and/or attachment
   - Set issuance date
   - Set status to "Published"

5. **Documents**:
   - Go to CMS → Documents
   - Upload file
   - Add title, description, category
   - Add tags for search
   - Set status to "Published"

### User Management

1. Go to Accounts → Users
2. Click "Add User"
3. Set username, password, email
4. Select role (Super Admin, Content Admin, or Content Editor)
5. Save

## Project Structure

```
ovpa_website/
├── accounts/           # User management app
│   ├── models.py      # Custom User model with roles
│   └── admin.py       # User admin interface
├── cms/               # Main CMS app
│   ├── models.py      # All CMS models
│   ├── admin.py       # CMS admin interfaces
│   ├── views.py       # Public-facing views
│   └── forms.py       # Contact and feedback forms
├── ovpa_website/      # Project configuration
│   ├── settings.py    # Django settings
│   └── urls.py        # URL routing
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Homepage
│   ├── news/          # News templates
│   ├── services/      # Service templates
│   ├── issuances/     # Issuance templates
│   ├── documents/     # Document templates
│   ├── events/        # Event templates
│   └── office/        # Office structure templates
└── static/            # Static assets
    ├── css/           # Stylesheets
    └── js/            # JavaScript
```

## Design Guidelines

### Colors
- **Base:** Clean slate/white background
- **Accents (use sparingly):**
  - Maroon (#8B0000) - Primary accent
  - Forest Green (#228B22) - Secondary accent
  - Gold (#FFD700) - Tertiary accent

### Typography
- Government-appropriate, accessible fonts
- Clear hierarchy
- Readable line lengths

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support
- Sufficient color contrast

## Deployment

### Production Checklist

1. **Environment Variables:**
   - Set `DEBUG=False`
   - Set strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`
   - Set up PostgreSQL database
   - Configure email backend

2. **Static Files:**
```bash
python manage.py collectstatic
```

3. **Database:**
```bash
python manage.py migrate
```

4. **Security:**
   - Enable HTTPS
   - Set secure cookies
   - Configure CSRF protection
   - Review security settings in `settings.py`

5. **Web Server:**
   - Use Gunicorn or uWSGI
   - Configure Nginx or Apache
   - Set up SSL certificates

### Example Gunicorn Command
```bash
gunicorn ovpa_website.wsgi:application --bind 0.0.0.0:8000
```

## Maintenance

### Backup
- Regular database backups
- Media files backup
- Environment configuration backup

### Updates
- Keep Django and dependencies updated
- Review security advisories
- Test updates in staging environment

### Monitoring
- Check logs in `logs/django.log`
- Monitor admin actions
- Review contact inquiries and feedback

## Support

For technical support or questions:
- Email: ovpa@up.edu.ph
- Phone: (02) 8981-8500

## License

© 2026 Office of the Vice President for Administration, University of the Philippines System. All rights reserved.
