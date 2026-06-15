# Packaging Line 4 Shutdown SOP (PL4 v1.0)

**Effective Equipment Stack:**
- Siemens S7-1500 PLC (Master Controller)
- Siemens WinCC HMI Panel (Operator Interface)
- SICK Multiscan14 Laser (Dimensional Quality)
- Cognex InSight 7010 Vision Camera (Defect Detection)
- SEW MOVIGEAR Drive Motors (Conveyor & Packaging)
- EtherCAT Network (Real-Time Field Communication)

---

## Purpose

Controlled shutdown of Packaging Line 4 at shift end, before maintenance tasks, or in event of fault condition. Ensures safe de-energization with data preservation and clean hand-off to next shift.

## Procedure

### Stage 1: Graceful Line Stop (5 minutes)

1. **Notify Downstream Operations**
   - Inform Quality and Logistics that line is being shut down
   - Allow existing packages currently in line to flow through naturally
   - Do NOT halt conveyor abruptly if possible (risks jamming)

2. **Reduce Production Speed to Zero Gradually**
   - Via WinCC HMI → Speed Dial: Set to 0%
   - Do NOT press STOP button (hard stop may cause jar/shock to drive systems)
   - Allow conveyor to coast to natural stop (~30 seconds typical)
   - Packaging motors will de-accelerate automatically (controlled brake)
   - Reference motor shutdown guidance: VENDOR-SEW-MG-001 (Section 1: Thermal Protection)

3. **Confirm Conveyor Stopped**
   - Visually verify no motion in conveyor belt
   - Via WinCC: Motor Status panel should display "STOPPED" for both motors
   - Record stoppage time in Electronic Logbook

### Stage 2: Sensor & Vision System Shutdown (3 minutes)

4. **Disable Vision Inspection Cell**
   - Via WinCC HMI → Vision → Tool Status → DISABLE
   - Wait 5 seconds for camera to flush its buffers
   - System will automatically save today's batch inspection report
   - Reference: VENDOR-COGNEX-INS-001 (Section 5: Reset & Troubleshooting)
   - Confirm WinCC displays "Vision: OFFLINE"

5. **Disable Laser Dimensioning Station**
   - Via WinCC HMI → Laser Diagnostics → DISABLE
   - Confirm status changes to "OFFLINE"
   - Reference: VENDOR-SICK-MS-001 (Section 3: Diagnostic Indicators)
   - Verify no measurement buffers remain in sensor (should see "Buffer: 0 pending" in HMI)
   - If buffer is not empty, contact Controls Engineering (indicates communication anomaly)

6. **Confirm EtherCAT Network Graceful Shutdown**
   - Via WinCC → Diagnostics → System Status → Network
   - Should display "EtherCAT: IDLE" (not errors or faults)
   - Check slave count returns to 0 after 10 seconds (all devices offline)
   - Reference: VENDOR-ECAT-NET-001 (Section 4: Common Network Issues)

### Stage 3: PLC Safe-to-Stop Verification (2 minutes)

7. **Verify S7-1500 Status**
   - Check PLC front panel LEDs:
     - RUN LED (green): May change to blinking (wait state)
     - ERR LED (red): Must remain OFF
     - BF LED (yellow): Must be OFF
   - Reference: VENDOR-SIEMENS-S7-001 (Section 1: Diagnostic LED States)
   - If ERR LED is ON or blinking → Investigate alarm before proceeding (see Emergency Actions)

8. **Confirm No Latched Alarms**
   - Via WinCC → Alarms → Active Alarms
   - Should display empty or only informational messages (green status)
   - If any orange or red alarms are present, note them in Electronic Logbook before shutdown

### Stage 4: Energy Isolation (requires authorization)

9. **Isolate Compressed Air (if maintenance work planned)**
   - Locate Main Air Isolation Valve (labeled MV-001, located on backbone panel)
   - CAUTION: Use 3-point lockout tagout per SAFE-SITE-001 procedure
   - Each authorized technician must apply personal lock
   - Post name badge on lock assembly
   - Verify no hiss or pressure indication after valve closure

10. **Verify Electrical Main Switch Status**
    - If full power-down required:
      - Switch main disconnect to OFF position (large red switch on control cabinet door)
      - Safe for maintenance work only with formal LOTO in place
      - Verify S7-1500 PLC goes dark (no LED indication after 5 seconds)
    - Reference: SAFE-SITE-001 (Lockout Tagout Procedure)

### Stage 5: System Documentation (2 minutes)

11. **Record Shift Summary in Electronic Logbook**
    - Via WinCC → Admin → Daily Log entry:
      - Date and Time (shutdown initiated)
      - Shift number and operator name
      - Production count for shift (if available from HMI statistics)
      - Parts rejected by Vision (number and types, if available)
      - Laser dimensional average and any anomalies
      - Any equipment faults or warnings noted during shift
      - Maintenance work required or planned (if any)
      - Next shift instructions (if applicable)
    - Save and close log entry

12. **Save Batch Report**
    - Via WinCC → Reports → Export Today's Batch Report
    - Export format: CSV (for Quality records)
    - Verify file transfers to network storage (path: //Manufacturing/PL4_Batch_Reports)
    - If export fails → Contact IT/Engineering (data loss risk)

13. **Exit HMI Gracefully**
    - Via WinCC screen bottom-right: Click "Logout" (not power-off)
    - Operator ID is recorded in audit trail
    - HMI returns to login screen (ready for next shift)

---

## Post-Shutdown Verification

Before leaving the shift:

✓ All motors showing STOPPED status  
✓ Vision and Laser systems showing OFFLINE  
✓ No active alarms (red or orange) on HMI  
✓ Electronic Daily Log completed and saved  
✓ Batch Report exported to network storage  
✓ Main line selector switch in MANUAL or OFF (depends on site standard)  
✓ If LOTO applied: All locks in place with name badges visible  

---

## Communication Loss Handling

**If Laser Station does not respond to DISABLE command:**

1. Confirm laser is physically connected (M12 connector fully seated)
   - Reference: VENDOR-SICK-MS-001 (Section 3: Electrical Interface)
2. Check EtherCAT network status: VENDOR-ECAT-NET-001 (Section 3)
3. If laser appears powered but unresponsive:
   - Perform manual laser power cycle: Switch OFF, wait 30 sec, ON
   - Rescan network from TIA Portal Diagnostic view
   - If still offline, contact Controls Engineering (command issued at 18:30)

**Escalation Path:**
- Minor issues (recovers on rescan) → Log and continue
- Persistent issues (>10 minutes) → Contact Controls Engineering on-call
- Data loss risk → Contact Plant Manager

---

## Document Cross-References

- **S7-1500 PLC:** VENDOR-SIEMENS-S7-001
- **WinCC HMI:** VENDOR-SIEMENS-WCC-001
- **SICK Laser:** VENDOR-SICK-MS-001
- **Cognex Vision:** VENDOR-COGNEX-INS-001
- **SEW Motors:** VENDOR-SEW-MG-001
- **EtherCAT Network:** VENDOR-ECAT-NET-001
- **Safety/LOTO:** SAFE-SITE-001

**Revision:** A  
**Last Updated:** 2026-03-11  
**Next Review:** 2026-09-11
