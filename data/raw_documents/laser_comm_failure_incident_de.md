# Stoerfall Laser Kommunikation (INC-LAS-001)

**Datum:** 2026-03-21  
**Betroffene Geraete:** SICK Multiscan14 Laser + SCALANCE X312 Switch + Siemens S7-1500  
**Netzwerk:** EtherCAT ueber industrielles Ethernet  
**Ausfallzeit:** 90 Sekunden (11:23:15 – 11:24:45 UTC)  

---

## Ereignisbeschreibung

Die Laser Dimensioning Station verlor waehrend laufender Produktion die Kommunikation zum S7-1500 PLC. Messdaten wurden fuer 90 Sekunden nicht uebertragen. Die Linie wurde automatisch verlangsamt (S7-1500 Sicherheitsfunktion bei EtherCAT-Timeout).

---

## Zeitlinie

| Uhrzeit | Ereignis |
|---------|---------|
| 11:23:15 | EtherCAT Slave-Timeout am S7-1500 (Laser-Slave reagiert nicht mehr) |
| 11:23:18 | WinCC HMI Alarm: "Laser: Kommunikation unterbrochen" (orange) |
| 11:23:22 | S7-1500 Sicherheitsfunktion: Foerderbandgeschwindigkeit auf 50 % reduziert |
| 11:24:30 | Operator prueft Kabelverbindung am SCALANCE X312 – M12-Stecker am Laser leicht gelockert |
| 11:24:38 | M12-Stecker fest eingrastend (hoerbares Einrasten) |
| 11:24:45 | Kommunikation wiederhergestellt – WinCC zeigt "Laser: ONLINE" |
| 11:25:10 | Linie wieder auf 100 % hochgefahren |

---

## Technische Ursache

### Primaere Ursache: Gelockerter M12-Stecker

**Befund:** M12-Stecker am EtherCAT-Eingang des SICK Multiscan14 war nicht vollstaendig eingerastet

**Nachweis:**
- Stecker sass ohne hoerbares Einrasten – 1,5 mm zu weit aussen
- Kein Kabelsicherungsbuegel montiert (Zugentlastung fehlte)
- SCALANCE X312 Port-LED fuer Laser-Port: Blinkte orange (intermittierend, kein stabiler Link)
- Referenz: VENDOR-SICK-MS-001 (Abschnitt 3: Elektrische Schnittstelle – M12 Steckertyp)
- Referenz: VENDOR-ECAT-NET-001 (Abschnitt 2: Physikalische Schicht – LED-Zustand orange = instabil)

**Mechanismus:**
- Vibrationen waehrend Produktionsbetrieb lockerten den nicht gesicherten M12-Stecker
- Kontaktunterbrechung im Stecker fuehrte zu EtherCAT Frame-Fehlern
- S7-1500 EtherCAT-Master registrierte Timeout (Konfiguriert: 100 ms)
- Sicherheitsfunktion aktiviert: Geschwindigkeit reduziert, Alarm ausgegeben
- Referenz: VENDOR-SIEMENS-S7-001 (Abschnitt 3: EtherCAT Slave Kommunikations-Timeout)

### Begleitende Ursache: Fehlende Zugentlastung

**Befund:** M12-Kabel am Laser laeuft ohne Zugentlastungsklemme frei durch den Kabelkanal

**Nachweis:**
- Kabelkanal zeigt Biegeradius < 3 x Kabeldurchmesser (Mindest: 4 x laut Spezifikation)
- Referenz: VENDOR-SICK-MS-001 (Abschnitt 3: Kabelspezifikation – Mindestbiegeradius)

**Massnahme:** Zugentlastungsschellen montiert; Kabelfuehrung mit ausreichendem Biegeradius verlegt

---

## Netzwerkdiagnose

Waehrend des Stoerfalls geloggter EtherCAT-Status (via TIA Portal Diagnosepuffer):

```
Frame Error Rate:  18 % (Grenzwert: < 1 %) -- KRITISCH
Slaves Configured: 4
Slaves Discovered: 3  (Laser-Slave fehlend)
Cycle Time:        14 ms (Soll: 10 ms)  -- Verzoegerung durch Retry-Mechanismus
Transmission Errors: 142 in letzten 1000 Frames
```

Referenz: VENDOR-ECAT-NET-001 (Abschnitt 3: EtherCAT Master Diagnostik – Schwellwerte)

---

## Sofortmassnahmen (waehrend Stoerfall)

1. Linie auf reduzierte Geschwindigkeit gesetzt (automatisch durch S7-1500)
2. Operator informierte Controls Engineering (telefonisch, 11:23:30)
3. Kabelverbindung am SCALANCE Switch visuell geprueft
4. M12-Stecker am Laser gefunden und eingerastet
5. Verbindung wiederhergestellt, Linie hochgefahren
6. Stoerfall im WinCC Tagesprotokoll dokumentiert

---

## Korrektive und Praeventive Massnahmen

| Massnahme | Umsetzung | Referenz | Status |
|-----------|-----------|----------|--------|
| M12-Stecker am Laser vollstaendig einrasten und Sicherungsring schliessen | Sofort | VENDOR-SICK-MS-001 Abschnitt 3 | Erledigt |
| Zugentlastungsschelle am Laserkabel montieren | Sofort | VENDOR-SICK-MS-001 Abschnitt 3 | Erledigt |
| Kabelbiegeradius auf > 4 x Kabeldurchmesser korrigieren | Innerhalb 1 Tag | VENDOR-ECAT-NET-001 Abschnitt 2 | Erledigt |
| Anlaufpruefung: M12-Stecker am Laser in Checkliste aufnehmen | Innerhalb 1 Woche | SOP-PL4-001 | In Bearbeitung |
| SCALANCE Port fuer Laser auf Fehlerrate ueberwachen (Schwellwert 1 %) | Innerhalb 2 Wochen | VENDOR-ECAT-NET-001 Abschnitt 3 | Geplant |
| Alle M12-Kabelstecker an PL4 auf Zugentlastung pruefen | Innerhalb 1 Monat | VENDOR-SICK-MS-001 | Geplant |

---

## Erkenntnisse

1. **Kleine mechanische Maengelkoennen grosse Auswirkungen haben:** 1,5 mm lockerer Stecker fuehrte zu 90 Sekunden Produktionsunterbrechung.
2. **Herstellerspezifikationen fuer Kabelverlegung beachten:** Mindestbiegeradius und Zugentlastung sind in VENDOR-SICK-MS-001 klar definiert – nicht vernachlaessigen.
3. **EtherCAT-Diagnose liefert schnelle Ursachenfindung:** Frame-Error-Rate und Slave-Count als erste Diagnoseschritte sehr effizient.

---

## Referenzierte Dokumente

- **VENDOR-SICK-MS-001:** SICK Multiscan14 Technische Referenz (Steckertyp, Kabelspezifikation)
- **VENDOR-ECAT-NET-001:** Industrial Ethernet Troubleshooting (LED-Zustande, Frame-Error-Raten)
- **VENDOR-SIEMENS-S7-001:** S7-1500 Diagnosereferenz (EtherCAT Timeout, Alarmcodes)
- **VENDOR-SIEMENS-WCC-001:** WinCC Bedienhandbuch (Alarmdarstellung)
- **SOP-PL4-001:** Anlaufverfahren (M12-Pruefung in Checkliste)

**Stoerfall dokumentiert am:** 2026-03-21  
**Erstellt von:** Automatisierungstechnik  
**Genehmigt von:** Controls Engineering Lead
