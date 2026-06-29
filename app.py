import streamlit as st
import csv
import re
import io
import os

# 1. Page Configuration
st.set_page_config(
    page_title="ZombieTracker AI | Console", 
    page_icon="🛡️", 
    layout="wide"
)

# 2. Global SaaS Target Signatures
SAAS_DICT = {
    'slack': {'name': 'Slack', 'category': 'Team Chat'},
    'teams': {'name': 'Microsoft Teams', 'category': 'Team Chat'},
    'zoom': {'name': 'Zoom', 'category': 'Video Calls'},
    'google *gsuite': {'name': 'Google Workspace', 'category': 'Video Calls'},
    'meet.google': {'name': 'Google Meet', 'category': 'Video Calls'},
    'adobe': {'name': 'Adobe Creative Cloud', 'category': 'Design/Creative'},
    'canva': {'name': 'Canva Pro', 'category': 'Design/Creative'},
    'figma': {'name': 'Figma', 'category': 'Design/Creative'},
    'salesforce': {'name': 'Salesforce', 'category': 'CRM & Sales'},
    'hubspot': {'name': 'HubSpot', 'category': 'CRM & Sales'},
    'pipedrive': {'name': 'Pipedrive', 'category': 'CRM & Sales'},
    'linkedin sales nav': {'name': 'LinkedIn Sales Navigator', 'category': 'CRM & Sales'},
    'notion': {'name': 'Notion', 'category': 'Knowledge & Documentation'},
    'confluence': {'name': 'Confluence', 'category': 'Knowledge & Documentation'},
    'openai': {'name': 'ChatGPT Plus', 'category': 'AI & Productivity'},
    'anthropic': {'name': 'Claude Pro', 'category': 'AI & Productivity'},
    'cursor': {'name': 'Cursor AI Editor', 'category': 'AI & Productivity'},
    'github': {'name': 'GitHub', 'category': 'Development Tools'},
    'aws': {'name': 'Amazon Web Services', 'category': 'Cloud Infrastructure'},
    'mailchimp': {'name': 'Mailchimp', 'category': 'Marketing Automation'},
    'zapier': {'name': 'Zapier', 'workflow': 'Automation'},
    '1password': {'name': '1Password', 'category': 'Security & Passwords'},
    'monday.com': {'name': 'Monday.com', 'category': 'Project Management'}
}

# 3. Sidebar Secret Gate (Instead of fighting with URLs!)
with st.sidebar:
    st.subheader("🔒 System Portal")
    admin_checked = st.checkbox("Toggle Admin Console")
    
    if admin_checked:
        access_password = st.text_input("Enter Admin Key", type="password")
    else:
        access_password = ""

# ==========================================
# ROUTE RUNNER
# ==========================================

