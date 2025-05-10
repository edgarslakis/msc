#!/bin/bash
#PBS -q batch
#PBS -N vcf_isec_compare
#PBS -m abe
#PBS -l walltime=01:00:00
#PBS -l nodes=1:ppn=2,pmem=4gb
#PBS -l feature='epyc'

module load bcftools/1.17

# Go to working directory
cd $PBS_O_WORKDIR

# Define directories and file names
SAREK_DIR="/mnt/beegfs2/home/edgars02/250505_el/sarek_output/variant_calling"
OUT_DIR="$PBS_O_WORKDIR/vcf_comparison_output"
mkdir -p $OUT_DIR

# Specify sample ID (adjust to your actual sample name)
SAMPLE="sample1"

# Input VCF files — adjust the filenames if needed
VCF_HC="${SAREK_DIR}/haplotypecaller/${SAMPLE}.hc.filtered.vcf.gz"
VCF_DV="${SAREK_DIR}/deepvariant/${SAMPLE}.dv.filtered.vcf.gz"

# Check files exist
if [[ ! -f $VCF_HC || ! -f $VCF_DV ]]; then
    echo "Error: One or both VCF files not found."
    exit 1
fi

# Index VCFs if not already indexed
if [[ ! -f "${VCF_HC}.tbi" ]]; then
    bcftools index $VCF_HC
fi

if [[ ! -f "${VCF_DV}.tbi" ]]; then
    bcftools index $VCF_DV
fi

# Perform intersection using bcftools isec
bcftools isec -p ${OUT_DIR}/${SAMPLE}_hc_vs_dv \
    -n=2 -w1 $VCF_HC $VCF_DV

# Description:
# -p: output directory
# -n=2: only variants common to both files
# -w1: match both position and genotype

# Optional: generate summary
echo "Variant comparison done for $SAMPLE. Results stored in $OUT_DIR."
