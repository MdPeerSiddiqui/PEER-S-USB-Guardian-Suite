#!/usr/bin/env python3
"""
================================================================================
PEER'S USB GUARDIAN SUITE v2.5 — Hardware Baiting & Endpoint Defense Suite
Author      : Mohammed Peer Siddiqui
Organization: Sqrock IT Solutions — Cybersecurity Internship (Alpha 2 Cohort)
Track       : Social Engineering Attack Simulations Using Python (Day 08)
Standard    : NIST SP 800-53 (MP-7, AC-19) | CIS Controls v8 | OWASP Social Engineering
================================================================================
"""

import os
import sys
import json
import socket
import platform
import datetime
import hashlib
import glob
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

BANNER = f"""
{Fore.CYAN}██████╗ ███████╗███████╗██████╗ {Fore.BLUE}███████╗    ██╗   ██╗███████╗██████╗ 
{Fore.CYAN}██╔══██╗██╔════╝██╔════╝██╔══██╗{Fore.BLUE}██╔════╝    ██║   ██║██╔════╝██╔══██╗
{Fore.CYAN}██████╔╝█████╗  █████╗  ██████╔╝{Fore.BLUE}███████╗    ██║   ██║███████╗██████╔╝
{Fore.CYAN}██╔═══╝ ██╔══╝  ██╔══╝  ██╔══██╗{Fore.BLUE}╚════██║    ██║   ██║╚════██║██╔══██╗
{Fore.CYAN}██║     ███████╗███████╗██║  ██║{Fore.BLUE}███████║    ╚██████╔╝███████║██████╔╝
{Fore.CYAN}╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝{Fore.BLUE}╚══════╝     ╚═════╝ ╚══════╝╚═════╝ 
{Fore.MAGENTA}  [+] USB DROP SIMULATION & ENDPOINT HARDENING SUITE v2.5
{Fore.LIGHTBLACK_EX}  [+] Author: Mohammed Peer Siddiqui | Sqrock IT Solutions Alpha 2
  [+] Standard: NIST SP 800-53 MP-7 | CIS Control 10.3 | MITRE ATT&CK T1091
==============================================================================={Style.RESET_ALL}"""

TELEMETRY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telemetry_logs")
DEFAULT_JSON_LOG = os.path.join(TELEMETRY_DIR, "recon_log.json")
DEFAULT_TXT_LOG = os.path.join(TELEMETRY_DIR, "recon_log.txt")
DEFAULT_MOUNT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simulated_usb_mount")

DANGEROUS_EXTENSIONS = [
    ".exe", ".scr", ".pif", ".bat", ".cmd", ".vbs", ".ps1", 
    ".vbe", ".jse", ".wsf", ".wsh", ".msc", ".jar", ".lnk"
]

SUSPICIOUS_CONTENT_PATTERNS = [
    "powershell", "cmd.exe", "rundll32", "certutil", 
    "bitsadmin", "wscript", "cscript", "mshta", "curl -o", "wget"
]


def ensure_directories():
    """Ensure required telemetry and output directories exist."""
    os.makedirs(TELEMETRY_DIR, exist_ok=True)
    os.makedirs(DEFAULT_MOUNT_DIR, exist_ok=True)


def calculate_file_hash(filepath):
    """Compute SHA-256 hash of a specified file."""
    if not os.path.exists(filepath):
        return "UNKNOWN_HASH"
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return "READ_ERROR"