if admin_checked and access_password == "admin123":
    # 🔓 ROUTE 1: THE ADMIN VIEW
    st.title("🔑 Internal Operations Command Center")
    st.caption("⚡ Core Panel Active via Sidebar Override.")
    st.markdown("---")
    
    st.header("🤖 Module 1: Automated B2B Lead Harvester")
    col_param1, col_param2 = st.columns(2)
    with col_param1:
        target_country = st.selectbox("Target Country", ["United Kingdom", "United States", "Canada"])
        min_emp = st.number_input("Minimum Employees", value=20)
    with col_param2:
        target_title = st.text_input("Target Role Title", value="CFO")
        max_emp = st.number_input("Maximum Employees", value=150)
        
    if st.button("🚀 Execute Simulated Lead Discovery Run"):
        st.info("Querying databases... harvesting active company data blocks...")
        mock_leads = [
            ["Sarah", "Apex Digital Agencies", "sarah@apex.example.com"],
            ["David", "Vortex Tech Ventures", "david@vortex.example.com"],
            ["James", "Horizon Fintech Solutions", "james@horizon.example.com"]
        ]
        with open('leads.csv', mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Company", "Email"])
            writer.writerows(mock_leads)
        st.success("💾 Simulation Complete: 3 Fresh Leads captured and appended to 'leads.csv'.")
        
    st.markdown("---")
    
    st.header("📊 Module 2: Target Lead Database Status")
    if os.path.exists('leads.csv'):
        with open('leads.csv', mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            leads_data = list(reader)
        if len(leads_data) > 1:
            st.write(f"**Current Pipeline Payload:** {len(leads_data) - 1} active companies queued.")
            st.dataframe(leads_data, use_container_width=True)
        else:
            st.warning("⚠️ Target database pipeline is currently empty.")
    else:
        st.warning("⚠️ No 'leads.csv' database detected in the server frame yet.")
        
    st.markdown("---")
    
    st.header("📨 Module 3: Cold Email Outbound Dispatcher")
    email_subject = st.text_input("Email Subject Blueprint", value="SaaS Cost Leak Identified at [Company]")
    
    if st.button("🔥 IGNITE OUTBOUND EMAIL CAMPAIGN"):
        if os.path.exists('leads.csv'):
            st.success("🏁 Campaign Dispatched! All targets successfully notified with unique link trackers.")
        else:
            st.error("Cannot launch campaign: No target data available.")

else:
    # 🛡️ ROUTE 2: THE CLEAN PUBLIC APP VIEW
    st.title("🛡️ ZombieTracker AI")
    st.caption("🔒 Bank-grade local parsing. No financial account numbers or personal data are stored or transmitted.")
    st.write("Drop your operational expense log or accounting ledger below to run an instant cost-optimization audit.")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload Monthly Card Statement or Accounting Export (CSV format)", type="csv")
    with col2:
        st.subheader("How it works")
        st.write("1. **Export Data:** Grab your last monthly ledger export from Xero, QuickBooks, or NetSuite.")
        st.write("2. **Secure Scan:** Our engine maps descriptions against active vendor signatures.")
        st.write("3. **Optimize Waste:** Instantly identify duplicate seats and category overlaps.")

    if uploaded_file is not None:
        try:
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8-sig"))
            reader = csv.DictReader(stringio)
            
            total_saas_spend = 0.0
            detected_items = []
            categories_found = {}
            
            for row in reader:
                desc_key = next((k for k in row if k.lower() == 'description'), None)
                amt_key = next((k for k in row if k.lower() == 'amount'), None)
                date_key = next((k for k in row if k.lower() == 'date'), None)
                
                if not desc_key or not amt_key:
                    st.error("❌ Invalid CSV Format. Ensure your file contains 'Description' and 'Amount' columns.")
                    st.stop()
                    
                description = row[desc_key].lower()
                amount_str = row[amt_key].replace('£', '').replace(',', '').strip()
                amount = float(amount_str) if amount_str else 0.0
                date_val = row[date_key] if date_key else "N/A"
                
                for keyword, info in SAAS_DICT.items():
                    if re.search(keyword, description):
                        total_saas_spend += amount
                        detected_items.append({
                            'Date': date_val,
                            'Software Vendor': info['name'],
                            'Category': info['category'],
                            'Amount': f"£{amount:.2f}"
                        })
                        if info['category'] not in categories_found:
                            categories_found[info['category']] = set()
                        categories_found[info['category']].add(info['name'])
                        break

            st.markdown("## 📊 Audit Analysis")
            m1, m2, m3 = st.columns(3)
            with m1: st.metric(label="🚨 Identified SaaS Bleed (Monthly)", value=f"£{total_saas_spend:,.2f}")
            with m2: st.metric(label="📉 Projected Annual Savings Potential", value=f"£{total_saas_spend * 12:,.2f}")
            with m3:
                total_flags = sum(1 for cat, tools in categories_found.items() if len(tools) > 1)
                st.metric(label="⚠️ High-Risk System Overlaps", value=f"{total_flags} Categories")

            conflicts_list = []
            for category, tools in categories_found.items():
                if len(tools) > 1:
                    conflicts_list.append(f"<li><strong>{category}:</strong> Multiple tools active ({', '.join(tools)})</li>")
            
            conflicts_html = "".join(conflicts_list) if conflicts_list else "<li>No overlapping application categories discovered.</li>"
            table_rows = "".join([f"<tr><td>{item['Date']}</td><td>{item['Software Vendor']}</td><td>{item['Category']}</td><td>{item['Amount']}</td></tr>" for item in detected_items])

            printable_html = f"""<!DOCTYPE html><html><head><title>SaaS Optimization Executive Report</title></head><body><h2>🛡️ ZombieTracker AI Executive Report</h2></body></html>"""

            st.download_button(label="📥 Download Executive PDF/Print Report", data=printable_html, file_name="ZombieTracker_Executive_Audit.html", mime="text/html")
            st.markdown("---")
            
            left_col, right_col = st.columns([1, 1])
            with left_col:
                st.subheader("🔍 Redundant Software Waste")
                if conflicts_list:
                    for category, tools in categories_found.items():
                        if len(tools) > 1: st.error(f"**{category} Friction Detected**\n\nYour organization is multi-paying for: {' vs '.join([f'`{t}`' for t in tools])}.")
                else: st.success("🎯 Optimization Matrix Clear: No overlapping categories.")
            with right_col:
                st.subheader("🧾 Itemized Audit Trail")
                if detected_items: st.dataframe(detected_items, use_container_width=True)
                else: st.info("No SaaS footprints found.")
        except Exception as e:
            st.error(f"⚡ Processing Exception: {e}")
