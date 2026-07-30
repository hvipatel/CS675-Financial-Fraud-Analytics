# Financial Fraud Analytics at Cloud Scale Using Apache Spark

## CS-675 Final Project

### Author
Havi Patel

---

# Project Overview

Financial institutions process millions of credit card transactions every day. Detecting fraudulent transactions quickly and accurately is essential to reducing financial losses and protecting customers.

This project develops a scalable fraud analytics platform using Apache Spark to analyze a large-scale credit card transaction dataset. By leveraging distributed computing, the project demonstrates how big data technologies can efficiently process millions of transactions, identify fraud patterns, and generate actionable business insights.

The project is being developed as part of the CS-675 Big Data Analytics at Cloud Scale course.

---

# Project Objectives

The objectives of this project are to:

- Process over 24 million credit card transactions using Apache Spark.
- Explore fraudulent and legitimate transaction patterns.
- Identify fraud trends based on merchant category, transaction amount, location, and payment method.
- Demonstrate distributed data processing techniques.
- Apply Spark optimizations such as caching and partitioning.
- Generate visualizations and business insights for fraud analysis.

---

# Dataset

**Dataset Name:** IBM Credit Card Transactions Dataset (Version 2)

### Dataset Summary

- Total Records: **24,386,900**
- Total Features: **15**
- Dataset Type: Financial Transactions
- File Format: CSV

### Dataset Features

- User
- Card
- Year
- Month
- Day
- Time
- Amount
- Use Chip
- Merchant Name
- Merchant City
- Merchant State
- Zip
- MCC
- Errors?
- Is Fraud?

---

# Technologies Used

- Python
- Apache Spark (PySpark)
- Jupyter Notebook
- Java 17
- Docker
- Git
- GitHub
- AWS (planned deployment)

---

# Project Structure

```
CS675_Financial_Fraud_Project/

├── README.md
├── datasets/
├── notebooks/
├── src/
├── results/
├── images/
└── docs/
```

---

# Current Progress

### Completed

- Environment setup
- Apache Spark configured
- Jupyter Notebook configured
- Dataset successfully loaded
- Spark session verified

### Current Phase

Data Understanding

---

# Planned Analysis

The project will answer questions such as:

- What percentage of transactions are fraudulent?
- Which merchant categories experience the most fraud?
- Which states have the highest fraud activity?
- Does chip usage reduce fraud?
- Which transaction amounts are associated with fraud?
- During which hours does fraud occur most frequently?
- Which merchants generate the highest number of fraudulent transactions?

---

# Expected Outcome

The final deliverable will be a scalable fraud analytics platform capable of processing over 24 million financial transactions using Apache Spark. The project will demonstrate distributed data processing, performance optimization, and analytical reporting while producing actionable fraud insights.

---

## Project Status

**Current Status:** 🟢 In Progress