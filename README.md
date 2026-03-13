# Enterprise Demand Forecasting & Inventory Optimization

## Overview

This project implements an end-to-end **demand forecasting and inventory optimization pipeline** using the **M5 Forecasting dataset**. The goal is to forecast product demand and determine optimal inventory policies that minimize total supply chain costs while maintaining a desired service level.

The project combines **data engineering, forecasting models, and operations research techniques** to simulate how different service levels affect inventory costs. By modeling holding cost, ordering cost, and stockout penalties, the system identifies the **service level that minimizes total inventory cost**.

This type of analysis is commonly used in **retail, e-commerce, and supply chain management** to balance product availability with operational efficiency.

---

## Problem Statement

Retail companies must maintain sufficient inventory to satisfy customer demand while minimizing operational costs. Maintaining high inventory levels improves product availability but increases holding costs. On the other hand, maintaining low inventory reduces holding costs but increases the risk of stockouts, lost sales, and customer dissatisfaction.

The key challenge is determining the **optimal service level** that balances these competing costs.

This project analyzes how service level impacts the following cost components:

* **Holding Cost** – Cost of storing and maintaining inventory
* **Ordering Cost** – Cost incurred when placing replenishment orders
* **Stockout Cost** – Cost associated with running out of inventory
* **Total Cost** – Combined effect of all inventory costs

By simulating service levels between **80% and 99%**, the model identifies the service level that **minimizes total inventory cost**.

---

## Dataset

The project uses the **M5 Forecasting dataset**, which contains historical sales data for thousands of products across multiple stores and categories.

The dataset includes:

* Product level sales history
* Calendar information
* Price data
* Store and category metadata

These datasets are combined to build demand forecasting models and simulate inventory decisions.

---

## Project Architecture

```
m5-demand-forecasting-inventory-optimization
│
├── notebooks
│   Exploratory analysis and experimentation
│
├── sql
│   SQL pipeline used for data preparation and feature engineering
│
├── src
│   Core Python scripts for forecasting models and inventory simulation
│
├── reports
│   Generated figures and analysis results
│
├── requirements.txt
│   Python dependencies
│
└── README.md
   Project documentation
```

---

## Methodology

### 1. Data Preparation

The raw dataset is processed using a structured SQL pipeline. Feature engineering includes:

* Calendar features
* Price related features
* Demand volatility analysis
* Lag and rolling statistics

These features help improve the accuracy of forecasting models.

---

### 2. Demand Forecasting

Machine learning models are used to predict future product demand. The forecasting stage provides expected demand values that serve as inputs for inventory optimization.

Typical forecasting techniques used include:

* Gradient Boosting models (LightGBM)
* Time series feature engineering
* Lag-based demand predictors

---

### 3. Inventory Optimization Model

The inventory system uses classical **Economic Order Quantity (EOQ)** and **Safety Stock** models.

Key components include:

**Economic Order Quantity (EOQ)**
Determines the optimal order quantity that minimizes ordering and holding costs.

**Safety Stock Calculation**
Safety stock is computed based on demand variability and lead time uncertainty.

**Service Level Simulation**
The model evaluates service levels from **0.80 to 0.99** and calculates:

* Holding cost
* Ordering cost
* Stockout cost
* Total inventory cost

---

## Cost Tradeoff Analysis

As service level increases:

* **Holding cost increases** because more safety stock must be maintained.
* **Stockout cost decreases** because shortages become less frequent.
* **Ordering cost remains relatively constant.**

These competing effects create a **U-shaped total cost curve**.

The optimal service level occurs at the point where **total inventory cost is minimized**.

---

## Results

The simulation identifies the service level where total inventory cost is minimized.

Example result from the model:

* **Optimal Service Level:** ~97%
* **Minimum Total Cost:** Determined by the simulation output

At this point, the balance between stock availability and inventory carrying cost is optimal.

---

## Key Concepts Demonstrated

This project demonstrates several important supply chain and analytics concepts:

* Demand forecasting
* Feature engineering for time series data
* Economic Order Quantity (EOQ)
* Safety stock modeling
* Service level optimization
* Cost trade-off analysis
* Simulation based decision making

These techniques are widely used in **retail analytics, supply chain management, and operations consulting**.

---

## Technologies Used

* Python
* Pandas
* NumPy
* LightGBM
* SQL
* Jupyter Notebooks
* Data visualization libraries

---

## Future Improvements

Possible extensions of this project include:

* Multi-product inventory optimization
* Reinforcement learning based inventory control
* Demand uncertainty simulations
* Integration with real-time dashboards
* Supply chain network optimization

---

## Applications

The methods used in this project are applicable in industries such as:

* Retail and e-commerce
* Supply chain management
* Logistics optimization
* Operations strategy
* Inventory planning systems

---

## Author

**Satvik Asthana**

B.Tech Robotics & AI
Manav Rachna University

Interests:

* Machine Learning
* Data Analytics
* Supply Chain Optimization
* AI Systems