def collect_host_telemetry(output_json=DEFAULT_JSON_LOG, output_txt=DEFAULT_TXT_LOG):
    """
    Collect benign host reconnaissance data (simulates non-destructive discovery).
    Strictly educational and non-destructive.
    """
    ensure_directories()
    
    # Resolve host networking info safely
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "127.0.0.1"

    # Determine user identity and environment
    username = os.getenv("USERNAME") or os.getenv("USER") or "unknown_user"
    user_domain = os.getenv("USERDOMAIN") or "LOCAL_WORKGROUP"
    system_root = os.getenv("SYSTEMROOT") or os.getenv("HOME") or "/"
    
    # Check privilege level safely
    is_admin = False
    try:
        if platform.system() == "Windows":
            import ctypes
            is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        else:
            is_admin = (os.geteuid() == 0)
    except Exception:
        is_admin = False

    telemetry = {
        "event_id": f"USB-REC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "hostname": hostname,
        "local_ip": local_ip,
        "username": username,
        "domain": user_domain,
        "privilege_level": "ELEVATED (Administrator/Root)" if is_admin else "STANDARD (Unprivileged User)",
        "os_type": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "working_directory": os.getcwd(),
        "system_root": system_root,
        "script_hash_sha256": calculate_file_hash(__file__),
        "threat_classification": "BENIGN_RECONNAISSANCE_SIMULATION",
        "action_flag": "CANARY_TRIGGERED"
    }

    # Save to JSON database
    existing_events = []
    if os.path.exists(output_json):
        try:
            with open(output_json, "r", encoding="utf-8") as jf:
                data = json.load(jf)
                if isinstance(data, list):
                    existing_events = data
                else:
                    existing_events = [data]
        except Exception:
            existing_events = []

    existing_events.append(telemetry)
    with open(output_json, "w", encoding="utf-8") as jf:
        json.dump(existing_events, jf, indent=2)

    # Save to Human-Readable TXT Report
    with open(output_txt, "w", encoding="utf-8") as tf:
        tf.write("===============================================================================\n")
        tf.write("       SQROCK IT SOLUTIONS - USB BAITING INCIDENT RECON REPORT                \n")
        tf.write("===============================================================================\n")
        tf.write(f"Incident Event ID   : {telemetry['event_id']}\n")
        tf.write(f"Timestamp (UTC)     : {telemetry['timestamp_utc']}\n")
        tf.write(f"Target Hostname     : {telemetry['hostname']}\n")
        tf.write(f"Source IP Address   : {telemetry['local_ip']}\n")
        tf.write(f"Logged-In Account   : {telemetry['username']} (Domain: {telemetry['domain']})\n")
        tf.write(f"Privilege Context   : {telemetry['privilege_level']}\n")
        tf.write(f"Operating System    : {telemetry['os_type']} {telemetry['os_release']} ({telemetry['architecture']})\n")
        tf.write(f"Payload Execution CWD: {telemetry['working_directory']}\n")
        tf.write(f"Payload SHA-256     : {telemetry['script_hash_sha256']}\n")
        tf.write(f"Classification      : {telemetry['threat_classification']}\n")
        tf.write("===============================================================================\n")

    return telemetry


def generate_bait_drive(target_dir=DEFAULT_MOUNT_DIR):
    """
    Generate a realistic, simulated bait USB drive environment with safe lure files,
    benign trigger scripts, and canary tokens.
    """
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. Simulated Autorun Configuration
    autorun_content = """[AutoRun]
open=beacon_launcher.bat
action=Open Drive to View Payroll Files
icon=payroll_icon.ico
label=Corporate Payroll Drive
"""
    with open(os.path.join(target_dir, "autorun.inf"), "w", encoding="utf-8") as f:
        f.write(autorun_content)

    # 2. Simulated Safe Decoy Text Document
    decoy_readme = """CONFIDENTIAL - SQROCK IT SOLUTIONS INTERNAL DISTRIBUTION ONLY
=============================================================
Document Title: Executive Salary Appraisal Index (Q4 2026)
Classification: Restricted Executive Tier

NOTICE: If you have discovered this removable drive outside corporate premises,
do not access or copy the contents. Immediately return this device to the
Sqrock IT Security Operations Center (Room 402, Building A).
"""
    with open(os.path.join(target_dir, "CONFIDENTIAL_PAYROLL_NOTICE.txt"), "w", encoding="utf-8") as f:
        f.write(decoy_readme)

    # 3. Simulated Double-Extension Lure (Benign demonstration)
    lure_bat = """@echo off
REM Benign Demonstration of Lure Trigger
echo [!] SQROCK SECURITY SIMULATION: USB Drop Payload Triggered!
echo Host: %COMPUTERNAME% | User: %USERNAME%
pause
"""
    with open(os.path.join(target_dir, "Q4_Executive_Salaries_2026.xlsx.bat"), "w", encoding="utf-8") as f:
        f.write(lure_bat)

    # 4. Benign Python Trigger (Simulates payload beacon)
    launcher_py = """# Benign USB Canary Beacon
import socket, datetime
print(f"[CANARY] USB Triggered on {socket.gethostname()} at {datetime.datetime.now()}")
"""
    with open(os.path.join(target_dir, "beacon_launcher.py"), "w", encoding="utf-8") as f:
        f.write(launcher_py)

    # 5. Simulated Canary Token File
    canary_data = {
        "token_id": "CANARY-USB-BAIT-2026-X89",
        "campaign": "Sqrock Physical Social Engineering Awareness",
        "drop_location": "Cafeteria / North Parking Gate",
        "created_at": datetime.datetime.now().isoformat()
    }
    with open(os.path.join(target_dir, "canary_token.json"), "w", encoding="utf-8") as f:
        json.dump(canary_data, f, indent=2)

    generated_files = os.listdir(target_dir)
    return {
        "target_directory": target_dir,
        "files_created": generated_files,
        "total_files": len(generated_files)
    }


