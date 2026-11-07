
import re
from urllib.parse import urlparse


def normalize_email_text(email_text):
    """Normalize common spelling and formatting variations."""

    text = email_text.lower()

    # Correct common bank account spelling variations.
    bank_account_pattern = (
        r"\bbank[\s-]*(?:account|accoutn|accout|acount)\b"
    )

    text = re.sub(
        bank_account_pattern,
        "bank account",
        text
    )

    # Normalize repeated whitespace.
    text = re.sub(r"\s+", " ", text)

    return text


def analyze_email(email_text):
    """Analyze email content and identify suspicious patterns."""

    if not isinstance(email_text, str) or not email_text.strip():
        return {
            "status": "Invalid",
            "risk": "Invalid Email",
            "reasons": ["Please enter valid email content."]
        }

    reasons = []
    text = normalize_email_text(email_text.strip())

    # Common phishing-related phrases.
    suspicious_words = [
        "verify your account",
        "verify your bank account",
        "urgent action",
        "password",
        "bank account",
        "click here",
        "claim your prize",
        "account suspended",
        "confirm your identity",
        "limited time",
        "immediately",
        "update your account",
        "security alert",
        "unusual activity",
        "account will be blocked",
        "payment required",
        "reset your password",
        "avoid suspension"
    ]

    for word in suspicious_words:
        if word in text:
            reason = f"Suspicious phrase detected: {word}"

            if reason not in reasons:
                reasons.append(reason)

    # Extract URLs from the original email.
    urls = re.findall(
        r"""https?://[^\s<>"']+""",
        email_text,
        flags=re.IGNORECASE
    )

    for url in urls:

        url = url.rstrip(".,;:!?)]}")

        try:
            parsed = urlparse(url)

            if not parsed.hostname:
                continue

            if parsed.scheme.lower() != "https":
                reason = (
                    "Email contains a link that does not use HTTPS."
                )

                if reason not in reasons:
                    reasons.append(reason)

            hostname = parsed.hostname.lower()

            if hostname.count(".") >= 3:
                reason = (
                    "Email contains a link with many subdomains."
                )

                if reason not in reasons:
                    reasons.append(reason)

        except ValueError:
            reason = "Email contains a potentially invalid URL."

            if reason not in reasons:
                reasons.append(reason)

    # Detect urgency and pressure tactics.
    urgency_patterns = [
        r"\burgent\b",
        r"\bimmediately\b",
        r"\bact now\b",
        r"\bwithin 24 hours\b",
        r"\bright away\b",
        r"\bwithout delay\b"
    ]

    if any(re.search(pattern, text) for pattern in urgency_patterns):
        reasons.append(
            "Email uses urgent or pressuring language."
        )

    # Calculate risk level.
    if len(reasons) >= 3:
        risk = "High"
    elif len(reasons) >= 1:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "status": "Analyzed",
        "risk": risk,
        "reasons": reasons if reasons else [
            "No suspicious patterns detected."
        ]
    }
