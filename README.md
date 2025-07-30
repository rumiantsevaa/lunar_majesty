
# 🌙 Lunar Majesty - DevOps Portfolio Project

**Serverless static website deployed via GitHub Pages with automated daily updates of dynamic content using GitHub Actions and an external PythonAnywhere node. Ensures zero downtime through safe atomic rebuilds.**

<img width="1280" height="540" alt="image" src="https://github.com/user-attachments/assets/437ebf01-33fc-43ff-827f-7bb72ac1744c" />



## 🎯 Project Goal

This project is designed to demonstrate understanding of DevOps principles and distributed systems architecture **without relying on Kubernetes** (due to the absence of budget for cloud infrastructure). 

The project showcases:

<img width="1250" height="337" alt="image" src="https://github.com/user-attachments/assets/3e3b12b2-f678-428d-8cf6-279b1657d17e" />

**_All the above in text:_**

✅ Zero Downtime Deployment via atomic rebuilds  
✅ Master-Worker architecture using publicly available platforms  
✅ Distributed Computing between GitHub Actions and PythonAnywhere  
✅ CI/CD Pipeline with automated daily updates  
✅ Infrastructure as Code via GitHub Actions workflows  


## 🏗️ System Architecture

<img width="1254" height="638" alt="image" src="https://github.com/user-attachments/assets/9a4da86b-9ab2-4333-be4e-95912dac8a23" />

**_More detailed nodes overview:_**

### Master Node: GitHub Actions Runner  
**Role:** Orchestrator & Primary Worker  
- Coordinates the entire data update process  
- Performs web scraping of lunar data  
- Manages the Worker Node via Selenium automation  
- Ensures zero downtime through atomic deployment  

### Worker Node: PythonAnywhere  
**Role:** Data Processing Unit  
- Receives raw data from the Master Node  
- Processes and translates the data  
- Sends back the processed data  
- Controlled remotely via Selenium WebDriver  


## 📁 Project Structure & File Responsibilities

<img width="1217" height="258" alt="image" src="https://github.com/user-attachments/assets/f2650e37-e490-4645-8960-6af593a0a20f" />

**_More detailed structure overview:_**

### 🤖 CI/CD Pipeline (`.github/workflows/`)

#### `parse+process.yml` – Master Node Workflow  
```yaml
# Main orchestrator for data update
```
**Responsibilities:**  
- Step 1: Scrape lunar data (`parse_data.py`)  
- Step 2: Transfer data to Worker Node (`bot_launcher.py`)  
- Step 3: Receive processed data back  
- Step 4: Save artifacts for next workflow  

#### `update_dynamic.yml` – Deployment Workflow  
```yaml
# Atomic deployment of updated content
```
**Responsibilities:**  
- Retrieve artifacts from previous workflow  
- Generate new JS content (`update_content.py`)  
- Atomic commit changes to the repository  
- Trigger GitHub Pages rebuild (zero downtime)  



## 🕷️ Data Collection Layer

### `parse_data.py` – Web Scraping Master  
```python
# Multi-source lunar data aggregator
```
**Demonstrates knowledge of:**  
- Selenium WebDriver for dynamic content scraping  
- Error handling and resilient scraping  
- Structured data output in JSON format  

**Scraped Data Sources:**  
- `moon_today_description()` – Current moon phases  
- `moon_dream_dictionary()` – Dream interpretations  
- `day_inspiration()` – Daily motivational content  



## 🤖 Node Communication Layer

### `bot_launcher.py` – Master-Worker Communication  
```python
# Selenium-based remote node controller
```
**Demonstrates knowledge of:**  
- Remote server automation via web interface  
- Selenium advanced techniques (iframe handling, file operations)  
- Secure credentials management via environment variables  
- Robust error handling with retry mechanisms  
- File transfer orchestration between nodes  

**Process Flow:**  

<img width="1252" height="666" alt="image" src="https://github.com/user-attachments/assets/7921456b-92b5-477e-b81a-e7606353947e" />

**_Detailed process flow in text:_**

- Authentication – Secure login to PythonAnywhere  
- Data Transfer – Upload JSON to worker node  
- Remote Execution – Run processing script on the worker  
- Result Retrieval – Download processed data  
- Cleanup – Session management and resource cleanup  


## ⚙️ Data Processing Layer

### `remote_PA_node_scripts/pythonanywhere_starter.py` – Worker Node Processor  
```python
# Data transformation and translation service
```
**Demonstrates knowledge of:**  
- Data transformation and cleaning  
- API integration
- Error handling for external services  
- JSON processing and validation  
- Modular function design  

**Processing Tasks:**  
- Clean and format moon phase data  
- Extract relevant dream interpretation text  
- Translate Russian content to English  
- Structure data for frontend consumption  


## 🛡️ DevOps Best Practices Implemented  

<img width="1152" height="483" alt="image" src="https://github.com/user-attachments/assets/d5f81f73-07dc-4577-ac4f-d38846a5ba34" />

**_All the above detailed in text:_**

**1. Zero Downtime Deployment**  
- Atomic commits – all changes in one transaction  
- GitHub Pages automatic rebuilds without service interruption  
- Validation steps before deployment  

**2. Security & Secrets Management**  
- GitHub Secrets for sensitive credentials  
- Environment variables for configuration  
- No hardcoded credentials in codebase  

**3. Error Handling & Resilience**  
- Retry mechanisms in `bot_launcher.py`  
- Graceful degradation in failure scenarios  
- Comprehensive logging for debugging  

**4. Infrastructure as Code**  
- GitHub Actions workflows as infrastructure definitions  
- Reproducible deployments via automated pipelines  
- Version-controlled infrastructure changes  

**5. Monitoring & Observability**  
- Workflow status tracking via GitHub Actions UI  
- Artifact management for debugging  
- Structured logging across components  



## 🚀 Scaling Considerations  

**Current Architecture Benefits:**  
- Cost-effective – uses free tiers  
- Maintainable – clear separation of concerns  
- Scalable logic – ready for cloud migration  

**Future Scaling Path:**  
- Docker containerization for consistent environments  
- Kubernetes deployment when budget allows  
- Cloud services integration (AWS Lambda, etc.)  
- Database integration for persistent storage  



## 📊 Technical Achievements  

- Distributed Computing without dedicated infrastructure  
- Master-Worker Pattern implementation via accessible platforms  
- Remote Process Orchestration via Selenium automation  
- Zero Downtime Updates for production website  
- Multi-source Data Aggregation with error handling  
- Cross-platform Compatibility (Linux, Windows)  
