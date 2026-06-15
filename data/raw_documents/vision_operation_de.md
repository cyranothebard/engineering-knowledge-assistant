# Bedienung Vision Inspection Cell (SOP-VIS-001)

**Geraet:** Cognex InSight 7010 Kamerasystem  
**Steuerung:** Siemens WinCC HMI + S7-1500 PLC  
**Netzwerk:** EtherCAT ueber SCALANCE X312 Switch  

---

## Zweck

Sicherer und reproduzierbarer Betrieb der Vision Inspection Cell fuer die Serienfertigung auf Packaging Line 4. Stellt sicher, dass alle Pruefergebnisse rueckverfolgbar und rezeptkonfrom sind.

---

## Voraussetzungen vor dem Start

- [ ] Kamera-LED am Geraet: GRUEN (Betrieb normal)
  - Referenz: VENDOR-COGNEX-INS-001 (Abschnitt 5: Zustandsanzeigen)
- [ ] WinCC HMI zeigt "Vision: ONLINE" und Kameratemperatur 35–50 °C
- [ ] Aktives Produktrezept mit Produktionsauftrag vergleichen (SKU-Nummer pruefen)
- [ ] Beleuchtungsintensitaet pruefen: Sollwert 42–48 % (sichtbar im HMI unter Vision Diagnose)
  - Referenz: VENDOR-COGNEX-INS-001 (Abschnitt 2: Beleuchtung)
- [ ] Kameraoptik visuell pruefen: keine Verschmutzung, kein Beschlag auf der Linse
- [ ] Fokusringschraube sitzt fest (Sichtpruefung – Schraube muss buerdig sein)
  - Referenz: VENDOR-COGNEX-INS-001 (Abschnitt 1: Optische Ausrichtung)

---

## Betriebsablauf

### Schritt 1: Vision Cell im HMI aktivieren

1. WinCC HMI → Vision → Werkzeugstatus → AKTIVIEREN
2. Warten bis HMI "Rezept laden..." abgeschlossen zeigt (5–8 Sekunden)
   - **Wichtig:** Linie NICHT starten, bevor Rezeptdownload bestaetigt ist
   - Grund: Asynchroner Download – unvollstaendiges Rezept fuehrt zu Falschausschleusungen
   - Referenz: VENDOR-COGNEX-INS-001 (Abschnitt 3: Haeufige Ausschleusungsmuster)
3. Status im HMI: "Vision: BEREIT" (gruen)

### Schritt 2: Livebild pruefen

1. WinCC HMI → Vision Diagnose → Livebild
2. Bild auf folgende Punkte pruefen:
   - Schaerfe: Konturlinien klar und nicht verwaschen
   - Helligkeit: Histogram gleichmaessig verteilt, keine Ueberbelichtung (weisse Bereiche)
   - Referenzkontur: Inspektionsrahmen liegt auf dem Referenzobjekt
3. Focus-Assist-Wert ablesen (sollte > 80 % sein)
   - Wenn < 70 %: Fokus nachstellen gemaess VENDOR-COGNEX-INS-001 (Abschnitt 1)

### Schritt 3: Pruefteil durchlaufen lassen

1. Fuenf Referenzteile manuell einlegen
2. Foerderband im Modus "Reduzierte Geschwindigkeit" (30 %) starten
3. Ergebnisse beobachten:
   - Erwartetes Ergebnis: 0 Ausschleusungen bei Referenzteilen
   - Falls Fehlklassifikation: Verfahren "Fehlklassifikationen – Sofortmassnahmen" einleiten
4. Produktionsgeschwindigkeit (100 %) erst nach erfolgreichem Referenzlauf freigeben

### Schritt 4: Produktionsbetrieb ueberwachen

Waehrend des laufenden Betriebs:

| Kennzahl | Sollwert | Massnahme bei Abweichung |
|----------|----------|-------------------------|
| Falschausschleusungsrate | < 2 % | Stopp; Beleuchtung und Fokus pruefen |
| Bildqualitaet (Focus Assist) | > 75 % | Fokus nachstellen |
| Kameratemperatur | 35–50 °C | Lueftung pruefen, Siemens Support informieren |
| Rezeptstatus | Aktiv = Produktions-SKU | Rezept pruefen und ggf. neu laden |

Ablesen der Kennzahlen: WinCC HMI → Prozesstransparenz → Vision-Statistik

---

## Fehlklassifikationen – Sofortmassnahmen

**Wenn mehr als 3 Fehlklassifikationen in 10 Teilen auftreten:**

1. Foerderband STOPPEN (WinCC Stopp-Taste)
2. Qualitaetsabteilung benachrichtigen
3. Ausgeschleuste Teile manuell sichten (echte Fehler oder Falschausweisung?)
4. Ursache bestimmen:

| Ursache | Symptom | Referenz | Massnahme |
|---------|---------|----------|-----------|
| Beleuchtung zu dunkel | Bild abgedunkelt, hohe Belichtungszeit | VENDOR-COGNEX-INS-001 Abschnitt 2 | Leuchtkopf reinigen, Halterung pruefen |
| Fokusdrift | Konturlinien verwaschen, Focus Assist < 70 % | VENDOR-COGNEX-INS-001 Abschnitt 1 | Fokusring nachziehen und arretieren |
| Falsches Rezept aktiv | SKU-Mismatch im Kamerastatus | VENDOR-COGNEX-INS-001 Abschnitt 3 | Richtiges Rezept neu laden; vollstaendigen Download abwarten |
| Kamera offline | WinCC zeigt "Vision: OFFLINE" | VENDOR-SIEMENS-WCC-001 Abschnitt 2 | Kamera Kaltstart; EtherCAT-Verbindung pruefen |

5. Nach Behebung: Referenzteile erneut durchlaufen lassen
6. Vorfall im WinCC Tagesprotokoll dokumentieren

---

## Formatumstellung

Bei jedem SKU-Wechsel oder Formatwechsel:

1. Linie stoppen
2. Neues Rezept im HMI auswaehlen (WinCC → Produktauswahl → [SKU])
3. Vollstaendigen Rezeptdownload abwarten (gruener Haken im HMI)
4. **Fokusring pruefen** – bei Hohenunterschied >5 mm zwischen Produkten ggf. nachstellen
   - Referenz: VENDOR-COGNEX-INS-001 (Abschnitt 1: Fokuseinstellung)
5. Fuenf Referenzteile des neuen Formats durchlaufen lassen
6. Erst nach fehlerfreiem Referenzlauf Produktion freigeben

---

## Referenzierte Dokumente

- **VENDOR-COGNEX-INS-001:** Cognex InSight 7010 Vision Systemreferenz (Fokus, Beleuchtung, Rezepte)
- **VENDOR-SIEMENS-WCC-001:** Siemens WinCC Bedienhandbuch (HMI-Statusanzeigen, Alarme)
- **SOP-PL4-001:** Anlaufverfahren Packaging Line 4 (Vision-Startschritt Abschnitt 2)
- **RCA-VIS-002:** Untersuchung Falschausschleusungen (Ursachen und Massnahmen)
- **QSTD-PL4-001:** Qualitaetsstandard Verpackung (Grenzwert Falschausschleusung <2 %)

**Dokumenten-ID:** SOP-VIS-001  
**Revision:** B  
**Letzte Aktualisierung:** 2026-03-12  
**Naechste Pruefung:** 2026-09-12
