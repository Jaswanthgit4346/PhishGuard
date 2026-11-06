
import csv
import os
from datetime import datetime

from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from backend.database import (
    get_scan_history,
    get_email_scan_history
)


# --------------------------------------------------
# GET COMBINED RECORDS FROM EXISTING MYSQL DATABASE
# --------------------------------------------------

def convert_row(row, scan_type):
    """
    Converts a database row into a common report format.
    Supports both dictionary rows and tuple rows.
    """

    if isinstance(row, dict):
        record_id = row.get("id", row.get("scan_id", ""))
        content = (
            row.get("url")
            or row.get("email_content")
            or row.get("content")
            or ""
        )
        risk = (
            row.get("risk_level")
            or row.get("risk")
            or "Unknown"
        )
        reasons = (
            row.get("reasons")
            or row.get("detection_reasons")
            or ""
        )
        scan_time = (
            row.get("scan_time")
            or row.get("created_at")
            or row.get("timestamp")
            or ""
        )

    else:
        values = list(row)

        record_id = values[0] if len(values) > 0 else ""
        content = values[1] if len(values) > 1 else ""
        risk = values[2] if len(values) > 2 else "Unknown"
        reasons = values[3] if len(values) > 3 else ""
        scan_time = values[4] if len(values) > 4 else ""

    return {
        "type": scan_type,
        "id": record_id,
        "content": str(content),
        "risk": str(risk),
        "reasons": str(reasons),
        "time": str(scan_time)
    }


def get_combined_scan_records():
    """Fetch URL and email scan records from MySQL."""

    records = []

    url_records = get_scan_history()
    email_records = get_email_scan_history()

    for row in url_records:
        records.append(convert_row(row, "URL"))

    for row in email_records:
        records.append(convert_row(row, "Email"))

    records.sort(
        key=lambda item: item["time"],
        reverse=True
    )

    return records


def get_report_statistics(records):
    """Calculate report statistics from the combined records."""

    stats = {
        "total": len(records),
        "low": 0,
        "medium": 0,
        "high": 0
    }

    for record in records:
        risk = record["risk"].lower()

        if "low" in risk:
            stats["low"] += 1
        elif "medium" in risk:
            stats["medium"] += 1
        elif "high" in risk:
            stats["high"] += 1

    return stats


# --------------------------------------------------
# CSV REPORT
# --------------------------------------------------

def generate_csv_report(file_path):

    try:
        records = get_combined_scan_records()
        stats = get_report_statistics(records)

        with open(
            file_path,
            mode="w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(["PHISHGUARD - SCAN REPORT"])
            writer.writerow([
                "Generated On",
                datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            ])

            writer.writerow([])
            writer.writerow(["SCAN SUMMARY"])
            writer.writerow(["Total Scans", stats["total"]])
            writer.writerow(["Low Risk", stats["low"]])
            writer.writerow(["Medium Risk", stats["medium"]])
            writer.writerow(["High Risk", stats["high"]])

            writer.writerow([])
            writer.writerow(["SCAN DETAILS"])

            writer.writerow([
                "Type",
                "Scan ID",
                "URL / Email Content",
                "Risk Level",
                "Detection Reasons",
                "Scan Time"
            ])

            for record in records:
                writer.writerow([
                    record["type"],
                    record["id"],
                    record["content"],
                    record["risk"],
                    record["reasons"],
                    record["time"]
                ])

        return True

    except Exception as error:
        print("CSV Report Error:", error)
        return False


# --------------------------------------------------
# PDF REPORT
# --------------------------------------------------

def generate_pdf_report(file_path):

    try:
        records = get_combined_scan_records()
        stats = get_report_statistics(records)

        document = SimpleDocTemplate(
            file_path,
            pagesize=landscape(A4),
            rightMargin=12 * mm,
            leftMargin=12 * mm,
            topMargin=12 * mm,
            bottomMargin=12 * mm
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontSize=22,
            textColor=colors.HexColor("#0B1120"),
            alignment=TA_CENTER,
            spaceAfter=8
        )

        heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=13,
            textColor=colors.HexColor("#087E9B"),
            spaceBefore=12,
            spaceAfter=8
        )

        cell_style = ParagraphStyle(
            "CellStyle",
            parent=styles["Normal"],
            fontSize=7,
            leading=9,
            wordWrap="CJK"
        )

        story = []

        # Title
        story.append(
            Paragraph("PHISHGUARD", title_style)
        )

        story.append(
            Paragraph(
                "Cybersecurity Scan Report",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 8))

        generated_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        story.append(
            Paragraph(
                f"<b>Generated On:</b> {generated_time}",
                styles["Normal"]
            )
        )

        # Summary
        story.append(
            Paragraph("Scan Summary", heading_style)
        )

        summary_data = [
            ["Total Scans", "Low Risk", "Medium Risk", "High Risk"],
            [
                str(stats["total"]),
                str(stats["low"]),
                str(stats["medium"]),
                str(stats["high"])
            ]
        ]

        summary_table = Table(
            summary_data,
            colWidths=[55 * mm] * 4
        )

        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#172238")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, 1),
             colors.HexColor("#E8F1F8")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8)
        ]))

        story.append(summary_table)

        # Detailed records
        story.append(
            Paragraph("Detailed Scan History", heading_style)
        )

        table_data = [[
            "Type",
            "ID",
            "URL / Email Content",
            "Risk",
            "Detection Reasons",
            "Scan Time"
        ]]

        for record in records:

            content = record["content"]

            if len(content) > 180:
                content = content[:180] + "..."

            safe_content = escape(content).replace("\n", "<br/>")
            safe_reasons = escape(record["reasons"]).replace(
                "\n", "<br/>"
            )

            table_data.append([
                Paragraph(escape(record["type"]), cell_style),
                Paragraph(escape(str(record["id"])), cell_style),
                Paragraph(safe_content, cell_style),
                Paragraph(escape(record["risk"]), cell_style),
                Paragraph(safe_reasons, cell_style),
                Paragraph(escape(record["time"]), cell_style)
            ])

        if len(table_data) == 1:
            table_data.append([
                Paragraph("No scan records found.", cell_style),
                "", "", "", "", ""
            ])

        details_table = Table(
            table_data,
            colWidths=[
                18 * mm,
                15 * mm,
                65 * mm,
                22 * mm,
                75 * mm,
                35 * mm
            ],
            repeatRows=1
        )

        details_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#172238")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.white,
                colors.HexColor("#F1F5F9")
            ]),
            ("PADDING", (0, 0), (-1, -1), 5)
        ]))

        story.append(details_table)

        # Footer
        def add_footer(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(colors.grey)
            canvas.drawString(
                12 * mm,
                7 * mm,
                "PhishGuard | Cybersecurity Scan Report"
            )
            canvas.drawRightString(
                landscape(A4)[0] - 12 * mm,
                7 * mm,
                f"Page {doc.page}"
            )
            canvas.restoreState()

        document.build(
            story,
            onFirstPage=add_footer,
            onLaterPages=add_footer
        )

        return True

    except Exception as error:
        print("PDF Report Error:", error)
        return False
