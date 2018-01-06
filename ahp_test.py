from ahplib import Comparison
import numpy as np

# Goal: choose job
lvl_1_crit_names = ('stakeholders', 'finance', 'strategic', 'other')
L1 = np.array([[1,1/5,1/9,1],
                [5,1,1,5],
                [9,1,1,5],
                [1,1/5,1/5,1],
                ])


C1 = Comparison(lvl_1_crit_names, L1, None)

print(C1.normal_comparison_matrix)
print(C1.ri, C1.ci, C1.cr)
