import numpy as np

import ahplib2 as ahp
from general import traverse_tree

c0 = ahp.Criteria('choose phone')
c01 = ahp.Criteria('ram')
c02 = ahp.Criteria('screen')
c0.add_children(c01)
c0.add_children(c02)

# manually create comparison matrix - must code a mechanism to
# get this data from the user
co_comparison_matrix = np.array([[1, 5],
                                 [1/5, 1]])

# manually enter alternative info, not yet sure how to model the data
# also need to code an input mechanism
alts = {'phone1': (8,'big'), 'phone2':(12,'small')}

# manually create alt comparison matricies
alt_compare_ram = np.array([[1, 2/3],
                            [3/2, 1]])
alt_compare_screen = np.array([[1, 3],
                               [1/3, 1]])

c0.get_comparison_matrix(co_comparison_matrix)
c0.col_sum_vector = ahp.create_col_sum_vector(c0.comparison_matrix)
c0.normal_comparison_matrix = ahp.normalize_criteria_matrix(c0.comparison_matrix, c0.col_sum_vector)
c0.priority_vector = ahp.calc_priority_vector(c0.normal_comparison_matrix)
c0.get_alt_comparison_matrix(alt_compare_ram)
c0.get_alt_comparison_matrix(alt_compare_screen)

for i, alt in enumerate(c0.alt_comparison_matrices):
    alt_col_sum = ahp.create_col_sum_vector(alt)
    norm_alt = ahp.normalize_criteria_matrix(alt, alt_col_sum)
    print('normed alt for index: ' + str(i))
    print(norm_alt)
    pv = ahp.calc_priority_vector(norm_alt)
    c0.alt_pvs.append(pv)

for i, pv in enumerate(c0.alt_pvs):
    print('pv for alt idx: ' + str(i))
    print(pv)



for i, child in enumerate(c0.children):
    print('alt for ' + child.name)
    print(c0.alt_comparison_matrices[i])
# print(alt_c01_compares)
# print(alt_c02_compares)
# print('c0 compare matrix')
# print(c0.comparison_matrix)
# print('c0 sum vector')
# print(c0.col_sum_vector)
# print('c0.normal matrix')
# print(c0.normal_comparison_matrix)
# print('c0 pv')
# print(c0.priority_vector)
#
#
# print('name: {}, weight: {}'.format(c0.name, c0.weight))
# print(c0.parent)
# print(c0.children)
# print('name: {}, weight: {}'.format(c01.name, c01.weight))
# print(c01.parent)
# print(c01.children)
# print('name: {}, weight: {}'.format(c02.name, c02.weight))
# print(c02.parent)
# print(c02.children)
