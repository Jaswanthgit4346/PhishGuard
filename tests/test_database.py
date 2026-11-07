
from backend.database import get_scan_history, get_dashboard_stats


def test_database_connection_and_history():
    print("\n----- DATABASE READ-ONLY TEST -----")

    records = get_scan_history()

    print("Database history retrieval successful.")
    print("Existing URL scan records:", len(records))

    print("\n----- DASHBOARD STATISTICS -----")

    stats = get_dashboard_stats()

    print("Total Scans:", stats["total"])
    print("Low Risk:", stats["low"])
    print("Medium Risk:", stats["medium"])
    print("High Risk:", stats["high"])

    assert isinstance(records, list)
    assert isinstance(stats, dict)
    assert stats["total"] >= 0

    print("\nDatabase read-only test completed successfully.")


if __name__ == "__main__":
    test_database_connection_and_history()
