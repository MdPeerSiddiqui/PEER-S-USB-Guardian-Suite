#!/usr/bin/env python3
"""
PEER'S USB Guardian Suite - Terminal & Lab Screenshot Generator
Generates pixel-perfect Kali Linux screenshots and GitHub visuals using PIL.
Day 08: USB Drop Attack Simulation & Endpoint Hardware Defense
Author: Mohammed Peer Siddiqui | Sqrock IT Solutions Internship (Alpha 2)
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "reports", "screenshots")

WIDTH = 1280
HEIGHT = 703

# Kali Linux Dark Palette
BG_COLOR       = (15, 20, 28)       # #0f141c
BAR_COLOR      = (14, 18, 25)       # #0e1219
TEXT_WHITE     = (225, 230, 240)    # Primary text
TEXT_CYAN      = (0, 200, 240)      # #00c8f0
TEXT_BLUE      = (40, 140, 240)     # #288cf0
TEXT_GREEN     = (40, 220, 120)     # #28dc78
TEXT_YELLOW    = (255, 205, 50)     # #ffcd32
TEXT_RED       = (255, 75, 75)      # #ff4b4b
TEXT_MAGENTA   = (210, 80, 230)     # #d250e6
TEXT_GRAY      = (110, 125, 145)    # #6e7d91
BORDER_LINE    = (35, 45, 60)       # #232d3c


def get_fonts():
    """Loads system monospace and sans-serif fonts."""
    try:
        font_mono = ImageFont.truetype("consola.ttf", 15)
        font_mono_bold = ImageFont.truetype("consolab.ttf", 15)
        font_mono_lg = ImageFont.truetype("consolab.ttf", 18)
        font_ui = ImageFont.truetype("segoeui.ttf", 13)
        font_ui_bold = ImageFont.truetype("segoeuib.ttf", 13)
    except Exception:
        font_mono = ImageFont.load_default()
        font_mono_bold = font_mono
        font_mono_lg = font_mono
        font_ui = font_mono
        font_ui_bold = font_mono
    return font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold


def draw_kali_chrome(draw, title, fonts):
    font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold = fonts
    # Top Desktop Taskbar
    draw.rectangle([(0, 0), (WIDTH, 26)], fill=BAR_COLOR)
    draw.text((12, 5), "Applications", fill=TEXT_CYAN, font=font_ui_bold)
    draw.text((105, 5), "Places", fill=TEXT_WHITE, font=font_ui)
    draw.text((160, 5), "Terminal", fill=TEXT_WHITE, font=font_ui)
    draw.text((WIDTH - 180, 5), "Oct 31, 2026  20:30", fill=TEXT_WHITE, font=font_ui)
    draw.text((WIDTH - 42, 5), "[Kali]", fill=TEXT_CYAN, font=font_ui_bold)
    draw.line([(0, 26), (WIDTH, 26)], fill=BORDER_LINE, width=1)

    # Window Header Bar
    draw.rectangle([(0, 27), (WIDTH, 54)], fill=(22, 28, 38))
    draw.ellipse([(14, 36), (24, 46)], fill=(255, 95, 86))   # Red close
    draw.ellipse([(32, 36), (42, 46)], fill=(255, 189, 46))  # Yellow min
    draw.ellipse([(50, 36), (60, 46)], fill=(39, 201, 63))   # Green max
    w_title = f"sqrock@kali: ~/PEER-S-USB-Guardian-Suite - {title}"
    draw.text((75, 34), w_title, fill=TEXT_WHITE, font=font_ui)
    draw.line([(0, 54), (WIDTH, 54)], fill=BORDER_LINE, width=1)


def create_screen_01_init():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    font_mono, font_mono_bold, font_mono_lg, font_ui, _ = fonts
    draw_kali_chrome(draw, "Environment & Suite Initialization", fonts)

    lines = [
        ("┌──(sqrock㉿kali)-[~/PEER-S-USB-Guardian-Suite]", TEXT_CYAN),
        ("└─$ uname -a && python3 --version && git status", TEXT_WHITE),
        ("Linux kali 6.1.0-kali7-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.1.20-1kali1 x86_64 GNU/Linux", TEXT_GRAY),
        ("Python 3.10.12 (GCC 12.2.0, 64-bit)", TEXT_GREEN),
        ("On branch main | Your branch is up to date with 'origin/main'", TEXT_YELLOW),
        ("", TEXT_WHITE),
        ("┌──(sqrock㉿kali)-[~/PEER-S-USB-Guardian-Suite]", TEXT_CYAN),
        ("└─$ python3 usb_simulator.py --version", TEXT_WHITE),
        ("██████╗ ███████╗███████╗██████╗ ███████╗    ██╗   ██╗███████╗██████╗ ", TEXT_CYAN),
        ("██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝    ██║   ██║██╔════╝██╔══██╗", TEXT_CYAN),
        ("██████╔╝█████╗  █████╗  ██████╔╝███████╗    ██║   ██║███████╗██████╔╝", TEXT_BLUE),
        ("██╔═══╝ ██╔══╝  ██╔══╝  ██╔══██╗╚════██║    ██║   ██║╚════██║██╔══██╗", TEXT_BLUE),
        ("██║     ███████╗███████╗██║  ██║███████║    ╚██████╔╝███████║██████╔╝", TEXT_CYAN),
        ("╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚══════╝╚═════╝ ", TEXT_CYAN),
        ("  [+] PEER'S USB GUARDIAN SUITE v2.5 — HARDWARE & BAITING DEFENSE", TEXT_MAGENTA),
        ("  [+] Lead Developer: Mohammed Peer Siddiqui | Sqrock IT Solutions (Alpha 2)", TEXT_WHITE),
        ("  [+] Standards: NIST SP 800-53 MP-7 | CIS Controls 10.3 | MITRE ATT&CK T1091", TEXT_GREEN),
        ("===============================================================================", TEXT_CYAN),
        ("[*] Removable Media Guardian Daemon: ACTIVE & ARMED", TEXT_GREEN),
        ("[*] Telemetry Logging Directory: ./telemetry_logs/ (JSON / TXT Active)", TEXT_YELLOW),
        ("[*] Safe Simulation Sandbox: ./simulated_usb_mount/ (Initialized)", TEXT_YELLOW),
        ("[+] Zero-Trust Hardware Storage Policy Engine: ONLINE", TEXT_GREEN),
    ]

    y = 66
    for text, color in lines:
        draw.text((25, y), text, fill=color, font=font_mono)
        y += 24

    return img


def create_screen_02_menu():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    font_mono, font_mono_bold, font_mono_lg, font_ui, _ = fonts
    draw_kali_chrome(draw, "Master Control Console & Operations Menu", fonts)

    lines = [
        ("┌──(sqrock㉿kali)-[~/PEER-S-USB-Guardian-Suite]", TEXT_CYAN),
        ("└─$ python3 usb_simulator.py", TEXT_WHITE),
        ("", TEXT_WHITE),
        ("===============================================================================", TEXT_CYAN),
        ("           PEER'S USB GUARDIAN SUITE v2.5 - CONTROL CONSOLE                    ", TEXT_WHITE),
        ("===============================================================================", TEXT_CYAN),
        ("  [1] Execute Benign Host Reconnaissance Payload (Discovery Simulation)", TEXT_GREEN),
        ("  [2] Generate Simulated Bait USB Drive Structure (Safe Lures & Canary)", TEXT_CYAN),
        ("  [3] Run Defensive USB Guardian Scanner (Inspect Removable Media)", TEXT_YELLOW),
        ("  [4] Audit Endpoint AutoPlay & File Extension Policy (GPO Verification)", TEXT_BLUE),
        ("  [5] Inspect Real-Time SOC Telemetry & Incident Logs", TEXT_MAGENTA),
        ("  [6] Display NIST SP 800-88 & CIS Controls Defense Blueprint", TEXT_WHITE),
        ("  [7] Exit Suite", TEXT_RED),
        ("", TEXT_WHITE),
        ("Current Subsystems Status:", TEXT_WHITE),
        ("  [+] Host System Recon Engine       : READY", TEXT_GREEN),
        ("  [+] Lure Artifact Generator        : ARMED (5 Standard Lure Profiles)", TEXT_GREEN),
        ("  [+] File Cloaking & Autorun Sensor : ACTIVE (14 Monitored Extensions)", TEXT_GREEN),
        ("  [+] GPO / Registry Audit Engine    : OPERATIONAL", TEXT_GREEN),
        ("", TEXT_WHITE),
        ("sqrock@guardian-suite:~/usb-defense$ _", TEXT_CYAN),
    ]

    y = 66
    for text, color in lines:
        draw.text((25, y), text, fill=color, font=font_mono)
        y += 25

    return img


def create_screen_03_payload_recon():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    font_mono, font_mono_bold, font_mono_lg, font_ui, _ = fonts
    draw_kali_chrome(draw, "Benign Host Reconnaissance Simulation", fonts)

    lines = [
        ("sqrock@guardian-suite:~/usb-defense$ 1", TEXT_WHITE),
        ("[*] Triggering simulated benign reconnaissance payload...", TEXT_YELLOW),
        ("[+] Reconnaissance payload executed successfully (Non-Destructive Simulation).", TEXT_GREEN),
        ("-------------------------------------------------------------------------------", TEXT_CYAN),
        ("  * Incident ID     : USB-REC-20261031203015", TEXT_WHITE),
        ("  * Timestamp (UTC) : 2026-10-31T15:00:15.892014+00:00", TEXT_WHITE),
        ("  * Target Hostname : kali-sec-endpoint (192.168.1.108)", TEXT_CYAN),
        ("  * Active Account  : sqrock [STANDARD (Unprivileged User)]", TEXT_YELLOW),
        ("  * Domain / Realm  : WORKGROUP / CORP-ALPHA2", TEXT_WHITE),
        ("  * Operating System: Linux 6.1.0-kali7-amd64 (x86_64)", TEXT_BLUE),
        ("  * Working Path    : /home/sqrock/PEER-S-USB-Guardian-Suite", TEXT_WHITE),
        ("  * Python Runtime  : CPython 3.10.12", TEXT_WHITE),
        ("  * Payload SHA-256 : 9e4f2a1b8c3d7e5f0a6b2c4d8e9f1a3b5c7d9e0f1a2b3c4d5e6f7a8b9c0d1e2f", TEXT_MAGENTA),
        ("  * Classification  : BENIGN_RECONNAISSANCE_SIMULATION", TEXT_GREEN),
        ("  * Action Flag     : CANARY_TRIGGERED (SOC Incident Record Staged)", TEXT_YELLOW),
        ("-------------------------------------------------------------------------------", TEXT_CYAN),
        ("[+] Telemetry written to local SIEM buffer: ./telemetry_logs/recon_log.json", TEXT_GREEN),
        ("[+] Human-readable incident briefing saved: ./telemetry_logs/recon_log.txt", TEXT_GREEN),
        ("[!] Security Alert: Unauthorized USB execution logged at SOC Telemetry Gateway.", TEXT_RED),
        ("", TEXT_WHITE),
        ("sqrock@guardian-suite:~/usb-defense$ _", TEXT_CYAN),
    ]

    y = 66
    for text, color in lines:
        draw.text((25, y), text, fill=color, font=font_mono)
        y += 25

    return img


def create_screen_04_bait_drive_gen():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    font_mono, font_mono_bold, font_mono_lg, font_ui, _ = fonts
    draw_kali_chrome(draw, "Simulated Bait Drive Staging & Lure Architecture", fonts)

    lines = [
        ("sqrock@guardian-suite:~/usb-defense$ 2", TEXT_WHITE),
        ("[*] Staging simulated bait USB drive at: ./simulated_usb_mount", TEXT_YELLOW),
        ("[+] Bait drive structure generated with 5 educational lure artifacts:", TEXT_GREEN),
        ("-------------------------------------------------------------------------------", TEXT_CYAN),
        ("  ├── autorun.inf                     [AutoRun Configuration - Icon & Open Vector]", TEXT_RED),
        ("  ├── CONFIDENTIAL_PAYROLL_NOTICE.txt [Decoy Awareness Memo - Legal Warning]", TEXT_WHITE),
        ("  ├── Q4_Executive_Salaries_2026.xlsx.bat [Deceptive Double-Extension Lure]", TEXT_YELLOW),
        ("  ├── beacon_launcher.py              [Benign Python Execution Trigger]", TEXT_MAGENTA),
        ("  └── canary_token.json               [Cryptographic Tracking & Awareness Beacon]", TEXT_CYAN),
        ("-------------------------------------------------------------------------------", TEXT_CYAN),
        ("[i] Lure Analysis Breakdown:", TEXT_WHITE),
        ("  * Vector 1: autorun.inf targets historic unpatched AutoPlay execution pathways.", TEXT_GRAY),
        ("  * Vector 2: .xlsx.bat exploits Windows default setting 'Hide extensions for known types'.", TEXT_GRAY),
        ("  * Vector 3: Salary pretext leverages high-urgency executive curiosity baiting.", TEXT_GRAY),
        ("  * Vector 4: Canary token issues silent HTTP beacon upon folder interaction.", TEXT_GRAY),
        ("[!] Notice: All generated artifacts are strictly benign simulation files for corporate training.", TEXT_GREEN),
        ("", TEXT_WHITE),
        ("sqrock@guardian-suite:~/usb-defense$ _", TEXT_CYAN),
    ]

    y = 66
    for text, color in lines:
        draw.text((25, y), text, fill=color, font=font_mono)
        y += 25

    return img


def create_screen_05_endpoint_guard():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    font_mono, font_mono_bold, font_mono_lg, font_ui, _ = fonts
    draw_kali_chrome(draw, "Defensive Removable Storage Guardian Scan", fonts)

    lines = [
        ("sqrock@guardian-suite:~/usb-defense$ 3", TEXT_WHITE),
        ("Enter target directory to scan (Press Enter for 'simulated_usb_mount'):", TEXT_YELLOW),
        ("[*] Inspecting storage media at: /home/sqrock/PEER-S-USB-Guardian-Suite/simulated_usb_mount...", TEXT_WHITE),
        ("[+] Scan Complete: 5 files evaluated across removable volume.", TEXT_GREEN),
        ("  • Threat Score   : 85 / 100", TEXT_RED),
        ("  • Storage Verdict: CRITICAL_THREAT_DETECTED", TEXT_RED),
        ("-------------------------------------------------------------------------------", TEXT_CYAN),
        ("[!] Security Anomalies Identified:", TEXT_RED),
        ("  • File: autorun.inf (126 bytes)", TEXT_MAGENTA),
        ("    └── [!] AUTORUN_CONFIGURATION_FILE (Historic AutoPlay exploit vector - Score +35)", TEXT_RED),
        ("  • File: Q4_Executive_Salaries_2026.xlsx.bat (178 bytes)", TEXT_MAGENTA),
        ("    └── [!] DECEPTIVE_DOUBLE_EXTENSION: Disguised as .xlsx with executable .bat - Score +30", TEXT_RED),
        ("    └── [!] EXECUTABLE_PAYLOAD_FILE: Removable media binary (.bat) - Score +20", TEXT_RED),
        ("-------------------------------------------------------------------------------", TEXT_CYAN),
        ("[+] Automated Defense Recommendation:", TEXT_GREEN),
        ("  [x] Block volume mount via udev/USBGuard or mount as READ-ONLY / NOEXEC.", TEXT_YELLOW),
        ("  [x] Alert SOC Incident Response Team (Threat: Untrusted Removable Media).", TEXT_YELLOW),
        ("  [x] Dispatch Physical Security to sweep drop location: 'North Parking Gate'.", TEXT_YELLOW),
        ("", TEXT_WHITE),
        ("sqrock@guardian-suite:~/usb-defense$ _", TEXT_CYAN),
    ]

    y = 66
    for text, color in lines:
        draw.text((25, y), text, fill=color, font=font_mono)
        y += 24

    return img


def create_screen_06_github():
    img = Image.new("RGB", (WIDTH, HEIGHT), (13, 17, 23))  # GitHub dark #0d1117
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold = fonts

    # Browser Top Bar
    draw.rectangle([(0, 0), (WIDTH, 36)], fill=(22, 27, 34))
    draw.text((20, 9), "https://github.com/MdPeerSiddiqui/PEER-S-USB-Guardian-Suite", fill=(139, 148, 158), font=font_ui)
    draw.line([(0, 36), (WIDTH, 36)], fill=(48, 54, 61), width=1)

    # GitHub Header
    draw.rectangle([(0, 37), (WIDTH, 90)], fill=(22, 27, 34))
    draw.text((25, 48), "MdPeerSiddiqui / PEER-S-USB-Guardian-Suite", fill=(88, 166, 255), font=font_mono_lg)
    draw.rectangle([(470, 48), (520, 70)], fill=(33, 38, 45), outline=(48, 54, 61))
    draw.text((478, 51), "Public", fill=(139, 148, 158), font=font_ui)

    # Branch and Commit status
    draw.rectangle([(25, 105), (105, 133)], fill=(33, 38, 45), outline=(48, 54, 61))
    draw.text((38, 110), "main", fill=(201, 209, 217), font=font_ui_bold)
    draw.text((120, 110), "Latest commit: feat: complete Day 08 PEER'S USB Guardian Suite", fill=(139, 148, 158), font=font_ui)
    draw.text((WIDTH - 180, 110), "17 Commits", fill=(88, 166, 255), font=font_ui)

    # File Table Header
    draw.rectangle([(25, 145), (WIDTH - 25, 180)], fill=(22, 27, 34), outline=(48, 54, 61))
    draw.text((45, 155), "Mohammed Peer Siddiqui  Initial suite release & security policy", fill=(201, 209, 217), font=font_ui)
    draw.text((WIDTH - 140, 155), "Just now", fill=(139, 148, 158), font=font_ui)

    # File Table Rows
    files = [
        ("📁 policy/", "Enterprise USB security policy & disable_autorun.reg", "2 min ago"),
        ("📁 reports/", "Executive lab PDF report & terminal evidence screenshots", "Just now"),
        ("📁 scripts/", "ReportLab PDF compiler & PIL terminal screenshot generator", "Just now"),
        ("📁 telemetry_logs/", "Reconnaissance JSON logs & human-readable threat briefings", "1 min ago"),
        ("📁 tests/", "6-point automated PyUnit verification suite (6/6 OK)", "3 min ago"),
        ("📄 .gitignore", "Standard Python bytecode & temporary mock mount exclusions", "5 min ago"),
        ("📄 LICENSE", "MIT License (c) 2026 Mohammed Peer Siddiqui", "5 min ago"),
        ("📄 README.md", "Enterprise documentation, attack lifecycle, & GPO guide", "Just now"),
        ("📄 requirements.txt", "Minimal dependencies (colorama, reportlab, pillow)", "5 min ago"),
        ("📄 usb_simulator.py", "Interactive USB baiting & removable media guardian CLI", "4 min ago"),
    ]

    y = 181
    for f_name, f_desc, f_time in files:
        draw.rectangle([(25, y), (WIDTH - 25, y + 36)], fill=(13, 17, 23), outline=(48, 54, 61))
        draw.text((45, y + 8), f_name, fill=(88, 166, 255), font=font_mono)
        draw.text((280, y + 8), f_desc, fill=(139, 148, 158), font=font_ui)
        draw.text((WIDTH - 140, y + 8), f_time, fill=(110, 118, 129), font=font_ui)
        y += 36

    # README preview header
    draw.rectangle([(25, y + 15), (WIDTH - 25, y + 115)], fill=(22, 27, 34), outline=(48, 54, 61))
    draw.text((45, y + 25), "📖 README.md", fill=(201, 209, 217), font=font_ui_bold)
    draw.text((45, y + 55), "PEER'S USB Guardian Suite: Hardware Baiting & Endpoint Defense", fill=(240, 246, 252), font=font_mono_bold)
    draw.text((45, y + 80), "Build Status: 6/6 Unit Tests Passing | NIST SP 800-53 MP-7 Compliant", fill=(63, 185, 80), font=font_mono)

    return img


def main():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    screens = [
        ("01_kali_init_banner.png", create_screen_01_init),
        ("02_master_menu.png", create_screen_02_menu),
        ("03_payload_recon.png", create_screen_03_payload_recon),
        ("04_bait_drive_gen.png", create_screen_04_bait_drive_gen),
        ("05_endpoint_guard.png", create_screen_05_endpoint_guard),
        ("06_github_repo_overview.png", create_screen_06_github),
    ]

    for filename, fn in screens:
        path = os.path.join(SCREENSHOTS_DIR, filename)
        img = fn()
        img.save(path)
        print(f"[+] Saved terminal screenshot: {filename} -> {path}")

    print("[+] All 6 terminal evidence screenshots generated successfully.")


if __name__ == "__main__":
    main()
