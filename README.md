# Commercial Margin Intelligence Platform
### Shifting Supply Chain Analytics from Volume to Profitability Optimization

---

## 📋 Executive Overview
Traditional supply chain reporting frameworks heavily prioritize volume-based metrics such as gross sales, shipment velocity, and order fulfillment rates. However, high sales volume frequently masks critical margin erosion driven by operational friction, structural underpricing, and suboptimal customer contracts. 

This repository contains an end-to-end commercial intelligence engine built for **APL Logistics** using **171,860 clean transaction records**. By implementing a strict python financial validation pipeline, multi-dimensional exploratory diagnostics, and an unsupervised machine learning model (K-Means Clustering), this platform successfully exposes hidden profit leaks and provides an interactive simulation layer for executive decision-making.

### 📊 Core Financial Matrix Uncovered
* **Total Clean Revenue Volume Analyzed:** `$35,088,763.20`
* **Net Operational Profitability:** `$3,795,103.65`
* **Global Corporate Net Profit Margin:** `10.82%`

---

## 🔍 Key Business Discoveries

### 1. The Strength Training Revenue Trap
While specialty categories like *Golf Bags & Carts* lead company profitability with a strong **17.46% net margin**, high-volume mainstream categories act as severe financial drains. The **Strength Training** category generated a massive **$53,950.53** in top-line sales volume but returned a net profit of only **$130.35**—translating to a near-zero operational margin of **0.24%**.

### 2. The Flat-Line Discount Anomaly
Statistical grouping disproved the common corporate hypothesis that front-end promotional discounting drives transaction losses. As discount rates scaled from **0% up to 25%**, the percentage of orders resulting in a financial loss remained completely locked between **18% and 19%**. This flat-line distribution proves that loss-making transactions are trapped by fixed back-end supply chain operational issues (e.g., freight carrier rates, handling overhead) rather than promotional coupon abuse.

### 3. Algorithmic Tier 4 Customer Risks (K-Means Clustering)
An unsupervised machine learning clustering model trained on standardized historical customer data exposed a major vulnerability. The pipeline successfully isolated a high-volume risk tier consisting of **1,955 customer accounts**. While they mimic high-value "Champions" on paper by averaging **$2,974.36 each** in sales, the algorithm unmasked them as highly destructive to corporate capital, generating a severe average net loss of **-$428.77 per account**.

---

## 🛠️ Project Repository Architecture

```text
Supply_Chain_Profitability_Analysis/
│
├── Notebook/                       
│   ├── data_cleaning.py               # Phase 2: Structural validation & anomaly extraction
│   ├── margin_analytics.py            # Phase 3: Multi-dimensional financial diagnostics
│   └── customer_segmentation.py       # Phase 3.5: Scikit-Learn K-Means pipeline
│
├── app/
│   ├── dashboard.py                   # Phase 4: Streamlit interactive platform script
│   └── screenshot1.png                # Embedded layout graphics
│
├── data/                              # Data directories (Kept local/ignored for privacy)
│   ├── APL_Logistics_Cleaned.csv
│   └── APL_Logistics_Segmented.csv
│
├── Project_Report.html                # Executive styled dashboard report HTML
└── README.md                          # Repository main landing briefing