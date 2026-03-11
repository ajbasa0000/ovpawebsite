import os
import django
import shutil
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from cms.models import NewsArticle, Event, MediaGallery
from django.contrib.auth import get_user_model
User = get_user_model()

from PIL import Image, ImageDraw

import urllib.request

def create_placeholder_image(path, seed, size=(800, 600)):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Using Picsum for beautiful, varied high-quality photo placeholders
    url = f"https://picsum.photos/seed/ovpa_{seed}/{size[0]}/{size[1]}"
    print(f"Downloading modern placeholder for {path}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        print(f"Download failed ({e}), falling back to modern abstract...")
        from PIL import Image, ImageDraw
        img = Image.new('RGB', size, color=(243, 244, 246)) # Sleek light gray
        draw = ImageDraw.Draw(img)
        img.save(path)

def populate_all():
    print("Clearing old data...")
    NewsArticle.objects.all().delete()
    Event.objects.all().delete()
    MediaGallery.objects.all().delete()
    
    # Ensure media directories exist
    os.makedirs('media/news', exist_ok=True)
    os.makedirs('media/media_gallery', exist_ok=True)
    
    news_data = [
        {
            "title": "UP System Administration Hosts 2026 Strategic Planning Workshop",
            "excerpt": "Key administrative officials gathered to outline the strategic priorities and digital transformation goals for the upcoming academic year.",
            "content": "<p>The Office of the Vice President for Administration recently concluded its annual strategic planning workshop. The event focused on aligning the university's operational capabilities with its long-term academic mission. Digital transformation and process streamlining were identified as core pillars for the 2026-2030 administrative roadmap.</p>",
            "color": (128, 0, 0) # Maroon
        },
        {
            "title": "Launch of the Unified Digital Administration Dashboard",
            "excerpt": "A new centralized portal has been developed to provide university executives with real-time operational metrics across all constituent universities.",
            "content": "<p>In a major leap towards data-driven governance, the OVPA has officially launched the Unified Digital Administration Dashboard. This platform integrates data from HR, procurement, and finance outposts to provide a real-time, comprehensive view of the university's administrative health.</p>",
            "color": (0, 75, 35) # Forest Green
        },
        {
            "title": "Implementation of the Comprehensive Employee Wellness Program",
            "excerpt": "Reflecting the administration's commitment to employee well-being, the new wellness initiative includes health tracking, fitness incentives, and mental health support.",
            "content": "<p>Recognizing the vital role of university staff, the System Human Resources Development Office (SHRDO) has rolled out a new Comprehensive Employee Wellness Program. The initiative provides preventative health resources, mental health counseling, and fitness subsidies to all eligible UP employees.</p>",
            "color": (218, 165, 32) # Gold
        },
        {
            "title": "Electric Vehicle Shuttle Service Begins Trial Operations",
            "excerpt": "As part of the university's sustainability initiative, a fleet of electric shuttles will now service the main administrative areas to reduce carbon emissions.",
            "content": "<p>The System Supply and Property Management Office (SSPMO) has initiated a trial run for the new Electric Vehicle Shuttle Service. Designed to promote environmental sustainability, these locally-assembled EV shuttles will provide zero-emission transport between key administrative buildings.</p>",
            "color": (70, 130, 180) # Steel Blue
        },
        {
            "title": "Groundbreaking Ceremony for the New Administrative Annex",
            "excerpt": "Construction has officially begun on the new annex building, which will house the consolidated records and digital infrastructure teams.",
            "content": "<p>University officials marked the beginning of construction for the new Administrative Annex. This state-of-the-art facility is designed specifically to support the growing digital infrastructure and records management requirements of the UP System.</p>",
            "color": (105, 105, 105) # Dim Gray
        }
    ]
    
    today = datetime.now()
    admin_user = User.objects.filter(is_superuser=True).first()
    
    print("Populating News Articles and Media Gallery with visual placeholders...")
    for idx, data in enumerate(news_data):
        # Create a placeholder image
        filename = f"placeholder_{idx}.png"
        news_img_path = os.path.join('media', 'news', filename)
        gallery_img_path = os.path.join('media', 'media_gallery', filename)
        
        # Pass a unique seed for varied photos
        create_placeholder_image(news_img_path, seed=f"news_{idx}")
        create_placeholder_image(gallery_img_path, seed=f"gallery_{idx}")
            
        NewsArticle.objects.create(
            title=data['title'],
            excerpt=data['excerpt'],
            content=data['content'],
            featured_image=f"news/{filename}",
            published_date=today - timedelta(days=idx*3),
            status='published',
            is_featured=(idx < 2),
            created_by=admin_user
        )

        MediaGallery.objects.create(
            title=f"Gallery: {data['title']}",
            description=f"Administrative showcase image for the recent {data['title']} announcement.",
            image_file=f"media_gallery/{filename}",
            published_date=today - timedelta(days=idx*4),
            status='published',
            created_by=admin_user
        )

    print("Populating Events...")
    events_data = [
        ("System-Wide Operations Conference", "Annual gathering of all administrative heads.", "UP Diliman Campus", 5, 'conference'),
        ("Procurement Guidelines Briefing", "Webinar detailing the new standardized procurement processes.", "Online / Zoom", 12, 'seminar'),
        ("HR Data Privacy Workshop", "Training session on handling employee records.", "Main Admin Building", 15, 'workshop'),
        ("Executive Committee Meeting", "Monthly strategic alignment meeting.", "OVPA Conference Room", 2, 'meeting')
    ]
    
    for title, desc, location, days_ahead, evt_type in events_data:
        event_date = today + timedelta(days=days_ahead)
        Event.objects.create(
            title=title,
            description=f"<p>{desc}</p>",
            start_datetime=event_date.replace(hour=9, minute=0),
            end_datetime=event_date.replace(hour=12, minute=0),
            location=location,
            event_type=evt_type,
            status='published',
            created_by=admin_user
        )

    print("Successfully populated News, Media Gallery, and Events with proper placeholders!")

if __name__ == '__main__':
    populate_all()