def scan_storage_media(target_path=DEFAULT_MOUNT_DIR):
    """
    Defensive Hardware Storage Guardian:
    Scans a folder or removable drive for social engineering indicators:
    - Autorun configurations (autorun.inf)
    - Executable files in root
    - Deceptive double extensions (.pdf.exe, .xlsx.bat)
    - Suspicious shell keywords in scripts
    """
    if not os.path.exists(target_path):
        return {"error": f"Target path '{target_path}' does not exist."}

    findings = []
    scanned_count = 0
    risk_score = 0

    for root, _, files in os.walk(target_path):
        for fname in files:
            scanned_count += 1
            fpath = os.path.join(root, fname)
            f_lower = fname.lower()
            file_issues = []

            # Check 1: autorun.inf detection
            if f_lower == "autorun.inf":
                file_issues.append("AUTORUN_CONFIGURATION_FILE (Historic AutoPlay exploit vector)")
                risk_score += 35

            # Check 2: Deceptive double extension
            # e.g., filename.pdf.exe or filename.xlsx.bat
            parts = f_lower.split(".")
            if len(parts) > 2:
                ext1 = f".{parts[-2]}"
                ext2 = f".{parts[-1]}"
                if ext2 in DANGEROUS_EXTENSIONS:
                    file_issues.append(f"DECEPTIVE_DOUBLE_EXTENSION: Disguised as {ext1} with executable {ext2}")
                    risk_score += 30

            # Check 3: Raw dangerous executable extensions
            _, ext = os.path.splitext(f_lower)
            if ext in DANGEROUS_EXTENSIONS and f_lower != "autorun.inf":
                file_issues.append(f"EXECUTABLE_PAYLOAD_FILE: Removable media binary ({ext})")
                risk_score += 20

            # Check 4: Suspicious script patterns
            if ext in [".bat", ".cmd", ".vbs", ".ps1", ".txt", ".inf", ".py"]:
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as content_file:
                        content = content_file.read().lower()
                        matched_patterns = [p for p in SUSPICIOUS_CONTENT_PATTERNS if p in content]
                        if matched_patterns:
                            file_issues.append(f"SUSPICIOUS_SCRIPT_PATTERNS: {', '.join(matched_patterns)}")
                            risk_score += 15
                except Exception:
                    pass

            if file_issues:
                findings.append({
                    "filename": fname,
                    "rel_path": os.path.relpath(fpath, target_path),
                    "file_size_bytes": os.path.getsize(fpath),
                    "issues": file_issues
                })

    # Normalized risk score 0 - 100
    risk_score = min(risk_score, 100)
    if risk_score >= 70:
        verdict = "CRITICAL_THREAT_DETECTED"
    elif risk_score >= 40:
        verdict = "HIGH_SUSPICION_UNAUTHORIZED_MEDIA"
    elif risk_score > 0:
        verdict = "LOW_RISK_ANOMALY"
    else:
        verdict = "CLEAN_DRIVE"

    return {
        "scan_path": target_path,
        "scanned_files": scanned_count,
        "threat_findings": findings,
        "threat_score": risk_score,
        "verdict": verdict,
        "scan_timestamp": datetime.datetime.now().isoformat()
    }


