import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from cms.models import Page, StaffMember, Event, Project
from django.contrib.auth import get_user_model
User = get_user_model()

def populate():
    print("Starting comprehensive data population from PDF content...")
    admin_user = User.objects.filter(is_superuser=True).first()
    
    # 1. Institutional Pillars (Mission & Vision)
    print("Seeding Institutional Pillars...")
    vision_content = """
    <p>To be a holistic and responsible steward of the University's resources, both human capital and properties, guiding University decisions on people, property, and fiscal operations with social responsibility and strategic insights.</p>
    """
    mission_content = """
    <p>Deliver holistic and responsive services in the development and administration of both human capital and properties. By merging strategic insights with operational excellence, we are committed to fostering a globally competitive human resource environment, optimizing the property and supply management, and ensuring financial resilience. Our goal is to enrich the work and life experiences of the University's stakeholders, driving forward the essence of social responsibility, accountability, and strategic stewardship in every endeavor.</p>
    """
    
    Page.objects.update_or_create(
        slug='vision',
        defaults={'title': 'Vision', 'content': vision_content, 'status': 'published', 'created_by': admin_user}
    )
    Page.objects.update_or_create(
        slug='mission',
        defaults={'title': 'Mission', 'content': mission_content, 'status': 'published', 'created_by': admin_user}
    )

    # 2. About Us / Office Overview (Comprehensive)
    print("Seeding Expanded Office Overview and Goals...")
    about_content = """
    <h3>Historical Overview</h3>
    <p>The Office of the Vice President for Administration (OVPA) was created at the 789th meeting of the Board of Regents (BOR) held on 25 November 1969, when the Board approved the reorganization of the central administration of the University. This was the first of a series of reorganization proposals pursuant to the authority granted by the Board of Regents to the President "to make a thorough study of the operations, organizations and structure of the University to enable him to determine the improvements that could be introduced".</p>
    
    <p>The Vice President for Administration is appointed by the Board on recommendation of the President and is directly responsible to the President for administrative operations. Historically, the office has overseen the following divisions:</p>
    <ul>
        <li>Office of Administrative Personnel Services (OAPS)</li>
        <li>Physical Plant Office (PPO)</li>
        <li>Security Division</li>
        <li>Property Division</li>
        <li>Cash Division</li>
        <li>Internal Audit Division</li>
        <li>Accounting Division</li>
    </ul>

    <p>In 1982, the office was briefly converted into an Office of the Vice Chancellor for Administration under UP Diliman, but was restored as a System-level Vice Presidency on December 18, 1989. In 1993, the President's Executive Staff was reorganized to further split administrative and fiscal operations from long-range planning. Finally, on August 26, 1999, the Office of the Vice President for Finance and Administration (OVPFA) was reorganized back to the current Office of the Vice President for Administration (OVPA).</p>

    <h3>Key Functions & Competencies</h3>
    <p>Based on the delegation of authority, the Vice President for Administration has competence over the following areas to support the UP President:</p>
    
    <h4>Human Resource Matters</h4>
    <ul>
        <li>Appointments of regular and contractual administrative personnel.</li>
        <li>Local special detail, study leaves, and study privileges.</li>
        <li>Permissions to teach after office hours or undertake limited practice of profession.</li>
        <li>Authority to undertake local travel and bonding of accountable officers.</li>
    </ul>

    <h4>Financial & Procurement Matters</h4>
    <ul>
        <li>Sign or countersign financial documents such as security bonds, vouchers, and warrants.</li>
        <li>Procurement of common-use supplies and equipment.</li>
        <li>Award of contracts up to Php 3,000,000 for each project.</li>
    </ul>

    <h3>STRATEGIC GOALS & 10-Point Plan</h3>
    <p>The OVPA is committed to a fully transformed and digitalized administrative system through the following strategic goals:</p>

    <h4>Goal 1: Strategic Human Resource Management</h4>
    <p>Targeting the transition of HR systems from transactional to strategic. Includes competency-based HR systems, talent development, and the PRIME-HRM accreditation.</p>
    <ul>
        <li>A. Competency-Based Human Resource Systems</li>
        <li>B. HR Analytics Program</li>
        <li>C. Rationalization of Organizational Structure and Personnel</li>
        <li>D. Employee Compensation, Welfare, and Benefits</li>
    </ul>

    <h4>Goal 2: Digital Transformation</h4>
    <p>Focuses on fully integrated, interoperable digital systems to support HR, financial, and property management through platforms such as PUSO and BULSA.</p>
    <ul>
        <li>E. Database Integration</li>
        <li>F. Re-engineering of Transactions</li>
    </ul>

    <h4>Goal 3: Operational Efficiency in Administrative Services</h4>
    <p>Aims to streamline and professionalize administrative processes through quality assurance, standardized policies, and collaborative governance.</p>
    <ul>
        <li>G. Productivity in the Workplace</li>
        <li>H. Communication Plan</li>
        <li>I. Service Delivery Improvement and Accreditation</li>
        <li>J. Partnerships: Collaboration, Compliance, and Cooperation</li>
    </ul>
    """
    Page.objects.update_or_create(
        slug='about',
        defaults={
            'title': 'About OVPA', 
            'content': about_content, 
            'meta_description': 'History, functions, and strategic goals of the Office of the Vice President for Administration.',
            'status': 'published', 
            'created_by': admin_user
        }
    )

    # 3. Staff Directory (Kept as is)
    print("Re-verifying Staff Directory...")
    # Staff already exists from previous run, but we can re-create to be sure
    StaffMember.objects.all().delete()
    staff_data = [
        ("Augustus C. Resurreccion", "Vice President for Administration", "OVPA", True),
        ("Tiffany Adelaine Tan", "Assistant Vice President for Administration", "OVPA", True),
        ("Richard S. Javier", "Assistant Vice President for Administration / HR Director", "OVPA", True),
        ("Michael P. Lagaya", "Special Assistant to the Vice President", "UP Open University", False),
        ("Rogelio T. Estrada", "Program Development Associate (PDA)", "UP Diliman", False),
        ("Rosalinda J. Tingco", "Program Development Associate (PDA)", "UP Diliman", False),
        ("Leizel P. Lectura", "Program Development Associate (PDA)", "UP Diliman", False),
        ("Jorel A. Manalo", "Program Development Associate (PDA)", "UP Manila", False),
        ("Mona Liza S. Todas", "Project Development Officer IV", "OVPA", False),
        ("Maria Jovie P. Quijano", "Administrative Officer III", "OVPA", False),
        ("Ma. Ailene B. Angeles", "Administrative Assistant V", "OVPA", False),
        ("Ranya Mae O. Balagot", "Supervising Office Associate", "OVPA", False),
        ("Paul Adrian C. Dela Cruz", "Administrative Assistant III", "OVPA", False),
        ("Maeven M. Enciso", "Senior Project Associate", "OVPA", False),
        ("Albert G. Esguerra", "Administrative Assistant III", "OVPA", False),
        ("Charlotte Yvette A. Gutierrez", "Administrative Assistant II", "OVPA", False),
        ("Wojthaila Mhae P. Luis", "Junior Office Associate", "OVPA", False),
        ("Sheena R. Vicente", "Supervising Office Associate", "OVPA", False),
        ("Jasfer M. Jumapao", "Senior Office Associate", "OVPA", False),
        ("Arlene A. Castillo", "Senior Project Officer", "OVPA", False),
        ("Siegfred C. Laborte", "Senior Office Associate", "OVPA", False),
        ("Ronald Lao", "Junior Research Analyst", "OVPA", False),
        ("Ericka Jazz L. Matriz", "Senior Office Aide", "OVPA", False),
    ]
    for idx, (name, pos, unit, is_top) in enumerate(staff_data):
        StaffMember.objects.create(
            name=name, position=pos, unit=unit, is_top_management=is_top,
            display_order=idx, status='published', created_by=admin_user
        )

    # 4. Events & Projects (Kept as is)
    print("Re-verifying Events and Projects...")
    Event.objects.update_or_create(
        title="Let's Talk Workshop: THIS WAY",
        defaults={
            'description': "<p>A workshop on Strengthening Organizational Leadership, Values, and Ethics.</p>",
            'start_datetime': datetime(2026, 4, 22, 9, 0),
            'end_datetime': datetime(2026, 4, 22, 17, 0),
            'location': "Room 301, UP ISSI, E.T. Virata Hall, UP Diliman",
            'event_type': 'workshop', 'status': 'published', 'created_by': admin_user
        }
    )
    Project.objects.update_or_create(
        slug='up-linang-program',
        defaults={
            'title': 'UP LINANG PROGRAM 2024-2026',
            'category': 'special',
            'excerpt': 'A comprehensive professional development program for UP administrative personnel.',
            'content': '<p>The UP LINANG Program is designed to enhance the competencies of administrative staff across all constituent universities, focusing on leadership, digital literacy, and service excellence.</p>',
            'status': 'published', 'created_by': admin_user
        }
    )

    print("Comprehensive data population complete!")

if __name__ == '__main__':
    populate()
