import re
import json
from file_handler import load_text
from input_validator import get_alu_choice
from output_handler import save_output

# ─────────────────────────────────────────
#  REGEX PATTERNS
# ─────────────────────────────────────────

URL_PATTERN   = r'https?://[^\s]+'
PHONE_PATTERN = r'(\+\d{1,3}[-\s]\d{1,4}[-\s]\d{3}[-\s]\d{3,4}|\b0\d{9}\b)'
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
ALU_EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@(?:alueducation\.com|alumni\.alueducation\.com|si\.alueducation\.com|alustudents\.com)'
CARD_PATTERN  = r'\b(?:\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}|\d{15})\b'


# ─────────────────────────────────────────
#  EXTRACTION FUNCTIONS
# ─────────────────────────────────────────

def extract_urls(text):
    return re.findall(URL_PATTERN, text)

def extract_phones(text):
    matches = re.findall(PHONE_PATTERN, text)
    return [m for m in matches if len(re.sub(r'\D', '', m)) >= 7]

def extract_emails(text, alu_only=False):
    pattern = ALU_EMAIL_PATTERN if alu_only else EMAIL_PATTERN
    return re.findall(pattern, text)

def extract_cards(text):
    return re.findall(CARD_PATTERN, text)


# ─────────────────────────────────────────
#  PRIVACY MASKING
# ─────────────────────────────────────────

def mask_card(card):
    digits = re.sub(r'\D', '', card)
    return digits[:4] + ' **** **** ' + digits[-4:]

def mask_email(email):
    local, domain = email.split('@')
    return local[:2] + '***@' + domain

def mask_phone(phone):
    digits = re.sub(r'\D', '', phone)
    return digits[:3] + '****' + digits[-3:]


# ─────────────────────────────────────────
#  DISPLAY RESULTS
# ─────────────────────────────────────────

def display(label, items, mask_fn=None):
    print(f"\n{'='*45}")
    print(f"  📌 {label} ({len(items)} found)")
    print(f"{'='*45}")
    if not items:
        print("  ⚠️  None found.")
    for item in items:
        displayed = mask_fn(item) if mask_fn else item
        print(f"  → {displayed}")


# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────

def main():
    input_path  = "input/raw-text.txt"
    output_path = "output/sample-output.json"

    print("\n" + "─"*45)
    print("  🔍 ALU Data Extraction & Validation Tool")
    print("─"*45)

    text     = load_text(input_path)
    alu_only = get_alu_choice()

    urls   = extract_urls(text)
    phones = extract_phones(text)
    emails = extract_emails(text, alu_only=alu_only)
    cards  = extract_cards(text)

    display("URLs", urls)
    display("Phone Numbers", phones, mask_fn=mask_phone)
    display("Emails", emails, mask_fn=mask_email)
    display("Credit Card Numbers", cards, mask_fn=mask_card)

    output_data = {
        "alu_only_filter": alu_only,
        "urls": urls,
        "phone_numbers": [mask_phone(p) for p in phones],
        "emails": [mask_email(e) for e in emails],
        "credit_cards": [mask_card(c) for c in cards]
    }

    save_output(output_data, output_path)
    print("\n  Done! 🎉\n")


if __name__ == "__main__":
    main()