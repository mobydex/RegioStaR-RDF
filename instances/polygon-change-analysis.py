#!/usr/bin/env python3
"""Generate the polygon-change table across RegioStaR geometry years.

Compares the BKG VG250 municipality geometries (one per `ARS_0` regional key)
year over year and reports, for each pair of years:

  * the change in the SET of municipalities (keys added / removed)
  * how many geometries differ, measured at several coordinate-precision
    levels, so that a sub-millimetre data re-derivation can be separated from
    real boundary edits.

The change counts are computed by *truncating* every coordinate to N decimal
places and comparing the resulting canonical per-key signature.  Truncation
(rather than rounding) reproduces the original analysis exactly; note that
`ogr2ogr` itself exposes rounding via the `OGR_WKT_PRECISION` environment /
config variable (significant digits, not decimals after the point).

Usage
-----
    python3 polygon-change-analysis.py [BASE_DIR] [YEAR ...]
        [--force] [--cache-dir PATH | -c PATH]

Defaults: BASE_DIR="." (the directory holding the extracted gpkg files),
          years = 2021 2022 2023 2024, cache = target/.poly-cache.

The per-year CSVs are cached under CACHE_DIR (target/.poly-cache by default,
override with --cache-dir) so re-running is fast; pass --force to re-extract
from the gpkg files.
"""

import csv
import os
import re
import subprocess
import sys
from collections import defaultdict

# --- configuration ----------------------------------------------------------

LAYER = "vg250_gem"          # gpkg layer holding the geometries
KEY = "ARS_0"               # 12-digit regional key used to match municipalities
TARGET_SRS = "OGC:CRS84"    # common CRS for comparison (degrees)

DEFAULT_YEARS = ("2021", "2022", "2023", "2024")
# Where per-year CSV extracts are cached.  Configurable via --cache-dir/-c
# (defaults to target/.poly-cache, next to the other build artifacts).
CACHE_DIR = os.path.join("target", ".poly-cache")

# Precision columns.  The first value is the number of decimals after the
# point (None = full precision); the label is a human-readable name.  The
# approximate scale is given at ~54 N latitude (1 deg ~ 111 km):
#   1e-2 deg ~ 1.1 km, 1e-3 ~ 110 m, 1e-4 ~ 11 m, 1e-5 ~ 1.1 m, 1e-6 ~ 0.11 m
PRECISIONS = (
    ("full", None),
    ("7dp", 7),
    ("6dp", 6),
    ("5dp", 5),
    ("4dp", 4),
    ("3dp", 3),
    ("2dp", 2),
)


# --- helpers ----------------------------------------------------------------

def gpkg_path(base, year):
    """Path to the per-year gpkg, mirroring the Makefile layout (under target/)."""
    return os.path.join(
        base, "target",
        f"vg250-ew_12-31.utm32s.gpkg.ebenen_{year}",
        "vg250-ew_ebenen_1231",
        f"DE_VG250_{year}.gpkg",
    )


