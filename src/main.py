import re
import json
from file_handler import load_text
from input_validator import get_alu_choice
from output_handler import save_output

# ─────────────────────────────────────────
#  REGEX PATTERNS
# ─────────────────────────────────────────

# ─────────────────────────────────────────
#  REGEX PATTERNS
# ─────────────────────────────────────────

# URL pattern:
# https?:// — matches http:// or https:// (the ? makes the 's' optional)
# [^\s]+    — matches everything after until a space is hit
# This ensures we only grab proper web URLs, not things like ftp:// or plain text
URL_PATTERN = r'https?://[^\s]+'

# Phone pattern:
# \+\d{1,3}      — international code starting with + (e.g. +250, +1, +44)
# [-\s]\d{1,4}   — area code separated by dash or space
# [-\s]\d{3}     — first digit group
# [-\s]\d{3,4}   — second digit group
# |\b0\d{9}\b    — OR a local number starting with 0 followed by 9 digits (e.g. 0712345678)
# The | separates two valid phone formats so both are matched
PHONE_PATTERN = r'(\+\d{1,3}[-\s]\d{1,4}[-\s]\d{3}[-\s]\d{3,4}|\b0\d{9}\b)'

# General email pattern:
# [a-zA-Z0-9._%+-]+ — local part before @ (letters, numbers, dots, underscores, etc.)
# @                  — literal @ symbol
# [a-zA-Z0-9.-]+    — domain name (e.g. gmail, alueducation)
# \.[a-zA-Z]{2,}    — dot followed by at least 2 letter extension (e.g. .com, .io)
# This covers all standard email formats
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# ALU-specific email pattern:
# Same local part as above but domain is restricted to known ALU domains only
# (?:...) is a non-capturing group — groups the options without returning them separately
# The | separates each valid ALU domain so any one of them can match
ALU_EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@(?:alueducation\.com|alumni\.alueducation\.com|si\.alueducation\.com|alustudents\.com)'

# Credit card pattern:
# \b                         — word boundary so we don't grab numbers mid-sentence
# \d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4} — 16 digits in groups of 4 (spaces or dashes optional)
# |                          — OR
# \d{15}                     — 15 digits with no separator (Amex format)
# \b                         — closing word boundary
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