#!/usr/bin/env python3

import subprocess
import pandas as pd
import os
from collections import defaultdict

workdir = "$workdir"  # Adjust this if needed to a specific path

# Read the searchResults.txt file
data = pd.read_csv('searchResults.txt', sep='\t')

# Create a dictionary to store files per sample ID
samples_dict = defaultdict(list)
for _, row in data.iterrows():
    sample_id = row['sample_id']
    mate1 = os.path.basename(row['mate1'])
    mate2 = os.path.basename(row['mate2'])
    samples_dict[sample_id].append((mate1, mate2))

# Create a list to store the new merged file information
new_records = []

# Process each sample
for sample_id, file_pairs in samples_dict.items():
    if len(file_pairs) == 1:
        mate1, mate2 = file_pairs[0]
        new_records.append({
            'sample_id': sample_id,
            'fc_id': data[data['sample_id'] == sample_id]['fc_id'].iloc[0],
            'lane': data[data['sample_id'] == sample_id]['lane'].iloc[0],
            'barcode': data[data['sample_id'] == sample_id]['barcode'].iloc[0],
            'type': data[data['sample_id'] == sample_id]['type'].iloc[0],
            'mate1': mate1,
            'mate2': mate2
        })
        continue

    merged_mate1 = f"{sample_id}_merged_1.fq.gz"
    merged_mate2 = f"{sample_id}_merged_2.fq.gz"

    # Full paths
    mate1_files = ' '.join([f"{workdir}/{pair[0]}" for pair in file_pairs])
    mate2_files = ' '.join([f"{workdir}/{pair[1]}" for pair in file_pairs])

    print(f"Merging files for sample {sample_id}...")

    # Merge mate1 files
    cmd1 = f"cat {mate1_files} > {merged_mate1}"
    print(f"Running: {cmd1}")
    subprocess.run(cmd1, shell=True, check=True)

    # Merge mate2 files
    cmd2 = f"cat {mate2_files} > {merged_mate2}"
    print(f"Running: {cmd2}")
    subprocess.run(cmd2, shell=True, check=True)

    print(f"Merged files created: {merged_mate1}, {merged_mate2}")

    new_records.append({
        'sample_id': sample_id,
        'fc_id': data[data['sample_id'] == sample_id]['fc_id'].iloc[0],
        'lane': data[data['sample_id'] == sample_id]['lane'].iloc[0],
        'barcode': '_'.join([str(data[data['sample_id'] == sample_id]['barcode'].iloc[i]) for i in range(len(file_pairs))]),
        'type': data[data['sample_id'] == sample_id]['type'].iloc[0],
        'mate1': merged_mate1,
        'mate2': merged_mate2
    })

# Create merged output file
merged_df = pd.DataFrame(new_records)
final_df = merged_df.groupby('sample_id').first().reset_index()
final_df.to_csv('searchResults_merged.txt', sep='\t', index=False)

print(f"Created searchResults_merged.txt with {len(final_df)} unique sample entries")
