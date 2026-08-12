#!/usr/bin/env bash

(cd instances && make all)
(cd ontology && make all)
mkdir -p target
cat instances/target/regiostar-2021.ttl instances/target/geometries.ttl ontology/target/code-labels.ttl ontology/target/scheme-labels.ttl ontology/target/aggregates.ttl > target/regiostar-merge.ttl

