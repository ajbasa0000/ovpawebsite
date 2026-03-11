import os
import django
import shutil
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from cms.models import MediaGallery, NewsArticle

def populate_media():
    print("Populating Media Gallery...")
    MediaGallery.objects.all().delete()
    
    # We'll copy some images from existing News Articles to use as dummy media
    articles = NewsArticle.objects.filter(status='published', featured_image__isnull=False)[:5]
    
    media_dir = os.path.join('media', 'media_gallery')
    os.makedirs(media_dir, exist_ok=True)
    
    for i, article in enumerate(articles):
        # Create a new Media Gallery item based on the article
        original_path = article.featured_image.path
        if not os.path.exists(original_path):
            continue
            
        filename = os.path.basename(original_path)
        new_filename = f"gallery_copy_{i}_{filename}"
        new_path = os.path.join(media_dir, new_filename)
        
        try:
            shutil.copy2(original_path, new_path)
            
            MediaGallery.objects.create(
                title=f"Gallery Event: {article.title}",
                description=f"A snapshot from our recent event. {article.excerpt}",
                image_file=f"media_gallery/{new_filename}",
                published_date=article.published_date.date() if article.published_date else datetime.now().date(),
                status='published'
            )
            print(f"Created gallery item for {article.title}")
        except Exception as e:
            print(f"Error copying {filename}: {e}")

if __name__ == '__main__':
    populate_media()
