# Packaging Line 4 Startup SOP (PL4 v1.0)

**Effective Equipment Stack:**
- Siemens S7-1500 PLC (Master Controller)
- Siemens WinCC HMI Panel (Operator Interface)
- SICK Multiscan14 Laser (Dimensional Quality)
- Cognex InSight 7010 Vision Camera (Defect Detection)
- SEW MOVIGEAR Drive Motors (Conveyor & Packaging)
- EtherCAT Network (Real-Time Field Communication)

---

## Purpose

Standardized startup procedure for Packaging Line 4 after planned downtime or shift handover. Ensures safe system initialization with hardware validation at each stage.

## Preconditions

- [ ] Verify lockout tagout has been cleared by authorized personnel
- [ ] LOTO documentation filed (reference: SAFE-SITE-001)
- [ ] Confirm compressed air pressure ≥6.0 bar (monitored via S7-1500 analog inputs)
- [ ] Verify 24 VDC main power is energized (check PLC PWR LED: steady green)
- [ ] Check HMI display: Alarms screen shows no active safety interlocks
- [ ] Visual inspection: No visible damage to conveyor, drives, or sensors

## Detailed Startup Sequence

### Stage 1: PLC Initialization (5 minutes)

1. **Verify S7-1500 Diagnostic Status**
   - Check indicator LEDs on PLC module:
     - RUN LED (green): Must be steady—indicates normal operation mode
     - ERR LED (red): Must be OFF—indicates no hardware faults
     - BF LED (yellow): Must be OFF—indicates battery/memory OK
   - Reference: VENDOR-SIEMENS-S7-001 (Section 1: Diagnostic LED States)
   - If any LED shows fault state → **STOP**: Do not proceed; contact Automation Engineering

2. **Confirm EtherCAT Network Ready**
   - Via WinCC HMI → Diagnostics → System Status → Network
   - Check "EtherCAT Master Status": Should display GREEN and "OPERATIONAL"
   - Verify slave count matches configured count (typically 4 slaves on PL4):
     - Slave 1: SICK Multiscan14 (Laser)
     - Slave 2: Cognex InSight 7010 (Vision)
     - Slave 3: SEW Motor Controller (Conveyor)
     - Slave 4: SEW Motor Controller (Packaging)
   - If count does not match → Check cable connections per VENDOR-ECAT-NET-001 (Section 2)
   - Reference: VENDOR-ECAT-NET-001 (Section 3: EtherCAT Master Diagnostics)

3. **Enable PLC Program Execution**
   - Switch physical mode selector on PLC to RUN (if not already)
   - WinCC HMI should display MODE: AUTOMATIC
   - Confirm no startup alarms appear in HMI alarm buffer

### Stage 2: Vision System Initialization (3 minutes)

4. **Cognex InSight 7010 Camera Live Check**
   - Via WinCC HMI → Vision Diagnostics → Live Image
   - Confirm live image appears (should see inspection cell reference standard)
   - Check camera status indicator: GREEN LED on camera body (visible through safety window)
   - If image is dark/fuzzy → Verify focus per VENDOR-COGNEX-INS-001 (Section 1: Optical Alignment)
   - Reference camera temperature in status panel (should be 35–50°C—normal operating range)
   - Verify last calibration date is within 30 days; if not → Run calibration per VENDOR-COGNEX-INS-001 (Section 3)

5. **Confirm Vision Tools Active**
   - HMI → Vision → Tool Status
   - Verify all inspection recipes for today's product are loaded and ENABLED
   - Test vision system: Place reference sample in cell
   - Verify camera returns "PASS" result
   - Expected timing: Vision result within 1 second of part arrival

### Stage 3: Laser Dimensioning Initialization (3 minutes)

6. **SICK Multiscan14 Sensor Calibration Check**
   - Location: Laser sensor mounted at exit of packaging cell
   - Verify LED on sensor body: GREEN (ready/operating normally)
   - Reference: VENDOR-SICK-MS-001 (Section 4: Diagnostic Indicators)
   - Via WinCC HMI → Laser Diagnostics → Sensor Status
   - Check calibration status: Should display "CALIBRATED" and timestamp within 7 days
   - If calibration is stale (>7 days) → Contact Process Engineering (SICK calibration requires reference plate not kept on-site)
   - Record baseline reference measurements (typical at +100 mm offset from home)

7. **Confirm Laser Communication**
   - HMI → Laser Diagnostics → EtherCAT Link Status: Must display GREEN and "OPERATIONAL"
   - Send one test measurement: System should respond within 100 ms
   - Typical measurement range: 500–850 mm (product height in packaging cell)
   - Reference: VENDOR-SICK-MS-001 (Section 3: Electrical Interface & EtherCAT Configuration)

### Stage 4: Motor & Drive System Check (3 minutes)

