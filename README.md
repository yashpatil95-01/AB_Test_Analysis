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
The dataset is sourced from Kaggle's [A/B Test Results](https://www.kaggle.com/datasets/adarsh0806/ab-testing-practice) dataset. Download the CSV file and place it in the project directory.

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


## Results

The analysis outputs:
- Statistical test results in console
- Summary CSV file saved to `results/ab_test_summary.csv`
- Clear recommendation based on p-value significance

## Author

**Yash Patil** - Manufacturing Engineer → Data Analytics