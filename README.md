# GROUP 3 - K-means Clustering Final Project

## Project Overview

This project implements the **K-means clustering algorithm from scratch in Python** and applies it to gene expression data.

The program reads the `Longotor1delta` dataset, uses only the genes listed in `interested_genes.txt`, normalizes the selected gene expression data, and runs a manually implemented K-means clustering algorithm with different K values. The final result is analyzed in a one-page conclusion report.

---

## Important Note

This project **does not use any built-in K-means clustering library or function**.

The K-means algorithm is written manually, including:

* Euclidean distance calculation
* Centroid initialization
* Cluster assignment
* Centroid update
* K-means iteration loop
* SSE/WCSS calculation

The project does **not** use:

* `sklearn.cluster.KMeans`
* `scipy`
* Any built-in clustering function

Only basic Python modules are used, such as:

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
3. Filter the dataset and keep only the selected genes.
4. Normalize the gene expression values.
5. Run K-means clustering implemented from scratch.
6. Test different K values.
7. Compare clustering results using SSE/WCSS and cluster size distribution.
8. Write a one-page conclusion report in English.

---

## Folder Structure

```text
GROUP3-Kmeans-FinalProject/
│
├── README.md
├── main.py
│
├── data/
│   ├── Longotor1delta.csv
│   └── interested_genes.txt
│
├── output/
│   ├── filtered_data.csv
│   ├── normalized_data.csv
│   ├── clusters_output.txt
│   └── k_results_summary.csv
│
└── report/
    └── conclusion_report.pdf
```

The original Excel file `Longotor1delta.xls` can be saved as `Longotor1delta.csv` before running the program. This makes the project easier to run in Python IDLE.

---

## Input Files

The required input files are placed in the `data/` folder:

* `Longotor1delta.csv`
  Gene expression dataset.

* `interested_genes.txt`
  List of genes used for filtering the dataset.

---

## Output Files

The program generates output files in the `output/` folder:

* `filtered_data.csv`
  Contains only the genes listed in `interested_genes.txt`.

* `normalized_data.csv`
  Contains the normalized gene expression values.

* `clusters_output.txt`
  Contains the clustering results for different K values.

* `k_results_summary.csv`
  Contains the SSE/WCSS and cluster size summary for each K value.

---

## Methodology

### 1. Data Filtering

The program reads the interested gene list and keeps only the matching genes from the gene expression dataset.

### 2. Data Normalization

The selected gene expression values are normalized using z-score normalization:

```text
normalized_value = (value - mean) / standard_deviation
```

Normalization is used so that all features have a comparable scale before clustering.

### 3. K-means Clustering

The K-means algorithm is implemented manually using the following steps:

1. Choose K initial centroids.
2. Assign each gene to the nearest centroid using Euclidean distance.
3. Update each centroid by calculating the mean of the genes in that cluster.
4. Repeat the assignment and update steps until the clusters do not change or the maximum number of iterations is reached.

### 4. Testing Different K Values

The program tests the following K values:

```text
K = 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
```

For each K value, the program records:

* SSE/WCSS
* Smallest cluster size
* Largest cluster size
* Empty cluster status
* General comment

---

## How to Run

This project is designed to run in **Python IDLE**.

### Steps

1. Open `main.py` in Python IDLE.
2. Make sure the `data/` folder contains:

   * `Longotor1delta.csv`
   * `interested_genes.txt`
3. Press `F5` to run the program.
4. Check the generated files in the `output/` folder.

---

## Main Functions in `main.py`

The project uses the following main functions:

```python
read_interested_genes(filename)
read_gene_data(filename, interested_genes)
normalize_by_column(data)
euclidean_distance(point1, point2)
calculate_sse(clusters, centroids)
kmeans(data, gene_names, k, max_iterations=100)
```

All of these functions are written manually in `main.py`.

---

## Experiment Summary

| K  |     SSE/WCSS | Smallest Cluster Size | Largest Cluster Size | Empty Cluster? | Comment               |
| -- | -----------: | --------------------: | -------------------: | -------------- | --------------------- |
| 2  | To be filled |          To be filled |         To be filled | No             | Too general           |
| 3  | To be filled |          To be filled |         To be filled | No             | To be discussed       |
| 4  | To be filled |          To be filled |         To be filled | No             | To be discussed       |
| 5  | To be filled |          To be filled |         To be filled | No             | To be discussed       |
| 6  | To be filled |          To be filled |         To be filled | No             | To be discussed       |
| 7  | To be filled |          To be filled |         To be filled | No             | To be discussed       |
| 8  | To be filled |          To be filled |         To be filled | No             | To be discussed       |
| 9  | To be filled |          To be filled |         To be filled | No             | To be discussed       |
| 10 | To be filled |          To be filled |         To be filled | No             | To be discussed       |
| 11 | To be filled |          To be filled |         To be filled | No             | To be discussed       |
| 12 | To be filled |          To be filled |         To be filled | No             | To be discussed       |
| 13 | To be filled |          To be filled |         To be filled | No             | Possibly too specific |

The final selected K value will be explained in the conclusion report.

---

## Conclusion Report

The one-page conclusion report includes:

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

K-means requires the number of clusters K to be selected before running the algorithm. The result may also be affected by the initial centroid selection. Therefore, multiple K values are tested before selecting the final result.

---

## Academic Integrity Statement

The K-means clustering algorithm in this project is implemented manually by the team. No built-in K-means clustering library or function is used.

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
