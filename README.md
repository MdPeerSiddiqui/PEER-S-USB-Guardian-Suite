# PEER'S USB Guardian Suite: Hardware Baiting & Endpoint Defense

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Security Standard](https://img.shields.io/badge/NIST-SP%20800--53%20MP--7-red.svg?style=for-the-badge&logo=nist)](https://csrc.nist.gov/)
[![CIS Controls](https://img.shields.io/badge/CIS%20Controls-v8%20Safeguard%2010.3-orange.svg?style=for-the-badge)](https://www.cisecurity.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Unit Tests](https://img.shields.io/badge/Unit%20Tests-6%2F6%20Passed-brightgreen.svg?style=for-the-badge)](tests/test_usb_guardian.py)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux%20%7C%20Windows-black.svg?style=for-the-badge&logo=linux)](https://www.kali.org/)

> **Day 08 Cybersecurity Internship Deliverable**  
> **Company:** Sqrock IT Solutions  
> **Specialization:** Social Engineering & Authentication Security Simulations Using Python  
> **Developer:** Mohammed Peer Siddiqui  
> **Repository:** [https://github.com/MdPeerSiddiqui/PEER-S-USB-Guardian-Suite](https://github.com/MdPeerSiddiqui/PEER-S-USB-Guardian-Suite)

---

## 📌 Executive Overview

Physical social engineering via dropped USB flash drives remains one of the most effective methods adversaries use to bypass external network firewalls and intrusion prevention systems. By exploiting human curiosity, financial incentives, or helpfulness, attackers entice employees into connecting unknown, weaponized removable media to corporate workstations.

**PEER'S USB Guardian Suite v2.5** is an enterprise-grade hardware baiting simulation, canary tracking, and endpoint storage defense framework developed for **Day 08** of the Sqrock IT Solutions Cybersecurity Internship. It provides a dual-perspective platform:
1. **Offensive Awareness Simulation:** Stages realistic bait drives populated with educational lure artifacts (executive payroll pretexts, double-extension shortcuts, and non-destructive discovery beacons).
2. **Defensive Endpoint Guardian:** Actively inspects mounted removable storage media, flags cloaked executables and `autorun.inf` threats, calculates volume threat scores, audits host AutoPlay/AutoRun policies, and provides automated Group Policy (GPO) and Windows Registry hardening templates.

```
+========================================================================+
|             PEER'S USB GUARDIAN SUITE v2.5 - ARCHITECTURE              |
+========================================================================+
|                                                                        |
|  [Simulated Physical Drop / Found USB Drive]                           |
|          |                                                             |
|          v                                                             |
|  [USB Drive Mount / Insertion]                                         |
|          |                                                             |
|   +------+----------------------------------------------------------+  |
|   | Dual-Perspective Assessment Framework                           |  |
|   |                                                                 |  |
|   |  OFFENSIVE AWARENESS SIMULATION (Educational Sandbox)           |  |
|   |   * Lure Pretexts: Q4_Executive_Salaries_2026.xlsx.bat          |  |
|   |   * Historic AutoRun Staging: autorun.inf                       |  |
|   |   * Non-Destructive Host Recon: Host, IP, User, SHA-256 Hash    |  |
|   |   * Silent Canary Tracking: canary_token.json beaconing         |  |
|   |                                                                 |  |
|   |  DEFENSIVE STORAGE GUARDIAN (NIST SP 800-53 MP-7 Compliant)     |  |
|   |   1. Heuristic Media Inspection (Autorun, cloaked extensions)   |  |
|   |      -> Cumulative Threat Score (0 - 100) & Verdict             |  |
|   |   2. Host Policy & Registry Audit (GPO Verification)            |  |
|   |      -> NoDriveTypeAutoRun = 0xFF (Disable AutoPlay)            |  |
|   |      -> HideFileExt = 0 (Force file extension visibility)       |  |
|   |   3. Structured SIEM Telemetry & Incident Reporting             |  |
|   |      -> JSON & Human-Readable Incident Briefing Generation      |  |
|   +-----------------------------------------------------------------+  |
+========================================================================+
```

---

## 🛡️ Core Capabilities

1. **Benign Host Reconnaissance Payload (`usb_simulator.py`)**
   - Simulates what an attacker's initial discovery script captures upon execution (MITRE ATT&CK T1082 / T1033).
   - Collects host machine name, local IP address, active user, elevation context (Administrator/Root vs Standard User), operating system platform/kernel, working directory, and payload script SHA-256 hash.
   - Strictly non-destructive and logs findings to structured JSON (`telemetry_logs/recon_log.json`) and human-readable incident briefs (`telemetry_logs/recon_log.txt`).

2. **Bait Drive Generator & Canary Tokens**
   - Automatically stages realistic removable drive folder structures (`simulated_usb_mount/`) with controlled educational lures:
     - `autorun.inf` (Simulates legacy AutoPlay launch targets).
     - `CONFIDENTIAL_PAYROLL_NOTICE.txt` (Educational awareness memo).
     - `Q4_Executive_Salaries_2026.xlsx.bat` (Deceptive double-extension simulation).
     - `beacon_launcher.py` (Benign Python trigger).
     - `canary_token.json` (Cryptographic awareness tracking token).

3. **Defensive Storage Guardian & Threat Scanner**
   - Heuristically inspects storage volumes for social engineering threats:
     - Flags `autorun.inf` configuration files (+35 risk points).
     - Detects deceptive double extensions (+30 risk points).
     - Identifies raw executable extensions (`.exe`, `.bat`, `.cmd`, `.vbs`, `.ps1`) (+20 risk points).
     - Scans script bodies for suspicious shell commands (`powershell`, `cmd.exe`, `rundll32`, `certutil`) (+15 risk points).
   - Generates normalized Threat Scores (0–100%) and actionable mitigation verdicts (`CRITICAL_THREAT_DETECTED`, `CLEAN_DRIVE`).

4. **Endpoint Policy & AutoPlay Auditor**
   - Audits Windows Registry settings (`NoDriveTypeAutoRun` and `HideFileExt`).
   - Ships with an automated one-click Registry remediation file (`policy/disable_autorun.reg`) and corporate GPO documentation (`policy/usb_security_policy.md`).

---

## 📂 Repository Structure

```
PEER-S-USB-Guardian-Suite/
├── usb_simulator.py              # Interactive USB baiting & storage guardian CLI suite
├── requirements.txt              # Core project dependencies (colorama, reportlab, pillow)
├── LICENSE                       # MIT License
├── README.md                     # Technical documentation & usage guide
├── policy/
│   ├── usb_security_policy.md    # Formal corporate removable media security policy
│   └── disable_autorun.reg       # Windows Registry hardening template (NoDriveTypeAutoRun = 0xFF)
├── telemetry_logs/
│   ├── recon_log.json            # Structured SOC incident telemetry database
│   └── recon_log.txt             # Human-readable incident briefing
├── tests/
│   └── test_usb_guardian.py      # 6-point automated PyUnit verification suite
├── scripts/
│   ├── generate_terminal_screens.py # Headless PIL terminal screenshot generator
│   └── generate_day08_pdf.py     # ReportLab multi-page executive report compiler
└── reports/
    ├── Day08_USB_Drop_Report_Sqrock_MdPeerSiddiqui.pdf # 7-page executive lab report
    └── screenshots/              # High-fidelity terminal evidence
        ├── 01_kali_init_banner.png
        ├── 02_master_menu.png
        ├── 03_payload_recon.png
        ├── 04_bait_drive_gen.png
        ├── 05_endpoint_guard.png
        └── 06_github_repo_overview.png
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git
- Kali Linux, Ubuntu, Debian, or Windows 10/11

### 2. Clone the Repository
```bash
git clone https://github.com/MdPeerSiddiqui/PEER-S-USB-Guardian-Suite.git
cd PEER-S-USB-Guardian-Suite
```

### 3. Create and Activate Virtual Environment
```bash
# On Linux / macOS / Kali:
python3 -m venv .venv
source .venv/bin/activate

# On Windows PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Execution & Usage Guide

Launch the master interactive console:
```bash
python usb_simulator.py
```

### Operational Modes:
- **`[1] Execute Benign Host Reconnaissance Payload`**  
  Triggers non-destructive discovery routine; captures host, IP, user, platform, and SHA-256 hash. Saves to `telemetry_logs/recon_log.json`.
- **`[2] Generate Simulated Bait USB Drive Structure`**  
  Stages simulated bait drive at `simulated_usb_mount/` with safe lure artifacts and canary token.
- **`[3] Run Defensive USB Guardian Scanner`**  
  Scans removable storage media or target folders for autorun, cloaked double extensions, and suspicious scripts.
- **`[4] Audit Endpoint AutoPlay & File Extension Policy`**  
  Audits operating system AutoPlay and extension settings; provides GPO remediation guidance.
- **`[5] Inspect Real-Time SOC Telemetry & Incident Logs`**  
  Displays timeline of recorded incidents from the local SIEM buffer.
- **`[6] Display NIST SP 800-88 & CIS Controls Defense Blueprint`**  
  Presents technical defense architecture, physical air-gapped cleaning kiosks, and hardware whitelisting standards.

---

## 🧪 Automated Unit Verification

A comprehensive 6-point test suite is included in `tests/test_usb_guardian.py`:

```bash
python -m unittest tests/test_usb_guardian.py -v
```

### Test Suite Results:
| Test Method | Target Component | Status |
| :--- | :--- | :---: |
| `test_collect_host_telemetry` | Host Discovery Engine & Log Serialization | `PASSED` |
| `test_generate_bait_drive` | Lure Staging Engine & Canary Generation | `PASSED` |
| `test_scan_clean_media` | Guardian Scanner Baseline on Clean Media | `PASSED` |
| `test_scan_autorun_detection` | AutoRun Heuristic Sensor & Severity Rating | `PASSED` |
| `test_scan_double_extension_detection` | Deceptive Double-Extension Cloaking Sensor | `PASSED` |
| `test_endpoint_policy_audit` | GPO & Registry Security Policy Auditor | `PASSED` |

**Verification Result: 6/6 Tests Passed (100% OK).**

---

## 📊 Security Architecture Comparison

| Feature Metric | Unprotected Endpoint | Hardened USB Guardian Architecture |
| :--- | :--- | :--- |
| **AutoRun / AutoPlay Execution** | Active (Executes on mount) | Enforced Disabled (`NoDriveTypeAutoRun = 0xFF`) |
| **File Extension Visibility** | Hidden by default | Forced Visible (`HideFileExt = 0`) |
| **Double Extension Detection** | Unchecked (User sees `.xlsx`) | Flagged & Blocked (Identified as `.bat`) |
| **Removable Storage Access** | Unrestricted Read/Write/Exec | Whitelisted / Mount as Read-Only (`noexec`) |
| **Discovery Payload Handling** | Unmonitored execution | Instant Canary Alert & SOC Telemetry Logging |
| **Human Defense Protocol** | User inserts drive to find owner | Zero-Trust "Never Plug It In" Policy |

---

## 📜 Compliance & Industry Standards

- **NIST SP 800-53 Rev. 5 (MP-7):** Media Use restrictions and mandatory disablement of automated execution features on removable media.
- **NIST SP 800-53 Rev. 5 (AC-19):** Access Control for Mobile and Removable Devices.
- **CIS Controls v8 (Safeguard 10.3):** Disable AutoRun and AutoPlay features across all enterprise assets.
- **MITRE ATT&CK T1091:** Replication Through Removable Media.

---

## 👤 Author & Acknowledgments

- **Lead Developer:** Mohammed Peer Siddiqui
- **Internship Organization:** Sqrock IT Solutions
- **Track:** Social Engineering Attack Simulations Using Python (Alpha 2 Cohort)
- **LinkedIn:** [Mohammed Peer Siddiqui](https://www.linkedin.com)
- **GitHub:** [@MdPeerSiddiqui](https://github.com/MdPeerSiddiqui)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for full details.
