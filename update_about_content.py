import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from cms.models import Page

def update_about_page():
    content = """
    <h3>Institutional Pillars</h3>
    <div style="margin-bottom: 3rem;">
        <h4 style="color: var(--color-maroon-primary);">VISION</h4>
        <p>To be a holistic and responsible steward of the University's resources, both human capital and properties, guiding University decisions on people, property, and fiscal operations with social responsibility and strategic insights.</p>
        
        <h4 style="color: var(--color-maroon-primary);">MISSION</h4>
        <p>Deliver holistic and responsive services in the development and administration of both human capital and properties. By merging strategic insights with operational excellence, we are committed to fostering a globally competitive human resource environment, optimizing the property and supply management, and ensuring financial resilience. Our goal is to enrich the work and life experiences of the University's stakeholders, driving forward the essence of social responsibility, accountability, and strategic stewardship in every endeavor.</p>
        
        <h4 style="color: var(--color-maroon-primary);">MANDATE</h4>
        <p>The Office of the Vice President for Administration (OVPA) is mandated to provide strategic leadership and administrative support to the University of the Philippines System in the areas of human resource management, property and supply management, and administrative policy formulation.</p>
        
        <h4 style="color: var(--color-maroon-primary);">CORE VALUES</h4>
        <p>Transparency, Integrity, Excellence, and Accountability.</p>
    </div>

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

    <h3>Committees & Support</h3>
    <p>Coordination and support for the following committees, as authorized or approved by the President:</p>
    
    <h4>UP System Fiscal Policies and Operations Committee (SFPOC)</h4>
    <p>The Vice President for Administration chairs and coordinates the System Fiscal Policies and Operations Committee (SFPOC), with the Vice President for Planning & Finance as Co-Chair. The SFPOC has the following functions:</p>
    <ul>
        <li>Review proposals on administrative and financial policy matters including incentives, honoraria, trust accounts, and investments from the various Constituent Universities (CUs) and units, for appropriate action and recommendations.</li>
        <li>Propose improvements, formulate, review and recommend innovations in operational procedures and guidelines for standardized implementation throughout the UP System.</li>
        <li>Address COA concerns in audit reports.</li>
        <li>Implementation and monitoring of administrative and financial policies.</li>
        <li>Propose improvements in system-wide policies and sharing of best practices in building administration, utilities management, procurement and related services.</li>
        <li>Formulate policies for the management, deployment, inventory, maintenance and security of university property and equipment.</li>
    </ul>

    <ul>
        <li><strong>UP System Personnel Committee (SPC):</strong> To discuss concerns/matters and policies with/of the CU HRDOs and come up with proposals or solutions.</li>
        <li><strong>UP System Disposal Committee:</strong> Responsible for disposal of non-serviceable equipment and supplies, as required by the Commission on Audit (COA).</li>
        <li><strong>UP System Human Resource Merit Promotion and Selection Board:</strong> Formerly known as Administrative Personnel Committee (SAPC), as an advisory body to the President on merit selection for administrative staff.</li>
        <li><strong>UP System Human Resource Development Committee (HRDC):</strong> Formerly Administrative Development Fund (ADF) Committee, to evaluate requests from UP System administrative staff to attend conferences, meetings and skills development courses.</li>
        <li><strong>Enhanced Hospitalization Programme (eHoPe) Committee:</strong> Evaluates requests for financial assistance for hospitalization expenses (up to PhP80,000 + PhP10,000 for medicines).</li>
        <li><strong>Union Management Consultative Body (UMCB) & Monitoring Committee (UMMC):</strong> Addressing concerns and grievances related to Collective Negotiation Agreements (CNAs) with AUPWU and AUPAEU.</li>
        <li><strong>SALN Review Committee:</strong> Evaluates SALN forms of UP System employees for proper accomplishment.</li>
        <li><strong>Ad Hoc Committees and Technical Working Groups (TWGs):</strong> Authorized and approved by the President.</li>
    </ul>

    <h3>Coordination & Other Services</h3>
    
    <h4>Security, Safety, Peace and Order</h4>
    <ul>
        <li>Coordinate with the UP Diliman Chancellor and other University officials in the formulation and implementation of policies for security, safety, peace and order with respect to UP System Offices.</li>
        <li>Supervise the building administrators of UP System Administration Buildings.</li>
        <li>Coordinate to advise the UP President on the suspension and resumption of work in UP System offices due to typhoons and other reasons.</li>
    </ul>

    <h4>Other Administrative Services</h4>
    <ul>
        <li><strong>UP Provident Fund:</strong> The Vice President for Administration serves as the ex-officio Vice-Chair of the Board of Trustees of the UP Provident Fund, Inc.</li>
        <li><strong>Communication Service Providers:</strong> Authorized to transact, negotiate and sign contracts; serve as contact person for after-sales dealings.</li>
        <li><strong>Transparency Seal:</strong> Maintenance and compliance with ARTA, PhilGEPS posting of APP, and requirements under the PBB.</li>
        <li>Support for special events and strategic initiatives; and perform other functions assigned by the President.</li>
    </ul>

    <h3>STRATEGIC GOALS & 10–Point Plan</h3>
    <p>OVPA is committed to a fully transformed and digitalized administrative system through the following strategic goals:</p>
    
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
    
    about_page, created = Page.objects.get_or_create(slug='about', defaults={'title': 'About OVPA', 'status': 'published'})
    about_page.content = content
    about_page.save()
    print(f"Updated 'About' page. Created: {created}")

if __name__ == "__main__":
    update_about_page()
