# Lockout Tagout Verfahren Lindau (SAFE-SITE-001)

**Geltungsbereich:** Packaging Line 4 – alle Energietraeger  
**Sicherheitsnorm:** EN ISO 13849-1 (Sicherheitsfunktionen), DGUV Vorschrift 3  
**Gilt fuer:** Siemens S7-1500, SEW MOVIGEAR Antriebe, FANUC CRX-10iA Roboter, Druckluftsystem  

---

## Zweck

Energieisolierung vor Wartungsarbeiten, Reinigung oder Eingriff in Gefahrenbereiche. Verhindert unbeabsichtigte Inbetriebnahme und schuetzt wartende Personen vor gefaehrlichen Energiequellen.

---

## Energietraeger auf Packaging Line 4

| Energietraeger | Quelle | Absperrvorrichtung | Ort |
|----------------|--------|--------------------|-----|
| Elektrik 400 V AC | Hauptverteiler | Hauptschalter Q1 | Schaltschrank, Tuer links |
| Steuerspannung 24 V DC | S7-1500 Netzteil | Sicherung F1–F6 | Schaltschrank, Reihe 3 |
| Druckluft 6 bar | Druckluftversorgung | Absperrventil MV-001 | Backbone-Panel, beschriftet |
| Roboterenergie | FANUC CRX Steuerung | E-Stop + Schluessel | Robotersteuerschrank, rote Taste |
| Antriebsenergie | SEW MOVIGEAR | Gemeinsam mit 400 V | Hauptschalter Q1 |

**Referenz Roboterabsicherung:** VENDOR-FANUC-CRX-001 (Abschnitt 2: Not-Aus-System)

---

## Verantwortlichkeiten

| Rolle | Aufgabe |
|-------|---------|
| Ausfuehrender Techniker | Eigenes Schloss anlegen; Null-Energie-Zustand pruefen |
| Schichtfuehrender | Freigabe fuer Anlagenstopp erteilen |
| Qualitaet / Produktion | Sicherstellung, dass kein laufender Auftrag unterbrochen wird |
| Controls Engineering | Unterstuetzung bei elektrischer Energieverifikation |

---

## Verfahren

### Schritt 1: Anlage anhalten und Freigabe einholen (2 Minuten)

1. Schichtfuehrender ueber geplante Wartung informieren
2. Produktionsauftrag abschliessen oder unterbrechen (kein Material in Maschine)
3. Anlage ueber WinCC HMI sicher stoppen:
   - Foerdergeschwindigkeit auf 0 % reduzieren
   - Warten bis alle Antriebe gestoppt (Status "GESTOPPT" im HMI)
   - Referenz: VENDOR-SIEMENS-WCC-001 (Abschnitt 3: STOPP-Taste Funktion)
4. Schriftliche Freigabe vom Schichtfuehrenden einholen (Formular F-SAFE-01)

### Schritt 2: Energiequellen identifizieren (2 Minuten)

1. Anlage entsprechend Energiequellentabelle (oben) begehen
2. Alle relevanten Energiequellen fuer den Arbeitsbereich markieren
3. Wenn Roboterzelle betroffen:
   - Zusaetzlich FANUC E-Stop identifizieren (rote Taste am Robotersteuerschrank)
   - Referenz: VENDOR-FANUC-CRX-001 (Abschnitt 2: E-Stop-Tastenstandorte)

### Schritt 3: Energiequellen abschalten und verriegeln (3 Minuten)

1. **Hauptschalter Q1 abschalten** (400 V AC + 24 V DC + SEW-Antriebe)
   - Schalter in Stellung OFF drehen
   - Schaltschloss (Vorhangschloss) in Bohrung des Schaltergriffs einfuehren
   - Eigenes Schloss einsperren (NICHT das Schloss eines Kollegen)
   - Namensschild am Schloss befestigen (Pflicht – gesetzliche Anforderung)

2. **Druckluft absperren** (Ventil MV-001)
   - Ventilgriff in Stellung GESPERRT drehen
   - Klemmschloss an Ventilgriff befestigen

3. **Roboter E-Stop sichern** (wenn Roboterzelle betroffen)
   - E-Stop-Taste am Steuerschrank gedrueckt halten lassen
   - Schloss auf E-Stop-Sammeleinrichtung anlegen
   - Referenz: VENDOR-FANUC-CRX-001 (Abschnitt 4: Zelleintrittsverfahren)

