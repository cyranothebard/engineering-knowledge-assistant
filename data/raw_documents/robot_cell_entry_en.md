# Robot Cell Entry Procedure (SAFE-ROB-001)

**Equipment:** FANUC CRX-10iA Collaborative Robot Arm  
**Safety Standard:** ISO/TS 15066 (Collaborative Robot Force Limits) + ISO 13849-1 (Safety Functions)  
**Lockout/Tagout:** Per SAFE-SITE-001 (Lockout Tagout Procedure Lindau)  

---

## Purpose

Establish safe entry procedures into the robot cell protective space for inspection, maintenance, or troubleshooting. Ensures compliance with collaborative robotics safety standards and prevents hazardous motion during human presence.

---

## Safety Zones & Restrictions

**Restricted Access Zone (Primary Workspace):**
- Full robot reach: ~1300 mm radius from robot base
- Height: ±600 mm from shoulder height
- Who can access: Only FANUC-trained maintenance personnel
- Entry procedure: See "Formal Cell Entry" section below
- Reference: VENDOR-FANUC-CRX-001 (Section 1: Safeguarding Zones)

**Secondary Collision Zone:**
- Exclusion radius: 2 meters from robot base (all directions)
- Risk: Parts or end-effector can be thrown beyond primary reach
- Who can access: General floor personnel, but protected by barriers
- Reference: VENDOR-FANUC-CRX-001 (Section 1)

**Collaborative Zone (Low-Risk Area):**
- Within 1.5 m from robot base
- Force limited to ≤80 N peak (soft robotics design)
- Speed limited to ≤250 mm/sec
- Humans may work alongside robot IF robot is in collaborative mode
- Reference: VENDOR-FANUC-CRX-001 (Section 1)

---

## Procedure for Formal Cell Entry

### Stage 1: Pre-Entry Communication (5 minutes)

1. **Notify Line Operations**
   - Contact shift supervisor or production lead: "Requesting cell entry for [reason]"
   - Typical reasons: Jam clearing, gripper adjustment, end-effector repair, teachback
   - Confirm that no other personnel are within 5 meters of cell

2. **Initiate Line Stop**
   - Via WinCC HMI: Press STOP button (graceful deceleration)
   - DO NOT use E-STOP unless immediate hazard present
   - Confirm robot comes to rest (should take <30 seconds for normal deceleration)
   - Reference: VENDOR-FANUC-CRX-001 (Section 2: E-Stop vs. Soft Stop)

3. **Verify Robot at Rest**
   - Visually confirm no motion in robot arm
   - Check teach pendant display: Should show "STOPPED" state
   - Listen: No servo hum or motor noise present

---

### Stage 2: Lockout/Tagout Application (3 minutes)

**Reference Procedure:** SAFE-SITE-001 (Lockout Tagout Procedure Lindau)

1. **Each Worker Applies Personal Lock**
   - Locate master E-stop button on robot control cabinet (red button, panel door)
   - Press E-stop button to armed position (physical mechanical latch engaged)
   - Apply personal lock (padlock + key) to E-stop assembly
   - Post name badge on lock identifying authorized person
   - Reference: VENDOR-FANUC-CRX-001 (Section 2: Emergency Stop System)

2. **Verify Zero-Energy State**
   - With LOTO lock applied, physically attempt to move robot arm by hand
   - Arm should NOT move (electromechanical brake engaged)
   - If arm has any motion → DO NOT PROCEED; contact electrician (brake failure)
   - Confirm mechanical lock is engaged per SAFE-SITE-001 checklist

3. **Document LOTO Application**
   - Record: Date, time, workers' names, lock serial numbers
   - If multiple teammates: Each applies own lock (no shared locks)
   - Post lockout log outside cell entrance

---

### Stage 3: Controller Mode Verification (1 minute)

1. **Set Robot Controller to TEACH/MAINTENANCE Mode**
   - If available: Rotate mode selector on teach pendant to TEACH position
   - Reference: VENDOR-FANUC-CRX-001 (Section 3: Teach Pendant Operation)
   - This disables automatic program execution

2. **Verify Mode on Teach Pendant Display**
   - Display should show: "MODE: TEACH" or "MAINTENANCE" (device-specific)
   - Not "AUTO" or "MANUAL" (full-speed execution modes)

3. **Confirm Speed Override Dial at 0–10%**
   - If you must manually jog arm: Set dial to ≤10% speed
   - Do NOT exceed 250 mm/sec in cell (collaborative speed limit)
   - Reference: VENDOR-FANUC-CRX-001 (Section 3: Speed Override Dial)

---

### Stage 4: Physical Cell Inspection (2 minutes)

1. **Visual Safety Walkdown**
   - Look for any hanging or suspended objects above work area
   - Check for any objects in robot workspace that might be struck
   - Verify no electrical cables draped where personnel could trip
   - Reference: VENDOR-FANUC-CRX-001 (Section 1: Operating Envelope)

2. **Verify Emergency Stop Access**
   - Confirm at least 2 emergency stop buttons are within arm's reach from your work position:
     - One on teach pendant (red button, wrist area)
     - One on robot base (red button, front face)
   - Test buttons work (press each, verify audible beep and brief arm motion stop)
   - Reference: VENDOR-FANUC-CRX-001 (Section 2: E-Stop Button Locations)

