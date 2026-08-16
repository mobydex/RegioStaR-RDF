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
  ?s rro:regioStaR4 ?x . ?x rdfs:label ?l
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

