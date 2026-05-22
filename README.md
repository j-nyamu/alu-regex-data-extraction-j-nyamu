# ALU Regex Data Extraction & Secure Validation

A Python command-line tool that scans raw text files and extracts structured data using regular expressions. Built with privacy in mind — sensitive data is masked before display and output.

---

## What it extracts

| Data Type | Example Match |
|---|---|
| URLs | `https://www.alueducation.com` |
| Phone Numbers | `+250 788 123 456`, `0712345678` |
| Emails | `jane.doe@alustudents.com` |
| Credit Card Numbers | `4111 1111 1111 1111` |

---

## Privacy & Masking

Sensitive fields are masked in both terminal output and JSON.
Full values are never stored or displayed in plain text.

| Type | Raw | Masked |
|---|---|---|
| Credit Card | `4111 1111 1111 1111` | `4111 **** **** 1111` |
| Email | `jane.doe@alustudents.com` | `ja***@alustudents.com` |
| Phone | `+250 788 123 456` | `250****456` |

---

## ALU-Specific Email Filter

When prompted, entering `yes` restricts email extraction to ALU formats only:

- `@alueducation.com`
- `@alumni.alueducation.com`
- `@si.alueducation.com`
- `@alustudents.com`

Entering `no` extracts all valid emails from the input file.

---

## Security Considerations

- Sensitive data (cards, emails, phones) is masked before display and before saving to JSON
- Credit card masking follows the PCI-DSS standard — only first 4 and last 4 digits shown
- Malformed and invalid inputs are safely ignored by the regex patterns
- Error handling prevents the program from crashing on missing, empty, or unwritable files

---

## Project Structure

---

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/j-nyamu/alu-regex-data-extraction-j-nyamu.git
cd alu-regex-data-extraction-j-nyamu
```

2. Run the script from the project root:
```bash
python src/main.py
```

3. When prompted, type `yes` to extract ALU emails only, or `no` for all emails.

4. Results are displayed in the terminal and saved to `output/sample-output.json`.

---

## Error Handling

| Scenario | Behaviour |
|---|---|
| `raw-text.txt` is missing | Prints clear error message and exits |
| `raw-text.txt` is empty | Prints clear error message and exits |
| User types something other than yes/no | Re-prompts until valid input is given |
| Output folder is not writable | Prints permission error and exits cleanly |

---

## Requirements

- Python 3.x
- No external libraries needed — uses built-in `re`, `json`, `os`, and `sys` modules