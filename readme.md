# Congressional Trading Ingest & Automation Gateway

An automated open-source intelligence (OSINT) data pipeline and visual dashboard designed to ingest public data streams, track high-volume targets, and route execution parameters to a simulated financial environment with strict risk guardrails.

## 📊 Project Overview & Core Architecture

This application is engineered as a decoupled, multi-layered data automation system that processes structural open-source intelligence (OSINT) data streams and routes execution logic to a sandbox financial environment via authentic external API integrations. 

The architecture is explicitly split into modular functional layers to ensure structural isolation, allowing seamlessly scalable transitions from development telemetry into live production endpoints.

### Key Technical Features
* **Decoupled Configuration Matrix:** Implements an external JSON configuration file (`watchlist.json`) to isolate operational data and target metrics from the underlying codebase, allowing parameters to be updated dynamically without code modification.
* **Multi-Target Pattern Matching:** Scales beyond a single data source by leveraging an array-based target watchlist to process complex incoming data structures across multiple high-volume profiles simultaneously.
* **Defensive Boundary Execution:** Integrates programmatic risk guardrails, including strict position limits and automated volume caps, to prevent over-allocation and enforce structural protection.
* **Isolated Environment Sandboxing:** Built and managed within a dedicated Python virtual environment (`venv`) to ensure absolute zero dependency friction with core system utilities.

---

## ⚙️ Deployment & Local Installation

Follow these steps to spin up the local development environment and launch the automated gateway matrix natively on macOS.

### 1. Clone the Architecture Repository
```bash
git clone [https://github.com/r-perry/trade-secrets.git](https://github.com/r-perry/trade-secrets.git)

cd trade-secrets

2. Establish an Isolated Virtual Environment

python3 -m venv dashboard_env
source dashboard_env/bin/activate

3. Inject Core System Dependencies

pip install streamlit pandas requests

4. Deploy the Automation Telemetry Gateway
Bash
streamlit run dashboard.py

🔒 Security Matrix & Risk Controls
Credential Decoupling: API tokens are isolated strictly within volatile memory via front-end sidebar inputs and are barred from repository history via strict local tracking filters.

Volume Isolation: Financial execution payloads are governed by max allocation metrics managed dynamically inside the configuration layer.