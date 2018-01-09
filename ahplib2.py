import sys

import numpy as np

# defined these functions as stand alone b/c, for now, I need to make the same calcs on
# matrices outside the Criteria objects - perhaps make them generic but still methods of
# the Criteria object?
def create_col_sum_vector(M):
    """
    create the column sum vector of M, each value in the vector is the sum of the corresponding column of M

    Args:
        M (np.array): numpy array/matrix

    Returns(np.array): vector of column sum values

    """
    return M.sum(axis=0)

def normalize_criteria_matrix(comparison_matrix, col_sum_vector):
    """
    create the normalized criteria matrix given the original criteria matrix and the column sum vector, do so by:

    for each column in C:
        replace each element e in the column w/the result of e/corresponding_column_sum_value

    i.e. normalize each column value by dividing by that column's sum

    we could just calculate col_sum vector, but it's used elsewhere, so let's not repeat that calculation

    Args:
        C (np.array):  square matrix with
        col_sum (np.array): vector of size = square matrix containing the sums of the columns of the criteria matrix

    Returns (np.array): normalized criteria matrix

    """

    shape = comparison_matrix.shape

    if len(shape) == 2 and shape[0] == shape[1]:  # matrix is 2-d and square
        num_col = shape[0]
        T = np.empty(shape)  # create empty array to accept new values, see comment below for additional context
        for col in range(num_col):
            # can't put the slice on both sides of the assignment operator b/c they are views, not copies
            # when I tried I got zero for all results/elements
            T[:, col] = comparison_matrix[:, col] / col_sum_vector[col]

    return T

def calc_priority_vector(normal_comparison_matrix):
        """
        Create the priority vector, i.e. the potential criteria weights from a normalized criteria matrix

        M should be a normalized matrix (if using the approximate pv technique)
        Args:
            C_norm(np.array): A normalized criteria matrix

        Returns(np.array): priority vector

        """
        return np.average(normal_comparison_matrix, axis=1)

