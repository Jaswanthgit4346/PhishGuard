
from backend.email_detection import analyze_email

email_text = """
URGENT ACTION REQUIRED!

Your bank account has been suspended.
Verify your account immediately.
Click here: http://example.com/verify-account
"""

result = analyze_email(email_text)

print("EMAIL ANALYSIS RESULT")
print("---------------------")
print("Status:", result["status"])
print("Risk Level:", result["risk"])

print("\nDetection Reasons:")
for reason in result["reasons"]:
    print("-", reason)
