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
            if "candidate" in lower_line or "cadidate" in lower_line:
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

def find_min_values(data):
    if not data: return []

    num_fields = len(data[0]["expression_values"])
    min_vals = [float('inf')] * num_fields
    
    for row in data:
        values = row["expression_values"]
        for idx in range(num_fields):
            if values[idx] is not None and values[idx] < min_vals[idx]:
                min_vals[idx] = values[idx]
    return min_vals

def find_max_values(data):
    
    if not data: return []
    num_fields = len(data[0]["expression_values"])
    max_vals = [float('-inf')] * num_fields
    
    for row in data:
        values = row["expression_values"]
        for idx in range(num_fields):
            if values[idx] is not None and values[idx] > max_vals[idx]:
                max_vals[idx] = values[idx]
    return max_vals

def min_max_normalize(data, expression_cols):
    mins = find_min_values(data)
    maxs = find_max_values(data)
    if not data: return data
    
    num_fields = len(data[0]["expression_values"])
    for row in data:
        values = row["expression_values"]
        for idx in range(num_fields):
            val = values[idx]
            if val is not None:
                denominator = maxs[idx] - mins[idx]
                values[idx] = (val - mins[idx]) / denominator if denominator != 0 else 0.0
    return data

# ============================================================
# PART 5: K-MEANS HELPER FUNCTIONS
# Owner: Phong
# ============================================================

def euclidean_distance(point1, point2):
    dist_sq = 0
    vals1 = point1["expression_values"]
    vals2 = point2["expression_values"]
    

    for idx in range(len(vals1)):
        v1 = vals1[idx] if vals1[idx] is not None else 0.0
        v2 = vals2[idx] if vals2[idx] is not None else 0.0
        dist_sq += (v1 - v2) ** 2
    return dist_sq ** 0.5


def choose_initial_centroids(data, k):
    return data[:k]


def assign_to_clusters(data, centroids):
    clusters = [[] for _ in range(len(centroids))]
    for gene in data:
        
        distances = [euclidean_distance(gene, c) for c in centroids]
        min_idx = distances.index(min(distances))
        clusters[min_idx].append(gene)
    return clusters


def calculate_new_centroids(clusters, old_centroids):
    new_centroids = []
    if not old_centroids: return new_centroids
    num_fields = len(old_centroids[0]["expression_values"])

    for i in range(len(clusters)):
        cluster = clusters[i]
        if not cluster:
            new_centroids.append(old_centroids[i])
            continue
            
        means = [0.0] * num_fields
        for gene in cluster:
            vals = gene["expression_values"]
            for idx in range(num_fields):
                means[idx] += vals[idx] if vals[idx] is not None else 0.0
        
        for idx in range(num_fields):
            means[idx] /= len(cluster)
            
        new_centroids.append({"expression_values": means})
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

def clusters_are_same(old_clusters, new_clusters):
    if len(old_clusters) != len(new_clusters):
        return False

    for i in range(len(old_clusters)):
        if len(old_clusters[i]) != len(new_clusters[i]):
            return False

        for j in range(len(old_clusters[i])):
            old_gene = old_clusters[i][j]
            new_gene = new_clusters[i][j]

            if old_gene["gene_id"] != new_gene["gene_id"]:
                return False

            if old_gene["gene_name"] != new_gene["gene_name"]:
                return False

    return True

def kmeans(data, k, max_iterations):
    if data == []:
        return [], [], 0

    if k <= 0:
        return [], [], 0

    if k > len(data):
        k = len(data)

    centroids = choose_initial_centroids(data, k)

    if max_iterations <= 0:
        final_clusters = assign_to_clusters(data, centroids)
        return final_clusters, centroids, 0

    old_clusters = []
    final_clusters = []
    iterations_used = 0

    for iteration in range(max_iterations):
        new_clusters = assign_to_clusters(data, centroids)
        new_centroids = calculate_new_centroids(new_clusters, centroids)

        iterations_used += 1
        final_clusters = new_clusters

        if old_clusters != [] and clusters_are_same(old_clusters, new_clusters):
            centroids = new_centroids
            break

        old_clusters = new_clusters
        centroids = new_centroids
    return final_clusters, centroids, iterations_used


def calculate_sse(clusters, centroids):
    sse = 0.0
    for i in range(len(clusters)):
        cluster = clusters[i]
        centroid = centroids[i]
        for gene in cluster:
            distance = euclidean_distance(gene, centroid)
            sse = sse + distance ** 2
    return sse


# ============================================================
# PART 7: ANALYZE CLUSTER RESULTS
# Owner: Nam
# ============================================================
def count_gene_types(cluster):
    candidate_count = 0
    known_count = 0
    for gene in cluster:
        if gene["gene_type"] == "candidate":
            candidate_count = candidate_count + 1
        elif gene["gene_type"] == "known":
            known_count = known_count + 1
    return candidate_count, known_count


