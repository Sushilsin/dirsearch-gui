
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import subprocess
import threading
import os
import csv
import webbrowser
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DirsearchTab(ttk.Frame):
    def __init__(self, parent, tab_name):
        super().__init__(parent)
        self.parent = parent
        self.tab_name = tab_name
        self.results = []
        self.filtered_status = tk.StringVar()
        self.raw_output = []
        self.setup_ui()

    def setup_ui(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(top_frame, text="Target URL:").grid(row=0, column=0, sticky='w')
        self.url_entry = ttk.Entry(top_frame, width=50)
        self.url_entry.grid(row=0, column=1)

        ttk.Label(top_frame, text="Wordlist:").grid(row=1, column=0, sticky='w')
        self.wordlist_entry = ttk.Entry(top_frame, width=50)
        self.wordlist_entry.insert(0, "wordlists/common.txt")
        self.wordlist_entry.grid(row=1, column=1)
        ttk.Button(top_frame, text="Browse", command=self.select_wordlist).grid(row=1, column=2)

        ttk.Label(top_frame, text="Options:").grid(row=2, column=0, sticky='w')
        self.options_entry = ttk.Entry(top_frame, width=50)
        self.options_entry.insert(0, "-e php,html")
        self.options_entry.grid(row=2, column=1)

        ttk.Label(top_frame, text="Timeout:").grid(row=3, column=0, sticky='w')
        self.timeout_entry = ttk.Entry(top_frame, width=10)
        self.timeout_entry.insert(0, "60")
        self.timeout_entry.grid(row=3, column=1, sticky='w')

        self.progress = ttk.Progressbar(top_frame, mode='determinate', maximum=100)
        self.progress.grid(row=4, column=0, columnspan=4, sticky='we', pady=5)

        ttk.Button(top_frame, text="Run Scan", command=self.run_scan).grid(row=5, column=1, sticky='e')
        ttk.Button(top_frame, text="Export CSV", command=self.export_csv).grid(row=5, column=2)
        ttk.Button(top_frame, text="Export HTML", command=self.export_html).grid(row=5, column=3)
        ttk.Button(top_frame, text="View Chart", command=self.show_status_chart).grid(row=5, column=4)

        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill='x', padx=10)
        ttk.Label(filter_frame, text="Filter by status:").pack(side='left')
        self.filter_entry = ttk.Entry(filter_frame, textvariable=self.filtered_status, width=10)
        self.filter_entry.pack(side='left', padx=5)
        ttk.Button(filter_frame, text="Apply", command=self.apply_filter).pack(side='left')
        ttk.Button(filter_frame, text="Clear", command=self.clear_filter).pack(side='left', padx=5)

        self.tree = ttk.Treeview(self, columns=("Status", "URL"), show="headings")
        self.tree.heading("Status", text="Status")
        self.tree.heading("URL", text="URL")
        self.tree.column("Status", width=100)
        self.tree.column("URL", width=800)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        self.tree.tag_configure('status_200', background='#d1fae5')
        self.tree.tag_configure('status_301', background='#fef9c3')
        self.tree.tag_configure('status_302', background='#fde68a')
        self.tree.tag_configure('status_403', background='#fecaca')
        self.tree.tag_configure('status_404', background='#e2e8f0')
        self.tree.tag_configure('status_500', background='#fca5a5')

        ttk.Label(self, text="Raw Output:").pack(anchor='w', padx=10)
        self.raw_text = tk.Text(self, height=10)
        self.raw_text.pack(fill='both', expand=False, padx=10, pady=(0, 10))

    def select_wordlist(self):
        path = filedialog.askopenfilename(title="Select Wordlist", filetypes=[("Text files", "*.txt")])
        if path:
            self.wordlist_entry.delete(0, tk.END)
            self.wordlist_entry.insert(0, path)

    def run_scan(self):
        script_path = filedialog.askopenfilename(title="Select dirsearch.py", filetypes=[("Python files", "*.py")])
        if not script_path:
            return

        url = self.url_entry.get().strip()
        wordlist = self.wordlist_entry.get().strip()
        options = self.options_entry.get().strip()
        timeout = int(self.timeout_entry.get().strip())

        if not script_path or not url:
            messagebox.showerror("Missing input", "Please provide both script path and URL.")
            return
        if not os.path.isfile(script_path):
            messagebox.showerror("Invalid path", "The dirsearch.py path is invalid.")
            return

        self.tree.delete(*self.tree.get_children())
        self.results.clear()
        self.raw_output.clear()
        self.raw_text.delete(1.0, tk.END)
        self.progress["value"] = 0

        cmd = ["python3", script_path, "-u", url]
        if wordlist:
            cmd += ["-w", wordlist]
        if options:
            cmd += options.split()

        threading.Thread(target=self._run_cmd, args=(cmd, timeout), daemon=True).start()

    def _run_cmd(self, cmd, timeout):
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            try:
                for line in proc.stdout:
                    self.parse_output(line)
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                messagebox.showwarning("Timeout", "Scan timed out.")
            else:
                messagebox.showinfo("Done", f"Scan completed. {len(self.results)} results.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def parse_output(self, line):
        line = line.strip()
        self.raw_output.append(line)
        self.raw_text.insert(tk.END, line + "\n")
        self.raw_text.see(tk.END)

        if "%" in line and "/" in line and "errors" in line:
            try:
                percent = float(line.split("%")[0].strip())
                self.progress["value"] = percent
            except:
                pass
        elif "]" in line and ' - ' in line:
            try:
                parts = line.split("] ", 1)[1].split(" - ")
                status = parts[0].strip()
                path = parts[-1].strip()
                if not status.isdigit() or int(status) < 100 or int(status) > 599:
                    return
                base_url = self.url_entry.get().strip().rstrip("/")
                url = path if path.startswith("http") else f"{base_url}/{path.lstrip('/')}"
                self.results.append((status, url))
                tag = f"status_{status}"
                self.tree.insert("", "end", values=(status, url), tags=(tag,))
            except:
                pass

    def export_csv(self):
        if not self.results:
            messagebox.showinfo("Info", "No results to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=f"{self.tab_name}_results.csv")
        if path:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Status", "URL"])
                writer.writerows(self.results)
            messagebox.showinfo("Saved", f"CSV exported to {path}")

    def export_html(self):
        if not self.results:
            messagebox.showinfo("Info", "No results to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".html", initialfile=f"{self.tab_name}_results.html")
        if path:
            with open(path, "w") as f:
                f.write("<html><body><h2>Dirsearch Results</h2><table border='1'><tr><th>Status</th><th>URL</th></tr>")
                for status, url in self.results:
                    f.write(f"<tr><td>{status}</td><td><a href='{url}'>{url}</a></td></tr>")
                f.write("</table></body></html>")
            messagebox.showinfo("Saved", f"HTML exported to {path}")

    def apply_filter(self):
        code = self.filtered_status.get().strip()
        self.tree.delete(*self.tree.get_children())
        for status, url in self.results:
            if status == code:
                tag = f"status_{status}"
                self.tree.insert("", "end", values=(status, url), tags=(tag,))

    def clear_filter(self):
        self.tree.delete(*self.tree.get_children())
        for status, url in self.results:
            tag = f"status_{status}"
            self.tree.insert("", "end", values=(status, url), tags=(tag,))

    def on_tree_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            url = self.tree.item(item, "values")[1]
            webbrowser.open(url)

    def show_status_chart(self):
        if not self.results:
            messagebox.showinfo("No Data", "No results to visualize.")
            return

        counter = Counter([status for status, _ in self.results])
        labels = list(counter.keys())
        values = list(counter.values())

        chart_win = tk.Toplevel(self)
        chart_win.title(f"{self.tab_name} - Status Code Chart")
        chart_win.geometry("520x420")

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title("HTTP Status Code Distribution")

        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

class DirsearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dirsearch Multi-Tab Scanner")
        self.geometry("1000x800")
        self.tab_counter = 1

        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(fill='both', expand=True)

        self.add_new_tab()
        add_tab_btn = ttk.Button(self, text="New Scan Tab", command=self.add_new_tab)
        add_tab_btn.pack(pady=5)

    def add_new_tab(self):
        tab_name = f"Scan {self.tab_counter}"
        tab = DirsearchTab(self.tab_control, tab_name)
        self.tab_control.add(tab, text=tab_name)
        self.tab_control.select(tab)
        self.tab_counter += 1

if __name__ == "__main__":
    app = DirsearchApp()
    app.mainloop()
