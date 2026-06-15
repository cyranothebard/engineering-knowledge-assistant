# Untersuchung Vibrationsalarm Packaging Line 4 (RCA-PL4-003)

**Datum:** 2026-03-16  
**Geraet:** SEW MOVIGEAR Antriebsmotor – Foerderband System A  
**Linie:** Packaging Line 4  
**Stillstandsdauer:** 38 Minuten (09:12–09:50 UTC)  

---

## Zusammenfassung

Wiederholte Vibrationsalarme an Packaging Line 4 fuehrten zu ungeplanten Stillstand. Drei unabhaengige mechanische Ursachen identifiziert, alle am SEW MOVIGEAR Antriebsstrang.

---

## Ereignisverlauf

| Uhrzeit | Ereignis |
|---------|----------|
| 08:45 | Erster Vibrationsalarm im WinCC HMI (Warnstufe gelb) |
| 09:00 | Zweiter Alarm, Schwingungsamplitiude angestiegen |
| 09:12 | Sicherheitsabschaltung (Alarmstufe rot) – Linie automatisch gestoppt |
| 09:50 | Linie nach Instandsetzung wieder in Betrieb |

**Alarmcode (S7-1500):** 0x8110 – Analogeingang Ueberbereich (Schwingungssensor ueberschritten Messgrenze)  
Referenz: VENDOR-SIEMENS-S7-001 (Abschnitt 2: Alarmcode 0x8110)

---

## Ursache 1: Lagerverschleiss auf der Antriebsseite

**Befund:** Foerderbandlager links zeigt sichtbaren Abrieb und Laufgeraeusch (Schleifen bei manuellem Drehen)

**Nachweis:**
- Lagertemperatur: 74 °C (Grenzwert: 80 °C, bereits erhoehter Bereich)
- Visuell: Abriebstaub an Lagerdeckel (schwarzes Pulver = Graphitabrieb)
- Laufgeraeusch: Metallisches Schleifen bei 1 Umdrehung pro Sekunde

**Mechanismus:**
- Lager laeuft seit letzter Instandhaltung 820 Stunden (Grenzwert: 500 Stunden)
- Schmierfettversorgung nicht fristgerecht erfolgt (Wartungslog zeigt Luecke)
- Referenz: VENDOR-SEW-MG-001 (Abschnitt 1: Schmierstoffintervall – max. 500 h)

**Massnahme:** Lager getauscht; Referenzwert nach Lagerwechsel gemessen: Temperatur 41 °C (normal)  
Referenz: VENDOR-SEW-MG-001 (Abschnitt 2: Lagerwechselverfahren)

---

## Ursache 2: Unwucht nach Rollenwechsel

**Befund:** Antriebsrolle zeigt 0.12 mm radiales Spiel (Grenzwert: 0.05 mm)

**Nachweis:**
- Messung mit Messuhr: 0.12 mm TIR (Total Indicated Runout) an Kupplung
- Bei niedrigen Drehzahlen sichtbares Taumeln (beobachtbar ohne Messmittel)

**Mechanismus:**
- Rollenwechsel wurde ohne Ausrichtprotokoll durchgefuehrt
- Schimpack-Anpassung (Unterlagsbleche) fehlt → Rolle hoehengemaess versetzt eingebaut
- Unwucht addiert sich zu Lagerverschleiss → kombinierter Effekt verstaerkte Vibration
- Referenz: VENDOR-SEW-MG-001 (Abschnitt 3: Kupplungsausrichtung – Grenzwert 0.05 mm)

**Massnahme:** Ausrichtung mit Messuhr auf 0.03 mm korrigiert; Schimpack angepasst  
Referenz: VENDOR-SEW-MG-001 (Abschnitt 3: Ausrichtmessverfahren)

---

## Ursache 3: Lose Motorbefestigung

**Befund:** Zwei von vier Befestigungsschrauben des SEW Motors waren nicht mit Sollanzugsdrehmoment angezogen

**Nachweis:**
- Visuelle Inspektion: Schrauben mit Drehmomentschluessel geprueft
- Soll: 18 Nm (Typenschild am Motor)
- Ist: Schraube 3 = 9 Nm, Schraube 4 = 11 Nm (beide deutlich zu niedrig)

**Mechanismus:**
- Lose Befestigung erhoehte Motorvibrationen auf Rahmen
- Resonanzfrequenz verschob sich in Betriebsdrehzahlbereich
- Referenz: VENDOR-SEW-MG-001 (Abschnitt 2: Lagerwechsel – Anzugsmoment-Spezifikation)

**Massnahme:** Alle vier Schrauben mit 18 Nm angezogen und mit Sicherungslack gesichert

---

## Korrektive Massnahmen

### Sofortmassnahmen (erledigt)
1. Lager getauscht – Referenz VENDOR-SEW-MG-001 Abschnitt 2
2. Kupplungsausrichtung korrigiert – Referenz VENDOR-SEW-MG-001 Abschnitt 3
3. Motorbefestigung auf 18 Nm angezogen
4. Schwingungswert nach Instandsetzung gemessen und dokumentiert (Basis: 0.8 mm/s)

### Praeventive Massnahmen (innerhalb 2 Wochen)
1. **Schmierplan aktualisieren:** Lagerwechsel alle 500 h (bisher nicht konsequent eingehalten)
   - Referenz: VENDOR-SEW-MG-001 (Abschnitt 1: Schmierplan)
2. **Rollenwechsel-Checklistestandard:** Ab sofort Ausrichtprotokoll bei jedem Rollenwechsel
   - Grenzwert: < 0.05 mm TIR
   - Referenz: VENDOR-SEW-MG-001 (Abschnitt 3)
3. **Drehmomentkontrolle in PM-Plan:** Motorbefestigung alle 6 Monate auf Anzugsmoment pruefen
   - Sollwert am Motorschild
4. **WinCC Alarmschwelle fuer Vibration:** Warnung bei 1.5 mm/s statt bisher 2.5 mm/s
   - Fruehzeitigere Erkennung von Schwingungsanstieg
   - Referenz: VENDOR-SIEMENS-WCC-001 (Abschnitt 2: Alarmschwellen konfigurieren)

---

## Erkenntnisse

1. **Mehrere Ursachen wirkten zusammen:** Jede Einzelursache haette die Anlage moeglicherweise nicht gestoppt – die Kombination war kritisch.
2. **Wartungsdokumentation ist entscheidend:** Schmierfettluecke war im Wartungslog sichtbar, aber nicht eskaliert worden.
3. **Spezifikationen aus Herstellerdokumentation verwenden:** Anzugsmomente und Ausrichtgrenzen aus VENDOR-SEW-MG-001 sind verbindlich – nicht schaetzen.

---

## Referenzierte Dokumente

- **VENDOR-SEW-MG-001:** SEW MOVIGEAR Instandhaltungshandbuch (Schmierung, Lager, Ausrichtung)
- **VENDOR-SIEMENS-S7-001:** S7-1500 Diagnosereferenz (Alarmcode 0x8110)
- **VENDOR-SIEMENS-WCC-001:** WinCC Bedienhandbuch (Alarmschwellen)
- **SOP-PL4-001:** Anlaufverfahren (erweiterte Motorpruefung bei Start)

**Untersuchung abgeschlossen:** 2026-03-16  
**Genehmigt von:** Instandhaltungsleiter  
**Naechste Pruefung:** 2026-06-16