def calculate_known_percentage(cluster):
    total_genes = len(cluster)
    if total_genes == 0:
        return 0.0
    candidate_count, known_count = count_gene_types(cluster)
    known_percentage = (known_count / total_genes) * 100
    return known_percentage


def get_candidate_genes(cluster):
    candidate_gene_list = []
    for gene in cluster:
        if gene["gene_type"] == "candidate":
            gene_name = gene["gene_name"]
            if gene_name == "":
                gene_name = gene["gene_id"]
            candidate_gene_list.append(gene_name)
    return candidate_gene_list


def summarize_clusters(clusters):
    cluster_summary = []

    for i in range(len(clusters)):
        cluster = clusters[i]

        candidate_count, known_count = count_gene_types(cluster)
        known_percentage = calculate_known_percentage(cluster)
        candidate_gene_names = get_candidate_genes(cluster)

        cluster_info = {
            "cluster_id": i + 1,
            "cluster_size": len(cluster),
            "known_count": known_count,
            "candidate_count": candidate_count,
            "known_percentage": known_percentage,
            "candidate_genes": candidate_gene_names
        }

        cluster_summary.append(cluster_info)
    return cluster_summary


def find_best_cluster(cluster_summary):
    if cluster_summary == []:
        return None

    best_cluster_info = cluster_summary[0]

    for i in range(1, len(cluster_summary)):
        current_cluster_info = cluster_summary[i]

        if current_cluster_info["known_percentage"] > best_cluster_info["known_percentage"]:
            best_cluster_info = current_cluster_info

        elif current_cluster_info["known_percentage"] == best_cluster_info["known_percentage"]:
            if current_cluster_info["known_count"] > best_cluster_info["known_count"]:
                best_cluster_info = current_cluster_info

    return best_cluster_info


# ============================================================
# PART 8: SAVE RESULTS
# Owner: Sơn
# ============================================================

def save_results(all_results, filename):
    """
    Save experiment results to results.csv.
    """
    f = open(filename, "w", encoding="utf-8")

    f.write("K;Iterations;SSE;Cluster Sizes;Best Cluster ID;Best Cluster Known Percentage;Potential Candidate Genes\n")
    
    for res in all_results:
   
        sizes_str = "-".join(str(size) for size in res["cluster_sizes"])
        

        genes_str = ",".join(res["potential_genes"])
        if genes_str == "":
            genes_str = "None"
            

        line = "{};{};{:.4f};{};{};{:.2f}%;{}\n".format(
            res["k"],
            res["iterations"],
            res["sse"],
            sizes_str,
            res["best_cluster_id"],
            res["known_percentage"],
            genes_str
        )
        f.write(line)
        
    f.close()


def print_result_summary(k, clusters, sse, iterations_used, cluster_summary):
    """
    Print result summary on screen.
    """
    print("-" * 60)
    print("EXPERIMENT SUMMARY FOR K = {}".format(k))
    print("-" * 60)
    print("Iterations Used : {}".format(iterations_used))
    print("SSE (Error)     : {:.4f}".format(sse))
    
    print("\nCluster Details:")
    for cluster in cluster_summary:
        print("  - Cluster {}: Size = {}, Known = {}, Candidates = {}, Known % = {:.2f}%".format(
            cluster["cluster_id"],
            cluster["cluster_size"],
            cluster["known_count"],
            cluster["candidate_count"],
            cluster["known_percentage"]
        ))
        
    best = find_best_cluster(cluster_summary)
    if best:
        print("\n=> Best Cluster: Cluster {} (Highest Known % = {:.2f}%)".format(
            best["cluster_id"], best["known_percentage"]
        ))
        print("=> Potential Genes inside: {}".format(", ".join(best["candidate_genes"]) if best["candidate_genes"] else "None"))
    print("\n")


# ============================================================
# PART 9: RUN EXPERIMENTS WITH DIFFERENT K VALUES
# Owner: Sơn
# ============================================================

def run_experiments(data, k_values, max_iterations):
    """
    Run K-means with different K values.
    """
    all_results = []
    
    for k in k_values:
        print("Running K-Means for K = {}...".format(k))
        

        clusters, centroids, iterations_used = kmeans(data, k, max_iterations)
        

        sse = calculate_sse(clusters, centroids)
        

        cluster_summary = summarize_clusters(clusters)
        

        best_cluster = find_best_cluster(cluster_summary)
        

        cluster_sizes = [c["cluster_size"] for c in cluster_summary]
        

        res_dict = {
            "k": k,
            "iterations": iterations_used,
            "sse": sse,
            "cluster_sizes": cluster_sizes,
            "best_cluster_id": best_cluster["cluster_id"] if best_cluster else -1,
            "known_percentage": best_cluster["known_percentage"] if best_cluster else 0.0,
            "potential_genes": best_cluster["candidate_genes"] if best_cluster else []
        }
        
        all_results.append(res_dict)
        
        # Hiển thị nhanh kết quả lên màn hình IDLE / Compiler để tiện theo dõi
        print_result_summary(k, clusters, sse, iterations_used, cluster_summary)
        
    return all_results


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
