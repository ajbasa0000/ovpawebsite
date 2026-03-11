from django.utils.text import slugify
from cms.models import Service
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

# Delete existing placeholder services
Service.objects.all().delete()

services_data = [
    {
        'category': 'external',
        'type': 'simple',
        'title': 'Issuance of Notice of Award',
        'duration': '20 minutes',
        'description': 'Providing official notifications to individuals or organizations who have been selected as the recipients of awards or contracts, outlining the terms, conditions, and responsibilities associated with the award. This process often involves notifying successful bidders or grant recipients in procurement or grant-related activities.',
        'where': 'Supplies and Property Management Office',
        'who': 'UP System Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Issuance of Travel Authority for Employees',
        'duration': '45 minutes',
        'description': 'This is for employees who are going abroad either for official or personal purpose. Travel Authority is required by the Department of Foreign Affairs from all government employees travelling outside the country',
        'where': 'Client',
        'who': 'UP System Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Processing of Application for Leave',
        'duration': '18 minutes',
        'description': 'An employee who goes on leave needs to file an application for leave/ secure approval of his/her superiors.',
        'where': 'Human Resources Development Office',
        'who': 'UP System Administration Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'complex',
        'title': 'Processing of Application for Special Monetization of Leave Credits',
        'duration': '4 days and 10 minutes',
        'description': 'An employee may file an application for special monetization, subject to approval and availability of funds. Reasons for special monetization include financial assistance for the damages brought about by natural disasters; health, medical and hospital needs; and education expenses, among others.',
        'where': 'Human Resources Development Office',
        'who': 'UP System Administration Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Processing of Application for Regular Monetization of Leave Credits',
        'duration': '20 minutes',
        'description': 'An employee may monetize his/her leave credits, subject to approval and availability of funds.',
        'where': 'Human Resources Development Office',
        'who': 'UP System Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'highly_technical',
        'title': 'Processing of Request for Honorarium',
        'duration': '8 days and 10 minutes',
        'description': 'Some employees perform additional tasks, over and above their regular duties; hence, additional compensation is in order.',
        'where': 'Unit',
        'who': 'UP System Administration Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'highly_technical',
        'title': 'Processing of Application for eHOPE',
        'duration': '14 days and 15 minutes',
        'description': 'Employees are entitled to reimbursement of hospital confinement expenses and medicines after confinement (guidelines based on the BOR approval).',
        'where': 'Client',
        'who': 'UP System Administration Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'highly_technical',
        'title': 'Processing of Request to Attend on Official Time Training Programs/Workshops/ Seminars with Request for Financial Assistance',
        'duration': '8 days, 6 hours and 30 minutes',
        'description': 'Employees are encouraged to participate in/attend relevant seminars, training programs, workshops, seminars and conferences. Financial assistance is extended, subject to evaluation/recommendation of the committee.',
        'where': 'Client',
        'who': 'UP Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Processing of Application for Limited Practice of Profession',
        'duration': '20 minutes',
        'description': 'Before employees practice their profession outside office hours, they must seek approval first.',
        'where': 'Client',
        'who': 'UP System Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'complex',
        'title': 'Processing of Request for Exemption from the President’s Memorandum on the Moratorium in Hiring Contractuals',
        'duration': '3 days, 3 hours and 35 minutes',
        'description': 'Some units lack personnel complement, hence, turn to contractuals or job orders to effectively function. However, a memo from the Office of the President was released to halt hiring of contractuals.',
        'where': 'Office of the University Secretary; System Offices',
        'who': "UP CU's/Units",
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Issuance of Appointment paper',
        'duration': '25 minutes',
        'description': 'The VPA is the signatory of appointment papers of System administrative employees.',
        'where': 'Human Resources Development Office',
        'who': 'UP System Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Issuance of Notice of Salary Adjustment (NOSA) and Notification of Salary Increase (NOSI)',
        'duration': '20 minutes',
        'description': 'Preparation and release of official documents reflecting approved salary adjustments or increases for UP System Administration personnel, in accordance with applicable government issuances.',
        'where': 'Human Resources Development Office',
        'who': 'UP System Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Evaluation of Request for Official Time to Attend Official Functions',
        'duration': '25 minutes',
        'description': 'Approval of the request allows employees to attend the activities on official time.',
        'where': 'Client',
        'who': 'UP System Employees',
        'classification': 'Request for official time'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Evaluation of Application for Reduced Tuition/ Fee',
        'duration': '20 minutes',
        'description': 'Approval of the request allows the employee to avail of reduced tuition/fee.',
        'where': 'Client',
        'who': 'UP System Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Processing of Application for Study Leave',
        'duration': '20 minutes',
        'description': 'An employee has a study leave privilege, subject to approval of superiors.',
        'where': 'Client',
        'who': 'UP System Administrative employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Approval of Terminal Leave Benefits',
        'duration': '2 days and 10 minutes',
        'description': 'This benefit is given to qualified employees who retired, resigned or separated from the service.',
        'where': 'Human Resources Development Office',
        'who': 'UP System Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'highly_technical',
        'title': 'Evaluation of Appeal for Benefits',
        'duration': '10 days, 4 hours and 10 minutes',
        'description': 'An employee who is not covered by a certain benefit may appeal.',
        'where': 'Client',
        'who': 'UP System Employee',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'complex',
        'title': 'Evaluation of Contract',
        'duration': '5 days and 30 minutes',
        'description': 'Before contracts are forwarded to the President and then to the BOR for approval or notation, the OVPA-SSPMO checks the completeness of the requirements.',
        'where': "CU's/Units",
        'who': 'Constituent Universities/Units',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Signing of Disbursement Voucher/ Check/ RADA',
        'duration': '17 minutes',
        'description': 'Payment method',
        'where': 'Cash Office',
        'who': 'UP System Administration Faculty, Administrative Staff and REPS',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Signing of Investment Papers',
        'duration': '15 minutes',
        'description': 'University’s investment documents',
        'where': 'Office of the Vice President for Planning and Finance',
        'who': 'Office of the Vice President for Planning and Finance',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Preparation of Checks for those without an LBP, DBP or Veterans Bank Account',
        'duration': '15 minutes',
        'description': 'Mode of payment is check instead of RADA (for those who do not have accounts at LBP, DBP or Veterans Bank).',
        'where': 'Unit',
        'who': 'UP System Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'complex',
        'title': 'Issuance of Appointment Paper as Disbursing/Collecting Officer',
        'duration': '3 days and 30 minutes',
        'description': 'An employee assigned as Disbursing/Collecting Officer should be given an appointment paper.',
        'where': 'Unit',
        'who': 'UP Permanent Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Issuance of Authority to Drive for Regular Personnel Not Sitting on a Driver Position',
        'duration': '40 minutes',
        'description': 'In the absence of a driver position, the need for a driver to drive an official vehicle may be addressed by giving authority to drive to a regular employee with a professional driver’s license.',
        'where': 'Unit',
        'who': 'UP Permanent Employees',
        'classification': 'G2G'
    },
    {
        'category': 'internal',
        'type': 'simple',
        'title': 'Issuance of Fidelity Bond (New and Renewal)',
        'duration': '30 minutes',
        'description': 'This is a requirement for employees appointed as Special Disbursing Officer',
        'where': 'Unit',
        'who': 'UP Permanent Employees',
        'classification': 'G2G'
    },
]

for i, data in enumerate(services_data):
    Service.objects.create(
        title=data['title'],
        service_category=data['category'],
        transaction_type=data['type'],
        duration=data['duration'],
        description=data['description'],
        where_to_secure=data['where'],
        who_may_avail=data['who'],
        classification=data['classification'],
        display_order=i,
        status='published',
        created_by=admin_user
    )

print(f"Successfully imported {len(services_data)} actual services.")