def extract(base, year, force=False, cache_dir=None):
    """Extract (KEY, WKT) at full precision -> {key: [wkt, ...]}.

    A municipality may appear as several features; every feature's WKT is
    kept so the per-key signature stays faithful to the data.  Results are
    cached as CSV under cache_dir (default CACHE_DIR) so re-runs skip the
    (slow) ogr2ogr step.
    """
    cache_dir = cache_dir or CACHE_DIR
    os.makedirs(cache_dir, exist_ok=True)
    csv_path = os.path.join(cache_dir, f"geo-{year}.csv")
    if force or not os.path.exists(csv_path):
        src = gpkg_path(base, year)
        if not os.path.exists(src):
            raise FileNotFoundError(
                f"geometry gpkg not found: {src}\n"
                f"(extract it first, e.g. via the Makefile geometry target)"
            )
        print(f"extracting {year} ...", file=sys.stderr)
        subprocess.run(
            [
                "ogr2ogr", "-f", "CSV", csv_path, src, LAYER,
                "-t_srs", TARGET_SRS, "-select", KEY,
                "-lco", "GEOMETRY=AS_WKT",
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    else:
        print(f"loading {year} (cached) ...", file=sys.stderr)
    return load_csv(csv_path)


def load_csv(csv_path):
    """Parse the ogr2ogr CSV -> {key: [wkt, ...]}.

    The CSV driver quotes the WKT field (which contains commas), so the
    `csv` module recovers each field cleanly.  The geometry column is first;
    the key column is located by name with a fall-back to the last column.
    """
    rows = defaultdict(list)
    with open(csv_path, newline="") as fh:
        reader = csv.reader(fh)
        try:
            header = [h.strip() for h in next(reader)]
        except StopIteration:
            return {}
        up = [h.upper() for h in header]
        key_i = up.index(KEY) if KEY in up else len(header) - 1
        geom_i = 0
        for i, h in enumerate(header):
            if i == key_i:
                continue
            if "WKT" in h.upper() or "geometry" in h.lower() or i == 0:
                geom_i = i
                break
        for row in reader:
            if len(row) <= max(key_i, geom_i):
                continue
            key = row[key_i].strip().strip('"')
            wkt = row[geom_i].strip().strip('"')
            if key and wkt:
                rows[key].append(wkt)
    return rows


def truncate(wkt, n):
    """Drop everything after the Nth decimal of every coordinate in `wkt`."""
    if n is None:
        return wkt
    return re.sub(r"(\d+\.\d{%d})\d+" % n, r"\1", wkt)


def signature(rows, n):
    """Canonical per-key signature at precision `n`.

    A key may have several features; their (truncated) WKTs are joined with
    ';' and sorted so the signature is independent of feature ordering.
    """
    out = {}
    for key, wkts in rows.items():
        out[key] = ";".join(sorted(truncate(w, n) for w in wkts))
    return out


# --- analysis ---------------------------------------------------------------

def analyze(data):
    years = sorted(data)

    # Precompute the signature for every (year, precision) once, so each year
    # is truncated a single time per precision instead of once per pair.
    sig = {y: {} for y in years}
    for y in years:
        for name, n in PRECISIONS:
            sig[y][n] = signature(data[y], n)

    # Header
    header = ("pair".ljust(9)
             + f"{'common':>7}"
             + "".join(f"{name:>7}" for name, _ in PRECISIONS)
             + "   | added / removed")
    print(header)
    print("-" * len(header))

    # Body (chronological pairs).  The key set is precision-independent, so
    # common / added / removed come from the extracted keys, not the sig dict.
    for a in range(len(years)):
        for b in range(a + 1, len(years)):
            ya, yb = years[a], years[b]
            set_a, set_b = set(data[ya]), set(data[yb])
            common = set_a & set_b
            added = len(set_b - set_a)
            removed = len(set_a - set_b)
            cells = []
            for name, n in PRECISIONS:
                sa_n, sb_n = sig[ya][n], sig[yb][n]
                changed = sum(
                    1 for k in common if sa_n.get(k) != sb_n.get(k)
                )
                cells.append(f"{changed:>7}")
            print(
                f"{ya}→{yb}".ljust(9)
                + f"{len(common):>7}"
                + "".join(cells)
                + f"   | +{added} / -{removed}"
            )


# --- entry point ------------------------------------------------------------

def parse_args(argv):
    years = []
    base = "."
    force = False
    cache_dir = CACHE_DIR
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg in ("--force", "-f"):
            force = True
        elif arg in ("--cache-dir", "-c"):
            cache_dir = argv[i + 1]
            i += 1
        elif arg.startswith("--cache-dir="):
            cache_dir = arg.split("=", 1)[1]
        elif arg.startswith("-"):
            sys.exit(f"unknown option: {arg}")
        elif re.fullmatch(r"\d{4}", arg):
            years.append(arg)
        else:
            base = arg
        i += 1
    if not years:
        years = list(DEFAULT_YEARS)
    return base, years, force, cache_dir


def main(argv):
    base, years, force, cache_dir = parse_args(argv)
    data = {}
    for y in years:
        data[y] = extract(base, y, force=force, cache_dir=cache_dir)
        print(f"  {y}: {sum(len(v) for v in data[y].values())} features, "
              f"{len(data[y])} keys", file=sys.stderr)
    analyze(data)


if __name__ == "__main__":
    main(sys.argv)
