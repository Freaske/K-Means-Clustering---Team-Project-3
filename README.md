# GROUP 3 - K-means Clustering Final Project

## Project Overview

This project implements the **K-means clustering algorithm in Python** and applies it to gene expression data.

The program reads the `Longotor1delta` dataset, uses only the genes listed in `interested_genes.txt`, normalizes the selected gene expression data, and then runs a manually implemented K-means clustering algorithm using different values of K. The final result is analyzed in a one-page conclusion report.

---

## Important Note

The following parts are implemented manually:

* Data filtering
* Data normalization
* Euclidean distance calculation
* Centroid initialization
* Cluster assignment
* Centroid update
* K-means iteration loop
* SSE/WCSS calculation for comparing different K values

The project does **not** use:

```python
sklearn.cluster.KMeans
scipy
any built-in clustering function
```

Only basic Python modules may be used for file handling and simple operations, such as:

```python
csv
random
math
```

---

## Project Requirements

The project performs the following steps:

1. Read the gene expression dataset.
2. Read the interested gene list from `interested_genes.txt`.
3. Filter the dataset and keep only the genes listed in `interested_genes.txt`.
4. Normalize the gene expression values.
5. Run the K-means clustering algorithm implemented from scratch.
6. Test different K values.
7. Compare clustering results using SSE/WCSS and cluster size distribution.
8. Write a one-page conclusion report in English.

---

## Folder Structure

```text
kmeans-gene-clustering-final-project/
│
├── README.md
├── main.py
│
├── data/
│   ├── Longotor1delta.xls
│   ├── Longotor1delta.csv
│   ├── interested_genes.txt
│   ├── filtered_data.csv
│   └── normalized_data.csv
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── metrics.py
│   └── kmeans.py
│
├── output/
│   ├── clusters_output.txt
│   └── k_results_summary.csv
│
└── report/
    └── conclusion_report.pdf
```

If the program is run in IDLE and reading `.xls` directly is difficult, the Excel file can be saved as `.csv` first. The K-means algorithm is still implemented manually from scratch.

---

## Dataset

### Input Files

* `Longotor1delta.xls`
  Original gene expression dataset.

* `Longotor1delta.csv`
  CSV version of the original dataset, used for easier execution in Python IDLE.

* `interested_genes.txt`
  A text file containing the list of genes that should be selected from the original dataset.

### Output Files

* `filtered_data.csv`
  Contains only the selected genes from `interested_genes.txt`.

* `normalized_data.csv`
  Contains the normalized expression values.

* `clusters_output.txt`
  Contains the clustering results for different K values.

* `k_results_summary.csv`
  Contains the comparison table for K values, SSE/WCSS, and cluster information.

---

## Methodology

### 1. Data Loading

The program first reads the list of interested genes from `interested_genes.txt`.

Then, it reads the gene expression dataset and keeps only the rows whose gene names appear in the interested gene list.

### 2. Data Normalization

Before applying K-means clustering, the selected gene expression values are normalized using z-score normalization:

```text
normalized_value = (value - mean) / standard_deviation
```

Normalization is necessary because different expression features may have different value ranges. Without normalization, features with larger numeric values could dominate the distance calculation.

### 3. K-means Clustering from Scratch

The K-means algorithm is implemented manually using the following steps:

1. Choose K initial centroids.
2. Assign each gene to the nearest centroid using Euclidean distance.
3. Recalculate each centroid based on the mean of the assigned genes.
4. Repeat the assignment and update steps until the clusters no longer change or the maximum number of iterations is reached.

The Euclidean distance between two data points is calculated manually:

```text
distance = sqrt((x1 - y1)^2 + (x2 - y2)^2 + ... + (xn - yn)^2)
```

### 4. Testing Different K Values

The program tests multiple K values, such as:

```text
K = 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
```

For each K value, the program records:

* SSE/WCSS
* Number of clusters
* Smallest cluster size
* Largest cluster size
* Whether empty clusters appear
* General comment about the clustering result

