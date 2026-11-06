
from backend.database import save_scan, get_scan_history

save_scan(
    "https://google.com",
    "Low",
    ["No suspicious patterns detected."]
)

print("\n----- SCAN HISTORY -----")

records = get_scan_history()

for record in records:
    print(record)
