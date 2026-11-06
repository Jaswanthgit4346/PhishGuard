
import re
from urllib.parse import urlparse


def analyze_email(email_text):

    email_text = email_text.strip()

    if not email_text:
        return {
            "status": "Invalid",
            "risk": "Invalid Email",
            "reasons": ["Please enter email content."]
        }

    reasons = []
    text = email_text.lower()

    suspicious_words = [
        "verify your account",
        "urgent action",
        "password",
        "bank account",
        "click here",
        "claim your prize",
        "account suspended",
        "confirm your identity",
        "limited time",
        "immediately"
    ]

    for word in suspicious_words:
        if word in text:
            reasons.append(f"Suspicious phrase detected: {word}")

    urls = re.findall(r'https?://[^\s<>"\']+', email_text)

    for url in urls:
        parsed = urlparse(url)

        if parsed.scheme != "https":
            reasons.append(
                "Email contains a link that does not use HTTPS."
            )

        hostname = parsed.hostname or ""

        if hostname.count(".") >= 3:
            reasons.append(
                "Email contains a link with many subdomains."
            )

    urgency_words = [
        "urgent",
        "immediately",
        "act now",
        "within 24 hours"
    ]

    if any(word in text for word in urgency_words):
        reasons.append(
            "Email uses urgent or pressuring language."
        )

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
