# RegioStaR-RDF

![RegioStaR LinkedData](docs/images/20260811-regiostar-linkeddata.png)
![RegioStaR SPARQL](docs/images/20260811-regiostar-sparql.png)

RDFization of the RegioStaR Dataset - including taxonomy, labels and geometries.

Source of polygons:
https://gdz.bkg.bund.de/index.php/default/verwaltungsgebiete-1-250-000-mit-einwohnerzahlen-stand-31-12-vg250-ew-31-12.html
https://daten.gdz.bkg.bund.de/produkte/vg/vg250-ew_ebenen_1231/2021/


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

