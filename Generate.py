import imaplib
import email
from email.header import decode_header
import time
import random
import string

# Generate a unique email address
def generate_unique_email():
    unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f'rylecohner+{unique_id}@yandex.com'

# Connect to the Yandex IMAP server and fetch the latest email
def fetch_latest_email(username, password):
    # Connect to the server
    mail = imaplib.IMAP4_SSL("imap.yandex.com")
    # Login to the account
    mail.login(username, password)
    # Select the mailbox you want to check
    mail.select("Social media")
    
    # Search for all emails in the inbox
    status, messages = mail.search(None, "ALL")
    # Get the list of email IDs
    email_ids = messages[0].split()
    
    # Get the latest email ID
    latest_email_id = email_ids[-1]
    
    # Fetch the email by ID
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            return msg

# Extract OTP from the email content
def extract_otp_from_email(msg):
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode()
            # Assuming the OTP is a 6-digit number in the email body
            otp = ''.join(filter(str.isdigit, body))
            if len(otp) == 6:
                return otp
    return None

def main():
    # Replace these with your Yandex email and password
    yandex_email = 'rylecohner@yandex.com'
    yandex_password = 'kirbyisntscared321'
    
    # Generate a unique email address
    generated_email = generate_unique_email()
    print(f"Generated email: {generated_email}")
    
    # Simulate waiting for an OTP email to be sent to the generated email address
    print("Waiting for OTP email...")
    time.sleep(30)  # Wait 30 seconds for the email to arrive
    
    # Fetch the latest email
    msg = fetch_latest_email(yandex_email, yandex_password)
    
    # Extract the OTP from the email
    otp = extract_otp_from_email(msg)
    
    if otp:
        print(f"Received OTP: {otp}")
    else:
        print("No OTP found in the latest email.")

if __name__ == "__main__":
    main()
