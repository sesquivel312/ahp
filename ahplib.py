#todo: some way to caclulate final weights - likely involves grah traversal

import sys

import numpy as np

# copied random index table from AHP tutorial doc, the None at position 0 eliminates the off-by-one
# problem -- matrix size starts at 1, list index starts at 0)
ri_lookup = [None, 0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 11.49]

class Comparison:
    """
    This is a collection of criteria to be compared and associated methods used
    for AHP

    It calculates priority vectors using the approximating method of averaging the rows of the normalized
    comparison matrix, rather than using the complete, linear algebra based method

    todo: switch priority vector and lambda calcs from approximate average method to using accurate linear algebra
    """


    comparison_matrix = None
    local_weight = 0  # 0 indicates no weight, not a value of 0
    global_weight = 0  # 0 means same as for local_weight

    def create_col_sum_vector(self, M):
        """
        create the column sum vector of M, each value in the vector is the sum of the corresponding column of M

        Args:
            M (np.array): numpy array/matrix

        Returns(np.array): vector of column sum values

        """
        return M.sum(axis=0)

    def normalize_criteria_matrix(self, C, col_sum):
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

        shape = C.shape

        if len(shape) == 2 and shape[0] == shape[1]:  # matrix is 2-d and square
            num_col = shape[0]
            Cp = np.empty(shape)  # create empty array to accept new values, see comment below for additional context
            for col in range(num_col):
                # can't put the slice on both sides of the assignment operator b/c they are views, not copies
                # when I tried I got zero for all results/elements
                Cp[:, col] = C[:, col] / col_sum[col]

        return Cp

    def calc_priority_vector(self, C_norm):
        """
        Create the priority vector, i.e. the potential criteria weights from a normalized criteria matrix

        Args:
            C_norm(np.array): A normalized criteria matrix

        Returns(np.array): priority vector

        """
        return np.average(C_norm, axis=1)

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

    def set_comparison_matrix(self, C):
        """
        set the comparison matrix for this Comparison

        Args:
            C(numpy.array): the RU portion of the comparison matrix

        Returns(numpy.array): the full comparison matrix

        """

        # verify C is square and 2d
        if not (len(C.shape) == 2 and C.shape[0] == C.shape[1]):
            sys.exit('comparison matrix is not square and 2d')

        return C  # just return the matrix as is for now, later will need to fill in the lower left submatrix

    def add_child(self, name):
        new_child = Comparison(name, parent=self)
        self.children.append(new_child)

    def __init__(self, name, parent=None, children=[]):
        """
        initialize the object with provided data and data derived from it

        set parent = None if this Comparison has no parent

        Args:
            criteria_names(tuple): tuple of criteria names
            comparison_matrix(numpy.array): the upper right portion of the comparison matrix (above diagonal)
            parent(Comparison): Parent Comparison object
        """

        self.name = name
        self.parent = parent
        self.children = children

        # todo: check for mismatch between # names and size of matrix
        # self.size = len(criteria_names)
        # self.comparison_matrix = self.set_comparison_matrix(comparison_matrix)
        # self.colsum = self.create_col_sum_vector(self.comparison_matrix)
        # self.normal_comparison_matrix = self.normalize_criteria_matrix(self.comparison_matrix, self.colsum)
        # self.priority_vector = self.calc_priority_vector(self.normal_comparison_matrix)
        # self.lmax = self.calc_lambda_max(self.colsum, self.priority_vector)
        # self.ri = self.ri_lookup[self.size]
        # self.ci = self.calc_consistency_idx(self.lmax, self.size)
        # self.cr = self.calc_consistency_ratio(self.ci, self.ri)


goal = Comparison('decide')

print(goal.name)
print(goal.parent)
print(goal.children)

goal.add_child('crit01')

print(goal.name)
print(goal.parent)
print(goal.children)
print()