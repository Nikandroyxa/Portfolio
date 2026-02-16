# MotoGP Racing: Full Stack Cloud Pipeline with GCP & BigQuery Analytics

## 📊 Project Overview

This project demonstrates a **Full Stack Cloud Data Pipeline** that collects MotoGP 2024 racing data through **Web Scraping**, stores & processes it using **Google Cloud Platform (GCP)** infrastructure, queries it with **BigQuery SQL**, generates professional **Data Visualizations** & maintains **Version Control** through **Git/GitHub**

The pipeline processes races from the 2024 MotoGP season through a 4-stage workflow: **Web Scraping**, **Cloud Storage**, **Cloud Database (BigQuery)**, & **Data Visualization**. The project showcases **Cloud Data Engineering** practices, **SQL Analytics**, full-stack development from data collection to insight generation & **software engineering practices with Git Version Control**

Using **GCP Cloud Storage & BigQuery**, the pipeline stored & queried race results, achieving comprehensive analysis of **11 race wins by Francesco Bagnaia (47.8%)**, while extracting insights from **7 performance metrics** including pole positions, fastest laps & circuit performance across the championship season

---

## 🎯 Key Objectives

- **Full Stack Development:**
  - Build **End-to-End Data Pipeline** from collection to visualization
  - Design modular & reusable code architecture
  - Version control with **Git/GitHub**

- **Cloud Infrastructure (GCP):**
  - Set up **Google Cloud Platform** project & authentication
  - Configure **Cloud Storage Bucket** for data files
  - Create **BigQuery Dataset & Tables**
  - Implement secure API access with Application Default Credentials (ADC)

- **Data Engineering:**
  - **Automated Web Scraping** from Wikipedia
  - **Cloud-based Data Storage & Retrieval**
  - **SQL queries for Cloud Data Warehousing**
  - Comparison of local (pandas) vs cloud (BigQuery) data access

- **Data Analytics & Visualization:**
  - Perform comprehensive **Exploratory Data Analysis (EDA)**
  - Generate 5 professional **Multi-Chart Visualizations**
  - Identify patterns in MotoGP championship performance
  - Extract actionable insights from racing data

---

## 📁 Project Structure
```
012_MotoGP_Racing_Analytics/
│
├── 001_src/                                    
│   ├── 001_fetch_data.py                      
│   ├── 002_cloud_data_access.py               
│   ├── 003_cloud_data_access_function.py      
│   ├── 004_bigquery_analysis.py               
│   └── 005_data_visualization.py              
│
├── 002_data/                                   
│   └── motogp_2024_results.csv                
│
├── 003_tests/                                  
│
├── 004_notebooks/                              
│   ├── 001_motogp_scraping_dev.ipynb          
│   ├── 002_test_cloud_access.ipynb            
│   ├── 003_test_cloud_access_function.ipynb   
│   ├── 004_bigquery_analysis.ipynb            
│   └── 005_data_visualization.ipynb           
│
├── 005_visualizations/                         
│   ├── viz_01_wins_by_rider.png               
│   ├── viz_02_pole_positions.png              
│   ├── viz_03_win_distribution.png            
│   ├── viz_04_performance_comparison.png      
│   └── viz_05_championship_battle.png         
│
└── README.md                                   
```

---

## 📈 Key Findings

**Championship Results:**
- **Champion: Francesco Bagnaia** - Dominated with 11 wins (47.8% win rate)
- **Runner-up: Jorge Martín & Marc Márquez** - Tied with 3 wins each (13.0%)
- **Total winners:** 5 different riders across 23 races
- **Most consistent:** Bagnaia won nearly half of all races

**Performance Insights:**
- **Pole position correlation:** Top qualifiers (Martín, Bagnaia) showed strong race performance
- **Fastest lap analysis:** Bagnaia secured 11 fastest laps, matching his win count
- **Circuit dominance:** Multiple wins at different circuits demonstrate versatility
- **Competition level:** 3-way battle for 2nd place (Martín, Márquez, Bastianini)

**Data Pipeline Performance:**
- **Web scraping:** 100% success rate extracting Wikipedia table data
- **Cloud storage:** 3.01 KB data stored in GCP London region (europe-west2)
- **BigQuery queries:** Sub-second query times for 23-row dataset
- **Visualization generation:** 5 high-resolution charts created in < 30 seconds

---

## 📊 Results Summary

| Metric | Value |
|--------|-------|
| **Total Races Analyzed** | 23 races |
| **Data Columns Collected** | 7 columns |
| **Cloud Storage Location** | GCP europe-west2 (London) |
| **Data Size (CSV)** | 3.01 KB |
| **BigQuery Dataset** | motogp_data |
| **BigQuery Table** | race_results_2024 |
| **Champion** | Francesco Bagnaia |
| **Total Wins (Bagnaia)** | 11 wins (47.8%) |
| **Different Winners** | 5 riders |
| **Visualizations Created** | 5 charts (300 DPI PNG) |
| **Pipeline Stages** | 4 stages |
| **Code Files** | 5 Python scripts + 5 Jupyter notebooks |
| **Lines of Code** | ~800 lines |

