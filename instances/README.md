# RegioStaR-RDF

Turns the **RegioStaR** reference areas and the **BKG VG250-EW** municipality
geometries into RDF, for the reference years **2021–2024**.

## Build

Requirements: `docker` (runs `mikulas/tarql`), `ogr2ogr` (GDAL), `wget`, `unzip`.

    make help   # list all targets
    make all    # build every year (2021–2024)
    make clean  # remove the generated *.ttl

Per year:

    make target/regiostar-<YEAR>.ttl
    make target/geometries-<YEAR>.ttl

`make all` first downloads the RegioStaR spreadsheet and the four BKG geometry
zips into `target/` (cached, so re-runs reuse them). Each artifact is produced
by `ogr2ogr` (the `ReferenzGebietsstand<YEAR>` sheet / the `VG250_GEM` layer,
reprojected to `OGC:CRS84`) piped into `tarql` via the matching `*.tarql`.

## Analysing geometry changes

    python3 polygon-change-analysis.py            # 2021–2024 by default
    python3 polygon-change-analysis.py --force    # re-extract from the gpkg files
    python3 polygon-change-analysis.py -c DIR     # custom cache directory

Compares the BKG municipality geometries across years at several
coordinate-precision levels, so a sub-millimetre data re-derivation can be
separated from real boundary edits. Per-year extracts are cached under
`target/.poly-cache/`.

## Licence

This derived dataset is provided under the
Datenlizenz Deutschland – Namensnennung – Version 2.0:
https://www.govdata.de/dl-de/by-2-0

## Sources

1. RegioStaR – Regionalstatistische Raumtypisierung
   Publisher: Bundesministerium für Digitales und Verkehr
   Source: https://mobilithek.info/offers/689522949364838400
   Licence: dl-de/by-2-0
   Data transformed into RDF for reference years 2021–2024.

2. Verwaltungsgebiete 1:250 000 mit Einwohnerzahlen (VG250-EW), 2021–2024
   © BKG (2026) dl-de/by-2-0 (Daten verändert)
   Datenquellen:
   https://sgx.geodatenzentrum.de/web_public/gdz/datenquellen/datenquellen_vg_nuts.pdf
