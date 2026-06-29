import csv
import re

# 1. The target dictionary of common corporate SaaS keywords
SAAS_DICT = {
    'slack': 'Slack (Team Chat)',
    'adobe': 'Adobe Creative Cloud (Design)',
    'zoom': 'Zoom (Video Calls)',
    'salesforce': 'Salesforce (CRM)',
    'hubspot': 'HubSpot (Marketing/Sales)',
    'canva': 'Canva Pro (Design)',
    'monday.com': 'Monday.com (Project Management)',
    'github': 'GitHub (Development)',
    'microsoft *365': 'Microsoft 365 (Office Tools)',
    'google *gsuite': 'Google Workspace (Email/Drive)',
    'aws': 'Amazon Web Services (Hosting)',
    'figma': 'Figma (Design/UI)'
}

def scan_expenses(csv_file_path):
    total_saas_spend = 0.0
    detected_items = []
    
    print("🤖 Starting Zombie Tracker Scan...\n")
    
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        # Assumes a standard business CSV with headers like: Date, Description, Amount
        reader = csv.DictReader(file)
        
        for row in reader:
            # Standardize text for easy matching
            description = row['Description'].lower()
            amount = float(row['Amount'].replace('£', '').replace(',', '').strip())
            
            # Check description against our dictionary
            for keyword, clean_name in SAAS_DICT.items():
                if re.search(keyword, description):
                    total_saas_spend += amount
                    detected_items.append({
                        'date': row['Date'],
                        'name': clean_name,
                        'amount': amount
                    })
                    break # Stop checking other keywords for this line
                    
    # 2. Generate the instant Audit Report
    print("=" * 45)
    print("       🔴 ZOMBIE TRACKER AUDIT REPORT       ")
    print("=" * 45)
    print(f"Total Software Spend Detected: £{total_saas_spend:,.2f}\n")
    print("Flagged Subscriptions To Review:")
    print("-" * 45)
    
    for item in detected_items:
        print(f"📅 {item['date']} | 🛠️ {item['name']:<30} | 💸 £{item['amount']:.2f}")
    
    print("=" * 45)
    print("💡 Next Step: Cross-reference these with active staff accounts to kill the waste.")

# Run the scanner
# scan_expenses('mock_statement.csv')