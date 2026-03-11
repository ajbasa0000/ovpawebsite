import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from cms.models import Project
from django.utils.text import slugify

def update_sspmo():
    print("Updating SSPMO Projects...")
    
    # Clean up old duplicates if any
    if Project.objects.filter(slug="gamit").count() > 1:
        Project.objects.filter(slug="gamit").first().delete()
    if Project.objects.filter(slug="suplay").count() > 1:
        Project.objects.filter(slug="suplay").first().delete()

    # 1. SPMO Hub
    spmo_hub_title = "SPMO Hub (Central Portal)"
    spmo_hub_excerpt = "The entry point for all users, providing a unified dashboard, global announcements, and seamless navigation to the specialized apps."
    spmo_hub_content = """
    <h2>Core Features</h2>
    <ul>
        <li><strong>Unified SSO Authentication:</strong> Uses Google SSO (via django-allauth) and session sharing to ensure users only log in once.</li>
        <li><strong>Medical Professional Theme:</strong> A clean, trust-inspiring aesthetic (slate/blue/white palette) with SVG medical icon backgrounds to convey a sense of organization and precision.</li>
        <li><strong>News & Announcements Engine:</strong> A dynamic newsfeed with pop-out modals allowing administrators to instantly broadcast updates across the whole university network from a single point.</li>
        <li><strong>Centralized App Launcher:</strong> Secure gateways dropping users seamlessly into GAMIT, SUPLAY, or LIPAD without friction.</li>
    </ul>
    """
    Project.objects.update_or_create(
        slug=slugify("SPMO Hub (Central Portal)"),
        defaults={
            'title': spmo_hub_title,
            'category': 'sspmo',
            'excerpt': spmo_hub_excerpt,
            'content': spmo_hub_content,
            'status': 'published'
        }
    )

    # 2. GAMIT
    gamit_excerpt = "A massive asset tracking and lifecycle management engine handling rigorous COA compliance and multi-stage PAR (Property Acknowledgment Receipt) workflows."
    gamit_content = """
    <h2>Core Features</h2>
    <ul>
        <li><strong>4-Tab Asset Detail System:</strong> Assets are tracked across four strict dimensions:
            <ul>
                <li>Property Details: Identification, barcodes/imagery, location.</li>
                <li>Finance & Valuation: Depreciation tracking (Straight-Line, Declining Balance) and accumulated value.</li>
                <li>Lifecycle: Warranty expiry, insurance value, and disposal methods.</li>
                <li>Government/COA: Fund sourcing, UACS codes, and PPE classification.</li>
            </ul>
        </li>
        <li><strong>Role-Based Access Control:</strong> Highly granular roles (SPMO_ADMIN, ACCT_ADMIN, USER_AO, INSPECTOR, CHIEF, etc.) controlling exactly who can edit which tab of an asset.</li>
        <li><strong>Comprehensive Audit Trail:</strong> The AssetChangeLog meticulously tracks every explicit field change on any asset (who, what, when, IP address).</li>
        <li><strong>Service & Maintenance Logs:</strong> Dedicated logs tracking work done, cost, technician, and subsequent service dates per asset.</li>
    </ul>
    <h2>Key Innovations</h2>
    <ul>
        <li><strong>The 9-State PAR Workflow Engine:</strong> A rigorous state machine for Batch Procurement ranging from "Anticipatory Procurement" to "PAR Released." It prevents sequence jumping, guarantees that inspection only occurs after delivery validation, and requires digital signatures from specific roles at precise gates.</li>
        <li><strong>Automated PDF Generation:</strong> Generates legally binding, digital PARs and Acceptance Reports via ReportLab mapped onto official A4 templates, instantly injecting digital signatures upon chief approval.</li>
    </ul>
    """
    Project.objects.update_or_create(
        slug="gamit",
        defaults={
            'title': "GAMIT (Government Asset Management Inventory Tracking)",
            'category': 'sspmo',
            'excerpt': gamit_excerpt,
            'content': gamit_content,
            'status': 'published'
        }
    )

    # 3. SUPLAY
    suplay_excerpt = "An overarching e-commerce style internal marketplace for office supplies, featuring dynamic inventory mapping, budgeting, and checkout functionality."
    suplay_content = """
    <h2>Core Features</h2>
    <ul>
        <li><strong>Catalog & Marketplace Workflow:</strong> Employees can browse categories, view product stocks, add items to a shopping cart, and perform a streamlined multi-step checkout just like modern consumer apps.</li>
        <li><strong>Order Lead-Time Monitoring:</strong> Tracks specific timestamps (created_at, approved_at, completed_at) internally to allow unit heads to measure the exact SLA turnaround times from request to actual delivery.</li>
        <li><strong>Stock Batch Tracking:</strong> StockBatch allows granular, batch-level recording of received inventories, preventing FIFO/LIFO disruptions and accurately reflecting the exact cost of each delivery iteration.</li>
    </ul>
    <h2>Key Innovations</h2>
    <ul>
        <li><strong>Annual Procurement Plan (APP) Intelligent Tracker:</strong> The suite features an embedded AnnualProcurementPlan mechanism defining what each department requested per month (Jan-Dec). It tracks allocations against a quantity_consumed running total, acting as an automated guardrail to prevent budget overruns dynamically at checkout.</li>
    </ul>
    """
    Project.objects.update_or_create(
        slug="suplay",
        defaults={
            'title': "SUPLAY (Sustainable Supply Utilization, Purchasing, Logistics, Asset and Yield Assessment)",
            'category': 'sspmo',
            'excerpt': suplay_excerpt,
            'content': suplay_content,
            'status': 'published'
        }
    )
    print("SSPMO Projects Updated successfully.")

if __name__ == '__main__':
    update_sspmo()
