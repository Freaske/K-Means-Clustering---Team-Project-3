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
    candidate_genes = []
    known_genes = []

    current_section = ""

    f = open(filename, "r", encoding="utf-8")

    for line in f:
        line = line.strip()

        if line == "":
            continue

        lower_line = line.lower()

        if line.startswith("#"):
            if "candidate" in lower_line:
                current_section = "candidate"
            elif "known" in lower_line or "longevity" in lower_line:
                current_section = "known"
            continue

        if current_section == "candidate":
            gene = clean_gene_name(line)
            if gene != "" and gene not in candidate_genes:
                candidate_genes.append(gene)

        elif current_section == "known":
            gene = clean_gene_name(line)
            if gene != "" and gene not in known_genes:
                known_genes.append(gene)

    f.close()

    return candidate_genes, known_genes

def clean_gene_name(gene_name):
    gene_name = gene_name.strip()
    gene_name = gene_name.replace("\ufeff", "")
    gene_name = gene_name.replace(",", "")
    gene_name = gene_name.replace(";", "")
    return gene_name

# ============================================================
# PART 2: READ DATASET
# Owner: Thành
# ============================================================

def read_dataset(filename):
    dataset = []

    f = open(filename, "r", encoding="utf-8-sig")

    for line in f:
        line = line.strip()

        if line == "":
            continue

        row = line.split(";")
        dataset.append(row)

    f.close()

    header = dataset[0]
    dataset = dataset[1:]

    return dataset, header

def find_gene_columns(header):
    gene_id_col = -1
    gene_name_col = -1
    expression_cols = []

    for i in range(len(header)):
        col = header[i].strip().lower()

        if col == "public id":
            gene_id_col = i

        elif col == "gene":
            gene_name_col = i

        elif col == "sch9/wt" or col == "ras2/wt" or col == "tor1/wt":
            expression_cols.append(i)

    return gene_id_col, gene_name_col, expression_cols

def convert_to_float(value):
    value = value.strip()

    if value == "":
        return None

    value = value.replace(",", ".")

    try:
        number = float(value)
        return number
    except:
        return None
# ============================================================
# PART 3: FILTER ONLY INTERESTED GENES
# Owner: Thành
# ============================================================


def filter_interested_genes(dataset, gene_id_col, gene_name_col, expression_cols,
                            candidate_genes, known_genes):

    filtered_data = []
    skipped_genes = []

    found_genes = []

    for row in dataset:
        gene_id = row[gene_id_col].strip()
        gene_name = row[gene_name_col].strip()

        gene_type = ""

        if gene_id in candidate_genes or gene_name in candidate_genes:
            gene_type = "candidate"
        elif gene_id in known_genes or gene_name in known_genes:
            gene_type = "known"

        if gene_type != "":
            expression_values = []

            for col in expression_cols:
                value = convert_to_float(row[col])
                expression_values.append(value)

            filtered_data.append({
                "gene_id": gene_id,
                "gene_name": gene_name,
                "expression_values": expression_values,
                "gene_type": gene_type
            })

            if gene_id in candidate_genes or gene_id in known_genes:
                found_genes.append(gene_id)

            if gene_name in candidate_genes or gene_name in known_genes:
                found_genes.append(gene_name)

    all_interested_genes = candidate_genes + known_genes

    for gene in all_interested_genes:
        if gene not in found_genes:
            skipped_genes.append(gene)

    return filtered_data, skipped_genes
                                
 
def save_skipped_genes(skipped_genes, filename):
    f   = open(filename, "w", encoding="utf-8")
 
    for gene in skipped_genes:
        f.write(gene + "\n")
    f.close()

# ============================================================
# PART 4: NORMALIZATION
# Owner: Phong
# ============================================================

def find_min_values(data, expression_cols):
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
    dist_sq = 0
    for col in expression_cols:
        dist_sq += (float(point1[col]) - float(point2[col])) ** 2
    return dist_sq ** 0.5


def choose_initial_centroids(data, k):
    return data[:k]


def assign_to_clusters(data, centroids, expression_cols):
    clusters = [[] for _ in range(len(centroids))]

    for gene in data:
        distances = [euclidean_distance(gene, c, expression_cols) for c in centroids]
        min_idx = distances.index(min(distances))
        clusters[min_idx].append(gene)

    return clusters


def calculate_new_centroids(clusters, old_centroids, expression_cols):
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