def audit_endpoint_policy():
    """
    Audits the current operating system host configuration for AutoRun/AutoPlay protection.
    Provides actionable remediation templates.
    """
    os_name = platform.system()
    audit_results = {
        "os_platform": os_name,
        "timestamp": datetime.datetime.now().isoformat(),
        "autoplay_status": "UNKNOWN",
        "file_ext_masking": "UNKNOWN",
        "recommended_gpo": "Computer Configuration -> Administrative Templates -> Windows Components -> AutoPlay Policies",
        "recommended_registry": r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\NoDriveTypeAutoRun = 0xFF"
    }

    if os_name == "Windows":
        try:
            import winreg
            # Check NoDriveTypeAutoRun
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, 
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", 
                    0, 
                    winreg.KEY_READ
                )
                val, _ = winreg.QueryValueEx(key, "NoDriveTypeAutoRun")
                winreg.CloseKey(key)
                if val == 0xFF:
                    audit_results["autoplay_status"] = "PROTECTED (NoDriveTypeAutoRun = 0xFF / Disabled for all drives)"
                else:
                    audit_results["autoplay_status"] = f"VULNERABLE (NoDriveTypeAutoRun = {hex(val)} / Partial protection)"
            except FileNotFoundError:
                audit_results["autoplay_status"] = "VULNERABLE (No GPO restriction key present in HKLM)"

            # Check HideFileExt
            try:
                key2 = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, 
                    r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", 
                    0, 
                    winreg.KEY_READ
                )
                val2, _ = winreg.QueryValueEx(key2, "HideFileExt")
                winreg.CloseKey(key2)
                if val2 == 0:
                    audit_results["file_ext_masking"] = "PROTECTED (File extensions are VISIBLE)"
                else:
                    audit_results["file_ext_masking"] = "VULNERABLE (Known file extensions are HIDDEN)"
            except FileNotFoundError:
                audit_results["file_ext_masking"] = "DEFAULT_CONFIG"
        except Exception as e:
            audit_results["autoplay_status"] = f"AUDIT_ERROR: {str(e)}"
    else:
        # Non-Windows systems (Linux/Kali/macOS)
        audit_results["autoplay_status"] = "N/A (Linux/Unix requires udev rule or desktop automount disablement)"
        audit_results["file_ext_masking"] = "N/A (File extensions not cloaked by default on POSIX)"
        audit_results["recommended_linux_control"] = "USBGuard daemon / udev rules restricting unauthorized storage devices"

    return audit_results


def load_telemetry_logs(log_path=DEFAULT_JSON_LOG):
    """Load and return recorded incident telemetry events."""
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]
    except Exception:
        return []


# ==============================================================================
# INTERACTIVE CLI PRESENTATION
# ==============================================================================

def print_menu():
    print(f"\n{Fore.LIGHTBLACK_EX}--- [ PEER'S USB GUARDIAN CONTROL CONSOLE ] ---{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}[1]{Fore.WHITE} Execute Benign Host Reconnaissance Payload (Discovery Simulation)")
    print(f"  {Fore.CYAN}[2]{Fore.WHITE} Generate Simulated Bait USB Drive Structure (Safe Lures & Canary)")
    print(f"  {Fore.CYAN}[3]{Fore.WHITE} Run Defensive USB Guardian Scanner (Inspect Removable Media)")
    print(f"  {Fore.CYAN}[4]{Fore.WHITE} Audit Endpoint AutoPlay & File Extension Policy (GPO Verification)")
    print(f"  {Fore.CYAN}[5]{Fore.WHITE} Inspect Real-Time SOC Telemetry & Incident Logs")
    print(f"  {Fore.CYAN}[6]{Fore.WHITE} Display NIST SP 800-88 & CIS Controls Defense Blueprint")
    print(f"  {Fore.CYAN}[7]{Fore.RED} Exit Suite")


