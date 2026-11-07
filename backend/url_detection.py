
from urllib.parse import urlparse
import re
import ipaddress


def analyze_url(url):

    if not isinstance(url, str) or not url.strip():
        return {
            "status": "Invalid",
            "risk": "No URL entered",
            "reasons": ["Please enter a URL."]
        }

    url = url.strip()

    # Reject whitespace inside URLs.
    if re.search(r"\s", url):
        return {
            "status": "Invalid",
            "risk": "Invalid URL",
            "reasons": ["The entered URL contains invalid whitespace."]
        }

    # Reject incorrectly written HTTP/HTTPS schemes.
    if re.match(r"^https?/", url, re.IGNORECASE):
        return {
            "status": "Invalid",
            "risk": "Invalid URL",
            "reasons": ["Invalid URL format. Use http:// or https://."]
        }

    # Add HTTPS when the user enters a domain without a scheme.
    if "://" not in url:
        url = "https://" + url

    try:
        parsed = urlparse(url)

        if parsed.scheme.lower() not in ("http", "https"):
            raise ValueError

        hostname = parsed.hostname

        if not hostname:
            raise ValueError

        # Validate port if one is provided.
        parsed.port

        if any(char in hostname for char in (" ", "/", "\\", "@")):
            raise ValueError

    except ValueError:
        return {
            "status": "Invalid",
            "risk": "Invalid URL",
            "reasons": ["The entered URL is not valid."]
        }

    reasons = []

    # Check whether the URL uses HTTPS.
    if parsed.scheme.lower() != "https":
        reasons.append("URL does not use HTTPS.")

    # Check for an IP address instead of a domain name.
    try:
        ipaddress.ip_address(hostname)
        reasons.append(
            "URL uses an IP address instead of a domain name."
        )
    except ValueError:
        pass

    # Check suspicious keywords.
    suspicious_words = [
        "login", "verify", "banking", "password",
        "account", "secure", "update", "free", "gift"
    ]

    for word in suspicious_words:
        if word in url.lower():
            reasons.append(
                f"Suspicious keyword detected: {word}"
            )

    # Check for @ symbol.
    if "@" in url:
        reasons.append("URL contains an @ symbol.")

    # Check unusually long URLs.
    if len(url) > 100:
        reasons.append("URL is unusually long.")

    # Check excessive subdomains.
    if len(hostname.split(".")) > 4:
        reasons.append("URL contains many subdomains.")

    # Determine risk level.
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
