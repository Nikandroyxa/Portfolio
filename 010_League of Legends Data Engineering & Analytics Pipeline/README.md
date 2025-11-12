# **LoL Data Engineering (API) & Analytics Pipeline**

## 📊 **Project Overview**

This project aimed to develop a comprehensive **data pipeline and Machine Learning solution** to predict win/loss outcomes in League of Legends matches using personal gameplay data. The primary goal was to gain hands-on experience with **Data Engineering (API integration, data collection)** and **Data Science (exploratory analysis, feature engineering, predictive modeling)**.

Using the **Riot Games API**, we collected 460 Katarina matches from 1,000 total games in the CLASSIC queue (EUW server). The project demonstrates end-to-end ML workflow: from API data extraction and cleaning, through exploratory data analysis (EDA), to building and evaluating multiple classification models. The best model achieved **94.57% accuracy** with an **AUC of 0.986**, successfully identifying the key factors that determine victory.

---

## 🎯 **Key Objectives**

### 📁 **Project Structure**
```
📁 API - LoL Data Engineering & Analytics Pipeline/
│
├── 📓 01_Riot_API_Data_Collection.ipynb
├── 📓 02_EDA_Kata_Classic_1000.ipynb
├── 📓 03_ML_Win_Prediction.ipynb
│
└── 📊 katarina_matches_1000.csv
```
---

1. **Data Engineering Practice:**
   - Authenticate and interact with Riot Games API
   - Build a robust data collection pipeline with rate limiting and error handling
   - Extract, transform, and store match data in structured format

2. **Data Science Application:**
   - Perform comprehensive exploratory data analysis (EDA)
   - Engineer meaningful features from raw game statistics
   - Identify correlations (Heatmap) between performance metrics and win outcomes

3. **Machine Learning Development:**
   - Train and compare multiple classification models (Logistic Regression, Random Forest, Gradient Boosting)
   - Optimize model performance through feature selection
   - Interpret model predictions and feature importance

---

## 📈 **Key Findings**

### **Win Prediction Performance:**
- **Best Model:** Logistic Regression
- **Accuracy:** 94.57% (87 correct predictions out of 92 test games)
- **ROC-AUC Score:** 0.986 (near-perfect discrimination)
- **Precision:** 98% for losses, 92% for wins
- **Recall:** 91% for losses, 98% for wins

### **Top Predictive Features (by correlation with winning):**
1. **Team Towers** (+0.705) - Strongest predictor
2. **Team Dragons** (+0.646) - Critical objective control
3. **KDA Ratio** (+0.498) - Individual performance metric
4. **Team Barons** (+0.461) - Game-closing objective
5. **Gold per Minute** (+0.449) - Economic efficiency

### **Gameplay Insights:**
- **Team objectives dominate individual skill:** 3 of top 4 predictors are team objectives (towers, dragons, barons)
- **KDA threshold identified:** KDA > 5 correlates with 80%+ win rate; KDA < 2 correlates with 14% win rate
- **Player playstyle:** Late-game scaler (57.4% win rate in 35+ min games vs 40% in <20 min games)
- **CS efficiency:** CS per minute shows minimal correlation (+0.068), indicating kills/objectives matter more than farming for this assassin playstyle

### **Strategic Recommendations:**
- **Prioritize dragons:** 0-1 dragons = 14% WR, 2+ dragons = 64%+ WR
- **Secure baron after wins:** 83% win rate when baron is secured
- **Push towers:** 6+ towers = 67% win rate, 9+ towers = 99% win rate
- **Survive early game:** Focus on reaching 2-3 item power spike (25-35 minutes)

## 📊 **Results Summary**

| Metric | Value |
|--------|-------|
| **Total Games Analyzed** | 460 |
| **Features Extracted** | 21 |
| **Model Accuracy** | 94.57% |
| **ROC-AUC Score** | 0.986 |
| **Test Set Size** | 92 games |
| **Correct Predictions** | 87 / 92 |
| **Top Predictor** | Team Towers (r=0.705) |

