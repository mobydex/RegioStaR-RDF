CWD = $(shell pwd)

VER = $(error specify VER=releasefile-name e.g. VER=1.9.7-rc2)
loud = echo "@@" $(1);$(1)

TARQL = docker run --rm -i -v "$$(pwd):/data" mikulas/tarql
SANSA_TARQL = docker run --rm -i -v "$$(pwd):/data" aksw/rpt:2.0.0-rc7 sansa tarql

# Source: https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: help all clean

.ONESHELL:
help:   ## Show these help instructions
	@sed -rn 's/^([a-z0-9_\/\.-]+):[^#]*## (.*)$$/"\1" "\2"/p' < $(MAKEFILE_LIST) | xargs printf "make %-20s# %s\n"

target: ## mkdir target
	mkdir -p target

target/code-labels.ttl: code-labels.csv code-labels.tarql | target ## RDFize RegioStaR labels
	$(SANSA_TARQL) /data/code-labels.tarql /data/code-labels.csv --out-format turtle/blocks > target/code-labels.ttl

target/scheme-labels.ttl: scheme-labels.csv scheme-labels.tarql | target ## RDFize RegioStaR labels
	$(SANSA_TARQL) /data/scheme-labels.tarql /data/scheme-labels.csv --out-format turtle/blocks > target/scheme-labels.ttl

target/properties.ttl: code-labels.csv properties.tarql | target ## RDFize RegioStaR properties
	$(SANSA_TARQL) /data/properties.tarql /data/code-labels.csv --out-format turtle/blocks > target/properties.ttl

target/aggregates.ttl: aggregates.csv aggregates.tarql | target ## RDFize RegioStaR aggregates
	$(SANSA_TARQL) /data/aggregates.tarql /data/aggregates.csv --out-format turtle/blocks > target/aggregates.ttl

all: target/code-labels.ttl target/scheme-labels.ttl target/aggregates.ttl target/properties.ttl ## Create all RDF files

clean: ## Remove all generated RDF files
	rm -f target/code-labels.ttl target/scheme-labels.ttl target/aggregates.ttl target/properties.ttl

