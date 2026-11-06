
from backend.url_detection import analyze_url

url = input("Enter a URL to scan: ")

result = analyze_url(url)

print("\n----- PhishGuard Scan Result -----")
print("Status:", result["status"])
print("Risk Level:", result["risk"])
print("Reasons:")

for reason in result["reasons"]:
    print("-", reason)
