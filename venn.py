from matplotlib import pyplot as plt
from matplotlib_venn import venn2

# Replace with your actual counts
A = 53380960  # unique to VCF1
B = 53146614  # unique to VCF2
AB = 391709232  # shared variants

venn2(subsets=(A, B, AB), set_labels=('Raimonds 2023-08-09', 'Edgars 2025-02-10'))
plt.title("RG0004 haplotypecaller.g.vcf.gz")
plt.savefig("RG0004.png", dpi=300, bbox_inches='tight')
plt.show()
