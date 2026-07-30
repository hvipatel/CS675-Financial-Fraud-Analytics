# Geospatial Credit Card Fraud Analytics Using Apache Spark and AWS

## CS-675 Final Project

**Author:** Havi Patel

---

# Table of Contents

1. Project Overview
2. Business Problem
3. Project Objectives
4. System Architecture
5. Technology Stack
6. Dataset Description
7. Local Development Environment
8. Installation & Setup
9. Running the Project
10. Data Processing Pipeline
11. Spark Implementation
12. AWS Cloud Deployment
13. Results & Analysis
14. Repository Structure
15. Future Improvements
16. References

---

# 1. Project Overview

Financial institutions process millions of credit card transactions every day, making fraud detection a significant challenge. Traditional data processing techniques become increasingly inefficient as transaction volumes continue to grow, requiring scalable distributed computing solutions capable of handling large datasets efficiently.

This project demonstrates a complete big data analytics workflow using Apache Spark to process and analyze **24,386,900** IBM credit card transactions. To provide additional geographic context, the transaction data is enriched using the **U.S. Census ZIP Code Tabulation Area (ZCTA) Gazetteer**, enabling location-based fraud analysis.

Beyond local Spark analytics, the project extends into the cloud by deploying supporting infrastructure on AWS using Terraform. The processed datasets are stored in Amazon S3, cataloged using AWS Glue, and queried through Amazon Athena to validate that cloud-based analytical results are consistent with those generated locally in Apache Spark.

The project showcases distributed data processing, geospatial data enrichment, cloud analytics, and reproducible infrastructure deployment while demonstrating practical applications of big data technologies in financial fraud analysis.

---

# 2. Business Problem

Financial organizations generate enormous volumes of transaction data each day. Detecting fraudulent activity within these datasets requires systems capable of processing millions of records efficiently while producing timely and accurate analytical insights.

Traditional single-machine processing approaches struggle to scale as data volumes increase, resulting in slower query performance and limited analytical capability. Distributed computing frameworks such as Apache Spark overcome these limitations by partitioning workloads across multiple processing cores, significantly improving performance for large-scale data analytics.

This project addresses these challenges by developing a scalable fraud analytics pipeline capable of processing over 24 million credit card transactions, enriching them with geographic reference data, and generating business insights that can support fraud monitoring and decision-making.

---

# 3. Project Objectives

The primary goal of this project is to demonstrate how Apache Spark can be used to perform scalable financial fraud analytics on a large transaction dataset while integrating cloud technologies for validation and reproducibility.

The specific objectives are:

- Process over **24 million** credit card transactions using Apache Spark.
- Identify fraud patterns across payment methods, merchant categories, transaction amounts, and geographic locations.
- Enrich transaction records using U.S. Census ZIP Code Tabulation Area (ZCTA) reference data.
- Demonstrate distributed data processing techniques using Spark DataFrames.
- Validate analytical results using Amazon Athena.
- Deploy cloud infrastructure using Terraform.
- Produce business insights that support fraud monitoring and decision-making.

---

# 4. System Architecture

The project follows a complete big data analytics pipeline beginning with local Spark processing and ending with cloud-based validation on AWS.

```text
                    IBM Credit Card Transactions
                                 │
                                 ▼
                        Apache Spark (PySpark)
                                 │
                                 ▼
                     Data Cleaning & Preparation
                                 │
                                 ▼
                  ZIP Code Enrichment (Broadcast Join)
                                 │
                                 ▼
                     Fraud Analytics & Aggregations
                                 │
                                 ▼
                     Business Insights & Results
                                 │
                ┌────────────────┴────────────────┐
                ▼                                 ▼
          Local Spark Results              Upload to Amazon S3
                                                  │
                                                  ▼
                                            AWS Glue Catalog
                                                  │
                                                  ▼
                                             Amazon Athena
                                                  │
                                                  ▼
                                  Validation of Spark Results
```

The processing pipeline performs all analytical operations locally using Apache Spark. The resulting datasets are then stored in Amazon S3, cataloged using AWS Glue, and queried through Amazon Athena to confirm that cloud-based analytics produce results consistent with those generated locally.

---

# 5. Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Primary programming language |
| Apache Spark (PySpark) | Distributed data processing and analytics |
| JupyterLab | Interactive notebook development |
| Docker | Local development environment |
| Java 17 | Spark runtime dependency |
| uv | Python dependency and environment management |
| Git | Version control |
| GitHub | Source code hosting and collaboration |
| Amazon S3 | Cloud data storage |
| AWS Glue Data Catalog | Metadata management |
| Amazon Athena | Cloud SQL analytics |
| Terraform | Infrastructure as Code (IaC) |

