# Vision False Reject Investigation (RCA-VIS-002)

**Investigation Date:** 2026-03-15  
**Equipment:** Cognex InSight 7010 Vision Camera  
**Line:** Packaging Line 4  
**Duration of False Rejects:** 2.5 hours (10:00–12:30 UTC)  
**Impact:** 47 conforming packages rejected; batch hold risk  

---

## Executive Summary

Vision inspection false reject rate spiked from <1% baseline to 8.3%. Three independent causes, acting together:

1. **Backlight intensity dropped below validated range** (optical degradation)
2. **Camera focus drifted after SKU format change** (mechanical drift)
3. **Wrong inspection recipe remained active after format change** (procedural gap)

All three factors combined created the acute failure condition.

---

## Root Cause #1: Backlight Intensity Drift

**Finding:** Backlight LED measured at 38% nominal (spec: 42–48%)

**Evidence:**
- Live image appeared dim vs. baseline reference image
- Image histogram skewed left (darker pixels overrepresented)
- Camera auto-exposure extended from 3.2 ms to 5.1 ms (+59%)
- Higher exposure introduced motion blur on fast product motion

**Root cause:** Loose M4 fastener on light fixture allowed tilt of 3–4°, reducing effective light coverage by ~12%

**Reference:** VENDOR-COGNEX-INS-001 (Section 2: Lighting Setup & Troubleshooting)

**Resolution:** Tightened all fasteners; intensity returned to 46% nominal

---

## Root Cause #2: Camera Focus Drift

**Finding:** Focus ring rotated ~0.5 mm from locked position after recipe format change

**Evidence:**
- Operator manually adjusted focus for Box Type B (55 mm) after Type A (50 mm) changeover
- Did NOT re-lock focus ring with set-screw after adjustment
- Vibration during high-speed operation caused gradual 0.5 mm drift
- At 250 mm working distance, this ~5 mm blur circle at image plane

**Mechanism:**
- Box Type B has glossy label surface vs. Type A matte cardboard
- Out-of-focus image reduced label edge contrast
- Edge-detection algorithm became sensitive to subtle print variance
- False rejects triggered on normal label registration

**Reference:** VENDOR-COGNEX-INS-001 (Section 1: Optical Alignment & Focus)

**Resolution:** Re-locked focus ring, verified focus on Type B sample (Focus Assist >85%)

---

## Root Cause #3: Wrong Inspection Recipe Active

**Finding:** Recipe "BoxType A" remained active on camera while HMI displayed "Type B"

**Evidence:**
- HMI Product Selector showed "Type B" (correct)
- Camera active recipe showed "BoxA_Inspection_v2" (wrong)
- Recipe download did not complete (user cancelled after ~3 seconds, assuming done)

**Root cause:** Procedural—Recipe download is asynchronous (5–8 seconds typical). User impatience created race condition.

**Recipe mismatch cascade:**
- Type A recipe looks for sharp 90° label corners
- Type B boxes have 8 mm rounded corners
- Type A recipe applied to Type B sees rounded corners as "defect" → reject triggered

**Reference:** VENDOR-COGNEX-INS-001 (Section 3: Common Reject Patterns)

**Resolution:** Modified HMI recipe-change logic:
  - Added "Recipe Downloading..." progress bar
  - Disabled convey START button until recipe confirmed
  - Added mandatory 5-part trial run post-recipe-change

---

## Corrective Actions

### Immediate (Done)
- Tightened backlight fixture fasteners; intensity restored
- Re-locked focus ring; verified focus quality
- Reloaded correct recipe with full download confirmation
- Manually inspected 47 rejected packages; all conforming (released)

### Short-Term (1–2 weeks)
- WinCC recipe-change safety: Progress bar + START button lock
- Backlight quarterly inspection: Check LED intensity (42–48%), tighten fasteners
- Shift-start checklist: Verify focus-ring lock set-screw tight
- Added new verification step to PL4-001 Startup SOP

### Long-Term (1–3 months)
- Preventive LED replacement at 3,000 operating hours
- Training update: Recipe download timing, verification importance
- Review firmware upgrade (Cognex v7.2) for improved recipe-sync reliability

---

## Process Improvements

| Improvement | Benefit | Complexity |
|-------------|---------|------------|
| Auto-disable START during recipe download | Prevents user impatience race condition | Low |
| Progress bar visibility | Clear feedback to operator | Low |
| Mandatory trial run post-recipe-change | Detects mismatch before production | Medium |
| Quarterly backlight inspection | Proactive LED aging management | Low |
| Focus-ring lock daily verification | Mechanical stability assurance | Low |

---

## Document References

- VENDOR-COGNEX-INS-001 (calibration, troubleshooting, lighting)
- SOP-PL4-001 (startup procedure—new recipe verification)
- SOP-PL4-002 (sensors section)
- Robot_cell_entry_en.md (focus verification added)

**Investigation completed:** 2026-03-15  
**Approved by:** Manufacturing Engineering Manager
