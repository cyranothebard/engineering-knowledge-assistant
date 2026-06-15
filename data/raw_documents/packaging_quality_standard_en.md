# Packaging Quality Standard (QSTD-PL4-001)

**Scope:** Packaging Line 4 – All Product Families  
**Quality Systems:** Cognex InSight 7010 (Vision), SICK Multiscan14 (Dimensional)  
**Control System:** Siemens S7-1500 + WinCC  

---

## Purpose

Defines quality acceptance criteria for Packaging Line 4 output, specifying measurement methods, tolerance limits, and escalation conditions. All criteria are verified using the on-line automated inspection systems unless stated otherwise.

---

## Quality Parameters

### 1. Seal Integrity

**Method:** Seal force measured by in-line load cell (hardwired to S7-1500 analog input)  
**Specification:**
- Nominal seal force: 45–55 N (per product specification sheet)
- Lower Specification Limit (LSL): 40 N (auto-reject below this)
- Upper Specification Limit (USL): 65 N (auto-reject above this; potential overheat)

**Monitoring:**
- Seal force displayed in real-time on WinCC HMI → Process Data → Seal Monitoring
- Reference: VENDOR-SIEMENS-WCC-001 (Section 3: Numeric Input Fields – live trend display)

**Escalation:**
- >3 consecutive rejects on seal: Stop line; contact Process Engineering within 10 min

### 2. Label Position Tolerance

**Method:** Cognex InSight 7010 vision inspection (edge detection, pixel-to-mm calibration)  
**Specification:**
- Label center position: ±1.5 mm from nominal (X and Y axes)
- Rotation: ±1.0° from nominal

**Measurement:**
- Pixel-to-mm mapping from camera calibration (accurate to ±0.1 mm at working distance)
- Reference: VENDOR-COGNEX-INS-001 (Section 3: Camera Calibration – pixel-to-mm mapping)

**Escalation:**
- >5 label-position rejects in 50 parts: Verify camera calibration and recipe  
- Reference: VENDOR-COGNEX-INS-001 (Section 4: False Reject Diagnosis)

### 3. Dimensional Limits (Package Height/Width)

**Method:** SICK Multiscan14 laser dimensional measurement  
**Specification:**
- Package height: Nominal ± 3.0 mm (product-specific; set in active recipe)
- Package width: Nominal ± 2.0 mm
- Measurement repeatability must be ≤±0.05 mm for all measurements to be valid

**Measurement:**
- SICK Multiscan14 takes 25 Hz continuous measurements along package travel
- Average of 5 measurements per package reported to S7-1500
- Reference: VENDOR-SICK-MS-001 (Section 1: Measurement Principles)

**Pre-condition:** Sensor calibration valid (timestamp <7 days, per SOP-LAS-001)
- If calibration expired: Dimensional data is NOT valid for quality release
- Reference: SOP-LAS-001 (Section: Recalibration Schedule)

**Escalation:**
- Measurement repeatability >±0.1 mm: Calibration required immediately; hold lot
- Reference: VENDOR-SICK-MS-001 (Section 2: Calibration Procedure)

### 4. Vision Inspection False Reject Rate

**Method:** Automated tracking via Cognex InSight 7010; reported to WinCC batch report  
**Target:** False reject rate < 2.0% per batch  
**Critical threshold:** > 5.0% in any 30-minute window triggers mandatory investigation

**Definition:**
- False reject: Good part marked as "reject" by vision system
- True reject: Part with confirmed quality defect
- False reject rate = False rejects / (True rejects + False rejects) × 100%

**Common causes of elevated false rejects (per RCA-VIS-002):**
- Backlight intensity below 42% nominal
- Camera focus drift after format change
- Wrong inspection recipe active
- Reference: VENDOR-COGNEX-INS-001 (Section 2–3) and RCA-VIS-002

**Escalation:**
- > 2% false reject rate: Contact Quality Engineering within 30 min
- > 5% false reject rate: Stop line; mandatory investigation before restart

---

## First Article Inspection

**Mandatory after:**
- Line startup (per SOP-PL4-001, Stage 5)
- Format/SKU changeover
- Maintenance work affecting inspection systems
- After any alarm condition that triggered automatic line stop

**First Article Requirements:**

| Check | Method | Acceptance |
|-------|--------|------------|
| Visual inspection | Manual (trained Quality personnel) | No visible defects |
| Seal integrity | Load cell reading | 40–65 N |
| Label position | Manual gauge OR vision system | ±1.5 mm, ±1.0° |
| Dimensional check | Laser + manual verification | Within dimensional spec |
| Cognex recipe active | Verify SKU in camera status | Matches production order |

**Release authority:** Quality Engineer or designated Quality Technician

**Escalation:**
- If 2 consecutive first articles fail: **Production blocked** until Quality Engineering releases
- Reason must be documented in WinCC logbook and Quality non-conformance system
- Reference: VENDOR-SIEMENS-WCC-001 (Section 4: Data Entry – validation workflow)

---

## In-Process Sampling Plan

**Frequency:** Every 30 minutes during production  
**Sample size:** 3 units per sample

| Parameter | Measurement Method | Frequency |
|-----------|-------------------|-----------|
| Seal integrity | Load cell (automated, continuous) | Every part |
| Label position | Cognex InSight (automated, continuous) | Every part |
| Package dimensions | SICK Multiscan14 (automated, continuous) | Every part |
| Visual cosmetics | Manual inspection by operator | 3 parts / 30 min |

**Automatic Rejection:**
- Any parameter outside specification triggers automatic reject gate (S7-1500 controlled)
- Rejected parts physically diverted to reject chute (separate from conforming output)
- All rejections logged in WinCC batch report with timestamp and rejection code

---

## End-of-Batch Quality Release

**Required data for batch release:**
1. WinCC batch report exported and reviewed by Quality Technician
2. Total reject count and false reject rate within specifications
3. First article approval documented
4. Seal, label, and dimension capability statistics within control limits

**Release path:**
- Quality Technician signs batch release form
- Products can be transferred to warehouse/dispatch
- Batch report archived to: //Manufacturing/Quality/PL4_Batch_Reports/

---

## Document References

- **VENDOR-COGNEX-INS-001:** Cognex InSight Vision System (calibration, recipe, false reject patterns)
- **VENDOR-SICK-MS-001:** SICK Multiscan14 (dimensional specifications, repeatability)
- **VENDOR-SIEMENS-WCC-001:** WinCC HMI (batch reporting, alarm display)
- **VENDOR-SIEMENS-S7-001:** S7-1500 (automatic rejection control, analog inputs)
- **SOP-LAS-001:** Laser calibration procedure (calibration validity)
- **SOP-PL4-001:** Startup SOP (first article context)
- **RCA-VIS-002:** Vision false reject investigation (causes and remedies)

**Document ID:** QSTD-PL4-001  
**Revision:** B  
**Last Updated:** 2026-03-20  
**Next Review:** 2026-09-20