### Schritt 4: Restenergie abbauen und Null-Energie-Zustand pruefen (3 Minuten)

1. **Elektrisch:**
   - Pruefgeraet (Spannungspruefer, Kategorie CAT III) an Schaltschrankeingang halten
   - Messung an L1, L2, L3 gegen PE: Alle < 10 V AC (Nullenergie bestaetigt)
   - Warten Sie mindestens 30 Sekunden nach dem Abschalten (Kondensatoren im S7-1500 Netzteil entladen sich)
   - Referenz: VENDOR-SIEMENS-S7-001 (Abschnitt: Wiederanlauffverfahren – Kondensatorentladung)

2. **Druckluft:**
   - Ablasshahn am Ende der Druckluftleitung oeffnen
   - Warten bis Manometer auf 0 bar abfaellt (typisch 10–15 Sekunden)
   - Ventil schliessen

3. **Roboterenergie:**
   - Pruefen, ob Roboterarm per Hand bewegt werden kann
   - Arm darf sich NICHT bewegen (elektromechanische Bremse muss eingerastet sein)
   - Wenn Arm beweglich: NICHT eingreifen; Elektriker benachrichtigen (Bremsenausfall)
   - Referenz: VENDOR-FANUC-CRX-001 (Abschnitt 2: Reaktion auf E-Stop)

### Schritt 5: Eingriff durchfuehren

1. Null-Energie-Zustand verifiziert → Eingriff kann beginnen
2. Waehrend des Eingriffs: Schloss verbleibt am Absperrpunkt (darf nicht entfernt werden)
3. Wenn weitere Personen an der Anlage arbeiten: Jede Person legt eigenes Schloss an
4. Bei Arbeiten in der Roboterzelle: Zusaetzlich SAFE-ROB-001 beachten

### Schritt 6: Wiederinbetriebnahme nach Abschluss der Arbeiten

1. Alle Werkzeuge und Materialien aus dem Arbeitsbereich entfernen
2. Sicherheitsbereiche absuchen – keine Personen mehr in der Anlage?
3. Jede Person entfernt **nur ihr eigenes Schloss** (Schluesselprinzip)
4. Schriftliche Meldung an Schichtfuehrenden: "Wartung abgeschlossen, Anlage freigegeben"
5. Anlage entsprechend SOP-PL4-001 (Anlaufverfahren) wiederanfahren

---

## Besondere Situationen

**Schloss verloren oder Schluessel defekt:**
- Verantwortliche Person muss anwesend sein
- Schloss kann nur durch Werksschutz aufgebrochen werden (dokumentationspflichtig)
- Niemals Schloss eines Kollegen ohne dessen Anwesenheit entfernen

**Mehrere Teams gleichzeitig:**
- Gruppenverriegelungsbox verwenden (Box aufhaengen; alle Teams haengen eigene Schloesser ein)
- Anlage bleibt gesperrt, solange IRGENDEIN Schloss eingehaengt ist

**Roboter-Sondersituation (Zelleintritt):**
- Zusaetzlich SAFE-ROB-001 (Robot Cell Entry Procedure) vollstaendig durchfuehren
- Referenz: VENDOR-FANUC-CRX-001 (Abschnitt 4: LOTO und Zelleintritt)

---

## Referenzierte Dokumente

- **VENDOR-FANUC-CRX-001:** FANUC CRX-10iA Sicherheitsreferenz (E-Stop, Bremsen, LOTO)
- **VENDOR-SIEMENS-WCC-001:** WinCC Bedienhandbuch (Anlage sicher stoppen)
- **VENDOR-SIEMENS-S7-001:** S7-1500 Diagnose (Kondensatorentladung, Wiederanlauf)
- **SAFE-ROB-001:** Zelleintrittsverfahren Roboter (ergaenzendes Sicherheitsverfahren)
- **SOP-PL4-001:** Anlaufverfahren Packaging Line 4 (Wiederinbetriebnahme)

**Dokumenten-ID:** SAFE-SITE-001  
**Revision:** C  
**Letzte Aktualisierung:** 2026-03-18  
**Kritisches Sicherheitsdokument – jaehrliche Pruefpflicht**  
**Naechste Pruefung:** 2027-03-18
