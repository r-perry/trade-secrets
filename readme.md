# Congressional Trading Ingest & Automation Gateway

An automated open-source intelligence (OSINT) data pipeline and visual dashboard designed to ingest public data streams, track high-volume targets, and route execution parameters to a simulated financial environment with strict risk guardrails.

## 📊 Project Overview & Core Architecture

This application is engineered as a decoupled, multi-layered data automation system that processes mock open-source intelligence (OSINT) data streams and routes execution logic to a sandbox environment via external API integrations. 

The architecture is explicitly split into modular functional layers to ensure structural isolation, easy maintenance, and operational security.

### Key Technical Features
* **Decoupled Configuration Matrix:** Implements an external JSON configuration file (`watchlist.json`) to isolate operational data and target metrics from the underlying codebase, allowing parameters to be updated dynamically without code modification.
* **Multi-Target Pattern Matching:** Scales beyond a single data source by leveraging an array-based target watchlist to process complex incoming data structures across multiple high-volume profiles simultaneously.
* **Defensive Boundary Execution:** Integrates programmatic risk guardrails, including strict position limits and automated volume caps, to prevent over-allocation and enforce structural protection.
* **Isolated Environment Sandboxing:** Built and managed within a dedicated Python virtual environment (`venv`) to ensure absolute zero dependency friction with core system utilities.