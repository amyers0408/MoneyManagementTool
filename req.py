import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# List of required packages for the web server
REQUIRED_PACKAGES = ["flask", "werkzeug", "jinja2", "itsdangerous", "click", "blinker"]

class RequirementInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget App Dependency Manager")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        # Style Configuration
        style = ttk.Style()
        style.theme_use("clam")

        # Header Title
        title_label = ttk.Label(
            root, 
            text="Flask & Dependencies Setup", 
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(pady=10)

        # Package List Frame
        pkg_frame = ttk.LabelFrame(root, text=" Target Packages ")
        pkg_frame.pack(fill="x", padx=15, pady=5)

        pkg_str = ", ".join(REQUIRED_PACKAGES)
        ttk.Label(pkg_frame, text=pkg_str, font=("Segoe UI", 9, "italic"), wraplength=480).pack(pady=8, padx=10)

        # Button Frame
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill="x", padx=15, pady=10)

        self.btn_check = ttk.Button(btn_frame, text="Check Status", command=self.check_status)
        self.btn_check.pack(side="left", expand=True, fill="x", padx=3)

        self.btn_install = ttk.Button(btn_frame, text="Install All", command=self.install_packages)
        self.btn_install.pack(side="left", expand=True, fill="x", padx=3)

        self.btn_uninstall = ttk.Button(btn_frame, text="Uninstall All", command=self.uninstall_packages)
        self.btn_uninstall.pack(side="left", expand=True, fill="x", padx=3)

        # Output Terminal Window
        out_frame = ttk.LabelFrame(root, text=" Output Log ")
        out_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self.log_area = scrolledtext.ScrolledText(out_frame, wrap=tk.WORD, font=("Consolas", 9), state='disabled')
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)

    def log(self, text):
        """Append text to the GUI log output."""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.root.update_idletasks()

    def set_buttons_state(self, state):
        """Enable or disable interactive buttons during execution."""
        self.btn_check.config(state=state)
        self.btn_install.config(state=state)
        self.btn_uninstall.config(state=state)

    def check_status(self):
        """Check if target packages are installed in the current environment."""
        self.log("--- Checking package installation status ---")
        self.set_buttons_state('disabled')

        installed_count = 0
        for pkg in REQUIRED_PACKAGES:
            cmd = [sys.executable, "-m", "pip", "show", pkg]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                self.log(f"[INSTALLED]   {pkg}")
                installed_count += 1
            else:
                self.log(f"[MISSING]     {pkg}")

        self.log(f"Status Summary: {installed_count}/{len(REQUIRED_PACKAGES)} packages present.\n")
        self.set_buttons_state('normal')

    def install_packages(self):
        """Install required packages via pip."""
        self.log("--- Starting Package Installation ---")
        self.set_buttons_state('disabled')

        cmd = [sys.executable, "-m", "pip", "install"] + REQUIRED_PACKAGES
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in iter(process.stdout.readline, ''):
            if line:
                self.log(line.strip())

        process.wait()
        if process.returncode == 0:
            self.log("--- Installation Complete! --- \n")
            messagebox.showinfo("Success", "All dependencies installed successfully!")
        else:
            self.log("--- Installation Failed --- \n")
            messagebox.showerror("Error", "An error occurred during installation.")

        self.set_buttons_state('normal')

    def uninstall_packages(self):
        """Uninstall target packages via pip."""
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to uninstall Flask and its related packages?")
        if not confirm:
            return

        self.log("--- Starting Package Uninstallation ---")
        self.set_buttons_state('disabled')

        cmd = [sys.executable, "-m", "pip", "uninstall", "-y"] + REQUIRED_PACKAGES
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in iter(process.stdout.readline, ''):
            if line:
                self.log(line.strip())

        process.wait()
        if process.returncode == 0:
            self.log("--- Uninstallation Complete! --- \n")
            messagebox.showinfo("Success", "Dependencies uninstalled successfully!")
        else:
            self.log("--- Uninstallation Failed --- \n")
            messagebox.showerror("Error", "An error occurred during uninstallation.")

        self.set_buttons_state('normal')

if __name__ == "__main__":
    root = tk.Tk()
    app = RequirementInstallerApp(root)
    root.mainloop()