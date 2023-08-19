import argparse
import requests
import time
import json

# Generate a temporary email address from GuerrillaMail
res = requests.get('https://api.guerrillamail.com/ajax.php?f=get_email_address')
email = res.json()['email_addr']
print(f'\033[94mYour default email:\033[0m \033[96m{email}\033[0m')

# Parse command line arguments
parser = argparse.ArgumentParser(description="Send a test email")
parser.add_argument('-n', '--name', required=True, help='Your name')
parser.add_argument('-r', '--recipient', required=True, help='Email recipient')
parser.add_argument('-s', '--subject', required=True, help='Message subject')
parser.add_argument('-m', '--message', required=True, help='Email message body')
parser.add_argument('-e', '--email', default=email, help='Alternative email address')
args = parser.parse_args()
altEmail = args.email

# Set up the email message payload
payload = {
    'sender': {'name': args.name, 'email': altEmail},
    'to': [{'email': args.recipient}],
    'subject': args.subject,
    'htmlContent': args.message
}

# Set up the Sendinblue API endpoint and credentials
api_url = 'https://api.sendinblue.com/v3/smtp/email'
api_key = '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'

# Send the email message
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'api-key': api_key
}

try:
    res = requests.post(api_url, headers=headers, data=json.dumps(payload))
    res.raise_for_status()
    print(f'\033[92mEmail sent from {altEmail} to {payload["to"][0]["email"]} successfully.\033[0m')
except requests.exceptions.HTTPError as e:
    print(f'\033[91mError sending email: {e.response.text}\033[0m')

if not altEmail or altEmail == email:
    time.sleep(5)

    inbox_res = requests.get(f'https://api.guerrillamail.com/ajax.php?f=get_email_list&offset=0&zone=guerrillamail.com&site=guerrillamail.com&inbox_only=1&lang=en&_=1647254886059')
    inbox_emails = inbox_res.json()['list']
    for inbox_email in inbox_emails:
        inbox_email_res = requests.get(f'https://api.guerrillamail.com/ajax.php?f=fetch_email&email_id={inbox_email["mail_id"]}&site=guerrillamail.com&lang=en&_={int(time.time()*1000)}')
        inbox_email_data = inbox_email_res.json()['data']
        if inbox_email_data['mail_from'] == f'Anonymous <{email}>' and inbox_email_data['mail_subject'] == args.subject:
            print(f'\033[92mThe email sent from {email} with subject "{args.subject}" was received.\033[0m')
            break