---

## 🔄 Process

### 1. Web Scraping & Data Collection

**Data Source:**
- Target: Wikipedia 2024 MotoGP Season page
- Method: **BeautifulSoup HTML parsing**
- Data structure: HTML table → Pandas DataFrame

**Scraping Pipeline:**
- Sent HTTP GET request to Wikipedia page
- Parsed HTML with BeautifulSoup
- Located MotoGP results table by class name
- Extracted table headers and rows
- Converted to structured Pandas DataFrame

**Feature Extraction:**
- **7 columns extracted per race:**
  - `Round`: Race number (1-23)
  - `Date`: Race date
  - `Grand Prix`: Event name
  - `Circuit`: Track location
  - `Winning rider`: Race winner
  - `Pole position`: Qualifying leader
  - `Fastest lap`: Fastest race lap holder

**Data Export:**
- Saved to local CSV: `002_data/motogp_2024_results.csv`
- Format: 23 rows × 7 columns
- Encoding: UTF-8

### 2. Google Cloud Platform Setup & Cloud Storage

**GCP Project Configuration:**
- Created GCP project: `012-MotoGP-Racing-Analytics`
- Enabled APIs: Cloud Storage API, BigQuery API
- Installed Google Cloud CLI (gcloud)

**Authentication Setup:**
- Authenticated with Application Default Credentials (ADC)
- Command: `gcloud auth application-default login`
- Secured API access for local development

**Cloud Storage Implementation:**
- Created bucket: `motogp-racing-data-2024`
- Region: `europe-west2` (London)
- Storage class: Standard
- Uploaded CSV file (3.01 KB)

**Python Integration:**
- **Procedural approach:** Direct API calls with storage client
- **Function-based approach:** Modular `main()` function
- Both methods successfully:
  - Connected to GCP project
  - Accessed Cloud Storage bucket
  - Downloaded CSV data as text
  - Loaded into Pandas DataFrame
  - Displayed race results and statistics

### 3. BigQuery Cloud Database & SQL Analytics

**BigQuery Setup:**
- Created dataset: `motogp_data`
- Created table: `race_results_2024`
- Schema: Auto-detected from CSV (7 STRING columns)
- Data loading: Direct import from Cloud Storage

**Python-BigQuery Integration:**
- Used `google-cloud-bigquery` library
- Created BigQuery client with project authentication
- Executed SQL queries programmatically
- Converted query results to Pandas DataFrames
- Compared with Cloud Storage method

### 4. Data Visualization & Analysis

**Visualization Development:**
- Platform: Matplotlib & Seaborn

**Charts Created:**

1. [**Wins by Rider** (Bar Chart)](005_visualizations/viz_01_wins_by_rider.png)
   
2. [**Pole Positions** (Horizontal Bar Chart)](005_visualizations/viz_02_pole_positions.png)
   
3. [**Win Distribution** (Pie Chart)](005_visualizations/viz_03_win_distribution.png)
   
4. [**Performance Comparison** (Grouped Bar Chart)](005_visualizations/viz_04_performance_comparison.png)
   
5. [**Championship Battle** (Line Chart)](005_visualizations/viz_05_championship_battle.png)
   
**Analysis Insights:**
- Bagnaia's consistency: Won in various conditions and circuits
- Competition for 2nd: Tight battle between Martín and Márquez
- Performance metrics: Wins correlated with poles and fastest laps
- Championship narrative: Bagnaia's steady accumulation vs others' sporadic wins

---

## 💻 Technologies Used

### **Programming & Development:**
- **Python** 
- **VS Code:** IDE for script development

### **Web Scraping & Data Collection:**
- **requests:** HTTP requests to Wikipedia
- **BeautifulSoup4:** HTML parsing and table extraction

### **Cloud Infrastructure (GCP):**
- **Google Cloud Platform:**
  - Cloud Storage (file storage, bucket management)
  - BigQuery (cloud data warehouse, SQL analytics)
- **google-cloud-storage** 
- **google-cloud-bigquery** 
- **Google Cloud CLI (gcloud)**
- **Authentication** Application Default Credentials (ADC)

### **Data Processing & Analysis:**
- **Pandas:** Data cleaning, transformation, aggregation
- **NumPy:** Numerical operations
- **StringIO:** In-memory file handling for cloud data

### **Data Visualization:**
- **Matplotlib** 
- **Seaborn** 
- **Chart Types**
- **Export:** High-resolution PNG (300 DPI)

### **Version Control & Project Management:**
- **Git:** Version control system
- **GitHub:** Remote repository hosting

---