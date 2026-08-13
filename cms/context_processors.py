from .models import AdvisoryTicker

def advisory_ticker(request):
    """
    Context processor making active advisory ticker items globally available across all templates.
    """
    advisories = AdvisoryTicker.objects.filter(is_active=True, status='published').order_by('display_order', '-created_at')
    return {
        'active_advisories': advisories
    }
