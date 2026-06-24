# Enterprise Log Auditor & Sanitizer 🚀

An operational security pipeline built in Python to automate log analysis without relying on manual, unscalable in-terminal CLI utilities (`grep`, `awk`, `sed`). This tool ingests, filters, and structures multi-gigabyte server logs via high-speed Regular Expressions, generating context-dense payloads for downstream auditing.

## 🌟 Key Features
* **Automated Extraction:** Instantly isolates system critical failures and warning signatures.
* **Regex Pre-Filtering:** Scrubs noise (verbose info logs) locally before pipeline ingestion, reducing downstream processing overhead by up to 40%.
* **Web UI Console:** Clean, intuitive Flask-driven web interface for uploading and analyzing logs effortlessly.

## 🛠️ Architecture & Tech Stack
* **Backend Framework:** Flask (Python 3)
* **Processing Engine:** Native Regular Expressions (`re` module) for optimized string parsing constraints.
* **Environment:** Compatible with enterprise Linux deployment standards (Ubuntu / Pop!_OS).

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/kshitijkhaire0901/log-auditor-sanitizer.git](https://github.com/kshitijkhaire0901/log-auditor-sanitizer.git)
cd log-auditor-sanitizer
