```
ab-test-analysis/
│
├── ab_test_analysis.py
├── ab_test_analysis.ipynb
├── README.md
└── requirements.txt
```

# A/B Test Analysis

## Objective
Evaluate the results of an A/B test to determine if a new product feature should be rolled out, using statistical hypothesis testing.

## Tools Used
- Python (pandas, scipy.stats)
- Jupyter Notebook

## Dataset
The dataset is sourced from Kaggle's [A/B Test Results](https://www.kaggle.com/rohitsahoo/ab-testing) dataset. Download the CSV file and place it in the project directory.

## Key Tasks
- Load and explore the dataset
- Perform hypothesis testing on conversion rates
- Calculate p-values and confidence intervals
- Provide a clear recommendation based on statistical evidence

## How to Run

1. Clone the repo.
2. Download the dataset CSV from Kaggle and place it inside the repo folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Requirements
```bash
pandas
statsmodels

```   