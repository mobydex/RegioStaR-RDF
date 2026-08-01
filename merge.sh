#!/usr/bin/env bash

(cd instances && make all)
(cd ontology && make all)
mkdir -p target
cat instances/target/regiostar-2021.ttl instances/target/geometries.ttl ontology/target/labels.ttl ontology/target/aggregates.ttl > target/regiostar-merge.ttl

