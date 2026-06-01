# ============================================================
# GROUP 3 - K-MEANS CLUSTERING FINAL PROJECT
# File: main.py
#
# Rules:
# - Do NOT use sklearn, pandas, numpy, scipy, or built-in KMeans
# - Use only basic Python knowledge:
#   file I/O, lists, loops, if/else, functions
# - Run this file in IDLE or Python compiler
# ============================================================


# ============================================================
# GLOBAL FILE NAMES
# ============================================================

DATA_FILE = "Longotor1delta.csv"
GENE_FILE = "interested_genes.txt"
RESULT_FILE = "results.csv"
SKIPPED_FILE = "skipped_genes.txt"


# ============================================================
# PART 1: READ INTERESTED GENES
# Owner: Thành
# ============================================================

def read_interested_genes(filename):
    """
    Read interested_genes.txt.

    Return:
        candidate_genes: list of candidate gene names
        known_genes: list of known longevity gene names
    """
    # TODO:
    # 1. Open interested_genes.txt
    # 2. Read all lines
    # 3. Separate candidate genes and known longevity genes
    # 4. Return two lists


def clean_gene_name(gene_name):
    """
    Clean gene name text.

    Example:
        Remove spaces, newline characters, etc.

    Return:
        cleaned gene name
    """
    # TODO:
    # Remove unnecessary spaces or newline characters


# ============================================================
# PART 2: READ DATASET
# Owner: Thành
# ============================================================

def read_dataset(filename):
    """
    Read Longotor1delta.csv.

    Return:
        dataset: list containing all rows from the dataset
        header: first row of the dataset
    """
    # TODO:
    # 1. Open Longotor1delta.csv
    # 2. Read lines
    # 3. Split each line by comma
    # 4. Store rows in a list
    # 5. Return header and dataset


def find_gene_columns(header):
    """
    Find the important column indexes.

    Return:
        gene_id_col
        gene_name_col
        expression_cols
    """
    # TODO:
    # Find which column contains gene ID
    # Find which column contains gene name
    # Find expression value columns, such as:
    # sch9/wt, ras2/wt, tor1/wt


def convert_to_float(value):
    """
    Convert a string value to float.

    Return:
        float number
    """
    # TODO:
    # Convert value to float
    # If value is missing or invalid, handle it carefully


# ============================================================
# PART 3: FILTER ONLY INTERESTED GENES
# Owner: Thành
# ============================================================

def filter_interested_genes(dataset, gene_id_col, gene_name_col, expression_cols,
                            candidate_genes, known_genes):
    """
    Keep only genes listed in interested_genes.txt.

    Return:
        filtered_data
        skipped_genes
    """
    # TODO:
    # 1. Go through each row in dataset
    # 2. Check whether gene ID or gene name is in candidate_genes or known_genes
    # 3. If matched, keep the gene
    # 4. If not found, skip it
    # 5. Each kept gene should contain:
    #    gene_id, gene_name, expression_values, gene_type
    #
    # gene_type should be:
    # "candidate" or "known"


def save_skipped_genes(skipped_genes, filename):
    """
    Save skipped genes to skipped_genes.txt.

    Return:
        nothing
    """
    # TODO:
    # Write skipped gene names into a text file


# ============================================================
# PART 4: NORMALIZATION
# Owner: Phong
# ============================================================

def find_min_values(data, expression_cols):
    """
    Find minimum value for each expression column.

    Return:
        min_values
    """
    # TODO:
    # For each expression column, find the minimum value

    min_vals = {}
    for col in expression_cols:
        min_val = float('inf')
        for row in data:
            try:
                val = float(row[col])
                if val < min_val:
                    min_val = val
            except (ValueError, KeyError):
                continue
        min_vals[col] = min_val
    return min_vals

def find_max_values(data, expression_cols):
    """
    Find maximum value for each expression column.

    Return:
        max_values
    """
    # TODO:
    # For each expression column, find the maximum value

    max_vals = {}
    for col in expression_cols:
        max_val = float('-inf')
        for row in data:
            try:
                val = float(row[col])
                if val > max_val:
                    max_val = val
            except (ValueError, KeyError):
                continue
        max_vals[col] = max_val
    return max_vals

def min_max_normalize(data, expression_cols):
    """
    Normalize expression values using min-max normalization.

    Formula:
        new_value = (old_value - min_value) / (max_value - min_value)

    Return:
        normalized_data
    """
    # TODO:
    # 1. Find min values
    # 2. Find max values
    # 3. Normalize each expression value
    # 4. Return normalized data

    mins = find_min_values(data, expression_cols)
    maxs = find_max_values(data, expression_cols)
    
    for row in data:
        for col in expression_cols:
            val = float(row[col])
            denominator = maxs[col] - mins[col]
            if denominator != 0:
                row[col] = (val - mins[col]) / denominator
            else:
                row[col] = 0.0
    return data

# ============================================================
# PART 5: K-MEANS HELPER FUNCTIONS
# Owner: Phong
# ============================================================

def euclidean_distance(point1, point2, expression_cols):
    """
    Calculate Euclidean distance between two points.

    Return:
        distance
    """
    # TODO:
    # Use loop to calculate distance manually
    dist_sq = 0
    for col in expression_cols:
        dist_sq += (float(point1[col]) - float(point2[col])) ** 2
    return dist_sq ** 0.5


