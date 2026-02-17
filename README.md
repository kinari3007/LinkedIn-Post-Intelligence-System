# LinkedIn Post Intelligence System

A data-driven system to analyze LinkedIn post captions and predict engagement potential.

## Setup Instructions

### 1. Virtual Environment
A virtual environment has been created in the `venv` folder.

### 2. Activate Virtual Environment
```bash
# On Windows
.\venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
All required libraries are already installed. If you need to reinstall:
```bash
pip install -r requirements.txt
```

### 4. Run the Notebook
```bash
jupyter notebook notebooks/02_engagement_prediction_model.ipynb
```

## Project Structure
- `data/raw/` - Contains the LinkedIn dataset (LinkedIN_Caption_DataSet.xlsx)
- `notebooks/` - Jupyter notebooks for analysis and modeling
- `src/models/` - Saved models and vectorizers
- `requirements.txt` - All Python dependencies with exact versions

## Model Features
- Predicts engagement scores (High/Medium/Low) based on post content
- Identifies which content lines drive engagement predictions
- Uses Random Forest classifier with TF-IDF features
- Provides line-by-line content attribution analysis with impact scores
- Visualizes feature importance and model performance

## Dataset
The dataset contains 2,500 LinkedIn posts with:
- Post content/text
- Likes, comments, and shares metrics
- Engagement calculated as: likes + (2 × comments) + (3 × shares)
