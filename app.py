import streamlit as st
import csv
import re
import io

# 1. Premium Page Configuration
st.set_page_config(
    page_title="ZombieTracker AI | Enterprise SaaS Audit", 
    page_icon="🛡️", 
    layout="wide"
)

# 2. Complete Robust Visual Style Overrides (High-Contrast Dark Theme)
st.markdown("""
    <style>
    /* Global Background and Typography */
    .main { background-color: #0e1117 !important; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background-color: #0e1117 !important; 
        color: #ffffff !important; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* Make typography elements highly visible */
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    .stMarkdown p, li, span { color: #e5e7eb !important; }
    small, .stCaption { color: #9ca3af !important; }
    
    /* Premium File Uploader Adjustments */
    div[data-testid="stFileUploader"] label p { color: #ffffff !important; font-weight: 700; font-size: 18px; }
    div[data-testid="stFileUploaderDropzone"] { background-color: #1f2937 !important; border: 2px dashed #4b5563 !important; border-radius: 10px; }
    div[data-testid="stFileUploaderDropzone"] span { color: #ffffff !important; }
    div[data-testid="stFileUploaderDropzone"] small { color: #9ca3af !important; }
    
    /* Force Download Buttons to have dark text over light backgrounds so they are readable */
    button[data-testid="stBaseButton-secondary"] { 
        background-color: #3b82f6 !important; 
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
    }
    button[data-testid="stBaseButton-secondary"] p { 
        color: #ffffff !important; 
        font-weight: 700 !important; 
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #2563eb !important;
    }
    
    /* Metric Cards High Contrast Visibility Overrides */
    .stMetric { background-color: #1f2937 !important; padding: 22px !important; border-radius: 12px !important; border: 1px solid #374151 !important; }
    
    /* Target labels directly and force to white */
    div[data-testid="metric-container"] label, 
    div[data-testid="stMetricLabel"] p, 
    div[data-testid="stMetricLabel"] span { 
        color: #ffffff !important; 
        font-size: 14px !important; 
        font-weight: 700 !important; 
        text-transform: uppercase !important; 
    }
    
    /* Target primary large financial numbers and force to white */
    div[data-testid="metric-container"] div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] div { 
        color: #ffffff !important; 
        font-weight: 800 !important; 
        font-size: 32px !important; 
    }
    
    /* Data Tables Configuration */
    div[data-testid="stDataFrame"] { background-color: #111827 !important; border-radius: 8px; border: 1px solid #374151; padding: 5px; }
    </style>
""", unsafe_allow_html=True)

# 3. Comprehensive Global SaaS Target Database
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

# 4. App Branding Header Layout
st.markdown("# 🛡️ ZombieTracker <span style='color:#3b82f6; font-size:24px;'>AI</span>", unsafe_allow_html=True)
st.caption("🔒 Bank-grade metadata parsing. No financial account numbers or personal data are stored or transmitted.")
st.write("Drop your operational expense log below to run an instant cost-optimization audit.")

st.markdown("---")

# 5. Dashboard Input Layout Grid
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload Monthly Card Statement (CSV format)", type="csv")

with col2:
    st.markdown("""
    ### How it works
    1. **Upload:** Export statement as CSV from your banking app.
    2. **Scan:** Our engine maps descriptions against active vendor signatures.
    3. **Optimize:** Instantly review duplicate seats and category spending overlaps.
    """)

# 6. Data Processing and Core Compilation Engine
if uploaded_file is not None:
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8-sig"))
    reader = csv.DictReader(stringio)
    
    total_saas_spend = 0.0
    detected_items = []
    categories_found = {}
    
    for row in reader:
        description = row['Description'].lower()
        amount = float(row['Amount'].replace('£', '').replace(',', '').strip())
        
        for keyword, info in SAAS_DICT.items():
            if re.search(keyword, description):
                total_saas_spend += amount
                detected_items.append({
                    'Date': row['Date'],
                    'Software Vendor': info['name'],
                    'Category': info['category'],
                    'Amount': f"£{amount:.2f}"
                })
                
                if info['category'] not in categories_found:
                    categories_found[info['category']] = set()
                categories_found[info['category']].add(info['name'])
                break

    # 7. Dynamic Financial Output Matrix
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
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #ffffff; margin: 40px; line-height: 1.6; }}
            .header {{ border-bottom: 2px solid #3b82f6; padding-bottom: 20px; margin-bottom: 30px; }}
            .title {{ font-size: 28px; font-weight: bold; color: #111827; }}
            .subtitle {{ font-size: 14px; color: #ffffff; }}
            .metrics {{ display: table; width: 100%; margin-bottom: 30px; border-collapse: separate; border-spacing: 15px 0; }}
            .metric-card {{ display: table-cell; background: #f3f4f6; padding: 20px; border-radius: 8px; border: 1px solid #ffffff; width: 33%; }}
            .metric-label {{ font-size: 12px; text-transform: uppercase; color: #6b7280; font-weight: bold; }}
            .metric-value {{ font-size: 22px; font-weight: bold; color: #ef4444; margin-top: 5px; }}
            .section {{ margin-bottom: 30px; }}
            h2 {{ font-size: 18px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px; color: #1f2937; }}
            ul {{ padding-left: 20px; color: #b91c1c; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th, td {{ border: 1px solid #e5e7eb; padding: 10px; text-align: left; font-size: 13px; }}
            th {{ background-color: #f9fafb; font-weight: bold; }}
            .footer {{ margin-top: 50px; font-size: 11px; color: #9ca3af; text-align: center; border-top: 1px solid #e5e7eb; padding-top: 20px; }}
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
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Software Vendor</th>
                        <th>Category</th>
                        <th>Amount</th>
                    </tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
    </body>
    </html>
    """

    # Upgraded, highly visible brand button
    st.download_button(
        label="📥 Download Executive PDF/Print Report",
        data=printable_html,
        file_name="ZombieTracker_Executive_Audit.html",
        mime="text/html"
    )

    st.markdown("---")

    # 8. Split View Layout: Actionable System Alerts vs Itemized Log Data
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        st.subheader("🔍 Redundant Software Waste")
        conflicts_found = False
        for category, tools in categories_found.items():
            if len(tools) > 1:
                conflicts_found = True
                tool_list = " vs ".join([f"`{t}`" for t in tools])
                st.error(f"**{category} Friction Detected**\n\nYour organization is multi-paying for: {tool_list}.")
                st.caption("💡 *Consolidation Strategy:* Migrating teams to a single standard platform slashes administrative overhead by an estimated 35%.")
                
        if not conflicts_found:
            st.success("🎯 Optimization Matrix Clear: No overlapping application categories discovered.")

    with right_col:
        st.subheader("🧾 Itemized Audit Trail")
        st.dataframe(detected_items, use_container_width=True)
        
    st.markdown("---")
    st.success("🔒 Local session scan complete. Clear browser data or upload a new file to reset the compiler pipeline.")