def interactive_cli():
    print(BANNER)
    while True:
        print_menu()
        choice = input(f"\n{Fore.GREEN}sqrock@guardian-suite{Fore.WHITE}:{Fore.BLUE}~/usb-defense{Fore.WHITE}$ ").strip()

        if choice == "1":
            print(f"\n{Fore.YELLOW}[*] Triggering simulated benign reconnaissance payload...{Style.RESET_ALL}")
            res = collect_host_telemetry()
            print(f"{Fore.GREEN}[+] Reconnaissance payload executed successfully (Non-Destructive).{Style.RESET_ALL}")
            print(f"  {Fore.LIGHTCYAN_EX}• Incident ID    :{Fore.WHITE} {res['event_id']}")
            print(f"  {Fore.LIGHTCYAN_EX}• Target Hostname:{Fore.WHITE} {res['hostname']} ({res['local_ip']})")
            print(f"  {Fore.LIGHTCYAN_EX}• Active Account :{Fore.WHITE} {res['username']} [{res['privilege_level']}]")
            print(f"  {Fore.LIGHTCYAN_EX}• OS Platform    :{Fore.WHITE} {res['os_type']} {res['os_release']} ({res['architecture']})")
            print(f"  {Fore.LIGHTCYAN_EX}• Payload SHA-256:{Fore.WHITE} {res['script_hash_sha256'][:32]}...")
            print(f"  {Fore.LIGHTCYAN_EX}• Telemetry Saved:{Fore.GREEN} {DEFAULT_JSON_LOG} & {DEFAULT_TXT_LOG}")

        elif choice == "2":
            print(f"\n{Fore.YELLOW}[*] Staging simulated bait USB drive at: {DEFAULT_MOUNT_DIR}{Style.RESET_ALL}")
            res = generate_bait_drive()
            print(f"{Fore.GREEN}[+] Bait drive structure generated with {res['total_files']} educational lure artifacts:{Style.RESET_ALL}")
            for item in res["files_created"]:
                print(f"  {Fore.CYAN}├── {Fore.WHITE}{item}")
            print(f"{Fore.YELLOW}[!] Notice: Files are completely benign demonstrations with awareness banners.{Style.RESET_ALL}")

        elif choice == "3":
            scan_dir = input(f"{Fore.YELLOW}Enter target directory to scan (Press Enter for '{DEFAULT_MOUNT_DIR}'): {Style.RESET_ALL}").strip()
            if not scan_dir:
                scan_dir = DEFAULT_MOUNT_DIR
            print(f"\n{Fore.YELLOW}[*] Inspecting storage media at: {scan_dir}...{Style.RESET_ALL}")
            scan_res = scan_storage_media(scan_dir)
            if "error" in scan_res:
                print(f"{Fore.RED}[-] Scan Error: {scan_res['error']}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}[+] Scan Complete: {scan_res['scanned_files']} files evaluated.{Style.RESET_ALL}")
                print(f"  {Fore.LIGHTCYAN_EX}• Threat Score   :{Fore.WHITE} {scan_res['threat_score']} / 100")
                verdict_color = Fore.RED if "CRITICAL" in scan_res['verdict'] or "HIGH" in scan_res['verdict'] else Fore.GREEN
                print(f"  {Fore.LIGHTCYAN_EX}• Storage Verdict:{verdict_color} {scan_res['verdict']}{Style.RESET_ALL}")
                
                if scan_res["threat_findings"]:
                    print(f"\n{Fore.RED}[!] Security Anomalies Identified:{Style.RESET_ALL}")
                    for f in scan_res["threat_findings"]:
                        print(f"  {Fore.MAGENTA}• File: {Fore.WHITE}{f['filename']} ({f['file_size_bytes']} bytes)")
                        for issue in f["issues"]:
                            print(f"    {Fore.RED}└── [!] {issue}{Style.RESET_ALL}")
                else:
                    print(f"  {Fore.GREEN}[+] No malicious autorun or cloaked file patterns detected.{Style.RESET_ALL}")

        elif choice == "4":
            print(f"\n{Fore.YELLOW}[*] Auditing host operating system AutoPlay & extension settings...{Style.RESET_ALL}")
            audit = audit_endpoint_policy()
            print(f"{Fore.GREEN}[+] Host Security Assessment Completed:{Style.RESET_ALL}")
            print(f"  {Fore.LIGHTCYAN_EX}• Platform          :{Fore.WHITE} {audit['os_platform']}")
            print(f"  {Fore.LIGHTCYAN_EX}• AutoPlay Policy   :{Fore.WHITE} {audit['autoplay_status']}")
            print(f"  {Fore.LIGHTCYAN_EX}• File Ext Cloaking :{Fore.WHITE} {audit['file_ext_masking']}")
            print(f"  {Fore.LIGHTCYAN_EX}• Recommended GPO   :{Fore.YELLOW} {audit['recommended_gpo']}")
            print(f"  {Fore.LIGHTCYAN_EX}• Registry Template :{Fore.GREEN} policy/disable_autorun.reg")

        elif choice == "5":
            print(f"\n{Fore.YELLOW}[*] Querying local SOC incident telemetry repository...{Style.RESET_ALL}")
            events = load_telemetry_logs()
            if not events:
                print(f"{Fore.YELLOW}[i] No incident telemetry logs found. Run Option 1 to trigger an event.{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}[+] Total Logged Security Incidents: {len(events)}{Style.RESET_ALL}")
                for idx, ev in enumerate(events[-5:], 1):
                    print(f"\n  {Fore.CYAN}--- Incident Record #{idx} ---{Style.RESET_ALL}")
                    print(f"    ID       : {ev.get('event_id')}")
                    print(f"    Time     : {ev.get('timestamp_utc')}")
                    print(f"    Target   : {ev.get('hostname')} | User: {ev.get('username')}")
                    print(f"    Verdict  : {ev.get('threat_classification')}")

        elif choice == "6":
            print(f"\n{Fore.CYAN}==============================================================================={Style.RESET_ALL}")
            print(f"{Fore.GREEN}    ENTERPRISE REMOVABLE MEDIA SECURITY & BAITING COUNTERMEASURES BLUEPRINT   {Style.RESET_ALL}")
            print(f"{Fore.CYAN}==============================================================================={Style.RESET_ALL}")
            print(f"""
{Fore.YELLOW}1. Technical Disablement (GPO / Registry):{Fore.WHITE}
   - Force NoDriveTypeAutoRun = 0xFF (255) to disable AutoRun on all storage types.
   - Force HideFileExt = 0 to expose malicious double-extension tricks (.pdf.exe).

{Fore.YELLOW}2. Endpoint Data Loss Prevention (DLP) & Device Control:{Fore.WHITE}
   - Implement USB Device Whitelisting by Vendor ID (VID) and Product ID (PID).
   - Restrict non-whitelisted mass storage media to READ-ONLY or block entirely.
   - Deploy USBGuard (Linux) or Windows Defender Device Control.

{Fore.YELLOW}3. Physical Security & Air-Gapped Kiosks:{Fore.WHITE}
   - Establish dedicated 'Forensic Cleaning Kiosks' for inspecting external media.
   - Physical USB port blockers on public-facing and reception workstations.

{Fore.YELLOW}4. Continuous Human Defense (Zero-Trust Baiting Awareness):{Fore.WHITE}
   - Enforce the "Never Plug It In" protocol across all staff tiers.
   - Mandatory hand-off to IT Security for any lost or discovered flash drive.
""")

        elif choice == "7":
            print(f"\n{Fore.CYAN}[+] Exiting PEER'S USB Guardian Suite. Security active.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}[-] Invalid option. Please select 1 through 7.{Style.RESET_ALL}")


if __name__ == "__main__":
    interactive_cli()
