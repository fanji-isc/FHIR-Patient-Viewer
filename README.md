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


```bash
docker compose up --build
```

The first build takes several minutes while IRIS loads all patient data.

| URL | Description |
|---|---|
| http://localhost:3000 | Patient Viewer |
| http://localhost:8080/csp/sys/UtilHome.csp | IRIS Management Portal (`_SYSTEM` / `demo`) |


## Using Your Own Data

Replace the files in `fhirdata/100Set/` with your own FHIR R4 Bundle JSON files, then rebuild:
```bash
docker compose up --build
```
