import os
import django
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from cms.models import ClaimableCheck

def seed_cash_office_data():
    print("Seeding System Cash Office Claimable Checks with PIN security...")
    
    sample_checks = [
        {
            'payee_name': 'Acme Office & Scientific Equipment Solutions Inc.',
            'voucher_number': 'DV-2026-08-0194',
            'check_number': '000482910',
            'amount': Decimal('148500.00'),
            'check_date': date.today() - timedelta(days=2),
            'claim_status': 'ready',
            'pin_code': '123456',
            'claiming_requirements': '1. BIR Official Receipt / Sales Invoice\n2. 2 Valid Government IDs\n3. Secretary Certificate (for Corporate Payee)',
            'remarks': 'Check is ready at Window 2. Please request for OR before release.',
            'status': 'published'
        },
        {
            'payee_name': 'Metro Manila Digital Technology Services Co.',
            'voucher_number': 'DV-2026-08-0205',
            'check_number': '000482911',
            'amount': Decimal('435200.50'),
            'check_date': date.today() - timedelta(days=1),
            'claim_status': 'ready',
            'pin_code': '888999',
            'claiming_requirements': '1. Official Receipt / Collection Receipt\n2. Company ID & Valid Gov ID of authorized bearer\n3. SPA / Authorization Letter',
            'remarks': 'Ready for pick-up between 8:00 AM - 3:30 PM.',
            'status': 'published'
        },
        {
            'payee_name': 'Dr. Ramon Maria Santos (Honoraria & Expert Services)',
            'voucher_number': 'DV-2026-08-0182',
            'check_number': '000482898',
            'amount': Decimal('28500.00'),
            'check_date': date.today() - timedelta(days=5),
            'claim_status': 'ready',
            'pin_code': '555123',
            'claiming_requirements': '1. Two (2) Valid Government IDs (PRC / Passport / Driver\'s License)\n2. Signed Voucher Claim Slip',
            'remarks': 'Individual payee honorarium check.',
            'status': 'published'
        },
        {
            'payee_name': 'Filipino Construction & General Builders Corp.',
            'voucher_number': 'DV-2026-08-0210',
            'check_number': None,
            'amount': Decimal('1250000.00'),
            'check_date': date.today(),
            'claim_status': 'processing',
            'pin_code': '654321',
            'claiming_requirements': '1. Progress Billing Clearance\n2. Official Receipt\n3. BIR Form 2307 receipt acknowledgment',
            'remarks': 'Under accounting audit review. Expected release in 2 business days.',
            'status': 'published'
        },
        {
            'payee_name': 'Luzon Laboratory Supplies & Chemicals Provider',
            'voucher_number': 'DV-2026-07-0891',
            'check_number': '000481005',
            'amount': Decimal('89400.00'),
            'check_date': date.today() - timedelta(days=20),
            'claim_status': 'released',
            'pin_code': '999000',
            'date_released': date.today() - timedelta(days=15),
            'claiming_requirements': 'Claimed by Mr. Jose Cruz (Sales Representative) with OR #88491.',
            'remarks': 'Claimed and acknowledged on file.',
            'status': 'published'
        },
        {
            'payee_name': 'Quezon City Paper & Printing Press',
            'voucher_number': 'DV-2026-08-0222',
            'check_number': '000482915',
            'amount': Decimal('54100.00'),
            'check_date': date.today() - timedelta(days=3),
            'claim_status': 'ready',
            'pin_code': '111222',
            'claiming_requirements': '1. Official Receipt\n2. Two (2) Valid IDs',
            'remarks': 'Available at Cashier Counter 1.',
            'status': 'published'
        },
        {
            'payee_name': 'UP Alumni Association - System Event Logistics Grant',
            'voucher_number': 'DV-2026-08-0150',
            'check_number': '000482850',
            'amount': Decimal('75000.00'),
            'check_date': date.today() - timedelta(days=10),
            'claim_status': 'released',
            'pin_code': '333444',
            'date_released': date.today() - timedelta(days=8),
            'claiming_requirements': 'Claimed by UPAA Secretariat.',
            'remarks': 'Released.',
            'status': 'published'
        }
    ]

    count = 0
    for item in sample_checks:
        obj, created = ClaimableCheck.objects.get_or_create(
            voucher_number=item['voucher_number'],
            defaults=item
        )
        if not created:
            for k, v in item.items():
                setattr(obj, k, v)
            obj.save()
            print(f"Updated PIN and details for {obj.payee_name} - DV #{obj.voucher_number} (PIN: {obj.pin_code})")
        else:
            count += 1
            print(f"Created check for {obj.payee_name} - DV #{obj.voucher_number} (PIN: {obj.pin_code})")
            
    print(f"Successfully updated/seeded claimable check PIN records!")

if __name__ == '__main__':
    seed_cash_office_data()
