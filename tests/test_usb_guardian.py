#!/usr/bin/env python3
"""
================================================================================
Automated Unit Verification Suite for PEER'S USB Guardian Suite
Author      : Mohammed Peer Siddiqui
Organization: Sqrock IT Solutions — Cybersecurity Internship (Alpha 2 Cohort)
================================================================================
"""

import os
import sys
import json
import shutil
import tempfile
import unittest

# Ensure parent directory is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from usb_simulator import (
    collect_host_telemetry,
    generate_bait_drive,
    scan_storage_media,
    audit_endpoint_policy,
    load_telemetry_logs
)


class TestUSBGuardianSuite(unittest.TestCase):
    """Test suite covering host discovery, bait generation, and storage defense."""

    def setUp(self):
        """Create temporary sandbox directory for test artifacts."""
        self.test_dir = tempfile.mkdtemp()
        self.test_json_log = os.path.join(self.test_dir, "test_recon.json")
        self.test_txt_log = os.path.join(self.test_dir, "test_recon.txt")

    def tearDown(self):
        """Clean up temporary test sandbox."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_collect_host_telemetry(self):
        """Verify benign host reconnaissance collects required fields non-destructively."""
        data = collect_host_telemetry(output_json=self.test_json_log, output_txt=self.test_txt_log)
        
        self.assertIn("event_id", data)
        self.assertIn("hostname", data)
        self.assertIn("username", data)
        self.assertIn("os_type", data)
        self.assertIn("privilege_level", data)
        self.assertIn("script_hash_sha256", data)
        self.assertEqual(data["threat_classification"], "BENIGN_RECONNAISSANCE_SIMULATION")
        
        # Verify files were generated on disk
        self.assertTrue(os.path.exists(self.test_json_log))
        self.assertTrue(os.path.exists(self.test_txt_log))

    def test_generate_bait_drive(self):
        """Verify bait drive staging generates correct educational lure files and canary tokens."""
        mount_dir = os.path.join(self.test_dir, "mount_test")
        result = generate_bait_drive(target_dir=mount_dir)
        
        self.assertEqual(result["target_directory"], mount_dir)
        self.assertGreaterEqual(result["total_files"], 4)
        
        files = os.listdir(mount_dir)
        self.assertIn("autorun.inf", files)
        self.assertIn("CONFIDENTIAL_PAYROLL_NOTICE.txt", files)
        self.assertIn("canary_token.json", files)

    def test_scan_clean_media(self):
        """Verify storage guardian returns clean verdict for benign, non-executable files."""
        clean_dir = os.path.join(self.test_dir, "clean_media")
        os.makedirs(clean_dir, exist_ok=True)
        
        with open(os.path.join(clean_dir, "safe_document.txt"), "w") as f:
            f.write("This is a clean corporate memo.")
            
        with open(os.path.join(clean_dir, "quarterly_budget.csv"), "w") as f:
            f.write("ID,Department,Budget\n1,Marketing,50000")

        res = scan_storage_media(clean_dir)
        self.assertEqual(res["threat_score"], 0)
        self.assertEqual(res["verdict"], "CLEAN_DRIVE")
        self.assertEqual(len(res["threat_findings"]), 0)

    def test_scan_autorun_detection(self):
        """Verify storage guardian flags autorun.inf files with appropriate severity score."""
        autorun_dir = os.path.join(self.test_dir, "autorun_media")
        os.makedirs(autorun_dir, exist_ok=True)
        
        with open(os.path.join(autorun_dir, "autorun.inf"), "w") as f:
            f.write("[AutoRun]\nopen=payload.bat\n")

        res = scan_storage_media(autorun_dir)
        self.assertGreaterEqual(res["threat_score"], 35)
        self.assertTrue(any("autorun.inf" in f["filename"].lower() for f in res["threat_findings"]))

    def test_scan_double_extension_detection(self):
        """Verify storage guardian identifies deceptive double-extension cloaking."""
        deceptive_dir = os.path.join(self.test_dir, "deceptive_media")
        os.makedirs(deceptive_dir, exist_ok=True)
        
        with open(os.path.join(deceptive_dir, "Executive_Bonus.pdf.exe"), "w") as f:
            f.write("MOCK_BINARY_DATA")

        res = scan_storage_media(deceptive_dir)
        self.assertGreaterEqual(res["threat_score"], 40)
        
        issues = res["threat_findings"][0]["issues"]
        self.assertTrue(any("DECEPTIVE_DOUBLE_EXTENSION" in issue for issue in issues))

    def test_endpoint_policy_audit(self):
        """Verify endpoint policy audit returns OS platform details and GPO hardening paths."""
        audit = audit_endpoint_policy()
        self.assertIn("os_platform", audit)
        self.assertIn("autoplay_status", audit)
        self.assertIn("recommended_gpo", audit)
        self.assertIn("recommended_registry", audit)


if __name__ == "__main__":
    unittest.main()
