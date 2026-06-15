# Conveyor Jam Root Cause Analysis (RCA-CON-001)

**Investigation Date:** 2026-03-14  
**Equipment:** Conveyor System A (SEW MOVIGEAR Drive Motor)  
**Line:** Packaging Line 4  
**Downtime:** 47 minutes (13:45–14:32 UTC)  

---

## Executive Summary

Repeated conveyor jams caused significant downtime. Primary causes: mechanical misalignment of guideways combined with accumulated material buildup, AND timing drift in upstream robotic infeed control. The SEW motor coupling showed minor misalignment, indicating bearing wear or mounting shift.

---

## Root Cause Findings

### Cause #1: SEW Motor Coupling Misalignment

**Finding:** Dial indicator test measured 0.08 mm radial runout at coupling face (limit: 0.05 mm per VENDOR-SEW-MG-001)

**Evidence:**
- Uneven wear pattern visible on both coupling halves
- Motor housing vibration elevated during 30% speed trial
- Bearing temperature normal, bearing sound slightly irregular

**Reference:** VENDOR-SEW-MG-001 (Section 3: Motor Coupling Alignment)

### Cause #2: Accumulated Cardboard Dust

**Finding:** ~300 mL of fine cardboard particles collected in transfer plate trough

**Evidence:**
- Visible 5 mm accumulation across 1.2 m length
- Increased product drag by 15–20%
- Combined with misalignment, created jam risk

### Cause #3: Robot Infeed Timing Drift

**Finding:** Release signal drifted +45 ms over 2 hours (logged via S7-1500 diagnostics)

**Evidence:**
- Expected: 250 ms ±10 ms timing window
- Actual: 258 ms drifting to 303 ms
- Lateral product momentum + misaligned sideguide increased binding risk

**Reference:** VENDOR-FANUC-CRX-001 (Section 1: Safeguarding Zones, timing)

---

## Corrective Actions

1. **Coupling realignment to 0.03 mm runout** – Reference: VENDOR-SEW-MG-001 (Section 3)
2. **Transfer plate cleaning + vacuum integration**
3. **Robot timing recalibration** + 5-part trial run mandate per startup SOP
4. **Quarterly coupling alignment verification** added to maintenance schedule
5. **Post-recipe-change verification** added to PL4-001 Startup SOP

---

## Document References

- VENDOR-SEW-MG-001 (coupling alignment procedures)
- VENDOR-FANUC-CRX-001 (robot timing/safety)
- VENDOR-SIEMENS-S7-001 (cycle time monitoring)
- SOP-PL4-001 (enhanced startup verification)

**Completed:** 2026-03-14
