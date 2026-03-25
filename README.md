# FHIR Patient Viewer

## Overview

Learning and exploring FHIR R4 clinical data is difficult without a visual tool. This project provides a simple browser-based viewer to browse, drill into, and inspect FHIR patient records stored in InterSystems IRIS for Health.

## Features

A web app that runs entirely in Docker. It loads 115 synthetic patient records into an InterSystems IRIS for Health FHIR server and lets you browse them in a web interface.

**Data source:** [Synthea](https://github.com/synthetichealth/synthea) — an open-source synthetic patient generator. All 115 patients are fictional. Each patient record includes conditions, observations, medications, encounters, procedures, immunizations, and more, stored as standard FHIR R4 Bundles.

**What you can do in the viewer:**
- Search patients by name
- Click a patient to see all their resource types (Condition, Observation, MedicationRequest, etc.)
- Expand any field to explore nested FHIR data
- Click a `reference` field to jump directly to the referenced resource
- View the raw JSON of any resource

## Quick Start

### Option 1 — Full Stack (Docker)

Includes a built-in IRIS FHIR server preloaded with 115 synthetic patients.

```bash
docker compose up --build
```

The first build takes several minutes while IRIS loads all patient data.

| URL | Description |
|---|---|
| http://localhost:3000 | Patient Viewer |
| http://localhost:8080/csp/sys/UtilHome.csp | IRIS Management Portal (`_SYSTEM` / `ISCDEMO`) |

### Option 2 — Connect to an Existing FHIR Server

Already have IRIS running? No Docker build needed — requires Python 3.

1. Edit `viewer/config.js` with your server URL and credentials
2. Run `./start-viewer.sh` and open http://localhost:3000


## Using Your Own Data

Replace the files in `fhirdata/100Set/` with your own FHIR R4 Bundle JSON files, then rebuild:
```bash
docker compose up --build
```
