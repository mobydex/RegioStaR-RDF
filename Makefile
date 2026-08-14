CWD = $(shell pwd)

LATEST_YEAR = 2024
VERSION = 1.1.0

# Source: https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: help latest-year-only all-years archive clean

help:   ## Show these help instructions
	@sed -rn 's/^([a-z0-9_\-\/.-]+):[^#]*## (.*)$$/"\1" "\2"/p' < $(MAKEFILE_LIST) | xargs printf "make %-20s# %s\n"

latest-year-only: ## Build + merge only the latest year (2024)
	$(MAKE) -C instances target/regiostar-$(LATEST_YEAR).ttl target/geometries-$(LATEST_YEAR).ttl target/sameas-$(LATEST_YEAR).ttl
	$(MAKE) -C ontology all
	mkdir -p target
	cat instances/target/regiostar-$(LATEST_YEAR).ttl \
	    instances/target/geometries-$(LATEST_YEAR).ttl \
	    instances/target/sameas-$(LATEST_YEAR).ttl \
	    ontology/target/code-labels.ttl ontology/target/scheme-labels.ttl \
	    ontology/target/aggregates.ttl ontology/target/geofactor-labels.ttl \
	    > target/regiostar-latest.ttl
	@echo "wrote target/regiostar-latest.ttl"

# The merged output deliberately contains NO sameas links: only one sameas-YYYY.ttl
# may ever be loaded into a store (it marks one edition as the current state).
all-years: ## Build + merge all years (2021-2024)
	$(MAKE) -C instances all
	$(MAKE) -C ontology all
	mkdir -p target
	cat instances/target/regiostar-2021.ttl instances/target/regiostar-2022.ttl \
	    instances/target/regiostar-2023.ttl instances/target/regiostar-2024.ttl \
	    instances/target/geometries-2021.ttl instances/target/geometries-2022.ttl \
	    instances/target/geometries-2023.ttl instances/target/geometries-2024.ttl \
	    ontology/target/code-labels.ttl ontology/target/scheme-labels.ttl \
	    ontology/target/aggregates.ttl ontology/target/geofactor-labels.ttl \
	    > target/regiostar-all-years.ttl
	@echo "wrote target/regiostar-all-years.ttl"
	@echo "also produced sameas link files (load only ONE per store): instances/target/sameas-2021.ttl, sameas-2022.ttl, sameas-2023.ttl, sameas-2024.ttl"

archive: all-years ## Package all-years output into target/RegioStaR-RDF-<version>.tar.gz
	mkdir -p target/RegioStaR-RDF-$(VERSION)/ontology target/RegioStaR-RDF-$(VERSION)/instances
	cp ontology/target/*.ttl target/RegioStaR-RDF-$(VERSION)/ontology/
	cp instances/target/*.ttl target/RegioStaR-RDF-$(VERSION)/instances/
	tar -czf target/RegioStaR-RDF-$(VERSION).tar.gz -C target RegioStaR-RDF-$(VERSION)
	rm -rf target/RegioStaR-RDF-$(VERSION)
	@echo "wrote target/RegioStaR-RDF-$(VERSION).tar.gz"

clean: ## Remove merged datasets
	rm -f target/regiostar-latest.ttl target/regiostar-all-years.ttl
