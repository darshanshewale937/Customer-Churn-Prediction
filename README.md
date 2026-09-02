\# Customer Churn Prediction



An end-to-end machine learning project that predicts whether a telecom customer is likely to churn.



\## Project Overview



This project uses the IBM Telco Customer Churn dataset to:



\- Clean and explore customer data

\- Identify churn patterns

\- Train and compare machine learning models

\- Predict churn through a Streamlit web application



\## Dataset



The dataset contains 7,043 customer records and 21 columns, including:



\- Demographics

\- Account information

\- Service subscriptions

\- Billing details

\- Churn status



\## Key Findings



\- Month-to-month customers had the highest churn rate: 42.71%

\- Fiber optic customers had a churn rate of 41.89%

\- Customers using electronic checks had the highest churn rate: 45.29%



\## Models Used



\- Logistic Regression

\- Random Forest Classifier



\## Model Performance



| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |

|---|---:|---:|---:|---:|---:|

| Logistic Regression | 80.55% | 65.72% | 55.88% | 60.40% | 84.21% |

| Random Forest | 77.08% | 56.06% | 63.10% | 59.37% | 82.20% |



Logistic Regression was selected as the best overall model based on accuracy, precision, F1-score, and ROC-AUC.



\## Tools and Technologies



\- Python

\- Pandas

\- NumPy

\- Matplotlib

\- Seaborn

\- Scikit-learn

\- Streamlit



\## Project Structure



```text

customer-churn-prediction/

├── app/

│   └── app.py

├── data/

│   └── WA\_Fn-UseC\_-Telco-Customer-Churn.csv

├── models/

│   └── churn\_model.joblib

├── notebooks/

│   └── churn\_analysis.ipynb

├── requirements.txt

└── README.md

\## Author

Darshan Shewale

