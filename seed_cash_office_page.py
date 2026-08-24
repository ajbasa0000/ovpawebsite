import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from cms.models import CashOfficePage

def seed_cash_office_page():
    print("Seeding default Cash Office Page content for CMD...")
    page, created = CashOfficePage.objects.get_or_create(id=1)
    
    page.hero_title = "System Cash Office (SCO)"
    page.hero_subtitle = "Managing financial collections, cash disbursements, Landbank electronic payment processing, and supplier check releases across the University of the Philippines System."
    page.cashier_hours = "Mon - Fri: 8:00 AM - 5:00 PM (No Noon Break)"
    page.office_location = "SFAB Building, Magsaysay rd. cor Agoncillo, UP Diliman Campus, Quezon City"
    page.releasing_phone = "(02) 8981-8500 loc. 2524 / 2525"
    page.voip_extensions = "VOIP: 2618 / 2540"
    page.contact_email = "upsystemcash@up.edu.ph"
    
    page.mandate_title = "Fiscal Governance & Cashiering Excellence"
    page.mandate_content = "<p>The <strong>System Cash Office (SCO)</strong> operates under the direct supervision of the Office of the Vice President for Administration (OVPA). It safeguards University monetary assets, enforces strict treasury governance according to New Government Accounting System (NGAS) and Commission on Audit (COA) standards, and maintains transparent, accessible payment systems for suppliers, personnel, and students across all Constituent Universities (CUs).</p>"
    
    page.bor_history_title = "BOR 1144th Executive Creation & Institutional Evolution"
    page.bor_history_content = "<p>The UP System Cash Office was officially established at the <strong>1144th Meeting of the Board of Regents (BOR) on 31 August 2000</strong> via Executive Order, becoming operational on May 5, 2001. Previously serviced by the UP Diliman Cash Office, the creation of a dedicated System Cash Office addressed the growing volume of System-wide transactions. Today, SCO operates out of the <strong>SFAB Building (Old School of Statistics), Magsaysay Ave. cor. A. Agoncillo St.</strong>, maintaining regular cash management reporting on Cash Receipts, Cash Disbursements, and Investments submitted to COA, OVPPF, DBM, and the UP President.</p>"
    
    page.citizens_charter_summary = "<p>In accordance with the official <strong>UP System Citizen's Charter</strong>, SCO maintains a strict continuous counter service from <strong>8:00 AM to 5:00 PM (No Noon Break)</strong> with guaranteed fast-track processing targets:</p><div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;'><div style='background: rgba(16,185,129,0.1); border: 1px solid #10b981; padding: 1rem; border-radius: 12px;'><strong style='color: #047857; font-size: 1.1rem;'>Official Collections & OR Issuance</strong><div style='font-size: 1.5rem; font-weight: 800; color: #065f46; margin: 0.25rem 0;'>8 Minutes</div><span style='font-size: 0.85rem; color: #047857;'>Target turnaround under normal circumstances</span></div><div style='background: rgba(2,132,199,0.1); border: 1px solid #0284c7; padding: 1rem; border-radius: 12px;'><strong style='color: #0369a1; font-size: 1.1rem;'>Check & RDA Release</strong><div style='font-size: 1.5rem; font-weight: 800; color: #075985; margin: 0.25rem 0;'>10 Minutes</div><span style='font-size: 0.85rem; color: #0369a1;'>Target turnaround from vault retrieval to release</span></div></div>"
    
    page.rda_process_flow = "<p>Request to Debit Account (RDA) handles electronic bank disbursements via Landbank WeAccess for Payroll, Honoraria, Overload, Reimbursements, and Student Allowances:</p><ol><li><strong>DV Receipt</strong>: DVs received from System Accounting Office (UPSAO).</li><li><strong>Data Audit & Encoding</strong>: SCO Staff verifies payee name, bank account number, amount, and fund code, then encodes into Landbank WeAccess.</li><li><strong>Chief Certification</strong>: SCO Chief verifies all encoded data for accuracy and counter-signs.</li><li><strong>VPA Final Executive Approval</strong>: Transmitted to Vice President for Administration for final digital approval and direct bank credit dispatch.</li></ol>"
    
    page.check_process_flow = "<p>Commercial Check Disbursement handles vendor bills, contractor payments, and special cash advances:</p><ol><li><strong>Disbursement Voucher Audit</strong>: SCO checks DVs for valid supporting documents and fund codes.</li><li><strong>Check Printing & Counter-signing</strong>: Commercial check printed, recorded in Check Register, and signed by SCO Chief and VPA.</li><li><strong>Vault Storage</strong>: Check deposited into Cashier Vault pending release.</li><li><strong>Window 2 Release</strong>: Claimant presents BIR Official Receipt/Sales Invoice and 2 valid IDs at Window 2 for check release.</li></ol>"
    
    page.receivable_process_flow = "<p>Collection of official university revenues, grants, rental payments, and administrative fees:</p><ol><li><strong>Order of Payment</strong>: Payee presents Order of Payment from issuing university unit.</li><li><strong>Remittance & Verification</strong>: Cashier verifies documents and receives payment (cash, check, or electronic transfer).</li><li><strong>Official Receipt Issuance</strong>: Official Receipt (OR) issued in 5 minutes and collections deposited daily to authorized government depository bank.</li></ol>"

    page.window_1_desc = "Official Receipt issuance for student tuition, transcript fees, administrative clearances, dorm deposits, and general collections."
    page.window_2_desc = "Disbursement checks and Advice to Debit Account (ADA) notices for suppliers, contractors, and corporate vendors."
    page.window_3_desc = "Faculty & staff payroll checks, overload honoraria, research stipends, and student assistant allowances."
    page.window_4_desc = "Official travel cash advances, project fund liquidations, petty cash replenishment, and emergency advances."
    page.claiming_guidelines = "<p>To ensure smooth verification and prevent authorization delays, please bring mandatory documents when claiming your check at <strong>Window 2, Cash Office</strong>:</p><ul><li><strong>1. Original BIR Official Receipt / Sales Invoice</strong>: BIR-registered Official Receipt matching the DV amount.</li><li><strong>2. Two (2) Valid Government IDs</strong>: Passport, Driver's License, UMID, PRC ID, or Company ID with photo and signature.</li><li><strong>3. Special Power of Attorney (SPA) / Authorization Letter</strong>: Required if a representative is claiming on behalf of the supplier or payee, accompanied by valid IDs of both payee and representative.</li></ul>"
    page.status = "published"
    page.save()
    
    print("Successfully seeded Cash Office Page Content (ID=1) with official SCO files data!")

if __name__ == '__main__':
    seed_cash_office_page()
