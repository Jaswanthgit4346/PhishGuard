
from urllib.parse import urlparse
import re
import ipaddress


def analyze_url(url):

    url = url.strip()

    if not url:
        return {
            "status": "Invalid",
            "risk": "No URL entered",
            "reasons": ["Please enter a URL."]
        }

    # Add https:// if the user does not enter a scheme
    if "://" not in url:
        url = "https://" + url

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname

        if not hostname:
            raise ValueError

    except ValueError:
        return {
            "status": "Invalid",
            "risk": "Invalid URL",
            "reasons": ["The entered URL is not valid."]
        }

    reasons = []

    # Check whether the URL uses HTTPS
    if parsed.scheme != "https":
        reasons.append("URL does not use HTTPS.")

    # Check for IP address instead of domain name
    try:
        ipaddress.ip_address(hostname)
        reasons.append("URL uses an IP address instead of a domain name.")
    except ValueError:
        pass

    # Check suspicious keywords
    suspicious_words = [
        "login", "verify", "banking", "password",
        "account", "secure", "update", "free", "gift"
    ]

    for word in suspicious_words:
        if word in url.lower():
            reasons.append(f"Suspicious keyword detected: {word}")
    # Check for @ symbol
    if "@" in url:
        reasons.append("URL contains an @ symbol.")

    # Check unusually long URLs
    if len(url) > 100:
        reasons.append("URL is unusually long.")

    # Check excessive subdomains
    if len(hostname.split(".")) > 4:
        reasons.append("URL contains many subdomains.")

    # Determine risk level
    if len(reasons) >= 3:
        risk = "High"
    elif len(reasons) >= 1:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "status": "Analyzed",
        "risk": risk,
        "reasons": reasons if reasons else ["No suspicious patterns detected."]
    }