def choose_initial_centroids(data, k):
    """
    Choose initial centroids for K-means.

    Return:
        centroids
    """
    # TODO:
    # Simple method:
    # Use the first k genes as initial centroids
    return data[:k]


def assign_to_clusters(data, centroids, expression_cols):
    """
    Assign each gene to the nearest centroid.

    Return:
        clusters
    """
    # TODO:
    # 1. For each gene, calculate distance to each centroid
    # 2. Find nearest centroid
    # 3. Put gene into that cluster
    clusters = [[] for _ in range(len(centroids))]

    for gene in data:
        distances = [euclidean_distance(gene, c, expression_cols) for c in centroids]
        min_idx = distances.index(min(distances))
        clusters[min_idx].append(gene)

    return clusters


def calculate_new_centroids(clusters, old_centroids, expression_cols):
    """
    Calculate new centroids by taking the average of each cluster.

    Return:
        new_centroids
    """
    # TODO:
    # 1. For each cluster, calculate mean of expression values
    # 2. If a cluster is empty, keep old centroid

    new_centroids = []

    for i in range(len(clusters)):
        cluster = clusters[i]
        
        # if empty, keep old_centroids[i]
        if not cluster:
            new_centroids.append(old_centroids[i])
            continue
            
        means = {col: 0.0 for col in expression_cols}
        for gene in cluster:
            for col in expression_cols:
                means[col] += float(gene[col])
        
        for col in means:
            means[col] /= len(cluster)
        new_centroids.append(means)

    return new_centroids


def clusters_changed(old_clusters, new_clusters):
    """
    Check whether cluster assignments changed.

    Return:
        True or False
    """
    # TODO:
    # Compare old clusters and new clusters
    # Return True if changed
    # Return False if not changed

    if len(old_clusters) != len(new_clusters):
        return True
    # Compare cluster sizes as a simple check for changes 
    for i in range(len(old_clusters)):
        if len(old_clusters[i]) != len(new_clusters[i]):
            return True
    return False


# ============================================================
# PART 6: K-MEANS MAIN ALGORITHM
# Owner: Nam
# ============================================================

def kmeans(data, k, max_iterations):
    """
    Run K-means clustering.

    Return:
        final_clusters
        final_centroids
        iterations_used
    """
    # TODO:
    # 1. Choose initial centroids
    # 2. Repeat:
    #       assign genes to nearest centroid
    #       calculate new centroids
    #       stop if clusters do not change
    # 3. Return final clusters, centroids, and number of iterations


def calculate_sse(clusters, centroids):
    """
    Calculate Sum of Squared Errors.

    Return:
        sse
    """
    # TODO:
    # For each gene:
    #   calculate distance to its cluster centroid
    #   square the distance
    #   add to total SSE


# ============================================================
# PART 7: ANALYZE CLUSTER RESULTS
# Owner: Nam
# ============================================================

def count_gene_types(cluster):
    """
    Count candidate genes and known longevity genes in one cluster.

    Return:
        candidate_count
        known_count
    """
    # TODO:
    # Count how many genes are candidate
    # Count how many genes are known


def calculate_known_percentage(cluster):
    """
    Calculate percentage of known longevity genes in one cluster.

    Return:
        known_percentage
    """
    # TODO:
    # known_percentage = known_count / total_genes


def get_candidate_genes(cluster):
    """
    Get candidate gene names from one cluster.

    Return:
        candidate_gene_list
    """
    # TODO:
    # Return only candidate gene names in the cluster


def summarize_clusters(clusters):
    """
    Create summary information for all clusters.

    Return:
        cluster_summary
    """
    # TODO:
    # For each cluster, record:
    # cluster ID
    # cluster size
    # known gene count
    # candidate gene count
    # known percentage
    # candidate gene names


def find_best_cluster(cluster_summary):
    """
    Find cluster with highest known longevity gene percentage.

    Return:
        best_cluster_info
    """
    # TODO:
    # Compare known percentages
    # Return the cluster with highest known percentage


# ============================================================
# PART 8: SAVE RESULTS
# Owner: Sơn
# ============================================================

def save_results(all_results, filename):
    """
    Save experiment results to results.csv.

    Return:
        nothing
    """
    # TODO:
    # Save columns:
    # K, iterations, SSE, cluster sizes,
    # best cluster ID, known percentage, potential genes


def print_result_summary(k, clusters, sse, iterations_used, cluster_summary):
    """
    Print result summary on screen.

    Return:
        nothing
    """
    # TODO:
    # Print K
    # Print iterations used
    # Print SSE
    # Print cluster summary


# ============================================================
# PART 9: RUN EXPERIMENTS WITH DIFFERENT K VALUES
# Owner: Sơn
# ============================================================

def run_experiments(data, k_values, max_iterations):
    """
    Run K-means with different K values.

    Return:
        all_results
    """
    # TODO:
    # For each K:
    #   run kmeans
    #   calculate SSE
    #   summarize clusters
    #   store result


# ============================================================
# PART 10: MAIN PROGRAM
# Owner: Nam
# ============================================================

def main():
    """
    Main program flow.
    """
    # TODO:
    # 1. Read interested genes
    # 2. Read dataset
    # 3. Find important columns
    # 4. Filter interested genes
    # 5. Save skipped genes
    # 6. Normalize data
    # 7. Run experiments with K = 2, 3, 4, 5, 6, ... ,13
    # 8. Save results
    # 9. Print final message


# ============================================================
# RUN PROGRAM
# ============================================================
if __name__ == "__main__":
    main()
