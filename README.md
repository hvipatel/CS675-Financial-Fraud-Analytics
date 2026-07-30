# Geospatial Credit Card Fraud Analytics Using Apache Spark and AWS

This repository contains my CS-675 Final Project for Big Data Analytics at Cloud Scale.

## Project Overview

The project analyzes 24,386,900 credit card transactions using Apache Spark and enriches them with U.S. Census ZIP Code data for geospatial fraud analysis.

The local Spark results were also validated in AWS using S3, Glue, and Athena.

## Technologies

- Apache Spark
- PySpark
- Python
- JupyterLab
- Docker
- AWS S3
- AWS Glue
- AWS Athena
- Terraform

## Datasets

1. IBM Credit Card Transactions  
   - 24,386,900 transaction records
   - Includes payment method, amount, merchant information, ZIP code, and fraud label

2. U.S. Census ZCTA Gazetteer  
   - 33,791 ZIP Code Tabulation Areas
   - Used for geographic enrichment

## Key Results

- Total transactions: 24,386,900
- Fraudulent transactions: 29,757
- Overall fraud rate: approximately 0.122%
- Online transactions had the highest number of fraudulent transactions
- Spark and Athena produced matching analytical results
- Geographic enrichment matched approximately 87.02% of transaction records

## Repository Structure

```text
code-starter/
└── CS675_Financial_Fraud_Project/
    ├── notebooks/
    ├── src/
    ├── docs/
    ├── output/
    └── README.md

cloud-starter/
└── student-workspace/
    └── Terraform configuration

###Link for the project: https://github.com/hvipatel/CS675-Financial-Fraud-Analytics/tree/main/code-starter

