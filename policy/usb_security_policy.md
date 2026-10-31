# Enterprise Removable Media & USB Security Policy

**Document ID:** SEC-POL-USB-2026-V1  
**Organization:** Sqrock IT Solutions / Enterprise Infrastructure Security  
**Standard Compliance:** NIST SP 800-53 Rev. 5 (MP-7, AC-19), CIS Controls v8 (Safeguard 10.3), ISO/IEC 27001:2022 (Control A.8.10)  
**Author:** Mohammed Peer Siddiqui, Lead Security Intern  
**Approved By:** Chief Information Security Officer (CISO)  
**Effective Date:** October 2026  

---

## 1. Purpose & Scope
This policy establishes mandatory operational and technical controls governing the physical connection, authorization, and monitoring of removable storage media (including USB flash drives, external hard drives, SD cards, and Human Interface Devices) to corporate endpoints, laptops, and virtualized workstations.

The objective is to eliminate infection vectors from physical social engineering (USB drops, baiting) and prevent unauthorized exfiltration of proprietary data.

---

## 2. Threat Analysis: The USB Baiting Attack Lifecycle
Physical social engineering via dropped USB media exploits human curiosity, greed, and helpfulness. 

```
+--------------------------------------------------------------------------+
|                       USB DROP ATTACK LIFECYCLE                          |
+--------------------------------------------------------------------------+
|  1. Weaponization & Staging                                              |
|     * Attacker brands USB drive with corporate logo / stickers.          |
|     * Pretexts: "Executive_Salaries_2026.xlsx", "Confidential_HR.pdf"    |
|     * Payloads: Benign beacon, disguised LNK shortcut, HID BadUSB.       |
|                                                                          |
|  2. Physical Infiltration & Placement                                    |
|     * Deployed in employee parking lots, reception lounges, cafeteria.    |
|                                                                          |
|  3. Victim Discovery & Curiosity Trigger                                 |
|     * Employee finds drive, seeks to identify owner or read salary data. |
|                                                                          |
|  4. Insertion & Execution Attempt                                        |
|     * Unrestricted AutoPlay / user double-clicks disguised shortcut.      |
|     * Host reconnaissance executes, beacons to Command & Control (C2).   |
+--------------------------------------------------------------------------+
```

---

## 3. Mandatory Technical Controls

### 3.1. Complete AutoRun and AutoPlay Disablement
* **Windows Platforms:** AutoRun (`autorun.inf`) and AutoPlay must be disabled across all drive types (removable, CD-ROM, fixed network mounts) via Active Directory Group Policy (GPO):
  - Path: `Computer Configuration -> Administrative Templates -> Windows Components -> AutoPlay Policies`
  - Policy: `Turn off AutoPlay` -> Set to **Enabled (All Drives)**.
  - Policy: `Set the default behavior for AutoPlay` -> Set to **Do not execute any AutoPlay commands**.
* **Registry Key Enforcement:**
  - `HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\NoDriveTypeAutoRun = 0xFF (255)`
* **Linux / macOS Workstations:**
  - GNOME/KDE automounting must be disabled or managed via `dconf` / `udev` blacklisting rules.

### 3.2. Endpoint Privilege & Device Control (DLP)
* Non-administrative users are prohibited from mounting unapproved USB Mass Storage devices.
* Endpoint Detection & Response (EDR) and DLP agents must enforce hardware whitelist filtering based on Vendor ID (VID), Product ID (PID), and verified cryptographic serial numbers.
* Unauthorized USB devices must be automatically mounted in **Read-Only** mode or instantly blocked with an immediate SOC telemetry alert.

### 3.3. File Extension Cloaking Countermeasures
* Windows Explorer policy must permanently disable `Hide extensions for known file types` across all corporate endpoints. Double-extension tricks (e.g., `Executive_Salaries.pdf.exe` or `.pdf.lnk`) are immediately visible to users.

---

## 4. Operational & Human Countermeasures

1. **"Never Plug It In" Golden Rule:**
   - Employees discovering lost or misplaced USB flash drives, external storage devices, or charging cables must immediately surrender the item to Corporate Physical Security or the IT Help Desk.
   - Employees must never insert an unknown drive into personal or corporate workstations to "find out who owns it."

2. **Quarantine Sandbox Station:**
   - The Security Operations Center (SOC) maintains an air-gapped, isolated forensic kiosk running specialized non-persistent operating systems (e.g., Tails / Cuckoo Sandbox) to safely inspect found media.

3. **Annual Social Engineering & Baiting Simulation Drills:**
   - The security team conducts periodic controlled baiting drills using benign canary USB tokens to measure organizational resilience and retrain vulnerable departments.

---

## 5. Violations & Policy Enforcement
Connecting an unapproved personal USB drive to corporate assets classified under restricted or confidential environments constitutes a severe security policy breach, subjecting the individual to mandatory security retraining and administrative disciplinary review.
