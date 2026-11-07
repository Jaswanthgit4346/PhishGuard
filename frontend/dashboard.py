
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from backend.url_detection import analyze_url
from backend.email_detection import analyze_email

from backend.database import (
    connect_database,
    save_scan,
    save_email_scan,
    get_scan_history,
    get_email_scan_history,
    get_dashboard_stats,
    delete_scan_history_record,
    clear_scan_history
)

from backend.reports import (
    generate_csv_report,
    generate_pdf_report
)


class PhishGuardApp(tk.Tk):

    # COLORS

    BG = "#0B1120"
    SIDEBAR = "#111A2E"
    CARD = "#172238"
    CARD_HOVER = "#22334D"

    ACCENT = "#00D4FF"
    TEXT = "#F1F5F9"
    MUTED = "#94A3B8"

    GREEN = "#22C55E"
    RED = "#F87171"
    ORANGE = "#FBBF24"

    # HISTORY RISK COLORS

    LOW_BG = "#123326"
    LOW_FG = "#4ADE80"

    MEDIUM_BG = "#3A2D13"
    MEDIUM_FG = "#FBBF24"

    HIGH_BG = "#3B1D25"
    HIGH_FG = "#F87171"

    # INITIALIZATION

    def __init__(self):
        super().__init__()

        self.title("PhishGuard | Cybersecurity Center")
        self.geometry("1350x850")
        self.minsize(1050, 680)

        self.configure(bg=self.BG)

        self.current_page = "Dashboard"

        self.setup_styles()
        self.create_layout()
        self.show_dashboard()

    # STYLES

    def setup_styles(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.CARD,
            foreground=self.TEXT,
            fieldbackground=self.CARD,
            rowheight=38,
            borderwidth=0,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Treeview.Heading",
            background=self.SIDEBAR,
            foreground=self.ACCENT,
            font=("Segoe UI", 9, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", "#164E63")],
            foreground=[("selected", "white")]
        )

        style.configure(
            "TCombobox",
            fieldbackground=self.CARD,
            background=self.CARD,
            foreground=self.TEXT,
            arrowcolor=self.ACCENT
        )

    # MAIN LAYOUT

    def create_layout(self):

        self.sidebar = tk.Frame(
            self,
            bg=self.SIDEBAR,
            width=235
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_area = tk.Frame(
            self,
            bg=self.BG
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()

        self.main_canvas = tk.Canvas(
            self.main_area,
            bg=self.BG,
            highlightthickness=0
        )

        self.main_scrollbar = ttk.Scrollbar(
            self.main_area,
            orient="vertical",
            command=self.main_canvas.yview
        )

        self.main_canvas.configure(
            yscrollcommand=self.main_scrollbar.set
        )

        self.main_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.main_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.content = tk.Frame(
            self.main_canvas,
            bg=self.BG
        )

        self.content_window = self.main_canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.main_canvas.bind(
            "<Configure>",
            self.resize_content
        )

        self.main_canvas.bind(
            "<Enter>",
            lambda event: self.main_canvas.bind_all(
                "<MouseWheel>",
                self.on_mousewheel
            )
        )

        self.main_canvas.bind(
            "<Leave>",
            lambda event: self.main_canvas.unbind_all(
                "<MouseWheel>"
            )
        )

    # SCROLLING

    def update_scroll_region(self, event=None):

        self.main_canvas.configure(
            scrollregion=self.main_canvas.bbox("all")
        )

    def resize_content(self, event):

        self.main_canvas.itemconfigure(
            self.content_window,
            width=event.width
        )

    def on_mousewheel(self, event):

        self.main_canvas.yview_scroll(
            int(-event.delta / 120),
            "units"
        )

    # SIDEBAR

    def create_sidebar(self):

        tk.Label(
            self.sidebar,
            text="🛡 PhishGuard",
            font=("Segoe UI", 20, "bold"),
            bg=self.SIDEBAR,
            fg=self.ACCENT
        ).pack(
            anchor="w",
            padx=22,
            pady=(30, 5)
        )

        tk.Label(
            self.sidebar,
            text="CYBERSECURITY CENTER",
            font=("Segoe UI", 8, "bold"),
            bg=self.SIDEBAR,
            fg=self.MUTED
        ).pack(
            anchor="w",
            padx=24,
            pady=(0, 30)
        )

        menu_items = [
            ("⌂", "Dashboard"),
            ("◎", "URL Scanner"),
            ("✉", "Email Analyzer"),
            ("▤", "Scan History"),
            ("▣", "Reports"),
            ("⚙", "Settings")
        ]

        self.nav_buttons = {}

        for symbol, page in menu_items:

            button = tk.Button(
                self.sidebar,
                text=f"  {symbol}     {page}",
                font=("Segoe UI", 11),
                bg=self.SIDEBAR,
                fg=self.TEXT,
                activebackground=self.CARD_HOVER,
                activeforeground=self.ACCENT,
                anchor="w",
                relief="flat",
                bd=0,
                padx=20,
                pady=14,
                cursor="hand2",
                command=lambda p=page: self.navigate(p)
            )

            button.pack(
                fill="x",
                padx=10,
                pady=3
            )

            self.nav_buttons[page] = button

        tk.Frame(
            self.sidebar,
            bg=self.CARD_HOVER,
            height=1
        ).pack(
            fill="x",
            padx=20,
            pady=25
        )

        tk.Label(
            self.sidebar,
            text="SYSTEM STATUS",
            font=("Segoe UI", 8, "bold"),
            bg=self.SIDEBAR,
            fg=self.MUTED
        ).pack(
            anchor="w",
            padx=24
        )

        tk.Label(
            self.sidebar,
            text="●  Rule-based detection",
            font=("Segoe UI", 9),
            bg=self.SIDEBAR,
            fg=self.GREEN
        ).pack(
            anchor="w",
            padx=24,
            pady=8
        )

        tk.Label(
            self.sidebar,
            text="●  MySQL storage",
            font=("Segoe UI", 9),
            bg=self.SIDEBAR,
            fg=self.GREEN
        ).pack(
            anchor="w",
            padx=24
        )

        tk.Label(
            self.sidebar,
            text="Version 1.0",
            font=("Segoe UI", 9),
            bg=self.SIDEBAR,
            fg=self.MUTED
        ).pack(
            side="bottom",
            anchor="w",
            padx=24,
            pady=20
        )

    # NAVIGATION

    def navigate(self, page):

        self.current_page = page

        for name, button in self.nav_buttons.items():

            if name == page:
                button.configure(
                    bg=self.CARD_HOVER,
                    fg=self.ACCENT
                )

            else:
                button.configure(
                    bg=self.SIDEBAR,
                    fg=self.TEXT
                )

        self.main_canvas.yview_moveto(0)

        pages = {
            "Dashboard": self.show_dashboard,
            "URL Scanner": self.show_url_scanner,
            "Email Analyzer": self.show_email_analyzer,
            "Scan History": self.show_scan_history,
            "Reports": self.show_reports,
            "Settings": self.show_settings
        }

        pages[page]()

    # COMMON UI HELPERS

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def create_header(self, title, subtitle):

        header = tk.Frame(
            self.content,
            bg=self.BG
        )

        header.pack(
            fill="x",
            pady=(0, 25)
        )

        tk.Label(
            header,
            text=title,
            font=("Segoe UI", 25, "bold"),
            bg=self.BG,
            fg=self.TEXT
        ).pack(anchor="w")

        tk.Label(
            header,
            text=subtitle,
            font=("Segoe UI", 10),
            bg=self.BG,
            fg=self.MUTED
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    def create_card(self, parent, title, value, color):

        card = tk.Frame(
            parent,
            bg=self.CARD,
            padx=20,
            pady=20
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7
        )

        tk.Label(
            card,
            text=title.upper(),
            font=("Segoe UI", 9, "bold"),
            bg=self.CARD,
            fg=self.MUTED
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text=str(value),
            font=("Segoe UI", 28, "bold"),
            bg=self.CARD,
            fg=color
        )

        value_label.pack(
            anchor="w",
            pady=(12, 0)
        )

        return value_label

    def create_action_button(self, parent, text, command):

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=self.ACCENT,
            fg="#07111F",
            activebackground="#67E8F9",
            activeforeground="#07111F",
            relief="flat",
            bd=0,
            padx=18,
            pady=11,
            cursor="hand2"
        )

    def create_section_title(self, parent, title):

        tk.Label(
            parent,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg=self.BG,
            fg=self.TEXT
        ).pack(
            anchor="w",
            pady=(18, 12)
        )

    # DASHBOARD

    def show_dashboard(self):

        self.clear_content()

        self.create_header(
            "Security Dashboard",
            "Monitor phishing detection activity and security statistics."
        )

        stats = get_dashboard_stats()

        cards = tk.Frame(
            self.content,
            bg=self.BG
        )

        cards.pack(fill="x", pady=10)

        self.create_card(
            cards, "Total Scans", stats["total"], self.ACCENT
        )

        self.create_card(
            cards, "Low Risk", stats["low"], self.GREEN
        )

        self.create_card(
            cards, "Medium Risk", stats["medium"], self.ORANGE
        )

        self.create_card(
            cards, "High Risk", stats["high"], self.RED
        )

        self.create_section_title(
            self.content,
            "Quick Actions"
        )

        actions = tk.Frame(
            self.content,
            bg=self.BG
        )

        actions.pack(fill="x", pady=5)

        self.create_action_button(
            actions,
            "Scan a URL",
            lambda: self.navigate("URL Scanner")
        ).pack(side="left", padx=(0, 12))

        self.create_action_button(
            actions,
            "Analyze an Email",
            lambda: self.navigate("Email Analyzer")
        ).pack(side="left", padx=12)

        self.create_action_button(
            actions,
            "View History",
            lambda: self.navigate("Scan History")
        ).pack(side="left", padx=12)

        self.create_section_title(
            self.content,
            "Risk Distribution"
        )

        chart_frame = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=20,
            pady=20
        )

        chart_frame.pack(fill="x", pady=5)

        chart = tk.Canvas(
            chart_frame,
            height=190,
            bg=self.CARD,
            highlightthickness=0
        )

        chart.pack(fill="x")

        total = stats["total"]

        if total > 0:

            values = [
                ("Low Risk", stats["low"], self.GREEN),
                ("Medium Risk", stats["medium"], self.ORANGE),
                ("High Risk", stats["high"], self.RED)
            ]

            chart_width = 650

            chart.create_rectangle(
                20, 30,
                20 + chart_width, 65,
                fill="#26364E",
                outline=""
            )

            current_x = 20.0

            for name, value, color in values:

                width = float(chart_width * value / total)

                if width > 0:

                    chart.create_rectangle(
                        current_x, 30,
                        current_x + width, 65,
                        fill=color,
                        outline=""
                    )

                current_x += width

            for index, (name, value, color) in enumerate(values):

                y = 100 + index * 25

                chart.create_oval(
                    22, y,
                    34, y + 12,
                    fill=color,
                    outline=""
                )

                chart.create_text(
                    45, y + 6,
                    text=f"{name}: {value}",
                    anchor="w",
                    fill=self.TEXT,
                    font=("Segoe UI", 10)
                )

        else:

            chart.create_text(
                300, 80,
                text="No scan data available yet",
                fill=self.MUTED,
                font=("Segoe UI", 12)
            )

        self.create_section_title(
            self.content,
            "Recent Activity"
        )

        recent_frame = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=15,
            pady=10
        )

        recent_frame.pack(
            fill="both",
            expand=True
        )

        tree = ttk.Treeview(
            recent_frame,
            columns=("type", "content", "risk", "time"),
            show="headings",
            height=5
        )

        columns = [
            ("type", "TYPE", 100),
            ("content", "URL / EMAIL", 350),
            ("risk", "RISK", 120),
            ("time", "TIME", 180)
        ]

        for col, heading, width in columns:
            tree.heading(col, text=heading)
            tree.column(col, width=width)

        tree.pack(fill="both", expand=True)

        try:

            records = self.get_combined_history()

            for record in records[:5]:

                tree.insert(
                    "",
                    "end",
                    values=(
                        record[0],
                        str(record[2])[:65],
                        record[3],
                        record[5]
                    )
                )

        except Exception as error:

            messagebox.showerror(
                "Dashboard Error",
                str(error)
            )

        self.create_action_button(
            self.content,
            "Refresh Dashboard",
            self.show_dashboard
        ).pack(
            anchor="e",
            pady=15
        )

    # URL SCANNER

    def show_url_scanner(self):

        self.clear_content()

        self.create_header(
            "URL Security Scanner",
            "Check suspicious website links for phishing indicators."
        )

        card = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=30,
            pady=30
        )

        card.pack(fill="x", pady=10)

        tk.Label(
            card,
            text="Enter Website URL",
            font=("Segoe UI", 12, "bold"),
            bg=self.CARD,
            fg=self.TEXT
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        self.url_entry = tk.Entry(
            card,
            font=("Segoe UI", 12),
            bg="#0F1B30",
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat"
        )

        self.url_entry.pack(fill="x", ipady=13)

        self.create_action_button(
            card,
            "Analyze URL",
            self.scan_url
        ).pack(anchor="w", pady=20)

        self.url_result = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=25,
            pady=25
        )

        self.url_result.pack(
            fill="both",
            expand=True,
            pady=10
        )

        self.url_result_label = tk.Label(
            self.url_result,
            text="Your scan results will appear here.",
            font=("Segoe UI", 12),
            bg=self.CARD,
            fg=self.MUTED,
            justify="left",
            wraplength=850
        )

        self.url_result_label.pack(anchor="w")

    def scan_url(self):

        url = self.url_entry.get().strip()

        if not url:
            messagebox.showwarning(
                "Input Required",
                "Please enter a website URL."
            )
            return

        try:

            result = analyze_url(url)

            status = result.get("status", "Success")
            risk = result.get("risk", "Unknown")
            reasons = result.get("reasons", [])

            if status != "Analyzed":
                messagebox.showerror(
                    "URL Analysis Error",
                    str(result)
                )
                return

            if not save_scan(url, risk, reasons):
                messagebox.showerror(
                    "Database Error",
                    "URL was analyzed, but the result could not be saved."
                )
                return

            self.display_result(
                self.url_result_label,
                risk,
                reasons,
                "URL"
            )

        except Exception as error:

            messagebox.showerror(
                "Scan Failed",
                str(error)
            )

    # EMAIL ANALYZER

    def show_email_analyzer(self):

        self.clear_content()

        self.create_header(
            "Email Phishing Analyzer",
            "Analyze email content to identify suspicious messages."
        )

        card = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=25,
            pady=25
        )

        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="Paste Email Content",
            font=("Segoe UI", 12, "bold"),
            bg=self.CARD,
            fg=self.TEXT
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        self.email_text = tk.Text(
            card,
            height=12,
            font=("Consolas", 10),
            bg="#0F1B30",
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            wrap="word",
            padx=12,
            pady=12
        )

        self.email_text.pack(fill="both", expand=True)

        self.create_action_button(
            card,
            "Analyze Email",
            self.analyze_email_content
        ).pack(anchor="w", pady=18)

        self.email_result = tk.Label(
            card,
            text="Analysis results will appear here.",
            font=("Segoe UI", 11),
            bg=self.CARD,
            fg=self.MUTED,
            justify="left",
            wraplength=850
        )

        self.email_result.pack(
            anchor="w",
            pady=10
        )

    def analyze_email_content(self):

        email_content = self.email_text.get(
            "1.0",
            "end"
        ).strip()

        if not email_content:
            messagebox.showwarning(
                "Input Required",
                "Please paste email content."
            )
            return

        try:

            result = analyze_email(email_content)

            status = result.get("status", "Success")
            risk = result.get("risk", "Unknown")
            reasons = result.get("reasons", [])

            if status != "Analyzed":
                messagebox.showerror(
                    "Email Analysis Error",
                    str(result)
                )
                return

            if not save_email_scan(
                email_content,
                risk,
                reasons
            ):
                messagebox.showerror(
                    "Database Error",
                    "Email was analyzed, but the result could not be saved."
                )
                return

            self.display_result(
                self.email_result,
                risk,
                reasons,
                "Email"
            )

        except Exception as error:

            messagebox.showerror(
                "Analysis Failed",
                str(error)
            )

    # DISPLAY RESULTS

    def display_result(self, label, risk, reasons, scan_type):

        risk_colors = {
            "Low": self.GREEN,
            "Medium": self.ORANGE,
            "High": self.RED
        }

        color = risk_colors.get(
            risk,
            self.ACCENT
        )

        if isinstance(reasons, (list, tuple)):
            reason_text = "\n".join(
                f"• {reason}" for reason in reasons
            )
        else:
            reason_text = str(reasons)

        if not reason_text:
            reason_text = "No specific indicators were returned."

        label.configure(
            text=(
                f"{scan_type} Analysis Completed\n\n"
                f"Risk Level: {risk.upper()}\n\n"
                f"Detection Details:\n"
                f"{reason_text}\n\n"
                "Note: This is an automated rule-based assessment, "
                "not a guarantee that a link or message is safe."
            ),
            fg=color
        )

    # COMBINED HISTORY

    def get_combined_history(self):

        records = []

        url_records = get_scan_history()
        email_records = get_email_scan_history()

        for row in url_records:

            records.append((
                "URL",
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            ))

        for row in email_records:

            records.append((
                "EMAIL",
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            ))

        records.sort(
            key=lambda item: str(item[5]),
            reverse=True
        )

        return records

    # SCAN HISTORY PAGE

    def show_scan_history(self):

        self.clear_content()

        self.create_header(
            "Scan History",
            "Review, search, filter and delete previous security scans."
        )

        toolbar = tk.Frame(
            self.content,
            bg=self.BG
        )

        toolbar.pack(fill="x", pady=10)

        tk.Label(
            toolbar,
            text="Filter by risk:",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 10)
        ).pack(
            side="left",
            padx=(0, 10)
        )

        self.history_filter = ttk.Combobox(
            toolbar,
            values=["All", "Low", "Medium", "High"],
            state="readonly",
            width=12
        )

        self.history_filter.set("All")
        self.history_filter.pack(side="left")

        self.history_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.load_scan_history()
        )

        self.history_search = tk.Entry(
            toolbar,
            font=("Segoe UI", 10),
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            width=25
        )

        self.history_search.pack(
            side="left",
            padx=10,
            ipady=7
        )

        self.history_search.insert(
            0,
            "Search URL or email..."
        )

        self.history_search.bind(
            "<FocusIn>",
            self.clear_search_placeholder
        )

        self.history_search.bind(
            "<KeyRelease>",
            lambda event: self.load_scan_history()
        )

        # ACTION BUTTONS

        self.create_action_button(
            toolbar,
            "Refresh",
            self.load_scan_history
        ).pack(
            side="right",
            padx=4
        )

        self.create_action_button(
            toolbar,
            "Delete Selected",
            self.delete_selected_history
        ).pack(
            side="right",
            padx=4
        )

        self.create_action_button(
            toolbar,
            "Clear All History",
            self.delete_all_history
        ).pack(
            side="right",
            padx=4
        )

        # HISTORY TABLE

        table_frame = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=12,
            pady=12
        )

        table_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        columns = (
            "type",
            "id",
            "content",
            "risk",
            "reasons",
            "time"
        )

        self.history_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
            selectmode="browse"
        )

        headings = {
            "type": "TYPE",
            "id": "SCAN ID",
            "content": "URL / EMAIL CONTENT",
            "risk": "RISK",
            "reasons": "DETECTION REASONS",
            "time": "SCAN TIME"
        }

        widths = {
            "type": 80,
            "id": 70,
            "content": 260,
            "risk": 90,
            "reasons": 240,
            "time": 150
        }

        for col in columns:

            self.history_tree.heading(
                col,
                text=headings[col]
            )

            self.history_tree.column(
                col,
                width=widths[col],
                anchor="w"
            )

        # RISK-BASED ROW COLORS

        self.history_tree.tag_configure(
            "Low",
            background=self.LOW_BG,
            foreground=self.LOW_FG
        )

        self.history_tree.tag_configure(
            "Medium",
            background=self.MEDIUM_BG,
            foreground=self.MEDIUM_FG
        )

        self.history_tree.tag_configure(
            "High",
            background=self.HIGH_BG,
            foreground=self.HIGH_FG
        )

        self.history_tree.tag_configure(
            "Unknown",
            background=self.CARD,
            foreground=self.TEXT
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.history_tree.yview
        )

        self.history_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.history_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.load_scan_history()

    # SEARCH PLACEHOLDER

    def clear_search_placeholder(self, event):

        if self.history_search.get() == "Search URL or email...":
            self.history_search.delete(0, "end")

    # LOAD HISTORY

    def load_scan_history(self):

        if not hasattr(self, "history_tree"):
            return

        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        try:

            records = self.get_combined_history()

            selected_risk = self.history_filter.get()

            search_text = (
                self.history_search.get()
                .strip()
                .lower()
            )

            if search_text == "search url or email...":
                search_text = ""

            for record in records:

                (
                    scan_type,
                    scan_id,
                    content,
                    risk,
                    reasons,
                    scan_time
                ) = record

                if selected_risk != "All" and risk != selected_risk:
                    continue

                if search_text and search_text not in str(content).lower():
                    continue

                # Assign row color based on risk level

                risk_tag = str(risk).strip().capitalize()

                if risk_tag not in ("Low", "Medium", "High"):
                    risk_tag = "Unknown"

                self.history_tree.insert(
                    "",
                    "end",
                    values=(
                        scan_type,
                        scan_id,
                        str(content)[:100],
                        risk,
                        str(reasons)[:150],
                        scan_time
                    ),
                    tags=(risk_tag,)
                )

        except Exception as error:

            messagebox.showerror(
                "History Error",
                str(error)
            )

    # DELETE SELECTED RECORD

    def delete_selected_history(self):

        selected_items = self.history_tree.selection()

        if not selected_items:

            messagebox.showwarning(
                "No Record Selected",
                "Please select a URL or email record first."
            )

            return

        selected_item = selected_items[0]

        values = self.history_tree.item(
            selected_item,
            "values"
        )

        scan_type = values[0]
        scan_id = values[1]

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete this {scan_type} scan?\n\n"
            f"Scan ID: {scan_id}\n\n"
            "This action cannot be undone."
        )

        if not confirm:
            return

        success = delete_scan_history_record(
            scan_type,
            scan_id
        )

        if success:

            self.load_scan_history()

            messagebox.showinfo(
                "Deleted Successfully",
                f"{scan_type} scan #{scan_id} has been deleted."
            )

        else:

            messagebox.showerror(
                "Deletion Failed",
                "Unable to delete this record. Please check the database."
            )

    # CLEAR ALL HISTORY

    def delete_all_history(self):

        confirm = messagebox.askyesno(
            "Clear All History",
            "WARNING!\n\n"
            "This will permanently delete ALL URL and EMAIL scan records.\n\n"
            "This action cannot be undone.\n\n"
            "Do you want to continue?"
        )

        if not confirm:
            return

        success = clear_scan_history()

        if success:

            self.load_scan_history()

            messagebox.showinfo(
                "History Cleared",
                "All URL and email scan records have been deleted."
            )

        else:

            messagebox.showerror(
                "Deletion Failed",
                "Unable to clear history. Please check the database connection."
            )

    # REPORTS PAGE

    def show_reports(self):

        self.clear_content()

        self.create_header(
            "Security Reports",
            "Generate downloadable reports from your scan history."
        )

        stats = get_dashboard_stats()

        card = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=30,
            pady=30
        )

        card.pack(fill="x", pady=15)

        tk.Label(
            card,
            text="Report Overview",
            font=("Segoe UI", 17, "bold"),
            bg=self.CARD,
            fg=self.ACCENT
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        summary = (
            f"Total Scans: {stats['total']}\n\n"
            f"Low Risk: {stats['low']}\n"
            f"Medium Risk: {stats['medium']}\n"
            f"High Risk: {stats['high']}"
        )

        tk.Label(
            card,
            text=summary,
            font=("Segoe UI", 12),
            bg=self.CARD,
            fg=self.TEXT,
            justify="left"
        ).pack(anchor="w")

        self.create_section_title(
            self.content,
            "Export Reports"
        )

        export_card = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=30,
            pady=30
        )

        export_card.pack(fill="x")

        tk.Label(
            export_card,
            text="CSV Report",
            font=("Segoe UI", 13, "bold"),
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="w")

        tk.Label(
            export_card,
            text="Export scan records in spreadsheet-compatible CSV format.",
            font=("Segoe UI", 10),
            bg=self.CARD,
            fg=self.MUTED
        ).pack(
            anchor="w",
            pady=8
        )

        self.create_action_button(
            export_card,
            "Export CSV",
            self.export_csv_report
        ).pack(
            anchor="w",
            pady=(5, 20)
        )

        tk.Frame(
            export_card,
            bg=self.CARD_HOVER,
            height=1
        ).pack(
            fill="x",
            pady=15
        )

        tk.Label(
            export_card,
            text="PDF Report",
            font=("Segoe UI", 13, "bold"),
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="w")

        tk.Label(
            export_card,
            text="Generate a printable PDF security report.",
            font=("Segoe UI", 10),
            bg=self.CARD,
            fg=self.MUTED
        ).pack(
            anchor="w",
            pady=8
        )

        self.create_action_button(
            export_card,
            "Export PDF",
            self.export_pdf_report
        ).pack(
            anchor="w",
            pady=5
        )

    # EXPORT CSV

    def export_csv_report(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="PhishGuard_Report.csv"
        )

        if not path:
            return

        try:

            generate_csv_report(path)

            messagebox.showinfo(
                "Export Successful",
                f"CSV report saved successfully:\n{path}"
            )

        except Exception as error:

            messagebox.showerror(
                "CSV Export Failed",
                str(error)
            )

    # EXPORT PDF

    def export_pdf_report(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="PhishGuard_Report.pdf"
        )

        if not path:
            return

        try:

            generate_pdf_report(path)

            messagebox.showinfo(
                "Export Successful",
                f"PDF report saved successfully:\n{path}"
            )

        except Exception as error:

            messagebox.showerror(
                "PDF Export Failed",
                str(error)
            )

    # SETTINGS PAGE

    def show_settings(self):

        self.clear_content()

        self.create_header(
            "Application Settings",
            "Database connectivity, application information and statistics."
        )

        database_card = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=30,
            pady=25
        )

        database_card.pack(fill="x", pady=10)

        tk.Label(
            database_card,
            text="Database Connection",
            font=("Segoe UI", 16, "bold"),
            bg=self.CARD,
            fg=self.ACCENT
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        self.database_status = tk.Label(
            database_card,
            text="Checking database connection...",
            font=("Segoe UI", 11),
            bg=self.CARD,
            fg=self.MUTED
        )

        self.database_status.pack(
            anchor="w",
            pady=5
        )

        self.create_action_button(
            database_card,
            "Test Connection",
            self.test_database_connection
        ).pack(
            anchor="w",
            pady=15
        )

        statistics_card = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=30,
            pady=25
        )

        statistics_card.pack(fill="x", pady=10)

        tk.Label(
            statistics_card,
            text="Storage Statistics",
            font=("Segoe UI", 16, "bold"),
            bg=self.CARD,
            fg=self.ACCENT
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        self.settings_stats = tk.Label(
            statistics_card,
            text="Loading...",
            font=("Segoe UI", 11),
            bg=self.CARD,
            fg=self.TEXT,
            justify="left"
        )

        self.settings_stats.pack(anchor="w")

        self.create_action_button(
            statistics_card,
            "Refresh Statistics",
            self.refresh_settings_statistics
        ).pack(
            anchor="w",
            pady=15
        )

        info_card = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=30,
            pady=25
        )

        info_card.pack(fill="x", pady=10)

        tk.Label(
            info_card,
            text="Application Information",
            font=("Segoe UI", 16, "bold"),
            bg=self.CARD,
            fg=self.ACCENT
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        information = [
            "Application: PhishGuard",
            "Version: 1.0",
            "Platform: Python Tkinter",
            "Database: MySQL",
            "Detection: Offline Rule-Based Analysis",
            "Modules: URL Scanner, Email Analyzer, History and Reports"
        ]

        for item in information:

            tk.Label(
                info_card,
                text=item,
                font=("Segoe UI", 10),
                bg=self.CARD,
                fg=self.TEXT
            ).pack(
                anchor="w",
                pady=4
            )

        self.test_database_connection()
        self.refresh_settings_statistics()

    # TEST DATABASE CONNECTION

    def test_database_connection(self):

        try:

            connection = connect_database()

            if connection:

                connection.close()

                self.database_status.configure(
                    text="● Connected to MySQL successfully",
                    fg=self.GREEN
                )

            else:

                self.database_status.configure(
                    text="● MySQL connection failed",
                    fg=self.RED
                )

        except Exception as error:

            self.database_status.configure(
                text=f"● Connection error: {error}",
                fg=self.RED
            )

    # REFRESH SETTINGS STATISTICS

    def refresh_settings_statistics(self):

        try:

            stats = get_dashboard_stats()

            statistics_text = (
                f"Total Scans: {stats['total']}\n"
                f"Low Risk: {stats['low']}\n"
                f"Medium Risk: {stats['medium']}\n"
                f"High Risk: {stats['high']}"
            )

            self.settings_stats.configure(
                text=statistics_text
            )

        except Exception as error:

            self.settings_stats.configure(
                text=f"Unable to load statistics:\n{error}"
            )


# RUN APPLICATION

if __name__ == "__main__":

    app = PhishGuardApp()
    app.mainloop()
