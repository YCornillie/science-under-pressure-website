# Science under Pressure — Website

Website des Vereins **Science under Pressure (S.U.P.)**: wissenschaftliche Unterwasserarbeiten in
Archäologie, Marine Biologie & Ökologie sowie Ozeanographie & Gewässerkunde.
Live unter **https://science-under-pressure.org**.

Dark-Theme-Einseitenseite im Stil von [remix.run](https://remix.run). Statt der animierten
Rennstrecke zeigt der Hero ein **echtes bathymetrisches 3D-Relief** eines Schweizer Sees
(WebGL / Three.js). Statisch, ohne Backend: `index.html` ist self-contained, ergänzt um
`language-switcher.js`.

---

## Sektionen

| Sektion | Inhalt |
|--------|--------|
| **Hero** | „Science under Pressure" + 3D-Bathymetrie des Walensees. Leitgedanke: zwei Arten von Druck — **Tiefendruck** (unter Wasser) und **Umweltdruck** (Klimawandel darüber). Kennzahlen als Chips. |
| **Intro** | „Gewässer sind Archive, Lebensräume und Frühwarnsysteme zugleich" + Triade. |
| **Forschung** | 3 Karten: Unterwasserarchäologie · Marine Biologie & Ökologie · Ozeanographie & Gewässerkunde. Methoden-Tags. |
| **Mission** | Slogan + 3 Kerngedanken (Dokumentieren · Verstehen · Zugänglich machen). |
| **Service** | 6 Leistungen (Bathymetrie, Monitoring, Gutachten, Fotogrammetrie, Datenanalyse, Wissenschaftskommunikation). |
| **Über uns** | Verein, Gemeinnützigkeit, Neutralität, wissenschaftlicher Anspruch. |
| **Mitmachen / Kontakt** | Zielgruppen und `mailto:`-Link auf `info@science-under-pressure.org`. |
| **Footer** | Navigation, Impressum-Kurzfassung, Datenquelle. |

Eine Sektion „Aktuelles & Projekte" gibt es bewusst (noch) nicht — sie kommt, sobald es
reale Projekte zu zeigen gibt. `build.py` erzeugt dafür weiterhin die SVG-Thumbnails
(`__THUMB_A__` bis `__THUMB_D__`), die in der aktuellen Vorlage nicht verwendet werden.

**Look & Technik:** dunkles Abyss-Farbschema, bioluminescent-cyan Akzente, grosse fette
Typografie, Scroll-Reveal-Animationen, „Tiefen-Anzeige" am Rand, Maus-Parallaxe,
Kamerafahrt beim Scrollen. Der WebGL-Hero pausiert automatisch, sobald er weggescrollt ist.

---

## Zweisprachigkeit (DE / EN)

`language-switcher.js` ergänzt einen DE/EN-Schalter (oben rechts, mobil im Hamburger-Menü).

- Die Seite ist auf **Deutsch** geschrieben. Das Skript ersetzt zur Laufzeit Textknoten anhand
  eines Wörterbuchs (`en = { "deutscher Text": "English text" }`).
- Es tauscht ausserdem Meta-Description, Mail-Link, `lang`-Attribut und ARIA-Labels.
- Die Wahl wird in `localStorage` (`sup-language`) gespeichert. Mit `?lang=de` bzw. `?lang=en`
  lässt sich die Sprache per URL setzen. **Ohne gespeicherte Wahl startet die Seite auf Englisch.**
- **Wichtig:** Der deutsche Text in `_template.html` dient als Schlüssel. Wird ein deutscher Satz
  geändert, muss der Schlüssel im Wörterbuch angepasst werden, sonst bleibt die Stelle auf Englisch
  unübersetzt.

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
.
├── index.html              <- gebaute, self-contained Website (Heightmap + Logo eingebettet)
├── _template.html          <- Quell-Vorlage mit Platzhaltern (hier wird editiert)
├── build.py                <- bettet Heightmap + Logo ein, generiert SVG-Thumbnails -> index.html
├── language-switcher.js    <- DE/EN-Schalter inkl. Übersetzungs-Wörterbuch
├── logo.jpeg / logo.png    <- Vereinslogo (jpeg wird in den Build eingebettet)
├── assets/
│   └── walensee_heightmap.png   <- abgeleitete Heightmap (74 KB)
├── scripts/
│   └── process_bathy.py    <- swissBATHY3D-Rohdaten -> Heightmap (Doku/Reproduktion)
├── CNAME                   <- Custom Domain für GitHub Pages
└── googleaf71804cdeec808c.html  <- Google-Search-Console-Verifizierung
```

## Änderungen vornehmen

**Nie `index.html` von Hand bearbeiten.** Änderungen gehören in `_template.html` (bzw.
`language-switcher.js`), danach neu bauen:

```bash
pip install pillow    # numpy nur für scripts/process_bathy.py nötig
python build.py
```

`build.py` liest `assets/walensee_heightmap.png`, `logo.jpeg` und `_template.html` und
schreibt `index.html`. Die rohen swisstopo-Downloads werden dafür nicht gebraucht.

## Ansehen

`index.html` im Browser öffnen (Internet nötig — Three.js kommt vom CDN) oder lokal servieren:

```bash
python -m http.server 8777
```

## Hosting

- GitHub Pages, ausgeliefert vom Branch `main` (Repo ist öffentlich, da Pages im Gratis-Account
  nur so funktioniert).
- Domain `science-under-pressure.org` bei Infomaniak. DNS: 4× A-Record auf die GitHub-Pages-IPs
  (185.199.108.153 / .109.153 / .110.153 / .111.153), CNAME `www` -> `ycornillie.github.io`.
  HTTPS ist erzwungen.

## Offene Punkte / Ideen

- Kontaktformular: aktuell `mailto:`-Link. Später ggf. Formular-Service (Formspree, Web3Forms)
  oder eigenes Backend.
- Impressum um Sitz und Vertretung ergänzen, sobald der Verein formell eingetragen ist.
- Sektion „Aktuelles & Projekte" mit realen Projekten, Berichten und Fotos ergänzen.
- Weitere Mitglieder als GitHub-Collaborators hinzufügen.
- Barrierefreiheit: Reduced-Motion wird respektiert; Farbkontraste noch prüfen.
- Optional: anderes Gewässer im Hero (jeder swissBATHY3D-See lässt sich via
  `scripts/process_bathy.py` einsetzen), oder Framework-Umzug (Astro / Vite), falls die Site mehrseitig wird.
