import csv
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# CONFIGURATION BLOCK (Fill this in)
# ==========================================
SMTP_SERVER = "smtp.gmail.com"  # Outlook uses: smtp.office365.com
SMTP_PORT = 587
SENDER_EMAIL = "scholtzshaun40@gmail.com"  # Put your email address here
SENDER_PASSWORD = "uycp rqfl qbfb hwsa"         # Put your App Password here
# ==========================================

def run_outreach_campaign(leads_csv):
    print("🚀 Initializing ZombieTracker AI Outbound Bot...")
    
    try:
        # Connect to the live email server once at the start
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade connection to secure encryption
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("🔒 Secure connection established to email server.")
    except Exception as e:
        print(f"❌ Initial Connection Failure: {e}")
        print("💡 Hint: Did you remember to generate an App Password instead of using your normal login password?")
        return

    with open(leads_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            name = row['Name']
            company = row['Company']
            target_email = row['Email']
            
            # Crafting the high-converting CFO pitch
            subject = f"SaaS waste audit for {company}"
            body = f"Hi {name},\n\nI noticed {company} has been scaling its team recently. Usually, when mid-market companies grow, forgotten software subscriptions and tool overlaps (like paying for both Slack & Teams) creep onto corporate cards.\n\nWe built an automated metadata parser called ZombieTracker AI. If you drop last month's statement CSV into it, it isolates software bleed and spits out an executive cost-saving report in 0.5 seconds. \n\nIt runs entirely locally in your browser (we never see or store your financial numbers).\n\nWould you be open to running a free, 5-second audit to see where {company} might be leaking cash?\n\nBest regards,\nShaun\nFounder, ZombieTracker AI"
            
            # Assemble email data structure
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = target_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            try:
                # Transmit the message across the web live
                server.sendmail(SENDER_EMAIL, target_email, msg.as_string())
                print(f"📬 Sent: Highly-personalized pitch to {name} @ {company} ({target_email})")
                
                # Dynamic delay to mimic organic typing and protect server reputation
                time.sleep(2) 
            except Exception as e:
                print(f"❌ Failed sending to {target_email}. Error: {e}")
                
    server.quit()
    print("\n🏁 Campaign complete. All outgoing dispatches finalized.")

if __name__ == "__main__":
    run_outreach_campaign('leads.csv')