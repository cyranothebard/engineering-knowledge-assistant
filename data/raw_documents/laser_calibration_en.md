# Laser Dimensioning Calibration Procedure (SOP-LAS-001)

**Equipment:** SICK Multiscan14 Laser Distance Sensor  
**Control System:** Siemens S7-1500 PLC + WinCC HMI  
**Network:** EtherCAT over SCALANCE X312 Switch  

---

## Purpose

Calibrate the laser dimensioning station after maintenance, part changeover, measurement drift, or shipment. Ensures repeatability within ±0.05 mm per SICK specifications.

---

## Preconditions

- [ ] Laser sensor has been powered on for at least 10 minutes (warm-up for thermal stability)
- [ ] Sensor mounted perpendicular to measurement surface
- [ ] Reference calibration block available (included with sensor, part no. per SICK documentation)
- [ ] HMI displays laser diagnostics screen (Laser Status: GREEN, EtherCAT: OPERATIONAL)
- [ ] No active material or obstacles between sensor and reference surface

**Reference:** VENDOR-SICK-MS-001 (Section 2: Calibration Procedure)

---

## Calibration Steps

### Step 1: Prepare Test Setup (2 minutes)

1. Position reference calibration plate perpendicular to laser beam
   - Mounting distance: Typically 500–1000 mm from sensor (per your configuration)
   - Plate must be rigid and flat (deviation <0.1 mm)
   - Reference: VENDOR-SICK-MS-001 (Section 1: Measurement Principles specifications)

2. Verify sensor LED status: Should be solid GREEN (ready/operating)
   - Reference: VENDOR-SICK-MS-001 (Section 4: Diagnostic Indicators)

3. Record ambient temperature (may be requested by diagnostic later)
   - Note: Temperature changes >5°C can affect laser calibration accuracy

### Step 2: Warm-Up Phase (10 minutes)

1. Leave sensor at operating distance for 10 minutes without motion
   - Reason: Laser wavelength drifts during warm-up; allows thermal stabilization
   - Reference: VENDOR-SICK-MS-001 general practice; applies to ToF systems

2. Monitor WinCC HMI during warm-up:
   - Path: Diagnostics → Laser Status
   - Should show "READY" state after 5 minutes
   - Temperature display should stabilize (typically 38–42°C)

### Step 3: Load Reference Gauge Block (1 minute)

1. Via WinCC HMI:
   - Navigate to: Laser Diagnostics → Calibration Setup
   - Select: "Calibration Mode"
   - Confirm reference plate is in position
   - Check "Reference Gauge Block Loaded" checkbox

2. If prompted: Enter reference distance (example: 750 mm)
   - Must match your mounting distance exactly
   - Record in shift log for future reference

### Step 4: Run Automated Calibration Routine (2 minutes)

1. Press "Start Calibration" button in HMI
   - System will automatically:
     - Take 10 measurement samples at current mounting position
     - Calculate zero-distance offset
     - Compute repeatability (1σ spread)
     - Store calibration data in sensor flash memory

2. Monitor progress bar on HMI (typically completes in 30–60 seconds)

3. Check results on HMI display:
   ```
   Calibration Results:
   ├─ Offset: [value] mm (reference position zero-point)
   ├─ Repeatability: ±0.XX mm (1σ)  ← MUST be ≤±0.05 mm
   └─ Status: [PASSED / FAILED]
   ```

   **Acceptance Criteria:**
   - Repeatability ≤ ±0.05 mm → PASSED, calibration approved
   - Repeatability > ±0.05 mm → FAILED, investigate possible causes

### Step 5: Verify Known Reference Object (2 minutes)

1. Remove calibration plate

2. Measure a secondary reference object (known distance)
   - Example: Gauge block at 650 mm (or your verification distance)
   - System should read: [Expected distance] ±[±0.2 mm tolerance]

3. If verification passes:
   - Calibration is complete and locked to flash memory
   - Ready for production use

4. If verification fails (>±0.2 mm error):
   - Do NOT use sensor in production
   - Investigate failure causes (see troubleshooting)

### Step 6: Document Calibration (1 minute)

1. Record in calibration logbook (physical or digital):
   - Date and time of calibration
   - Operator name
   - Offset and repeatability values
   - Verification object result
   - Next scheduled recalibration date (typically 30 days)

2. Via WinCC HMI:
   - Navigate to: Admin → Calibration Log
   - Confirm entry saved with timestamp

---

## Common Failure Signals & Causes

| Signal | Cause | Reference | Solution |
|--------|-------|-----------|----------|
| **Repeatability >±0.05 mm** | Calibration surface not clean; optical misalignment | VENDOR-SICK-MS-001 (Section 3) | Clean front lens; re-verify mounting angle; repeat calibration |
| **No communication with sensor** | EtherCAT network fault; M12 connector loose | VENDOR-ECAT-NET-001 (Section 4) | Check M12 connector seating; verify SCALANCE switch LED green on sensor port |
| **Measurement readings drift during calibration** | Temperature not stabilized; ambient >50°C | VENDOR-SICK-MS-001 (Section 2) | Extend warm-up to 15 min; check for reflected heat source |
| **Sensor reports "Optics Error"** | Contaminated or damaged lens | VENDOR-SICK-MS-001 (Section 3) | Power down; clean lens with soft cloth; re-power and retry |
| **HMI shows calibration timeout** | EtherCAT cycle time exceeded; network latency | VENDOR-ECAT-NET-001 (Section 3) | Check CPU cycle time via S7-1500 diagnostics; verify cable integrity |

---

## Recalibration Schedule

| Circumstance | Action | Timeline |
|--------------|--------|----------|
| Normal production cycle | Scheduled recalibration | Every 30 days |
| After planned maintenance | Re-calibrate before restart | Immediate |
| After product format changeover | Verify reference only; recalibrate if needed | Per changeover SOP (PL4-001 Step 4) |
| After shipping/relocation | Full recalibration required | Immediate, before production |
| If measurement drift detected | Investigate + recalibrate | Within 2 hours of detection |
| Ambient temperature change >5°C | Recalibrate if in operation | Immediate if measured |

---

## Cross-Equipment Interactions

**S7-1500 PLC Impact:**
- If PLC cycle time exceeds 12 ms during calibration, calibration times out
- Reference: VENDOR-SIEMENS-S7-001 (Section 3: Communication Diagnostics)

**EtherCAT Network Impact:**
- If network latency >100 ms, measurement buffers may not flush cleanly
- Reference: VENDOR-ECAT-NET-001 (Section 3: Slave Communication Timeout)

**Startup/Shutdown Impact:**
- Calibration data persists across power cycles (stored in flash memory)
- After shutdown, verify calibration date <7 days as part of startup checklist
- Reference: SOP-PL4-001 (Step 6: SICK Multiscan14 Sensor Calibration Check)

---

## Document References

- **VENDOR-SICK-MS-001:** SICK Multiscan14 Technical Reference (calibration, specifications)
- **VENDOR-ECAT-NET-001:** Industrial Ethernet Troubleshooting (network diagnostics)
- **VENDOR-SIEMENS-S7-001:** S7-1500 Diagnostics (cycle time monitoring)
- **SOP-PL4-001:** Packaging Line 4 Startup SOP (calibration verification)
- **SOP-PL4-002:** Packaging Line 4 Shutdown SOP (data preservation)

**Document ID:** SOP-LAS-001  
**Revision:** B  
**Last Updated:** 2026-03-13  
**Next Review:** 2026-09-13
