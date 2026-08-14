# RegioStaR-RDF

RDFization of the RegioStaR Dataset - including taxonomy, labels and geometries.
The RDF downloads can be found in the [releases section](https://github.com/mobydex/RegioStaR-RDF/releases).

<table>
  <tr>
    <th align="center">Linked Data View</th>
    <th align="center">SPARQL View</th>
  </tr>
  <tr>
    <td align="center"><img src="docs/images/20260811-regiostar-linkeddata.png" width="400" alt="RegioStaR LinkedData"/></td>
    <td align="center"><img src="docs/images/20260811-regiostar-sparql.png" width="400" alt="RegioStaR SPARQL"/></td>
  </tr>
</table>

## Sources and Licenses

RegioStaR-RDF is a derived dataset created by transforming and combining the source datasets listed below. Both source datasets are made available under the [Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0)](https://www.govdata.de/dl-de/by-2-0).

The source data have been modified, in particular by transformation to RDF and by combining the RegioStaR classifications with administrative-area geometries. Reuse of RegioStaR-RDF is therefore subject to the licenses and attribution requirements of the respective source datasets.

The source code of this project is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

### Source 1: RegioStaR – Regionalstatistische Raumtypisierung

| Field | Details |
|---|---|
| Provider | Bundesministerium für Digitales und Verkehr (BMDV; now Bundesministerium für Verkehr, BMV) |
| Source | [Mobilithek](https://mobilithek.info/offers/689522949364838400) |
| Licence | [Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0)](https://www.govdata.de/dl-de/by-2-0) |
| Source attribution | BMV, [RegioStaR – Regionalstatistische Raumtypisierung](https://mobilithek.info/offers/689522949364838400), [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0) (Daten verändert) |
| Modifications | Data transformed into RDF and combined with administrative-area geometries |

### Source 2: Verwaltungsgebiete 1:250 000 mit Einwohnerzahlen (VG250-EW)

| Field | Details |
|---|---|
| Territorial reference date | 31 December 2021 |
| Source data landing page | [BKG Geodatenzentrum](https://gdz.bkg.bund.de/index.php/default/verwaltungsgebiete-1-250-000-mit-einwohnerzahlen-stand-31-12-vg250-ew-31-12.html) |
| Source data archive | [BKG Datenportal](https://daten.gdz.bkg.bund.de/produkte/vg/vg250-ew_ebenen_1231/2021/) |
| Concretely used product | `vg250-ew_12-31.utm32s.gpkg.ebenen.zip` |
| Licence | [Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0)](https://www.govdata.de/dl-de/by-2-0) |
| Source attribution | © [BKG](https://www.bkg.bund.de) (2026) [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0) (Daten verändert), Datenquellen: [BKG VG/NUTS data sources](https://sgx.geodatenzentrum.de/web_public/gdz/datenquellen/datenquellen_vg_nuts.pdf) |
| Modifications | Administrative-area data transformed into RDF and combined with RegioStaR classifications |
| Mapped subset | Only the land part of each administrative area (Geofaktor = 4); water parts (Geofaktor = 2) of coastal areas are excluded for now |

## Data Model

RegioStaR-RDF joins the two sources above into one linked dataset. Both key on the same 12-digit administrative-area identifier (`ARS_0`), so every RegioStaR unit maps 1:1 to exactly one VG250 land geometry.

### RegioStaR features

One feature resource per administrative area and reference year:

- `https://data.aksw.org/regiostar/regionalKey/<year>/<ARS_0>` — a `geo:Feature` carrying that year's RegioStaR types (`rro:type` → RegioStaR concepts of schemes 2, 4 and 5), plus `rro:regionalKey` (the [dcat-ap.de](http://dcat-ap.de/def/politicalGeocoding/regionalKey/) identifier) and `sdmx-dimension:refPeriod`.

### VG250 land geometries

The BKG *Verwaltungsgebiete* (VG, "administrative areas") 1:250 000 layer supplies the polygon for each administrative area. VG250 tags each geometry part with a *Geofaktor* (GF): areas that extend into the North Sea, the Baltic Sea or Lake Constance are split along the coast into a **land part (GF = 4)** and a **water part (GF = 2)** (154 areas in the 2024 edition). Following the VG250 documentation's recommendation for representing administrative areas, RegioStaR-RDF maps **only the land part (GF = 4)**; water parts are excluded for now and may be published as a separate dataset later.

Each RegioStaR feature therefore has exactly one geometry:

```turtle
<https://data.aksw.org/regiostar/regionalKey/2024/010010000000>
    a geo:Feature ;
    geo:hasGeometry <https://data.aksw.org/bkg/vg250/2024/geometry/DEBKGVG200000008> .

<https://data.aksw.org/bkg/vg250/2024/geometry/DEBKGVG200000008>
    a geo:Geometry ;
    dct:isVersionOf <https://data.aksw.org/bkg/vg250/geometry/DEBKGVG200000008> ;
    rro:geofactor <https://schema.aksw.org/regiostar/concept/geofactor/4> ;
    rro:ags0 "01001000" ;
    rro:ars0 "010010000000" ;
    geo:asWKT "MULTIPOLYGON (...)"^^geo:wktLiteral .

<https://data.aksw.org/bkg/vg250/geometry/DEBKGVG200000008>
    a rro:BkgObject ;
    dct:identifier "DEBKGVG200000008" .
```

### SameAs links (edition as current state)

Each reference year also ships a `sameas-<year>.ttl` file. For every RegioStaR feature of that year it emits one `owl:sameAs` link to the **year-less** dcat-ap.de identifier of the same administrative area:

```turtle
<https://data.aksw.org/regiostar/regionalKey/2024/010010000000>
    owl:sameAs <http://dcat-ap.de/def/politicalGeocoding/regionalKey/010010000000> .
```

Both sides key on the same 12-digit ARS, so the link joins the edition-specific feature to the canonical region it describes. Because the dcat-ap.de `regionalKey` IRI carries no year, loading a single edition's sameas file makes that year the **current / latest / default** view of each area: with `owl:sameAs` reasoning enabled, the edition's properties (RegioStaR types, label, geometry) merge into the shared canonical node.

> **Load only one sameas file per triple store.** The dcat-ap key is shared across editions, so loading several `sameas-<year>.ttl` files at once would let `owl:sameAs` transitivity merge *all* years' features into the same canonical nodes and collapse the year distinction. Pick the single edition you want as "current".

### IRI scheme

| Resource | IRI | Notes |
|---|---|---|
| RegioStaR feature | `https://data.aksw.org/regiostar/regionalKey/<year>/<ARS_0>` | `geo:Feature`; RegioStaR types per year via `rro:type` |
| VG250 geometry (yearly) | `https://data.aksw.org/bkg/vg250/<year>/geometry/<OBJID>` | `geo:Geometry` with `geo:asWKT`; land part only (Geofaktor = 4) |
| VG250 base geometry | `https://data.aksw.org/bkg/vg250/geometry/<OBJID>` | `rro:BkgObject`; stable identity across years, `dct:identifier` = `OBJID` |
| Geofactor concept | `https://schema.aksw.org/regiostar/concept/geofactor/<1-4>` | `skos:Concept` defined in the static ontology |

The geometry IRIs are **year-qualified** because BKG re-derives the VG250 layer every year: the same `OBJID` can carry a different WKT in different editions. The timeless base resource (`rro:BkgObject`) provides a stable identity that groups the yearly versions via `dct:isVersionOf`.

## Building

Prerequisites: Docker, GDAL (`ogr2ogr`), `wget`, `unzip`. Source downloads are cached under `instances/target/downloads/`.

| Target | Output |
|---|---|
| `make latest-year-only` | `target/regiostar-latest.ttl` — latest year (2024): RegioStaR features + VG250 land geometries + latest sameas links + static ontology (a self-contained "current state" store) |
| `make all-years` | `target/regiostar-all-years.ttl` — all editions 2021–2024 + static ontology, **without** sameas links; also produces the four `instances/target/sameas-<year>.ttl` files — load exactly **one** of them alongside (see “SameAs links” above) |
| `make archive` | `target/RegioStaR-RDF-<version>.tar.gz` — release archive bundling all instance `.ttl` files (RegioStaR, geometries, sameas 2021–2024) under `instances/` and all ontology `.ttl` files under `ontology/`, inside a top-level `RegioStaR-RDF-<version>/` folder |

## Useful SPARQL Queries

### RegioStaR Taxonomy

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rrr: <https://data.aksw.org/regiostar/>
PREFIX rro: <https://schema.aksw.org/regiostar/>

SELECT ?schemeLabel ?concept ?conceptLabel WHERE {
  ?scheme a rrr:RegioStaRScheme .
  ?concept skos:inScheme ?scheme .
  
  ?scheme rdfs:label ?schemeLabel .
  ?concept rdfs:label ?conceptLabel
}
```

### Regiopoles

```sparql
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
PREFIX rr: <http://www.w3.org/ns/r2rml#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rrr: <https://data.aksw.org/regiostar/>
PREFIX rro: <https://schema.aksw.org/regiostar/>

SELECT (geof:simplifyDp(geof:aggUnion(?wkt), 0.01) AS ?union) WHERE {
  ?s geo:hasGeometry/geo:asWKT ?wkt .
  ?s rro:type ?x . ?x rdfs:label ?l
  # FILTER(?x = <https://data.aksw.org/regiostar/concept/2/2>) # Ländliche Region
  FILTER(?x = rrr:concept\/4\/12) # Regiopolen
}
```

## Acknowledgements

The authors acknowledge the financial support by the German Federal
Ministry for Digital and Transport in the Project Moby Dex (project number 19F2266A).

| Field | Details |
|---|---|
| Project Summary | https://www.bmv.de/SharedDocs/DE/Artikel/mFUND/Projekte/moby-dex.html |
| Project Web Page | https://mobydex.org/ |