3. **Position Yourself for Safe Access**
   - Do NOT position body under suspended end-effector
   - Do NOT reach across robot base (blocks emergency stop access)
   - Keep teach pendant within arm's reach at all times

---

### Stage 5: Entry & Work Phase (Variable Duration)

1. **Enter Protected Space**
   - With all steps 1–4 complete, you may now enter cell
   - Walk slowly; do NOT run
   - Maintain visual line of sight to at least one E-stop button at all times

2. **If Manual Arm Motion Required**
   - Hold teach pendant in dominant hand at all times
   - Press directional pad to jog arm; RELEASE to stop motion
   - Motion only occurs while button held (dead-man control)
   - Reference: VENDOR-FANUC-CRX-001 (Section 3: Jog Buttons + enable switch)
   - Max speed: 10% (should be ~25 mm/sec linear motion at wrist)

3. **Perform Maintenance/Inspection Work**
   - Examples: Clear jam, adjust gripper, replace worn coupling, inspect tooling
   - If arm motion becomes necessary: Ensure lowest speed possible (1%–5%)
   - If jammed or stuck: Stop immediately; call electrician (do NOT force)

---

### Stage 6: Exit & Lockout Release (2 minutes)

1. **Clear Work Area**
   - Remove all tools and material from cell floor
   - Move arm to safe "park" position (preferably high and toward corner, away from entry)
   - Reference safe position diagram (usually posted on cell wall)

2. **Verify All Personnel Have Exited**
   - Verbal confirmation: "All clear for re-energization?"
   - Response from all workers: "Clear" or "Yes"
   - Do NOT proceed until all confirm

3. **Remove Personal LOTO Locks**
   - Each worker removes ONLY their own lock (use personal key)
   - Record removal: Date, time, worker name
   - Do NOT remove other workers' locks (violates lockout protocol)

4. **Verify LOTO Master E-Stop Released**
   - After all personal locks removed: Master E-stop should return to armed-off state
   - Press E-stop button once to release mechanical latch
   - Should click audibly and return to normal position
   - Reference: VENDOR-FANUC-CRX-001 (Section 2: E-Stop Recovery)

5. **Test Robot Motion (Optional Pre-Restart Check)**
   - Switch teach pendant to TEST mode (low-speed trials)
   - Jog arm through small motion at 10% speed (5 second duration)
   - Arm should move smoothly without grinding or unusual sounds
   - If motion abnormal: Stop; do NOT restart production; call maintenance

---

## Special Scenarios

### Scenario: Gripper Jam Requires Motion Verification

1. Apply LOTO as above (Section 2)
2. Set speed override to 5% (very conservative)
3. Keep teach pendant in hand continuously
4. Move arm manually to reproduce jam condition
5. Once verified: Move arm back to park position
6. Exit per Stage 6

### Scenario: Teach Pendant Battery Low

- **DO NOT** enter cell with low-battery pendant
- Reason: Pendant may lose control signal mid-motion
- Solution: Charge pendant for 20 min; use second pendant during wait
- Reference: VENDOR-FANUC-CRX-001 (Section 3: Teach Pendant)

### Scenario: E-Stop Button Was Pressed But Lockout Not Applied Yet

- **Risk:** Robot remains powered; E-stop latched but can be reset remotely
- **Recovery:** Apply full LOTO before entering (do NOT skip this step)
- Reference: VENDOR-FANUC-CRX-001 (Section 2: E-Stop System precedence)

---

## Hazard Response

| Condition | Immediate Action | Reference |
|-----------|------------------|-----------|
| Arm moves unexpectedly | Press E-STOP (teach pendant red button) | VENDOR-FANUC-CRX-001 (Section 2) |
| Feel any unusual vibration | Exit cell; press E-stop; call maintenance | Safety first |
| Pendant unresponsive | Press E-stop; exit; do NOT re-enter | Likely control failure |
| Another person enters cell | Press E-stop immediately; evacuate | Zero tolerance |
| Gripper/end-effector unusually hot | Do NOT touch; exit; notify maintenance | Thermal hazard |

---

## Training & Certification

- Only personnel trained on FANUC CRX-10iA safety procedures may perform cell entry
- Annual retraining required (or upon procedure revision)
- Certification valid for 12 months
- Reference: VENDOR-FANUC-CRX-001 (full manual required reading)

---

## Document References

- **VENDOR-FANUC-CRX-001:** FANUC CRX-10iA Safety & Operation (zones, E-stop, teach pendant)
- **SAFE-SITE-001:** Lockout Tagout Procedure Lindau (formal LOTO requirements)
- **SOP-PL4-001:** Packaging Line 4 Startup SOP (post-entry startup steps)
- **VENDOR-SIEMENS-WCC-001:** WinCC HMI (STOP button operation)

**Document ID:** SAFE-ROB-001  
**Revision:** A  
**Last Updated:** 2026-03-19  
**Critical Safety Document — Review Annually**  
**Next Review:** 2027-03-19
