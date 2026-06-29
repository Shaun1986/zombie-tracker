import streamlit as st
import csv
import re
import io

# 1. Premium Page Configuration (Clean, lightweight deployment)
st.set_page_config(
    page_title="ZombieTracker AI | Enterprise SaaS Audit", 
    page_icon="🛡️", 
    layout="wide"
)

# 2. Comprehensive Global SaaS Target Database
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
    'zapier': {'name': 'Zapier', 'category': 'Workflow Automation'},
    '1password': {'name': '1Password', 'category': 'Security & Passwords'},
    'monday.com': {'name': 'Monday.com', 'category': 'Project Management'}
}

# 3. App Branding Header Layout
st.title("🛡️ ZombieTracker AI")
st.caption("🔒 Bank-grade metadata parsing. No financial account numbers or personal data are stored or transmitted.")
st.write("Drop your operational expense log below to run an instant cost-optimization audit.")

st.markdown("---")

# 4. Dashboard Input Layout Grid
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload Monthly Card Statement (CSV format)", type="csv")

with col2:
    st.subheader("How it works")
    st.write("1. **Upload:** Export statement as CSV from your banking app.")
    st.write("2. **Scan:** Our engine maps descriptions against active vendor signatures.")
    st.write("3. **Optimize:** Instantly review duplicate seats and category spending overlaps.")

# 5. Data Processing and Core Compilation Engine
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

        # 6. Dynamic Financial Output Matrix
        st.markdown("## 📊 Audit Analysis")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="🚨 Identified SaaS Bleed (Monthly)", value=f"£{total_saas_spend:,.2f}")
        with m2:
            st.metric(label="📉 Projected Annual Savings Potential", value=f"£{total_saas_spend * 12:,.2f}")
        with m3:
            total_flags = sum(1 for cat, tools in categories_found.items() if len(tools) > 1)
            st.metric(label="⚠️ High-Risk System Overlaps", value=f"{total_flags} Categories")

        # ---- HTML Printable Report Document Logic ----
        conflicts_list = []
        for category, tools in categories_found.items():
            if len(tools) > 1:
                conflicts_list.append(f"<li><strong>{category}:</strong> Multiple tools active ({', '.join(tools)})</li>")
                
        conflicts_html = "".join(conflicts_list) if conflicts_list else "<li>No overlapping application categories discovered.</li>"
        table_rows = "".join([f"<tr><td>{item['Date']}</td><td>{item['Software Vendor']}</td><td>{item['Category']}</td><td>{item['Amount']}</td></tr>" for item in detected_items])

        printable_html = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>SaaS Optimization Executive Report</title>
            <style>
                body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; margin: 40px; line-height: 1.6; }}
                .header {{ border-bottom: 2px solid #3b82f6; padding-bottom: 20px; margin-bottom: 30px; }}
                .title {{ font-size: 28px; font-weight: bold; color: #111827; }}
                .subtitle {{ font-size: 14px; color: #6b7280; }}
                .metrics {{ display: table; width: 100%; margin-bottom: 30px; border-collapse: separate; border-spacing: 15px 0; }}
                .metric-card {{ display: table-cell; background: #f3f4f6; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; width: 33%; }}
                .metric-label {{ font-size: 12px; text-transform: uppercase; color: #6b7280; font-weight: bold; }}
                .metric-value {{ font-size: 22px; font-weight: bold; color: #ef4444; margin-top: 5px; }}
                .section {{ margin-bottom: 30px; }}
                h2 {{ font-size: 18px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px; color: #1f2937; }}
                ul {{ padding-left: 20px; color: #b91c1c; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                th, td {{ border: 1px solid #e5e7eb; padding: 10px; text-align: left; font-size: 13px; }}
                th {{ background-color: #f9fafb; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">🛡️ ZombieTracker AI</div>
                <div class="subtitle">SaaS Cost-Optimization Executive Report</div>
            </div>
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-label">Identified SaaS Bleed (Monthly)</div>
                    <div class="metric-value">£{total_saas_spend:,.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Projected Annual Savings</div>
                    <div class="metric-value" style="color: #10b981;">£{total_saas_spend * 12:,.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Redundant Categories</div>
                    <div class="metric-value">{total_flags}</div>
                </div>
            </div>
            <div class="section">
                <h2>🚨 Critical Software Overlaps & Waste</h2>
                <ul>{conflicts_html}</ul>
            </div>
            <div class="section">
                <h2>🧾 Itemized Audit Trail</h2>
                <table>
                    <thead><tr><th>Date</th><th>Software Vendor</th><th>Category</th><th>Amount</th></tr></thead>
                    <tbody>{table_rows}</tbody>
                </table>
            </div>
        </body>
        </html>
        """

        st.download_button(
            label="📥 Download Executive PDF/Print Report",
            data=printable_html,
            file_name="ZombieTracker_Executive_Audit.html",
            mime="text/html"
        )

        st.markdown("---")

        left_col, right_col = st.columns([1, 1])
        with left_col:
            st.subheader("🔍 Redundant Software Waste")
            if conflicts_list:
                for category, tools in categories_found.items():
                    if len(tools) > 1:
                        st.error(f"**{category} Friction Detected**\n\nYour organization is multi-paying for: {' vs '.join([f'`{t}`' for t in tools])}.")
            else:
                st.success("🎯 Optimization Matrix Clear: No overlapping application categories discovered.")

        with right_col:
            st.subheader("🧾 Itemized Audit Trail")
            if detected_items:
                st.dataframe(detected_items, use_container_width=True)
            else:
                st.info("No SaaS vendor footprints matched in this transaction log segment.")
                
        st.markdown("---")
        st.success("🔒 Local session scan complete.")
    except Exception as e:
        st.error(f"⚡ Processing Exception: {e}")