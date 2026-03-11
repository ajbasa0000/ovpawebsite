import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from cms.models import Project, ProjectImage
from django.conf import settings
import shutil

def seed_images():
    print("Seeding project images...")
    
    # Get the OVPA Dashboard project
    project = Project.objects.filter(slug='ovpa-dashboard').first()
    if not project:
        print("Project 'ovpa-dashboard' not found.")
        return
        
    print(f"Found project: {project.title}")
    
    # We will copy existing media files to use as dummy gallery images
    # Let's find some images in the media directory
    media_root = settings.MEDIA_ROOT
    gallery_dir = os.path.join(media_root, 'projects', 'gallery')
    os.makedirs(gallery_dir, exist_ok=True)
    
    # Find any existing images in media to copy
    source_images = []
    for root, dirs, files in os.walk(media_root):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                source_path = os.path.join(root, file)
                # Don't use images already in the gallery dir to avoid infinite loop of copies
                if 'gallery' not in source_path:
                    source_images.append(source_path)
                    if len(source_images) >= 4:
                        break
        if len(source_images) >= 4:
            break
            
    if not source_images:
        print("No source images found in media to use as placeholders.")
        return
        
    # Clear existing gallery for this project
    project.images.all().delete()
    print("Cleared existing images for the project.")
    
    # Create 4 images for the project
    for i, source_path in enumerate(source_images[:4]):
        filename = os.path.basename(source_path)
        dest_filename = f"sample_gallery_{i}_{filename}"
        dest_path = os.path.join(gallery_dir, dest_filename)
        
        # Copy file
        shutil.copy2(source_path, dest_path)
        
        # Create DB record
        with open(dest_path, 'rb') as f:
            django_file = File(f, name=dest_filename)
            pi = ProjectImage(
                project=project,
                caption=f"Sample screenshot {i+1} demonstrating the feature.",
            )
            pi.image.save(dest_filename, django_file, save=True)
            print(f"Created image {i+1}: {dest_filename}")
            
    print(f"Successfully seeded {project.images.count()} images for {project.title}.")

if __name__ == '__main__':
    seed_images()
