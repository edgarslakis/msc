#!/bin/bash
#PBS -q batch
#PBS -N isec_compare
#PBS -m abe
#PBS -l walltime=24:00:00
#PBS -l nodes=1:ppn=4,pmem=7gb
#PBS -l feature='epyc'

module load bio/bcftools/1.10.2

echo "[INFO] PBS job started at $(date)"
cd $PBS_O_WORKDIR || { echo "[ERROR] Failed to change to PBS_O_WORKDIR"; exit 1; }

# Reference genome (make sure .fai exists)
REF="/home_beegfs/groups/bmc/references/igenomes/Homo_sapiens/GATK/GRCh38/Sequence/WholeGenomeFasta/Homo_sapiens_assembly38.fasta"

# Input VCFs (gVCFs in this case)
VCF1="~/250210_RR_repr/Raimonds/RG0004-2023-08-09.haplotypecaller.g.vcf.gz"
VCF2="~/250210_RR_repr/sarek_output/variant_calling/haplotypecaller/E150013583_C/E150013583_C.haplotypecaller.g.vcf.gz"

# Expand paths (since ~ doesn't expand inside variables)
VCF1=$(realpath ~/250210_RR_repr/Raimonds/RG0004-2023-08-09.haplotypecaller.g.vcf.gz)
VCF2=$(realpath ~/250210_RR_repr/sarek_output/variant_calling/haplotypecaller/E150013583_C/E150013583_C.haplotypecaller.g.vcf.gz)

# Output normalized VCFs
OUT1="RG0004.norm.vcf.gz"
OUT2="E150013583_C.norm.vcf.gz"

echo "[INFO] Normalizing VCF1: $VCF1"
bcftools norm -f $REF -m -both -Oz -o $OUT1 $VCF1 || { echo "[ERROR] Normalization failed for VCF1"; exit 1; }
bcftools index $OUT1

echo "[INFO] Normalizing VCF2: $VCF2"
bcftools norm -f $REF -m -both -Oz -o $OUT2 $VCF2 || { echo "[ERROR] Normalization failed for VCF2"; exit 1; }
bcftools index $OUT2

echo "[INFO] Running bcftools isec to compare normalized VCFs"
bcftools isec -p isec_output $OUT1 $OUT2 || { echo "[ERROR] bcftools isec failed"; exit 1; }

echo "[INFO] Comparison complete. Results saved in ./isec_output/"
echo "[INFO] PBS job finished at $(date)"
