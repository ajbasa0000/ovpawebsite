import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from cms.models import Page

def seed_quality_policy_page():
    content = """
    <!-- Hero Banner -->
    <div style="background: linear-gradient(135deg, var(--color-maroon-dark) 0%, var(--color-maroon-primary) 100%); color: white; border-radius: 12px; padding: 3rem 2rem; margin-bottom: 3rem; text-align: center; box-shadow: 0 10px 25px rgba(123, 17, 19, 0.15);">
        <h2 style="color: #F8D677; font-size: 2.2rem; margin-top: 0; margin-bottom: 1rem; font-weight: 700; letter-spacing: -0.5px;">UP System Administration Quality Policy</h2>
        <p style="font-size: 1.15rem; max-width: 850px; margin: 0 auto 1.5rem; line-height: 1.8; opacity: 0.95;">
            The UP System Administration (UPSA) strives to provide academic, administrative, and technical support services to its stakeholders. UPSA is committed to creating and sustaining a culture of providing quality service in all its processes aligned with the fulfillment of the UP's vision, mission, and mandate, and conforming to ISO 9001 and other international standards.
        </p>
        <div style="display: inline-flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.15); padding: 8px 18px; border-radius: 30px; font-size: 0.95rem; border: 1px solid rgba(255,255,255,0.2);">
            <i class="fas fa-certificate" style="color: #F8D677;"></i>
            <span>Signed by <strong>Angelo A. Jimenez</strong>, UP President</span>
        </div>
    </div>

    <!-- 7 Operational Drivers Section -->
    <div style="margin-bottom: 4rem;">
        <div style="text-align: center; margin-bottom: 2.5rem;">
            <h3 style="color: var(--color-maroon-primary); font-size: 1.8rem; margin-bottom: 0.5rem;">The 7 Operational Drivers</h3>
            <p style="color: #6B7280; margin: 0;">Guided by the principles of <em>"Honor and Excellence in the Service of the Nation"</em></p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;">
            <div style="background: var(--color-bg-light, #F9FAFB); border-left: 4px solid #D97706; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem;">
                    <span style="background: #FEF3C7; color: #D97706; font-weight: 700; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem;">01</span>
                    <h4 style="margin: 0; color: var(--color-text-main); font-size: 1.1rem;">Stakeholder Engagement</h4>
                </div>
                <p style="margin: 0; font-size: 0.98rem; color: #4B5563; line-height: 1.6;">Actively engage stakeholders such as UPSA personnel, suppliers, community, and others through democratic consultation.</p>
            </div>

            <div style="background: var(--color-bg-light, #F9FAFB); border-left: 4px solid #DC2626; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem;">
                    <span style="background: #FEE2E2; color: #DC2626; font-weight: 700; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem;">02</span>
                    <h4 style="margin: 0; color: var(--color-text-main); font-size: 1.1rem;">Exceed Expectations</h4>
                </div>
                <p style="margin: 0; font-size: 0.98rem; color: #4B5563; line-height: 1.6;">Consistently meet the needs and expectations of all university stakeholders.</p>
            </div>

            <div style="background: var(--color-bg-light, #F9FAFB); border-left: 4px solid #7C3AED; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem;">
                    <span style="background: #EDE9FE; color: #7C3AED; font-weight: 700; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem;">03</span>
                    <h4 style="margin: 0; color: var(--color-text-main); font-size: 1.1rem;">Regulatory Compliance</h4>
                </div>
                <p style="margin: 0; font-size: 0.98rem; color: #4B5563; line-height: 1.6;">Strictly comply with statutory and regulatory requirements of relevant oversight agencies consistent with the UP Charter.</p>
            </div>

            <div style="background: var(--color-bg-light, #F9FAFB); border-left: 4px solid #2563EB; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem;">
                    <span style="background: #DBEAFE; color: #2563EB; font-weight: 700; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem;">04</span>
                    <h4 style="margin: 0; color: var(--color-text-main); font-size: 1.1rem;">Knowledge & Innovation</h4>
                </div>
                <p style="margin: 0; font-size: 0.98rem; color: #4B5563; line-height: 1.6;">Innovate and develop tools, mechanisms, and methods for knowledge creation and effective information dissemination.</p>
            </div>

            <div style="background: var(--color-bg-light, #F9FAFB); border-left: 4px solid #059669; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem;">
                    <span style="background: #D1FAE5; color: #059669; font-weight: 700; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem;">05</span>
                    <h4 style="margin: 0; color: var(--color-text-main); font-size: 1.1rem;">Enabling Environment</h4>
                </div>
                <p style="margin: 0; font-size: 0.98rem; color: #4B5563; line-height: 1.6;">Foster an enriching environment to promote academic, research, and public service activities.</p>
            </div>

            <div style="background: var(--color-bg-light, #F9FAFB); border-left: 4px solid #0284C7; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem;">
                    <span style="background: #E0F2FE; color: #0284C7; font-weight: 700; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem;">06</span>
                    <h4 style="margin: 0; color: var(--color-text-main); font-size: 1.1rem;">Resource Optimization</h4>
                </div>
                <p style="margin: 0; font-size: 0.98rem; color: #4B5563; line-height: 1.6;">Optimal utilization of UPSA resources to provide initiatives for constituent and autonomous units contributing to national development.</p>
            </div>

            <div style="background: var(--color-bg-light, #F9FAFB); border-left: 4px solid #16A34A; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem;">
                    <span style="background: #DCFCE7; color: #16A34A; font-weight: 700; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem;">07</span>
                    <h4 style="margin: 0; color: var(--color-text-main); font-size: 1.1rem;">SDG Alignment</h4>
                </div>
                <p style="margin: 0; font-size: 0.98rem; color: #4B5563; line-height: 1.6;">Strategically align policies on research, innovation, learning, and infrastructure with the UN Sustainable Development Goals (SDGs).</p>
            </div>
        </div>
    </div>

    <!-- Kalinangan Values Guide Section -->
    <div style="margin-bottom: 4rem;">
        <div style="text-align: center; margin-bottom: 2.5rem;">
            <span style="background: #FFFBEB; color: #B45309; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">OVPA Culture Guide</span>
            <h3 style="color: var(--color-maroon-primary); font-size: 2rem; margin-top: 0.5rem; margin-bottom: 0.5rem;">Kalinangán: Values in Practice</h3>
            <p style="color: #6B7280; max-width: 650px; margin: 0 auto;">A guide for OVPA personnel to embody, practice, and cultivate UP's core values in daily operations.</p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 2rem;">
            <!-- Honor Card -->
            <div style="border: 1px solid #E5E7EB; border-radius: 12px; overflow: hidden; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="background: var(--color-maroon-primary); color: white; padding: 1.5rem; text-align: center;">
                    <h4 style="margin: 0; font-size: 1.6rem; color: #F8D677; font-weight: 700; letter-spacing: 1px;">HONOR (DANGAL)</h4>
                    <p style="margin: 0.5rem 0 0; font-size: 0.95rem; opacity: 0.9;">Empathic • Trustworthy • Respectful • Professional • Patient • Honest • Adaptable</p>
                </div>
                <div style="padding: 1.5rem;">
                    <ul style="padding-left: 1.2rem; margin: 0; color: #374151; font-size: 0.98rem; line-height: 1.8;">
                        <li><strong>Warm Greetings:</strong> Greet clients and personnel with a smile ("Happy Morning/Afternoon!").</li>
                        <li><strong>Prompt Phone Conduct:</strong> Answer calls on or before the 2nd ring with a cheerful greeting and office identification.</li>
                        <li><strong>Filipino Courtesy:</strong> Show active gratitude and consistently use <em>"po"</em> and <em>"opo"</em>.</li>
                        <li><strong>Respectful Communication:</strong> Communicate with clarity, respect, and tone control across all written and verbal forms.</li>
                        <li><strong>Standard Compliance:</strong> Adhere to CSC office attire (MC No. 19, s. 2000) and maintain a 100% smoke-free workplace.</li>
                        <li><strong>Professional Conflict Resolution:</strong> Engage in open, private dialogue for conflict resolution, seeking supervisor mediation when required.</li>
                    </ul>
                </div>
            </div>

            <!-- Excellence Card -->
            <div style="border: 1px solid #E5E7EB; border-radius: 12px; overflow: hidden; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="background: #064E3B; color: white; padding: 1.5rem; text-align: center;">
                    <h4 style="margin: 0; font-size: 1.6rem; color: #A7F3D0; font-weight: 700; letter-spacing: 1px;">EXCELLENCE (HUSAY)</h4>
                    <p style="margin: 0.5rem 0 0; font-size: 0.95rem; opacity: 0.9;">Proactive • Future-Thinker • Quality Compliant • Continuous Learning</p>
                </div>
                <div style="padding: 1.5rem;">
                    <ul style="padding-left: 1.2rem; margin: 0; color: #374151; font-size: 0.98rem; line-height: 1.8;">
                        <li><strong>Citizen's Charter Alignment:</strong> Adhere strictly to the UP Citizen's Charter and Quality Management System Manual.</li>
                        <li><strong>Completed Staff Work (CSW):</strong> Practice CSW by identifying issues clearly, providing concise context, analyzing data-driven alternatives, and recommending actionable solutions.</li>
                        <li><strong>Urgency & Responsiveness:</strong> Prioritize urgent tasks, meet deadlines, and reply within <strong>2 hours</strong> when asked for progress updates.</li>
                        <li><strong>Safe Space for Innovation:</strong> Evaluate all employee suggestions constructively to encourage innovation without immediate dismissal.</li>
                        <li><strong>Growth & Mentorship:</strong> Maintain an Individual Development Plan (IDP) and participate in peer-to-peer unit mentoring.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Official Signed Documents Artifact Gallery -->
    <div style="margin-top: 4rem; padding-top: 3rem; border-top: 1px solid #E5E7EB;">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: var(--color-maroon-primary); font-size: 1.75rem; margin-bottom: 0.5rem;">Official Signed Policy & Value Charters</h3>
            <p style="color: #6B7280; margin: 0;">Click on any official poster below to view the signed high-resolution charter.</p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.25rem;">
            <div style="border-radius: 8px; overflow: hidden; border: 1px solid #E5E7EB; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center; background: #FAFAFA;">
                <a href="/media/quality_values/9c8e7990-79b0-40bb-af33-ff8ba15a4c9d.jpg" target="_blank" style="text-decoration: none; color: inherit;">
                    <img src="/media/quality_values/9c8e7990-79b0-40bb-af33-ff8ba15a4c9d.jpg" alt="UPSA Quality Policy & Operational Drivers" style="width: 100%; height: 220px; object-fit: cover; border-bottom: 1px solid #E5E7EB;">
                    <div style="padding: 10px; font-weight: 600; font-size: 0.9rem; color: var(--color-maroon-primary);">Quality Policy Overview</div>
                </a>
            </div>

            <div style="border-radius: 8px; overflow: hidden; border: 1px solid #E5E7EB; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center; background: #FAFAFA;">
                <a href="/media/quality_values/5dc28576-a3e0-4e6b-b565-8cc202db5ae7.jpg" target="_blank" style="text-decoration: none; color: inherit;">
                    <img src="/media/quality_values/5dc28576-a3e0-4e6b-b565-8cc202db5ae7.jpg" alt="Signed Quality Policy Document" style="width: 100%; height: 220px; object-fit: cover; border-bottom: 1px solid #E5E7EB;">
                    <div style="padding: 10px; font-weight: 600; font-size: 0.9rem; color: var(--color-maroon-primary);">Signed Policy Statement</div>
                </a>
            </div>

            <div style="border-radius: 8px; overflow: hidden; border: 1px solid #E5E7EB; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center; background: #FAFAFA;">
                <a href="/media/quality_values/5409580d-7115-4667-a53d-5972f25127f7.jpg" target="_blank" style="text-decoration: none; color: inherit;">
                    <img src="/media/quality_values/5409580d-7115-4667-a53d-5972f25127f7.jpg" alt="Kalinangan Honor Charter" style="width: 100%; height: 220px; object-fit: cover; border-bottom: 1px solid #E5E7EB;">
                    <div style="padding: 10px; font-weight: 600; font-size: 0.9rem; color: var(--color-maroon-primary);">Kalinangán: Honor Charter</div>
                </a>
            </div>

            <div style="border-radius: 8px; overflow: hidden; border: 1px solid #E5E7EB; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center; background: #FAFAFA;">
                <a href="/media/quality_values/3f4c7d11-fbd6-4db8-9df6-f65fc55fbf2d.jpg" target="_blank" style="text-decoration: none; color: inherit;">
                    <img src="/media/quality_values/3f4c7d11-fbd6-4db8-9df6-f65fc55fbf2d.jpg" alt="Kalinangan Excellence Charter" style="width: 100%; height: 220px; object-fit: cover; border-bottom: 1px solid #E5E7EB;">
                    <div style="padding: 10px; font-weight: 600; font-size: 0.9rem; color: var(--color-maroon-primary);">Kalinangán: Excellence Charter</div>
                </a>
            </div>
        </div>
    </div>
    """

    page, created = Page.objects.get_or_create(
        slug='quality-policy',
        defaults={
            'title': 'Quality Policy & Kalinangán Values',
            'status': 'published',
            'meta_description': 'UP System Administration Quality Policy, 7 Operational Drivers, and Kalinangán Honor & Excellence Charters.'
        }
    )
    page.title = 'Quality Policy & Kalinangán Values'
    page.content = content
    page.status = 'published'
    page.save()
    print(f"Quality Policy Page updated successfully! Created: {created}")

if __name__ == '__main__':
    seed_quality_policy_page()
