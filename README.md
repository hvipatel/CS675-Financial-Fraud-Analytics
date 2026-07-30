# Geospatial Credit Card Fraud Analytics Using Apache Spark and AWS

## CS-675 Final Project

**Author:** Havi Patel

---

## Project Overview

This repository contains my final project for **CS-675: Big Data Analytics at Cloud Scale**.

The project demonstrates how Apache Spark can be used to process and analyze large-scale financial transaction data efficiently. A dataset containing over **24 million** credit card transactions is analyzed to identify fraud patterns and generate business insights. The transaction data is enriched using U.S. Census ZIP Code Tabulation Area (ZCTA) data to support geospatial fraud analysis.

The project also demonstrates cloud-based analytics by validating Apache Spark results using **AWS S3**, **AWS Glue**, and **Amazon Athena**, with infrastructure provisioned through **Terraform**.

---

## Project Highlights

- Processed **24,386,900** credit card transactions using Apache Spark
- Performed distributed data processing and aggregation
- Enriched transaction data with U.S. Census ZIP Code information
- Analyzed fraud by:
  - Payment method
  - Merchant category (MCC)
  - State
  - ZIP Code
  - Transaction amount
- Validated Spark analytical results using Amazon Athena
- Demonstrated cloud deployment using Infrastructure as Code (Terraform)

---

## Technologies Used

- Apache Spark (PySpark)
- Python
- JupyterLab
- Docker
- AWS S3
- AWS Glue Data Catalog
- Amazon Athena
- Terraform
- Git & GitHub

---

## Datasets

### Dataset 1 — IBM Credit Card Transactions (Version 2)

- 24,386,900 transaction records
- 15 transaction attributes
- Includes fraud labels and merchant information

### Dataset 2 — U.S. Census ZCTA Gazetteer

- 33,791 ZIP Code Tabulation Areas
- Used for geographic enrichment of transaction data

---

## Key Results

| Metric | Result |
|---------|--------|
| Total Transactions | 24,386,900 |
| Fraudulent Transactions | 29,757 |
| Fraud Rate | 0.122% |
| ZIP Code Match Rate | Approximately 87.02% |

---

## Repository Structure

```text
.
├── README.md
├── code-starter/
│   ├── CS675_Financial_Fraud_Project/
│   │   ├── README.md
│   │   ├── notebooks/
│   │   ├── src/
│   │   ├── docs/
│   │   ├── output/
│   │   └── datasets/
│   ├── docker-compose.yml
│   ├── pyproject.toml
│   └── uv.lock
└── cloud-starter/
    └── student-workspace/
```

---

## Project Documentation

Detailed project documentation, implementation steps, setup instructions, and analytical results are available in:

```text
code-starter/CS675_Financial_Fraud_Project/README.md
```

---

## Project Status

**Status:** Completed !!

This project successfully demonstrates scalable financial fraud analytics using Apache Spark and AWS cloud technologies.

---

## Acknowledgment

This project was completed as part of the requirements for **CS-675: Big Data Analytics at Cloud Scale**.

###Link for the project: https://github.com/hvipatel/CS675-Financial-Fraud-Analytics/tree/main/code-starter