class Criteria:

    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []
        self.comparison_matrix = None
        self.col_sum_vector = None
        self.normal_comparison_matrix = None
        self.priority_vector = None
        self.weight = 0  # local weight, 0 indicates no weight rather than a value of zero
        self.alt_comparison_matrices = []  # list of comparison matricies, one per criteria, in criteria order
        self.alt_pvs = []  # list of alt priority vectors, one per criteria, in criteria order

    def add_child(self, criteria):
        criteria.parent = self
        self.children.append(criteria)

    def get_comparison_matrix(self, pairwise_comparisons=None):

        # THIS IS NOT COMPLETE - the param pariwise_comparisons is just the
        # upper right of the matrix (above the diagonal).  This function will
        # generate the lower left, below the diagonal from those values (1/value)
        # this is a placeholder for now and assumes the parameter is a numpy array
        # that is a complete comparison matrix

        self.comparison_matrix = pairwise_comparisons

    def get_alt_comparison_matrix(self, pairwise_comparisons=None):

        # THIS IS NOT COMPLETE - the param pariwise_comparisons is just the
        # upper right of the matrix (above the diagonal).  This function will
        # generate the lower left, below the diagonal from those values (1/value)
        # this is a placeholder for now and assumes the parameter is a numpy array
        # that is a complete comparison matrix

        # right now just adding matricies manually

        self.alt_comparison_matrices.append(pairwise_comparisons)

    def create_col_sum_vector(self):
        """
        create the column sum vector of M, each value in the vector is the sum of the corresponding column of M

        Args:
            M (np.array): numpy array/matrix

        Returns(np.array): vector of column sum values

        """
        self.col_sum_vector =  self.comparison_matrix.sum(axis=0)

    def normalize_criteria_matrix(self):
        """
        create the normalized criteria matrix given the original criteria matrix and the column sum vector, do so by:

        for each column in C:
            replace each element e in the column w/the result of e/corresponding_column_sum_value

        i.e. normalize each column value by dividing by that column's sum

        we could just calculate col_sum vector, but it's used elsewhere, so let's not repeat that calculation

        Args:
            C (np.array):  square matrix with
            col_sum (np.array): vector of size = square matrix containing the sums of the columns of the criteria matrix

        Returns (np.array): normalized criteria matrix

        """

        shape = self.comparison_matrix.shape

        if len(shape) == 2 and shape[0] == shape[1]:  # matrix is 2-d and square
            num_col = shape[0]
            T = np.empty(shape)  # create empty array to accept new values, see comment below for additional context
            for col in range(num_col):
                # can't put the slice on both sides of the assignment operator b/c they are views, not copies
                # when I tried I got zero for all results/elements
                T[:, col] = self.comparison_matrix[:, col] / self.col_sum_vector[col]

        self.normal_comparison_matrix = T

    def calc_priority_vector(self):
        """
        Create the priority vector, i.e. the potential criteria weights from a normalized criteria matrix

        Args:
            C_norm(np.array): A normalized criteria matrix

        Returns(np.array): priority vector

        """
        self.priority_vector = np.average(self.normal_comparison_matrix, axis=1)

    def calc_lambda_max(self, col_sum_vector, priority_vector):
        """
        calculate the value of lambda max (aka principal eigen value)

        Value is the "sum product" of the vector of column sums of the criteria matrix and the priority vector,
        which is the vector of row averages of the normalized criteria matrix (aka W?)

        todo: verify vector lengths match

        Args:
            col_sum_vector (np array): numpy array of the sums of the columns of the criteria matrix
            priority_vector (np array): numpy array of the averages of the rows of the normalized criteria matrix

        Returns (float): "sum product of the two supplied np arrays (aka vectors)
        """

        t = col_sum_vector * priority_vector

        return t.sum()

    def calc_consistency_idx(self, lmax, n):
        """
        return the consistency index given by (lmax - n)/(n - 1), where n is the number of criteria in he square
        criteria matrix

        Args:
            lmax(float): lambda_max
            n(int): number of criteria

        Returns(float): consistency index

        """

        return (lmax - n) / (n - 1)

    def calc_consistency_ratio(self, ci, ri):
        """
        return the consistency ratio: cr = ci/ri

        Args:
            ci(float): consistency index
            ri(float): random index

        Returns(float): consistency ratio

        """

        return ci / ri


# not yet sure how to handle the alternatives (aka alts), maybe it should be a class, or something else?
# manually creating it for now, format is {'alt_name': float_score}
alts = {'alt01': 0.0, 'alt02':0.0}


c0 = Criteria('decision')
c01 = Criteria('crit01')
c02 = Criteria('crit02')
c0.add_child(c01)
c0.add_child(c02)

c0_matrix = np.array([[1.0000, 3.0000],
                      [0.3333, 1.0000]])

# comparisons of the alts for each criteria
alt_c01_compares = np.array([[1, 7],
                            [.142857, 1]])
alt_c02_compares = np.array([[1,2],
                             [.5,1]])

c0.get_comparison_matrix(c0_matrix)
c0.col_sum_vector = create_col_sum_vector(c0.comparison_matrix)
c0.normal_comparison_matrix = normalize_criteria_matrix(c0.comparison_matrix, c0.col_sum_vector)
c0.priority_vector = calc_priority_vector(c0.normal_comparison_matrix)
c0.get_alt_comparison_matrix(alt_c01_compares)
c0.get_alt_comparison_matrix(alt_c02_compares)

for i, alt in enumerate(c0.alt_comparison_matrices):
    alt_col_sum = create_col_sum_vector(alt)
    norm_alt = normalize_criteria_matrix(alt, alt_col_sum)
    print('normed alt for index: ' + str(i))
    print(norm_alt)
    pv = calc_priority_vector(norm_alt)
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
