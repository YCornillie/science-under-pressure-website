# Science under Water — Website (Prototyp)

Dark-Theme-Wissenschaftsseite im Stil von [remix.run](https://remix.run) — statt der
animierten Rennstrecke zeigt der Hero ein **echtes bathymetrisches 3D-Relief** eines
Schweizer Sees (WebGL / Three.js). Self-contained: eine einzige `index.html`.

---

## Was gebaut wurde

Ein interaktiver Einseiten-Prototyp mit der kompletten Struktur aus dem Konzept:

| Sektion | Inhalt |
|--------|--------|
| **Hero** | „Science under Water" + 3D-Bathymetrie des Walensees. Leitgedanke: zwei Arten von Druck — **Tiefendruck** (unter Wasser) und **Umweltdruck** (Klimawandel darüber). Echte Kennzahlen als Chips. |
| **Intro** | „Gewässer sind Archive, Lebensräume und Frühwarnsysteme zugleich" + Triade. |
| **Forschungsbereiche** | 3 Karten: Unterwasserarchäologie · Marine Biologie & Ökologie · Ozeanographie & Gewässerkunde. Methoden-Tags. |
| **Aktuelles / Projekte** | 4 Projektkarten mit Ort · Forschungsfrage · Methode · Ergebnis + generierte Bathymetrie-SVG-Thumbnails. *(Beispielinhalte)* |
| **Mission** | Slogan + 3 Kerngedanken (Dokumentieren · Verstehen · Zugänglich machen). |
| **Service** | 6 Leistungen (Bathymetrie, Monitoring, Gutachten, Fotogrammetrie, Datenanalyse, Wissenschaftskommunikation). |
| **Über uns** | Verein, Gemeinnützigkeit, Neutralität, wissenschaftlicher Anspruch. |
| **Partner** | Logo-Raster + Kategorien (Universitäten, Museen, Behörden, Naturschutz …). |
| **Mitmachen / Kontakt** | Zielgruppen-Chips + Kontaktformular *(Platzhalter, ohne Backend)*. |
| **Footer / Impressum** | Navigation + Impressum-Gerüst *(zum Ausfüllen)*. |

**Look & Technik:** dunkles Abyss-Farbschema, bioluminescent-cyan Akzente, große fette
Typografie, Scroll-Reveal-Animationen, „Tiefen-Anzeige" am Rand, Maus-Parallaxe,
kamerafahrt beim Scrollen. Der WebGL-Hero pausiert automatisch, sobald er weggescrollt ist.

---

## Der 3D-Hero: echte Bathymetrie

Kein stilisiertes Relief, sondern das reale digitale Tiefenmodell des **Walensees**:

- **Quelle:** [swissBATHY3D © swisstopo](https://www.swisstopo.admin.ch/de/hoehenmodell-swissbathy3d) (offene Geodaten), bezogen über die swisstopo-STAC-API.
- **Rohdaten:** 46 ESRI-ASCII-GRID-Kacheln, 1 m Auflösung, LV95 (EPSG 2056), ~84 MB ZIP.
- **Aufbereitung** (`scripts/process_bathy.py`): Kacheln zu einem Mosaik zusammengesetzt, auf den See zugeschnitten, auf 12 m Zellen heruntergerechnet → **1277 × 242 px Heightmap-PNG** (R = Tiefe, G = Wassermaske).
- **Aus den Daten abgeleitete Kennzahlen** (im Hero angezeigt): **23,3 km²** Seefläche, **141 m** kartierter Tiefenbereich.
- Im Shader wird eine Ebene aus der Heightmap verformt, tiefenabhängig eingefärbt, mit Höhenlinien (Isobathen ~alle 10 m), leuchtendem Uferrand, Kaustik-Schimmer und Sonar-Sweep. Land wird transparent → der See „schwebt" als leuchtende Silhouette.

---

## Projektstruktur

```
ScienceUnderWater/
├── index.html              ← fertige, self-contained Website (Heightmap eingebettet)
├── _template.html          ← Quell-Vorlage mit Platzhaltern
├── build.py                ← bettet Heightmap ein + generiert SVG-Thumbnails → index.html
├── assets/
│   └── walensee_heightmap.png   ← abgeleitete Heightmap (74 KB)
├── scripts/
│   └── process_bathy.py    ← swissBATHY3D-Rohdaten → Heightmap (Doku/Reproduktion)
└── README.md
```

## Neu bauen

```bash
python build.py
```

Liest `assets/walensee_heightmap.png` + `_template.html` → schreibt `index.html`.
Benötigt Python mit `pillow` (und `numpy` nur für `scripts/process_bathy.py`).
Die rohen swisstopo-Downloads werden dafür **nicht** gebraucht.

## Ansehen

`index.html` direkt im Browser öffnen (Internet nötig — Three.js kommt vom CDN),
oder lokal servieren:

```bash
python -m http.server 8777
```

---

## Aufräumen

Die heruntergeladenen Rohdaten (88 MB ZIP + 46 ASC-Kacheln, ~390 MB) lagen nur im
temporären Scratchpad und wurden **entfernt**. Im Projekt bleiben ausschließlich
abgeleitete/verwendete Dateien.

## Offene Punkte / Ideen

- Kontaktformular an ein Backend / einen Mail-Dienst anbinden.
- Impressum, Vereinsname, echte Kontaktadresse und Logos einsetzen.
- Beispielprojekte durch reale Projektberichte + Fotos ersetzen.
- Optional: anderes Gewässer im Hero (jeder swissBATHY3D-See lässt sich via
  `scripts/process_bathy.py` einsetzen), oder Framework-Umzug (Astro / Vite),
  falls aus dem Prototyp eine mehrseitige Site wird.
- Barrierefreiheit: Reduced-Motion wird respektiert; Farbkontraste noch prüfen.