---

# 6. Dataset Description

This project combines two datasets to perform scalable financial fraud analytics with geospatial enrichment.

## Dataset 1: IBM Credit Card Transactions (Version 2)

The primary dataset contains historical credit card transactions used to analyze fraudulent activity.

### Dataset Summary

| Attribute | Value |
|-----------|-------|
| File Name | credit_card_transactions-ibm_v2.csv |
| Format | CSV |
| Total Records | 24,386,900 |
| Features | 15 |

### Dataset Schema

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

This dataset contains both legitimate and fraudulent transactions, allowing fraud patterns to be analyzed across multiple dimensions including payment methods, merchant categories, transaction amounts, and geographic locations.

---

## Dataset 2: U.S. Census ZIP Code Tabulation Area (ZCTA) Gazetteer

The second dataset provides ZIP Code reference information used to enrich the transaction data with geographic context.

### Dataset Summary

| Attribute | Value |
|-----------|-------|
| File Name | 2025_Gaz_zcta_national.txt |
| Format | Text |
| Purpose | ZIP Code lookup and geographic enrichment |

The ZCTA dataset enables transaction records to be matched with ZIP Code reference information, supporting location-based fraud analysis.

---

# 7. Local Development Environment

The project was developed and tested using the following software environment:

| Component | Version |
|----------|---------|
| Operating System | macOS |
| Python | 3.12 |
| Apache Spark | 3.5.8 |
| Java | 17 |
| JupyterLab | Latest |
| Docker Desktop | Latest |
| uv | Latest |
| Git | Latest |

---

# 8. Installation & Setup

## Clone the Repository

```bash
git clone https://github.com/hvipatel/CS675-Financial-Fraud-Analytics.git
```

## Navigate to the Project Directory

```bash
cd CS675-Financial-Fraud-Analytics
```

## Install Dependencies

```bash
cd code-starter
uv sync
```

## Activate the Virtual Environment

```bash
source .venv/bin/activate
```

## Launch JupyterLab

```bash
uv run jupyter lab
```

After JupyterLab opens in the browser, navigate to:

```text
code-starter/
└── CS675_Financial_Fraud_Project/
    └── notebooks/
        └── financial_fraud_analysis.ipynb
```

Open the notebook and execute the cells in order to reproduce the analysis.

---

# 9. Running the Project

The notebook performs the following workflow:

1. Load the IBM Credit Card Transactions dataset.
2. Load the U.S. Census ZCTA reference dataset.
3. Clean and prepare both datasets.
4. Enrich transaction records using ZIP Code matching.
5. Perform fraud analysis using Apache Spark.
6. Generate summary statistics and business insights.
7. Validate the analytical results using Amazon Athena.

---

# 10. Data Processing Pipeline

The project follows a structured data processing pipeline to transform raw transaction records into meaningful fraud analytics.

## Step 1 – Data Loading

Both datasets are loaded into Apache Spark DataFrames.

- IBM Credit Card Transactions dataset
- U.S. Census ZCTA Gazetteer dataset

Spark automatically distributes the data across partitions, allowing efficient processing of over 24 million transaction records.

---

## Step 2 – Data Cleaning and Preparation

The transaction dataset was prepared before analysis by:

- Removing currency symbols from transaction amounts
- Converting data types
- Handling missing ZIP Code values
- Verifying dataset schema
- Preparing fields for Spark transformations

The ZIP Code reference dataset was also cleaned to support accurate joins.

---

## Step 3 – Geographic Data Enrichment

The transaction dataset was enriched using the ZIP Code reference dataset.

A Spark **broadcast join** was used because the ZCTA lookup table is significantly smaller than the transaction dataset. Broadcasting the lookup table minimizes network communication and improves join performance.

Approximately **87.02%** of transaction records were successfully matched with ZIP Code reference information.

---

## Step 4 – Fraud Analytics

After enrichment, multiple analytical queries were performed, including:

- Fraud rate calculation
- Fraud by payment method
- Fraud by merchant category (MCC)
- Fraud by state
- Fraud by ZIP Code
- Fraud by transaction amount
- Summary statistics

These analyses demonstrate how distributed processing can efficiently aggregate millions of transaction records.

---

# 11. Apache Spark Implementation

Apache Spark was selected because it supports scalable distributed processing for large datasets that exceed the practical limits of traditional single-machine analysis.

