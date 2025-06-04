import os
import subprocess
import csv
import gc

# ============ 參數 =============
tau1_list = [0.08]
tau2_list = [0.02, 1.0]

output_csv = "test.csv"
data_name = "Samusik_01_cleaned"
index_name = "Event"

results = [["tau1", "tau2", "ARI", "NMI", "CH", "DB", "Leaf_Num"]]

# ============ 核心函數 ============

def parse_score_file(score_file_path):
    score_dict = {}
    with open(score_file_path, "r") as f:
        for line in f:
            if ":" in line:
                key, value = line.split(":", 1)
                score_dict[key.strip()] = value.strip()

    # Robust key matching
    def find_key(key_words):
        for key in score_dict:
            if all(kw.lower() in key.lower() for kw in key_words):
                return key
        raise KeyError(f"[❌ Error] Could not find key containing: {key_words}")

    try:
        ari = float(score_dict[find_key(["ari"])])
        nmi = float(score_dict[find_key(["nmi"])])
        ch = float(score_dict[find_key(["ch"])])
        db = float(score_dict[find_key(["db"])])
        leaf_raw = score_dict[find_key(["leaf", "number"])]
        # 提取數字
        leaf = int(''.join(filter(str.isdigit, leaf_raw)))
    except Exception as e:
        print(f"[❌ Error] Failed to parse score file: {e}")
        raise

    return ari, nmi, ch, db, leaf

# ============ Grid Search ============

for tau1 in tau1_list:
    for tau2 in tau2_list:
        print(f"\n--- Running tau1={tau1}, tau2={tau2} ---")
        try:
            # run main
            cmd = f"python3 execute.py --index={index_name} --data={data_name} --tau1={tau1} --tau2={tau2}"
            subprocess.run(cmd, shell=True, check=True)

            # load clustering score
            score_file = f"./applications/{data_name}-{tau1}-{tau2}/data/clustering_score.txt"
            if not os.path.exists(score_file):
                raise FileNotFoundError(f"Score file not found: {score_file}")

            ari, nmi, ch, db, leaf = parse_score_file(score_file)
            results.append([tau1, tau2, ari, nmi, ch, db, leaf])

        except Exception as e:
            print(f"[❌ Error] tau1={tau1}, tau2={tau2} failed: {e}")
            results.append([tau1, tau2, "PARSE_ERROR", "PARSE_ERROR", "PARSE_ERROR", "PARSE_ERROR", "PARSE_ERROR"])

        gc.collect()

# ============ 輸出 CSV ============

with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(results)

print(f"\n✅ All results written to {output_csv}")