### 5. Evaluation

The clustering quality is evaluated mainly by:

* SSE/WCSS value
* Balance of cluster sizes
* Interpretability of the clustering result

A lower SSE/WCSS generally indicates that genes are closer to their assigned centroids. However, increasing K usually decreases SSE/WCSS, so the final K should be selected based on both SSE/WCSS and meaningful cluster distribution.

---

## How to Run

This project is designed to run in **Python IDLE** or a normal Python compiler.

### Steps

1. Open `main.py` in Python IDLE.
2. Make sure all required input files are placed in the correct folder.
3. Press `F5` to run the program.
4. Check the output files in the `output/` folder.

### Expected Output

After running the program, the console should display results similar to:

```text
K = 2, SSE = ...
K = 3, SSE = ...
K = 4, SSE = ...
...
K = 10, SSE = ...
```

The detailed cluster results will be saved in:

```text
output/clusters_output.txt
```

The summary table will be saved in:

```text
output/k_results_summary.csv
```

---

## Main Functions

### Data Loading

```python
read_interested_genes(filename)
read_gene_data(filename, interested_genes)
```

These functions read the interested gene list and filter the gene expression dataset.

### Preprocessing

```python
normalize_by_column(data)
```

This function normalizes the expression data by column.

### Metrics

```python
euclidean_distance(point1, point2)
calculate_sse(clusters, centroids)
```

These functions calculate distance and SSE/WCSS manually.

### K-means Algorithm

```python
kmeans(data, gene_names, k, max_iterations=100)
```

This function performs K-means clustering from scratch and returns the final clusters, centroids, and SSE/WCSS value.

---

## Team Member Responsibilities

| Member   | Responsibility                                                                |
| -------- | ----------------------------------------------------------------------------- |
| Member 1 | Data loading and gene filtering                                               |
| Member 2 | Data normalization, Euclidean distance, and SSE/WCSS calculation              |
| Member 3 | K-means algorithm implementation from scratch                                 |
| Member 4 | Running experiments with different K values and writing the conclusion report |

---

## Experiment Summary

The experiment tests different K values and compares the clustering results.

| K  |     SSE/WCSS | Smallest Cluster Size | Largest Cluster Size | Comment               |
| -- | -----------: | --------------------: | -------------------: | --------------------- |
| 2  | To be filled |          To be filled |         To be filled | Too general           |
| 3  | To be filled |          To be filled |         To be filled | To be discussed       |
| 4  | To be filled |          To be filled |         To be filled | To be discussed       |
| 5  | To be filled |          To be filled |         To be filled | To be discussed       |
| 6  | To be filled |          To be filled |         To be filled | To be discussed       |
| 7  | To be filled |          To be filled |         To be filled | To be discussed       |
| 8  | To be filled |          To be filled |         To be filled | To be discussed       |
| 9  | To be filled |          To be filled |         To be filled | To be discussed       |
| 10 | To be filled |          To be filled |         To be filled | Possibly too specific |

The final selected K value will be discussed in the one-page conclusion report.

---

## Conclusion Report

The final report is written in English and includes:

1. Dataset and preprocessing description
2. K-means implementation summary
3. Comparison of different K values
4. Selected K value and explanation
5. Final conclusion about the clustering result

The report is saved in:

```text
report/conclusion_report.pdf
```

---

## Project Limitation

K-means clustering requires the number of clusters K to be specified before running the algorithm. Different K values may produce different clustering results. In addition, the algorithm may be affected by the initial centroid selection. Therefore, several K values are tested before selecting the final result.

---

## Academic Integrity Statement

The K-means clustering algorithm in this project is written manually by the team. No built-in K-means clustering library or function is used. External libraries for clustering are not used in the implementation.

---

## Team Members

* Member 1: Name
* Member 2: Name
* Member 3: Name
* Member 4: Name

---

## Course Information

* Course: Final Project
* Topic: K-means Clustering for Gene Expression Data
* Programming Language: Python
* Running Environment: Python IDLE / Python Compiler