The implementation uses the Spark DataFrame API to perform transformations and aggregations efficiently.

### Key Spark Features Used

- Spark DataFrames
- Distributed aggregations
- Filtering
- GroupBy operations
- Broadcast joins
- SQL functions
- Data type conversions

### Broadcast Join

The ZIP Code lookup dataset is relatively small compared to the transaction dataset.

Using Spark's broadcast join allows the lookup table to be copied to each executor, reducing shuffle operations and improving join performance during geographic enrichment.

### Distributed Analytics

Spark partitions the dataset across available processing resources, allowing millions of transactions to be analyzed in parallel while maintaining efficient execution times.

---

# 12. AWS Cloud Deployment

After completing the local Spark analysis, the project was deployed to AWS to validate the analytical results in a cloud environment.

## Cloud Services Used

- Amazon S3
- AWS Glue Data Catalog
- Amazon Athena
- Terraform

## Infrastructure Deployment

Terraform was used to provision the required AWS infrastructure, including:

- S3 bucket
- Glue Database
- Athena Workgroup

Infrastructure as Code makes the deployment reproducible and easier to manage.

## Data Validation

Both datasets were uploaded to Amazon S3.

AWS Glue catalogs were created to define the datasets.

Amazon Athena SQL queries were executed to reproduce the fraud analyses performed locally in Apache Spark.

The Athena query results matched the Spark results, demonstrating consistency between local distributed processing and cloud-based analytics.

---

# 13. Results & Analysis

The project successfully demonstrated scalable fraud analytics using Apache Spark on a dataset containing more than 24 million financial transactions.

## Processing Summary

| Metric | Result |
|---------|--------|
| Total Transactions Processed | 24,386,900 |
| Fraudulent Transactions | 29,757 |
| Overall Fraud Rate | 0.122% |
| ZIP Code Enrichment Rate | Approximately 87.02% |

---

## Fraud Analysis Performed

The following analyses were completed using Apache Spark and validated using Amazon Athena:

- Overall fraud rate
- Fraud by payment method
- Fraud by merchant category (MCC)
- Fraud by merchant state
- Fraud by ZIP Code
- Fraud by transaction amount
- Geographic enrichment analysis
- Summary statistics

The Spark and Athena results were consistent across all validation queries, demonstrating that the cloud implementation accurately reproduced the local analytics.

---

## Business Insights

Several important insights were identified during the analysis:

- Fraud represented approximately **0.122%** of all processed transactions.
- Online transactions showed the highest number of fraudulent transactions.
- Fraud distribution varied across merchant categories and geographic regions.
- Geographic enrichment enabled location-based fraud analysis using ZIP Code reference data.
- Apache Spark efficiently processed a dataset containing more than 24 million records while maintaining scalable performance.

---

# 14. Repository Structure

```text
CS675-Financial-Fraud-Analytics/
│
├── README.md
│
├── code-starter/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── docker-compose.yml
│   └── CS675_Financial_Fraud_Project/
│       ├── README.md
│       ├── datasets/
│       ├── notebooks/
│       │   └── financial_fraud_analysis.ipynb
│       ├── docs/
│       ├── output/
│       └── src/
│
└── cloud-starter/
    └── student-workspace/
```

---

# 15. Future Improvements

Potential enhancements for future versions of the project include:

- Implement real-time fraud detection using Apache Spark Structured Streaming.
- Develop machine learning models for fraud prediction using Spark MLlib.
- Build an interactive dashboard for fraud monitoring using Tableau or Power BI.
- Deploy the Spark workload on Amazon EMR for distributed cloud processing.
- Expand the analysis by incorporating additional financial or merchant datasets.

---

# 16. References

1. IBM Credit Card Transactions Dataset (Version 2)
2. U.S. Census Bureau ZIP Code Tabulation Area (ZCTA) Gazetteer
3. Apache Spark Documentation – https://spark.apache.org/docs/latest/
4. AWS Documentation – https://docs.aws.amazon.com/
5. Terraform Documentation – https://developer.hashicorp.com/terraform/docs

---

# Conclusion

This project demonstrates a complete end-to-end big data analytics workflow by combining Apache Spark, geospatial data enrichment, and AWS cloud services to analyze large-scale financial transaction data.

By integrating distributed computing with cloud-based validation, the project illustrates how modern big data technologies can efficiently process millions of records while generating meaningful business insights for fraud analysis. The implementation also demonstrates reproducible infrastructure deployment using Terraform and highlights the practical application of scalable analytics in the financial domain.


