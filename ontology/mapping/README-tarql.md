# RegioStaR Tarql mappings

The namespace IRIs at the top of all files are placeholders. Replace them consistently:

```sparql
PREFIX r: <https://example.org/regiostar/resource/>
PREFIX o: <https://example.org/regiostar/ontology/>
```

Run from a directory containing the mappings and CSV files:

```bash
tarql labels.tarql > labels.ttl
tarql aggregates.tarql > aggregates.ttl
cat regiostar-ontology.ttl labels.ttl aggregates.ttl > regiostar.ttl
```

Both mappings contain a `FROM` clause configured for the semicolon-delimited,
UTF-8 Excel CSV files. They deliberately read the CSV as headerless and skip the
first row, avoiding problems caused by the UTF-8 BOM in the first header cell.

Resource IRI pattern:

```text
r:scheme/{scheme}
r:concept/{scheme}/{code}
```

Examples:

```text
https://example.org/regiostar/resource/scheme/r4
https://example.org/regiostar/resource/concept/r4/11
https://example.org/regiostar/resource/concept/r17-plus/1111
```

`aggregates.tarql` emits both the exact custom relation and SKOS mapping
relations:

```turtle
r:concept/r7/73
    o:aggregates r:concept/r17/113 ;
    skos:narrowMatch r:concept/r17/113 .

r:concept/r17/113
    o:isAggregatedBy r:concept/r7/73 ;
    skos:broadMatch r:concept/r7/73 .
```
