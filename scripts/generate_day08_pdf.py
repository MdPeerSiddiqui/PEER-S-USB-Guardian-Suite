#!/usr/bin/env python3
"""
PEER'S USB Guardian Suite - Executive Multi-Page Lab Report Compiler (Day 08)
Sqrock IT Solutions Cybersecurity Internship Track: Social Engineering Attack Simulations Using Python

Compiles an authoritative 7-page executive engineering report integrating:
- 6 empirical execution screenshots (Kali Linux CLI cold boot, master menu, benign recon payload, bait drive staging, defensive guardian scan, GitHub repo)
- In-depth forensic explanations for every screenshot
- Deep technical analyses of physical USB baiting attacks, AutoRun/AutoPlay abuse, and file extension cloaking
- NIST SP 800-53 (MP-7, AC-19) & CIS Controls v8 compliant defense architecture (GPO disablement, USBGuard, DLP)
- Automated 6-point unit test validation ledger and ethical compliance statements
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
OUTPUT_PDF = os.path.join(REPORTS_DIR, "Day08_USB_Drop_Report_Sqrock_MdPeerSiddiqui.pdf")

# Palette definitions
NAVY_PRIMARY = colors.HexColor("#0B192C")
CYAN_ACCENT  = colors.HexColor("#008DDA")
DARK_BLUE    = colors.HexColor("#1E3E62")
SLATE_GRAY   = colors.HexColor("#415A77")
LIGHT_BG     = colors.HexColor("#F4F6F9")
BORDER_COLOR = colors.HexColor("#D0D7DE")
SUCCESS_COL  = colors.HexColor("#0E703C")
CRIT_COL     = colors.HexColor("#A8201A")
TEXT_DARK    = colors.HexColor("#1A1A1A")


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render total page count
    and persistent running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        page_num = self._pageNumber
        
        # Running Header (pages 2+)
        if page_num > 1:
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.6)
            self.line(36, 756, 576, 756)
            
            self.setFont("Helvetica", 7.5)
            self.setFillColor(SLATE_GRAY)
            self.drawString(36, 762, "Sqrock IT Solutions | Cybersecurity Internship — Day 08 Lab Report")
            self.drawRightString(576, 762, "PEER'S USB Guardian Suite v2.5")

        # Running Footer (all pages)
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.6)
        self.line(36, 36, 576, 36)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(SLATE_GRAY)
        self.drawString(36, 24, "Author: Mohammed Peer Siddiqui | Authorized Lab Environment | Confidential & Educational")
        self.drawRightString(576, 24, f"Page {page_num} of {total_pages}")
        
        self.restoreState()


def create_report():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY_PRIMARY,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=CYAN_ACCENT,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=NAVY_PRIMARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=DARK_BLUE,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_DARK,
        spaceAfter=5
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=DARK_BLUE
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=TEXT_DARK
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    def load_screenshot(filename, w=540, h=195):
        path = os.path.join(SCREENSHOTS_DIR, filename)
        if os.path.exists(path):
            return Image(path, width=w, height=h)
        return Paragraph(f"<b>[Screenshot missing: {filename}]</b>", callout_style)

    # =========================================================================
    # PAGE 1: TITLE, METADATA & EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("SQROCK IT SOLUTIONS — CYBERSECURITY INTERNSHIP", subtitle_style))
    story.append(Paragraph("Day 08: USB Drop Attack Simulation, Baiting Vector Analysis & Endpoint Hardware Defense", title_style))
    story.append(Spacer(1, 4))

    # Metadata Card
    meta_data = [
        [
            Paragraph("<b>Intern:</b> Mohammed Peer Siddiqui", table_cell),
            Paragraph("<b>Track:</b> Social Engineering Simulations (Python)", table_cell),
            Paragraph("<b>Date:</b> October 31, 2026", table_cell)
        ],
        [
            Paragraph("<b>Target Domain:</b> Physical Social Engineering / Removable Media", table_cell),
            Paragraph("<b>Standard:</b> NIST SP 800-53 MP-7 / CIS Controls 10.3", table_cell),
            Paragraph("<b>Framework:</b> MITRE ATT&CK T1091 (Replication Through Removable Media)", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 180, 180])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "Physical social engineering represents one of the most perilous gaps in enterprise perimeter defense. While modern network "
        "firewalls and web filters inspect ingress and egress network packets, physical baiting attacks (commonly referred to as "
        "<b>USB Drop Attacks</b>) bypass perimeter perimeters entirely by directly exploiting human curiosity, financial incentives, "
        "or helpfulness. In these attacks, adversaries scatter weaponized or beaconing removable media across strategic corporate "
        "locations (e.g., parking lots, lobbies, executive dining halls, and restrooms). Once an unsuspecting employee connects "
        "the drive to an internal corporate workstation, malicious execution chains are initiated via AutoPlay misconfigurations, "
        "deceptive double-extension file cloaking, or keystroke injection (BadUSB/HID emulation).",
        body_style
    ))
    story.append(Paragraph(
        "Under <b>Day 08</b> of the Sqrock IT Solutions Cybersecurity Internship, this laboratory research project developed and "
        "evaluated <b>PEER'S USB Guardian Suite v2.5</b>. The system demonstrates a dual-perspective framework: (1) an offensive "
        "awareness simulation engine capable of staging realistic bait drive lures (payroll pretexts, double-extension shortcuts, "
        "and benign reconnaissance triggers), and (2) an endpoint hardware defense guardian that audits host AutoPlay/AutoRun policies, "
        "detects cloaked executables, and provides automated GPO remediation rules aligned with <b>NIST SP 800-53 Rev. 5 (MP-7, AC-19)</b> "
        "and <b>CIS Controls v8 Safeguard 10.3</b>.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Removable Media Security Architecture Comparison", h1_style))
    matrix_data = [
        [
            Paragraph("Security Dimension", table_header),
            Paragraph("Default / Unrestricted Endpoint", table_header),
            Paragraph("Hardened USB Guardian Architecture", table_header)
        ],
        [
            Paragraph("AutoRun / AutoPlay Execution", table_cell),
            Paragraph("<font color='#A8201A'>Active / Prompts execution on mount</font>", table_cell),
            Paragraph("<font color='#0E703C'>Enforced Disabled (NoDriveTypeAutoRun = 0xFF)</font>", table_cell)
        ],
        [
            Paragraph("File Extension Visibility", table_cell),
            Paragraph("<font color='#A8201A'>Hidden (Vulnerable to .pdf.exe tricks)</font>", table_cell),
            Paragraph("<font color='#0E703C'>Enforced Visible (HideFileExt = 0 via GPO)</font>", table_cell)
        ],
        [
            Paragraph("Removable Storage Access", table_cell),
            Paragraph("<font color='#A8201A'>Unrestricted Read/Write/Execute</font>", table_cell),
            Paragraph("<font color='#0E703C'>Hardware Whitelisting / Read-Only Mount</font>", table_cell)
        ],
        [
            Paragraph("Discovery Payload Handling", table_cell),
            Paragraph("<font color='#A8201A'>Silent execution without SOC audit</font>", table_cell),
            Paragraph("<font color='#0E703C'>Instant Canary Alert & SIEM Logging</font>", table_cell)
        ],
        [
            Paragraph("Human Defense Protocol", table_cell),
            Paragraph("<font color='#A8201A'>User plugs drive in to identify owner</font>", table_cell),
            Paragraph("<font color='#0E703C'>Zero-Trust 'Never Plug It In' Policy</font>", table_cell)
        ]
    ]
    t_mat = Table(matrix_data, colWidths=[150, 190, 200])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_mat)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: THREAT MODELING, AUTOPLAY MECHANICS & INITIAL STATE
    # =========================================================================
    story.append(Paragraph("3. Threat Modeling & The USB Baiting Attack Lifecycle", h1_style))
    story.append(Paragraph(
        "The physical baiting attack lifecycle relies on a convergence of social engineering triggers and endpoint technical vulnerabilities. "
        "Attackers weaponize standard USB flash drives or programmable microcontrollers (such as ATmega32U4 BadUSB chips). "
        "The attack progression unfolds across four distinct operational phases:",
        body_style
    ))
    story.append(Paragraph(
        "<b>Phase 1: Weaponization & Staging:</b> The adversary curates pretexts tailored to organizational psychology. High-impact lures "
        "include executive compensation documents (e.g., <code>Q4_Executive_Salaries_2026.xlsx</code>), internal staff downsizing notifications, "
        "or vendor invoices. Malicious entry points leverage historical <code>autorun.inf</code> files, deceptive double extensions "
        "(e.g., <code>.xlsx.bat</code>), or shortcut hijacking (<code>.lnk</code>).<br/>"
        "<b>Phase 2: Physical Dissemination:</b> The drives are physically deposited in target-rich environments where authorized employees "
        "routinely congregate. Branded labels (e.g., 'Confidential - HR Department') significantly amplify the victim's perceived authenticity.<br/>"
        "<b>Phase 3: Insertion & Execution:</b> When inserted into an unhardened workstation, default Windows settings may trigger AutoPlay "
        "or present deceptive icons that entice the victim into double-clicking the disguised executable.<br/>"
        "<b>Phase 4: Reconnaissance & Exfiltration:</b> The payload executes a non-destructive reconnaissance sequence, capturing host identifiers, "
        "logged-in user context, privilege tiers, and active network connections, subsequently beaconing to attacker-controlled C2 servers.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Figure 1: Kali Linux Terminal Initialization & Environment Verification", h2_style))
    story.append(load_screenshot("01_kali_init_banner.png"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 1:</b> The empirical evidence captured in Figure 1 illustrates the initial deployment and "
        "verification of the PEER'S USB Guardian Suite within a dedicated Kali Linux 2026.1 kernel 6.1.0-kali7-amd64 laboratory environment. "
        "The cold-boot sequence confirms active Python 3.10.12 runtime availability, clean Git synchronization on the <code>main</code> branch, "
        "and automated arming of the Removable Media Guardian Daemon. The dual-tone ASCII banner validates the initialization of the "
        "NIST SP 800-53 MP-7 policy engine, staging paths in <code>./simulated_usb_mount/</code>, and structured event streaming into "
        "<code>./telemetry_logs/</code>. This multi-layered environment confirms zero dependencies on unverified third-party binaries.",
        callout_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: MASTER MENU & SUITE ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("4. Suite Architecture & Modular Control Interface", h1_style))
    story.append(Paragraph(
        "To provide a comprehensive instructional platform that bridges offensive social engineering awareness and defensive systems "
        "engineering, <b>PEER'S USB Guardian Suite v2.5</b> was architected into six modular subsystems. Each module is accessible via an "
        "interactive terminal console that enforces strict separation of concerns:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Module 1 (Benign Host Reconnaissance):</b> Executes non-destructive discovery routines, collecting environment context, "
        "host IP, active user, elevation context, and script SHA-256 digests without modifying system integrity.<br/>"
        "• <b>Module 2 (Simulated Bait Drive Generator):</b> Automatically stages realistic USB drive directory structures populated with "
        "safe lure files, simulated AutoRun configs, and awareness canary beacons.<br/>"
        "• <b>Module 3 (Removable Storage Guardian):</b> A defensive file integrity inspector that traverses mounted volumes, flagging "
        "dangerous extensions, double-extension cloaking, and suspicious script execution patterns.<br/>"
        "• <b>Module 4 (Endpoint Policy Auditor):</b> Performs host registry and GPO audits, evaluating whether AutoRun/AutoPlay is disabled "
        "and whether known file extensions are cloaked.<br/>"
        "• <b>Module 5 (SOC Telemetry Inspector):</b> Aggregates and displays recorded reconnaissance events from the local SIEM buffer.<br/>"
        "• <b>Module 6 (Compliance & Defense Blueprint):</b> Displays NIST SP 800-88, NIST SP 800-53, and CIS Controls v8 technical guidelines.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Figure 2: PEER'S USB Guardian Master Control Console", h2_style))
    story.append(load_screenshot("02_master_menu.png"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 2:</b> Figure 2 captures the master operator control console. The interface presents six discrete "
        "options accompanied by live subsystem status indicators confirming that the Host System Recon Engine, Lure Artifact Generator, "
        "File Cloaking & Autorun Sensor, and GPO Audit Engine are fully operational. The prompt structure utilizes standardized POSIX "
        "syntax (<code>sqrock@guardian-suite:~/usb-defense$</code>) providing complete terminal ergonomics for SOC analysts and penetration testers.",
        callout_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: BENIGN HOST RECONNAISSANCE SIMULATION
    # =========================================================================
    story.append(Paragraph("5. Benign Host Reconnaissance Simulation & Telemetry Analysis", h1_style))
    story.append(Paragraph(
        "When an attacker's payload executes upon USB insertion, the initial stage rarely involves destructive actions. Instead, standard "
        "adversarial playbooks (such as MITRE ATT&CK T1082 System Information Discovery and T1033 System Owner/User Discovery) execute "
        "rapid, stealthy reconnaissance to assess whether the target workstation resides within an Active Directory enterprise domain, "
        "holds elevated administrator privileges, or operates within a virtualized malware analysis sandbox.",
        body_style
    ))
    story.append(Paragraph(
        "Under <b>Option 1</b>, the suite executes an entirely benign simulation of this discovery phase. The telemetry engine queries standard "
        "system interfaces (Python standard library modules <code>socket</code>, <code>platform</code>, <code>os</code>, and <code>hashlib</code>) "
        "without triggering destructive side effects. Crucially, the payload calculates its own SHA-256 cryptographic digest to verify code "
        "integrity and logs all findings directly into <code>telemetry_logs/recon_log.json</code> and <code>telemetry_logs/recon_log.txt</code>.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Figure 3: Benign Host Reconnaissance Simulation Execution", h2_style))
    story.append(load_screenshot("03_payload_recon.png"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 3:</b> The terminal trace in Figure 3 confirms successful non-destructive payload execution. "
        "The engine generated a unique incident identifier (<code>USB-REC-20261031203015</code>), captured the UTC ISO 8601 timestamp, "
        "attributed the target hostname (<code>kali-sec-endpoint</code>) and internal network socket (<code>192.168.1.108</code>), verified "
        "the active user privileges (<code>sqrock [STANDARD (Unprivileged User)]</code>), and determined the host OS kernel. The payload "
        "fingerprinted its script body via SHA-256 (<code>9e4f2a1b8c3d...</code>), categorized the threat as <code>BENIGN_RECONNAISSANCE_SIMULATION</code>, "
        "and raised the <code>CANARY_TRIGGERED</code> action flag for immediate SOC alerting.",
        callout_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: BAITING LURE GENERATION & CANARY ARTIFACTS
    # =========================================================================
    story.append(Paragraph("6. Physical Bait Drive Staging, Social Engineering Lures & Canary Beacons", h1_style))
    story.append(Paragraph(
        "To test employee response protocols without endangering corporate infrastructure, security training teams deploy controlled bait "
        "drives populated with educational lures and canary tokens. Under <b>Option 2</b>, the suite stages a realistic bait drive file structure "
        "within <code>./simulated_usb_mount/</code>. The generator creates five distinct lure artifacts designed to model real-world threats:",
        body_style
    ))
    story.append(Paragraph(
        "1. <b>autorun.inf:</b> Replicates legacy AutoRun configuration syntax specifying an automatic launch target (<code>open=beacon_launcher.bat</code>) "
        "and custom volume label (<code>label=Corporate Payroll Drive</code>).<br/>"
        "2. <b>CONFIDENTIAL_PAYROLL_NOTICE.txt:</b> A legitimate-looking text memo that displays a prominent corporate security awareness "
        "advisory instructing the discoverer to return the drive to Room 402, Building A.<br/>"
        "3. <b>Q4_Executive_Salaries_2026.xlsx.bat:</b> A classic double-extension lure. When viewed on Windows endpoints with default "
        "settings (extensions hidden), the file appears as a spreadsheet icon named <code>Q4_Executive_Salaries_2026.xlsx</code>.<br/>"
        "4. <b>beacon_launcher.py:</b> A benign Python trigger script that outputs a harmless console message.<br/>"
        "5. <b>canary_token.json:</b> A cryptographic tracking artifact containing a unique campaign token (<code>CANARY-USB-BAIT-2026-X89</code>) "
        "and drop location metadata (<code>Cafeteria / North Parking Gate</code>).",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Figure 4: Simulated Bait Drive Staging & Lure Architecture", h2_style))
    story.append(load_screenshot("04_bait_drive_gen.png"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 4:</b> Figure 4 depicts the staging process of the simulated bait drive. Five distinct educational "
        "artifacts were populated into the mount point. The terminal output provides immediate pedagogical context, detailing how the "
        "payroll lure exploits human cognitive biases (authority, scarcity, and greed) while the file extension masking mechanism exploits "
        "operating system defaults. All generated artifacts are strictly non-weaponized and intended exclusively for corporate training.",
        callout_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: DEFENSIVE STORAGE GUARDIAN & HEURISTIC SCANNING
    # =========================================================================
    story.append(Paragraph("7. Defensive Removable Storage Guardian & Heuristic Threat Inspection", h1_style))
    story.append(Paragraph(
        "An effective endpoint defense architecture cannot rely solely on user compliance. Technical safeguards must actively inspect "
        "and neutralize untrusted removable media before unauthorized binaries execute. The <b>Defensive Storage Guardian</b> module "
        "(Option 3) implements an automated heuristic scanner capable of analyzing any mounted folder or external USB volume.",
        body_style
    ))
    story.append(Paragraph(
        "The guardian evaluates four critical threat dimensions: (1) detection of <code>autorun.inf</code> configuration files (+35 risk points), "
        "(2) deceptive double extensions hiding executable payloads (+30 risk points), (3) standalone binary/executable extensions such as "
        "<code>.exe</code>, <code>.bat</code>, <code>.vbs</code>, and <code>.ps1</code> (+20 risk points), and (4) suspicious shell execution strings "
        "inside script bodies (+15 risk points). If the cumulative threat score exceeds 70/100, the volume is classified as "
        "<b>CRITICAL_THREAT_DETECTED</b>, triggering automated mitigation advice.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Figure 5: Defensive USB Guardian Media Scan Output", h2_style))
    story.append(load_screenshot("05_endpoint_guard.png"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 5:</b> Figure 5 captures the Storage Guardian evaluating the simulated bait drive. The scanner "
        "analyzed all 5 volume files, identifying the dangerous <code>autorun.inf</code> configuration (+35) and the cloaked "
        "<code>Q4_Executive_Salaries_2026.xlsx.bat</code> double extension (+30 deceptive, +20 executable). The cumulative threat score "
        "reached <b>85 / 100</b>, triggering the <code>CRITICAL_THREAT_DETECTED</code> verdict. The system emitted immediate automated defense "
        "recommendations: unmounting/blocking the volume via udev/USBGuard, alerting the SOC, and dispatching physical security to the drop site.",
        callout_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: AUTOMATED UNIT VERIFICATION, NIST POLICY & GITHUB REPO
    # =========================================================================
    story.append(Paragraph("8. Automated Unit Test Verification & Quality Assurance", h1_style))
    test_data = [
        [
            Paragraph("Test Method Identifier", table_header),
            Paragraph("Target Functional Component", table_header),
            Paragraph("Verification Metric", table_header),
            Paragraph("Result", table_header)
        ],
        [
            Paragraph("<code>test_collect_host_telemetry</code>", table_cell),
            Paragraph("Reconnaissance Telemetry", table_cell),
            Paragraph("Validates JSON/TXT output & SHA-256 hash", table_cell),
            Paragraph("<font color='#0E703C'><b>PASSED</b></font>", table_cell)
        ],
        [
            Paragraph("<code>test_generate_bait_drive</code>", table_cell),
            Paragraph("Lure Staging Engine", table_cell),
            Paragraph("Confirms 5 artifacts & canary generation", table_cell),
            Paragraph("<font color='#0E703C'><b>PASSED</b></font>", table_cell)
        ],
        [
            Paragraph("<code>test_scan_clean_media</code>", table_cell),
            Paragraph("Storage Guardian Scanner", table_cell),
            Paragraph("Verifies 0 threat score on clean media", table_cell),
            Paragraph("<font color='#0E703C'><b>PASSED</b></font>", table_cell)
        ],
        [
            Paragraph("<code>test_scan_autorun_detection</code>", table_cell),
            Paragraph("AutoRun Heuristic Sensor", table_cell),
            Paragraph("Detects autorun.inf & adds +35 threat score", table_cell),
            Paragraph("<font color='#0E703C'><b>PASSED</b></font>", table_cell)
        ],
        [
            Paragraph("<code>test_scan_double_ext_detection</code>", table_cell),
            Paragraph("File Cloaking Detection", table_cell),
            Paragraph("Flags .xlsx.bat double extension (+50 score)", table_cell),
            Paragraph("<font color='#0E703C'><b>PASSED</b></font>", table_cell)
        ],
        [
            Paragraph("<code>test_endpoint_policy_audit</code>", table_cell),
            Paragraph("GPO & Registry Auditor", table_cell),
            Paragraph("Validates registry path & GPO remediation", table_cell),
            Paragraph("<font color='#0E703C'><b>PASSED</b></font>", table_cell)
        ]
    ]
    t_test = Table(test_data, colWidths=[150, 130, 190, 70])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Figure 6: GitHub Repository Overview (PEER-S-USB-Guardian-Suite)", h2_style))
    story.append(load_screenshot("06_github_repo_overview.png", w=540, h=175))
    story.append(Spacer(1, 4))

    story.append(Paragraph("9. Enterprise USB Defense Policy & Legal Compliance", h1_style))
    story.append(Paragraph(
        "<b>Mandatory Endpoint Hardening Controls:</b> To enforce comprehensive compliance with <b>NIST SP 800-53 MP-7 (Media Use)</b> "
        "and <b>CIS Controls v8 Safeguard 10.3</b>, enterprise system administrators must deploy the accompanying <code>policy/disable_autorun.reg</code> "
        "template across all endpoints. This registry script enforces <code>NoDriveTypeAutoRun = 0xFF</code> (disabling AutoRun across all drive "
        "classes) and sets <code>HideFileExt = 0</code> (disabling file extension cloaking in Windows Explorer). Furthermore, organizations must "
        "implement endpoint Device Control solutions (e.g., Windows Defender Device Control or Linux USBGuard) to restrict external storage "
        "to cryptographically approved hardware serial numbers.<br/>"
        "<b>Ethical & Legal Notice:</b> All simulations, lure artifacts, and reconnaissance scripts developed in this laboratory were executed "
        "exclusively within an isolated, authorized educational sandbox. No real-world targets, employee personal storage media, or unapproved "
        "production endpoints were engaged during this research.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Executive Lab Report PDF successfully compiled at:\n    {OUTPUT_PDF}")


if __name__ == "__main__":
    create_report()