---

## 🔄 **Process**

### **1. Data Collection & Engineering**
- **API Authentication:** Secured Riot API key using environment variables (.env file)
- **Data Pipeline:** Built automated collection system with rate limiting (20 requests/sec, 100 requests/2min)
- **Match Filtering:** Extracted only CLASSIC queue Katarina matches from match history
- **Feature Extraction:** Parsed 21 features per match from API response including:
  - Personal stats: kills, deaths, assists, CS, gold, damage, level
  - Team objectives: dragons, barons, towers, first blood
  - Calculated metrics: KDA ratio, per-minute stats, participation rates
- **Data Storage:** Saved structured dataset to CSV (460 games × 21 features)

### **2. Exploratory Data Analysis (EDA)**
- **Win Rate Analysis:** Identified 51.09% overall win rate (235W-225L)
- **Performance Comparison:** Analyzed wins vs losses across all metrics
  - Dragons: +200% in wins
  - KDA: +200% in wins (8.54 vs 2.84)
  - Towers: +166.7% in wins
  - Damage per minute: +47.6% in wins
- **KDA Distribution:** Categorized games into performance tiers
  - Poor (<2): 14.1% win rate
  - Good (3-5): 44.3% win rate
  - Great (5-10): 79.8% win rate
  - Legendary (10+): 92.5% win rate
- **Game Duration:** Discovered player performs best in 35+ minute games
- **Objective Impact:** Quantified win rate by dragon/baron/tower count
- **Correlation Analysis:** Created heatmap identifying strongest predictors

### **3. Feature Engineering & Selection**
- Selected 11 most impactful features based on correlation analysis:
  - Team objectives: towers, dragons, barons
  - Performance: KDA ratio, kills, deaths, assists
  - Efficiency: gold/min, damage/min
  - Other: first blood, level
- Excluded low-correlation features: CS, CS/min, total gold, total damage
- Applied StandardScaler for Logistic Regression (not needed for tree-based models)

### **4. Machine Learning Modeling**
- **Data Split:** 80% train (368 games), 20% test (92 games), stratified by win/loss
- **Models Trained:**
  1. **Logistic Regression:** 94.57% accuracy, 0.986 AUC ✅ WINNER
  2. **Gradient Boosting:** 88.04% accuracy, 0.981 AUC
  3. **Random Forest:** 85.87% accuracy, 0.981 AUC
- **Evaluation Metrics:**
  - Confusion Matrix: 41 TN, 4 FP, 1 FN, 46 TP
  - Classification Report: 95% weighted F1-score
  - ROC Curve: Near-perfect separation (AUC = 0.986)

### **5. Model Interpretation**
- **Logistic Regression advantages:**
  - Strong linear relationships between features and outcome
  - No overfitting on small dataset (460 games)
  - Interpretable coefficients
  - Robust to feature scaling
- **Error Analysis:** Only 5 misclassifications out of 92 test games
  - 4 false positives: Predicted win but lost (winnable games thrown)
  - 1 false negative: Predicted loss but won (comeback victory)

---

## 💻 **Technologies Used**

### **Data Engineering & API:**
- **Python:** requests, urllib, json
- **API Integration:** Riot Games API v4
- **Rate Limiting:** Custom implementation (20/sec, 100/2min)
- **Error Handling:** Try-except blocks, status code validation
- **Security:** python-dotenv for environment variable management

### **Data Processing & Analysis:**
- **Python:** Pandas, NumPy
- **Data Cleaning:** Missing value handling, type conversions
- **Feature Engineering:** Calculated metrics (KDA, per-minute stats, rates)
- **Data Visualization:** Matplotlib, Seaborn

### **Machine Learning:**
- **Framework:** Scikit-learn
- **Preprocessing:** StandardScaler, train_test_split
- **Models:** 
  - LogisticRegression
  - RandomForestClassifier
  - GradientBoostingClassifier
- **Evaluation:** 
  - Metrics: accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve
  - Cross-validation: Stratified split
