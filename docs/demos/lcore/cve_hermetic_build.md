# Lightspeed Core

![LCORE](images/lcore.jpg)

---

# Fixing CVEs in hermetic build environment

Pavel Tišnovský,
ptisnovs@redhat.com

---

## Hermetic build

* Downloads all sdists
* Network is disabled
* All packages are built w/o network access
* Results will be added into the dest. image

---

## Types of packages

* With sources (sdist)
* With sources, but with time consuming build
* Without sources (binary wheels)
* `pip` is special a bit

---

## Solution proposed by RH

* Standard Python registry
* RH Python registry with pre-built packages

---

## How to fix CVE?

* Package in PyPi?
    - update lockfile + requirements file
    - ETA - hours
* Package in RH Python registry
    - ask on forum-aipcc
    - exact workflow to be defined + refined
    - ETA - days (!!!)
* `pip` package
    - dunno ATM :(

---

## Thank you

