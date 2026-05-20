import re
import json
import os

# ─────────────────────────────────────────
#  LOAD INPUT FILE
# ─────────────────────────────────────────

def load_text(filepath):
    with open(filepath, "r") as f:
        return f.read()


# ─────────────────────────────────────────
#  REGEX PATTERNS
# ─────────────────────────────────────────

# URLs: must start with http:// or https://
URL_PATTERN = r'https?://[^\s]+'

# Phone numbers: international (+1-800-555-0199, +250 788 123 456) or local (0712345678)
PHONE_PATTERN = r'(\+\d{1,3}[-\s]\d{1,4}[-\s]\d{3}[-\s]\d{3,4}|\b0\d{9}\b)'

# All emails
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# ALU-specific emails only — (?:...) means group but don't capture separately
ALU_EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@(?:alueducation\.com|alumni\.alueducation\.com|si\.alueducation\.com|alustudents\.com)'

# Credit cards: 16 digits with spaces/dashes, or 15 digits (Amex)
CARD_PATTERN = r'\b(?:\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}|\d{15})\b'


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
#  SAVE OUTPUT TO JSON
# ─────────────────────────────────────────

def save_output(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\n✅ Results saved to {filepath}")


# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────

def main():
    input_path  = "input/raw-text.txt"
    output_path = "output/sample-output.json"

    print("\n" + "─"*45)
    print("  🔍 ALU Data Extraction & Validation Tool")
    print("─"*45)

    # Load the text
    text = load_text(input_path)

    # Ask user about ALU-only email filter
    choice = input("\n  Extract ALU-specific emails only? (yes/no): ").strip().lower()
    alu_only = choice == "yes"

    # Run all extractions
    urls   = extract_urls(text)
    phones = extract_phones(text)
    emails = extract_emails(text, alu_only=alu_only)
    cards  = extract_cards(text)

    # Display results with masking where needed
    display("URLs", urls)
    display("Phone Numbers", phones, mask_fn=mask_phone)
    display("Emails", emails, mask_fn=mask_email)
    display("Credit Card Numbers", cards, mask_fn=mask_card)

    # Build masked output for JSON
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