8. **SEW MOVIGEAR Motor Warm-Up**
   - Verify motor coupling alignment visually (no visible offset at shaft coupling)
   - Reference coupling inspection procedure: VENDOR-SEW-MG-001 (Section 3: Motor Coupling Alignment)
   - Jog Conveyor System A motor at 10% speed for 30 seconds
     - Via WinCC: Manual Mode → Conveyor Selection → Jog Forward (10%)
   - Listen for grinding/rattling noise: If heard → **STOP IMMEDIATELY** (bearing may be damaged)
   - Reference bearing diagnostics: VENDOR-SEW-MG-001 (Section 2: Bearing Replacement indicators)
   - Confirm motor temperature readings in HMI: Should start near ambient and rise gradually (normal ramp: ~2°C/minute)

9. **Packaging Drive Motor Test**
   - Jog Packaging Motor at 10% speed for 10 seconds
   - Verify smooth motion and thermal status (below 60°C, rising gradually)
   - Record baseline mechanical signature (listen for any unusual vibration)

### Stage 5: Coordinated Line Trial (5 minutes)

10. **Load Test Articles**
    - Place five reference packages on conveyor entry (manually)
    - Confirm packages are oriented per standard (label facing forward—see packaging standard QSTD-PL4-001)

11. **Run Trial at Reduced Speed (30% nominal)**
    - Via WinCC: Mode → Auto Trial Run
    - System will:
      - Start Conveyor at 30% speed
      - Activate Vision at each part arrival
      - Measure package dimensions via Laser
      - Stage packaging operations at nominal hold points
    - Monitor in real-time:
      - HMI displays part count and quality status
      - Reject count should be 0 for reference parts (false rejects indicate calibration issue)
      - Laser dimensional readouts should be nominally consistent (±0.2 mm variation acceptable)

12. **Review Trial Results**
    - Expected metrics:
      - Total cycle time for 5 parts: ~120 seconds (24 sec/part at 30% speed)
      - Vision reject rate: 0% (reference parts only)
      - Laser readings: All within nominal tolerance
      - No safety alarms triggered
      - No E-stop activation
    - If metrics acceptable → Proceed to Stage 6
    - If metrics unacceptable → Halt line, investigate, do NOT proceed to full speed

### Stage 6: Transition to Nominal Operations

13. **Ramp to 100% Production Speed**
    - Via WinCC: Speed Dial → 100%
    - Increase gradually over 2 minutes (do not jump to 100% instantly)
    - Observe:
      - Laser measurement consistency (should remain <±0.2 mm)
      - Vision false reject rate (should remain <2%)
      - Motor current draw (should stabilize at nominal, documented in logbook)
    - First article must be inspected by Quality before releasing production batch

14. **Document Startup Completion**
    - Record in Electronic Logbook (WinCC → Admin → Daily Log):
      - Date and time startup completed
      - Operator name and shift
      - Any equipment anomalies noted
      - Quality sign-off on first article
    - Store screenshot of final status screen

---

## Acceptance Criteria for Full Production Release

✓ All safety alarms cleared  
✓ No E-stop activation during trial  
✓ Vision false reject rate < 2% on reference parts  
✓ Laser station showing GREEN and OPERATIONAL status  
✓ All motor thermal indications in normal range  
✓ First article inspected and approved by Quality  
✓ Startup documentation logged electronically  

---

## Emergency Actions

| Condition | Immediate Action | Reference |
|-----------|------------------|-----------|
| Red alarm on HMI | Press STOP button; check alarm code via Diagnostics | VENDOR-SIEMENS-S7-001 (Section 2) |
| E-stop triggered | Contact shift supervisor; do NOT proceed until cleared | VENDOR-FANUC-CRX-001 (Section 2) |
| Laser shows RED LED | Power cycle laser; if RED persists, remove from service | VENDOR-SICK-MS-001 (Section 3) |
| Vision image dark/frozen | Check focus per vision troubleshooting; may indicate light failure | VENDOR-COGNEX-INS-001 (Section 2) |
| Motor grinding noise | Stop immediately; inspect coupling and bearing | VENDOR-SEW-MG-001 (Section 2) |

---

## Document Cross-References

- **S7-1500 PLC Diagnostics:** VENDOR-SIEMENS-S7-001
- **WinCC HMI Operation:** VENDOR-SIEMENS-WCC-001
- **SICK Laser Sensor:** VENDOR-SICK-MS-001
- **Cognex Vision Camera:** VENDOR-COGNEX-INS-001
- **SEW Motor & Drives:** VENDOR-SEW-MG-001
- **EtherCAT Network:** VENDOR-ECAT-NET-001
- **Robot Safety (cell entry):** VENDOR-FANUC-CRX-001
- **Related Safety:** SAFE-SITE-001 (LOTO Procedure)
- **Quality Standards:** QSTD-PL4-001

**Revision:** A  
**Last Updated:** 2026-03-10  
**Next Review:** 2026-09-10
