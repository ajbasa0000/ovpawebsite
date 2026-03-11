from django.utils import timezone
from cms.models import Issuance, NewsArticle, Service, Document
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

# 1. Generate Issuances
issuances_data = [
    {
        'title': 'Revised Guidelines on Administrative Staff Development Program',
        'number': 'MEMO-2026-001',
        'type': 'memo',
        'date': datetime.date(2026, 3, 1),
        'content': 'This memorandum outlines the updated procedures and eligibility criteria for administrative staff seeking professional development support...'
    },
    {
        'title': 'Call for Nominations: Outstanding Administrative Personnel 2026',
        'number': 'MEMO-2026-002',
        'type': 'memo',
        'date': datetime.date(2026, 3, 5),
        'content': 'We are pleased to announce the call for nominations for the annual Gawad Parangal for administrative staff who have shown exceptional commitment...'
    },
    {
        'title': 'Institutional Policy on Digital Transformation for Office Operations',
        'number': 'CIRCULAR-2026-01',
        'type': 'circular',
        'date': datetime.date(2026, 2, 25),
        'content': 'To streamline service delivery across all Constituent Units, this circular mandates the adoption of unified digital document tracking systems...'
    },
    {
        'title': 'Implementation of Synchronized Performance Review Cycle',
        'number': 'ORDER-2026-04',
        'type': 'order',
        'date': datetime.date(2026, 3, 10),
        'content': 'This order provides the schedule and mandatory requirements for the first quarter performance evaluation for the year 2026...'
    },
    {
        'title': 'Resolution on the Adoption of Sustainable Campus Management Practices',
        'number': 'RES-2026-08',
        'type': 'resolution',
        'date': datetime.date(2026, 2, 11),
        'content': 'The System Administration hereby adopts the unified framework for sustainability, focusing on energy efficiency and waste reduction in all offices...'
    },
]

for data in issuances_data:
    Issuance.objects.get_or_create(
        issuance_number=data['number'],
        defaults={
            'title': data['title'],
            'issuance_type': data['type'],
            'issuance_date': data['date'],
            'content': data['content'],
            'status': 'published',
            'created_by': admin_user
        }
    )

# 2. Generate News Articles
news_data = [
    {
        'title': 'UP System Administration Hosts Strategic Planning Workshop',
        'excerpt': 'Executive leaders from all constituent units gathered to align administrative goals for the next quadrennium.',
        'content': '<p>The Office of the Vice President for Administration successfully concluded its three-day strategic planning workshop...</p>',
        'featured': True
    },
    {
        'title': 'Modernization of Payroll and Benefits System Nears Completion',
        'excerpt': 'The new cloud-based system is expected to cut processing times by 40% for all university employees.',
        'content': '<p>In line with the Digital Transformation initiatives, the OVPA is rolling out the final phase of the Integrated Management System...</p>',
        'featured': True
    },
    {
        'title': 'OVPA Announces New Wellness Programs for Administrative Staff',
        'excerpt': 'Expanding benefits to include mental health support and fitness workshops starting this April.',
        'content': '<p>Prioritizing the holistic wellbeing of our human resources, the university introduces a series of new health initiatives...</p>',
        'featured': False
    },
    {
        'title': 'University Fleet Transition to Electric Vehicles Commences',
        'excerpt': 'First batch of EV shuttles arrived today for inter-campus transport services.',
        'content': '<p>As part of our commitment to a green campus, the administrative services division has started the phased replacement of fossil-fuel vehicles...</p>',
        'featured': False
    },
    {
        'title': 'Infrastructure Update: New Administrative Center Groundbreaking',
        'excerpt': 'The state-of-the-art facility will centralize core services for improved constituent accessibility.',
        'content': '<p>Groundbreaking ceremony was held this morning for the new UP System Administrative Center, marking a milestone in service optimization...</p>',
        'featured': True
    },
]

for i, data in enumerate(news_data):
    NewsArticle.objects.get_or_create(
        title=data['title'],
        defaults={
            'excerpt': data['excerpt'],
            'content': data['content'],
            'published_date': timezone.now() - datetime.timedelta(days=i),
            'is_featured': data['featured'],
            'status': 'published',
            'created_by': admin_user
        }
    )

# 3. Generate Documents
documents_data = [
    {
        'title': 'FY 2026 Strategic Mandate & Performance Framework',
        'category': 'reports',
        'tags': 'strategy, planning, performance',
        'description': 'Comprehensive report detailing the administrative goals and key performance indicators for the fiscal year 2026.'
    },
    {
        'title': 'Travel Reimbursement Form (Revised 2026)',
        'category': 'forms',
        'tags': 'finance, travel, reimbursement',
        'description': 'Official form for all administrative and academic staff travel expense claims.'
    },
    {
        'title': 'University Policy on Data Privacy & IT Security',
        'category': 'policies',
        'tags': 'it, privacy, security',
        'description': 'The unified framework for data protection and information security across all UP System offices.'
    },
    {
        'title': 'Standard Template for Board Resolutions',
        'category': 'templates',
        'tags': 'admin, templates, legal',
        'description': 'The approved layout and formatting for all official board resolutions and executive orders.'
    },
    {
        'title': 'Guidelines for Event Coordination & Campus Safety',
        'category': 'guidelines',
        'tags': 'events, safety, campus',
        'description': 'Standard operating procedures for organizing large-scale events and ensuring campus-wide security protocols.'
    },
]

for data in documents_data:
    Document.objects.get_or_create(
        title=data['title'],
        defaults={
            'category': data['category'],
            'tags': data['tags'],
            'description': data['description'],
            'status': 'published',
            'uploaded_by': admin_user
        }
    )

print(f"Successfully generated {len(issuances_data)} issuances, {len(news_data)} news articles, and {len(documents_data)} documents.")
