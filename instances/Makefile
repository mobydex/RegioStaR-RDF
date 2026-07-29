CWD = $(shell pwd)

POM = -f pom.xml
# Maven Clean Install Skip ; skip tests, javadoc, scaladoc, etc
MS = mvn -DskipTests -Dmaven.javadoc.skip=true -Dskip
MCIS = $(MS) clean install
MCCS = $(MS) clean compile

VER = $(error specify VER=releasefile-name e.g. VER=1.9.7-rc2)
loud = echo "@@" $(1);$(1)

TARQL = docker run --rm -i -v "$$(pwd):/data" mikulas/tarql

# Source: https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: help all clean

.ONESHELL:
help:   ## Show these help instructions
	@sed -rn 's/^([a-z0-9_\/\.-]+):[^#]*## (.*)$$/"\1" "\2"/p' < $(MAKEFILE_LIST) | xargs printf "make %-20s# %s\n"

target: ## mkdir target
	mkdir -p target

target/downloads: | target ## mkdir target/downloads
	mkdir -p target/downloads

target/downloads/2024_RegioStaR-Referenzdateien_Mobilthek.xlsx: | target/downloads ## Download Regiostar Spreadsheet (2024)
	wget -c 'https://mobilithek.info/mdp-api/files/aux/689522949364838400/2024%20RegioStaR-Referenzdateien_Mobilthek.xlsx' -O target/downloads/2024_RegioStaR-Referenzdateien_Mobilthek.xlsx.tmp
	mv target/downloads/2024_RegioStaR-Referenzdateien_Mobilthek.xlsx.tmp target/downloads/2024_RegioStaR-Referenzdateien_Mobilthek.xlsx

target/regiostar-2021.ttl: target/downloads/2024_RegioStaR-Referenzdateien_Mobilthek.xlsx regiostar-2021.tarql ## RDFize RegioStaR 2021
	ogr2ogr -f CSV /vsistdout/ target/downloads/2024_RegioStaR-Referenzdateien_Mobilthek.xlsx ReferenzGebietsstand2021 -s_srs OGC:CRS84 -t_srs OGC:CRS84 -lco GEOMETRY=AS_WKT -lco GEOMETRY_NAME=geometry | $(TARQL) --stdin /data/regiostar-2021.tarql > target/regiostar-2021.ttl

# target/2024_RegioStaR-Referenzdateien_Mobilthek.csv

target/downloads/vg250-ew_12-31.utm32s.gpkg.ebenen.zip: | target/downloads
	wget -c https://daten.gdz.bkg.bund.de/produkte/vg/vg250-ew_ebenen_1231/2021/vg250-ew_12-31.utm32s.gpkg.ebenen.zip -O target/downloads/vg250-ew_12-31.utm32s.gpkg.ebenen.zip.tmp
	mv target/downloads/vg250-ew_12-31.utm32s.gpkg.ebenen.zip.tmp target/downloads/vg250-ew_12-31.utm32s.gpkg.ebenen.zip

target/vg250-ew_12-31.utm32s.gpkg.ebenen/vg250-ew_ebenen_1231/DE_VG250.gpkg: target/downloads/vg250-ew_12-31.utm32s.gpkg.ebenen.zip
	# Note: -DD Sets the file creation date to the extraction data (i.e. now) rather than the archived date
	unzip -DD -d target -n target/downloads/vg250-ew_12-31.utm32s.gpkg.ebenen.zip

target/geometries.ttl: target/vg250-ew_12-31.utm32s.gpkg.ebenen/vg250-ew_ebenen_1231/DE_VG250.gpkg geometries.tarql
	ogr2ogr -f CSV /vsistdout/ target/vg250-ew_12-31.utm32s.gpkg.ebenen/vg250-ew_ebenen_1231/DE_VG250.gpkg VG250_GEM -t_srs OGC:CRS84 -lco GEOMETRY=AS_WKT -lco GEOMETRY_NAME=geometry | $(TARQL) --stdin /data/geometries.tarql > target/geometries.ttl

#target/opendata.hessen.de.ttl: | target ## download
#	rpt integrate -e remote --loc https://sparql.opendata.hessen.de/odp-hessen/ spo.rq --out-file target/opendata.hessen.de.ttl
#
#target/stage01.trig: | target/opendata.hessen.de.ttl ## select frankfurt
#	rpt integrate target/opendata.hessen.de.ttl 01-geolocation.rq gspo.rq --out-file target/stage01.trig
#
#target/stage02.ttl: target/opendata.hessen.de.ttl ## fetch metadata
#	rpt integrate target/opendata.hessen.de.ttl 02-fetch-catalog-metadata.rq --out-file target/stage02.ttl
#	#rpt integrate  -e remote --loc https://sparql.opendata.hessen.de/odp-hessen/ 02-fetch-catalog-metadata.rq --out-file target/stage02.ttl
#
#target/stage03.ttl: target/stage02.ttl ## delete dct:modified
#	rpt integrate target/stage02.ttl 03-delete-dct-modified.ru spo.rq --out-file target/stage03.ttl
#
#target/stage99.ttl: | target/stage01.trig target/stage03.ttl ## merge and flatten
#	rpt integrate target/stage01.trig target/stage03.ttl 'CONSTRUCT { ?s ?p ?o } { { ?s ?p ?o } UNION { GRAPH ?g { ?s ?p ?o } } }' --out-file target/stage99.ttl

all: target/regiostar-2021.ttl target/geometries.ttl

clean:
	rm target/regiostar-2021.ttl target/geometries.ttl
