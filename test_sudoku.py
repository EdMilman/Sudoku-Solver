import pytest
from sudoku import convertToSets, convertToInts, getRowLocations, solve, getColumnLocations, getBoxLocations, eliminate, \
    isSolved


@pytest.fixture(scope="module")
def problem():
    return [[0, 0, 4, 0, 0, 0, 0, 6, 7],
                [3, 0, 0, 4, 7, 0, 0, 0, 5],
                [1, 5, 0, 8, 2, 0, 0, 0, 3],

                [0, 0, 6, 0, 0, 0, 0, 3, 1],
                [8, 0, 2, 1, 0, 5, 6, 0, 4],
                [4, 1, 0, 0, 0, 0, 9, 0, 0],

                [7, 0, 0, 0, 8, 0, 0, 4, 6],
                [6, 0, 0, 0, 1, 2, 0, 0, 0],
                [9, 3, 0, 0, 0, 0, 7, 1, 0]]


@pytest.fixture(scope="module")
def sets(problem):
    return convertToSets(problem)


@pytest.fixture(scope="module")
def ints(sets):
    return convertToInts(sets)


@pytest.fixture(scope="module")
def row_locs():
    lst = []
    for row in range(9):
        temp = []
        for col in range(9):
            temp.append((row, col))
        lst.append(temp)
    return lst


@pytest.fixture(scope="module")
def col_locs():
    lst = []
    for col in range(9):
        temp = []
        for row in range(9):
            temp.append((row, col))
        lst.append(temp)
    return lst


# test convertToSets all items in lst are sets
def test_convert_to_set(sets):
    for lst in sets:
        for j in range(len(lst)):
            assert type(lst[j]) == set


# compares length of sets for a converted list of ints
def test_len_sets(problem, sets):
    for row in range(len(problem)):
        for col in range(len(problem[row])):
            if problem[row][col] == 0:
                assert len(sets[row][col]) == 9
            else:
                assert len(sets[row][col]) == 1


# tests random sample to ensure sets are 'full' sets
def test_random_set_sample_0(sets):
    sample = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    assert sets[0][0] == sample
    assert sets[5][3] == sample
    assert sets[8][8] == sample


# tests random sample that sets contain just 1 int
@pytest.mark.parametrize("col, row, result", [(0, 2, 4), (6, 7, 4), (4, 0, 8)])
def test_random_set_sample_not_0(sets, col, row, result):
    assert sets[col][row] == {result}


# test convertToInts contains only list types
def test_to_int(ints):
    for lst in ints:
        assert type(lst) == list


# test convertToInts only has lists of length 9
def test_len_to_int(ints):
    for lst in ints:
        assert len(lst) == 9


# tests random sample of convertToInts
@pytest.mark.parametrize("col, row, result", [(0, 0, 0), (7, 8, 0), (4, 8, 4), (5, 0, 4)])
def test_random_sample(ints, col, row, result):
    assert ints[col][row] == result


# tests problem == convertToInts(convertToSets(problem)))
def test_ints_vs_input(ints, problem):
    assert ints == problem


# test get row locations
@pytest.mark.parametrize("row, row2", [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)])
def test_row_locations(row_locs, row, row2):
    assert getRowLocations(row) == row_locs[row2]


# test get column locations
@pytest.mark.parametrize("col, col2", [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)])
def test_col_locations(col_locs, col, col2):
    assert getColumnLocations(col) == col_locs[col2]


# test get box locations
@pytest.mark.parametrize("row, col", [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
def test_getboxlocs_topleft(row, col):
    topleftbox = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    assert getBoxLocations((row, col)) == topleftbox


# test get box locations
@pytest.mark.parametrize("row, col", [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])
def test_getboxlocs_topmid(row, col):
    topmidbox = [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)]
    assert getBoxLocations((row, col)) == topmidbox


# test get box locations
@pytest.mark.parametrize("row, col", [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)])
def test_getboxlocs_topright(row, col):
    toprightbox = [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)]
    assert getBoxLocations((row, col)) == toprightbox


# test get box locations
@pytest.mark.parametrize("row, col", [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)])
def test_getboxlocs_midleft(row, col):
    midleftbox = [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)]
    assert getBoxLocations((row, col)) == midleftbox


# test get box locations
@pytest.mark.parametrize("row, col", [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)])
def test_getboxlocs_mid(row, col):
    midbox = [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]
    assert getBoxLocations((row, col)) == midbox


# test get box locations
@pytest.mark.parametrize("row, col", [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)])
def test_getboxlocs_midright(row, col):
    midright = [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)]
    assert getBoxLocations((row, col)) == midright


# test get box locations
@pytest.mark.parametrize("row, col", [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)])
def test_getboxlocs_botleft(row, col):
    botleft = [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)]
    assert getBoxLocations((row, col)) == botleft


# test get box locations
@pytest.mark.parametrize("row, col", [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)])
def test_getboxlocs_botmid(row, col):
    botmid = [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)]
    assert getBoxLocations((row, col)) == botmid


# test get box locations
@pytest.mark.parametrize("row, col", [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)])
def test_getboxlocs_botright(row, col):
    botright = [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]
    assert getBoxLocations((row, col)) == botright


# test eliminate
def test_elim():
    # elim 1 from 0, 1 and 0, 2
    assert eliminate([[{1, 2}, {1, 2}, {1, 2}, {1}], [{1}, {1}]], (0, 3), [(0, 1), (0, 2)]) == 2
    # elim 1 from every tuple except 0, 3 == location
    assert eliminate([[{1, 2}, {1, 2}, {1, 2}, {1}], [{1, 2}, {1, 2}]], (0, 3),
                     [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1)]) == 5
    # elim 3 - not in sets
    assert eliminate([[{1, 2}, {1}, {1}, {3}], [{1}, {1}]], (0, 3), [(0, 1), (0, 2)]) == 0
    # elim 2, tuple with 2 not in listOfLocations
    assert eliminate([[{1, 2}, {1}, {1}, {3}], [{1}, {2}]], (1, 1), [(0, 1), (0, 2)]) == 0
    # elim 2 with tuple in listOfLocations
    assert eliminate([[{1, 2}, {1}, {1}, {3}], [{1}, {2}]], (1, 1), [(0, 0), (0, 2)]) == 1


"""taken from testsudoku and converted to pytest"""


def test_Eliminate():
    sets = [[{1, 2}, {3}, {4}], [{1}, {3, 5, 7}, {2}], [{2, 3}, {2}, {1, 2, 3}]]
    location = (1, 2)  # contains {2}
    count = eliminate(sets, location, [(0, 0), (1, 0), (2, 2)])
    assert count == 2
    assert [[{1}, {3}, {4}], [{1}, {3, 5, 7}, {2}], [{2, 3}, {2}, {1, 3}]] == sets


def test_issolved_false(sets):
    assert isSolved(sets) is False
    assert isSolved([[{9}, {1, 2, 3, 4, 5, 6, 7, 8, 9}, {1, 2, 3, 4, 5, 6, 7, 8, 9},
                      {1, 2, 3, 4, 5, 6, 7, 8, 9}, {1, 2, 3, 4, 5, 6, 7, 8, 9}, {8},
                      {1, 2, 3, 4, 5, 6, 7, 8, 9}]]) is False


def test_issolved_true():
    assert isSolved([[{1}, {1}, {1}]]) is True
    assert isSolved([[{2}, {1}, {3}], [{2}, {2}, {1}]]) is True


def test_solve(sets):
    assert solve(sets) is True
    assert solve(convertToSets([[0, 0, 0, 7, 0, 0, 6, 8, 9],
                                [3, 0, 8, 0, 0, 0, 2, 0, 0],
                                [0, 0, 0, 8, 1, 0, 0, 4, 0],

                                [6, 0, 0, 0, 0, 0, 8, 0, 4],
                                [8, 0, 0, 3, 4, 9, 0, 0, 5],
                                [7, 0, 5, 0, 0, 0, 0, 0, 3],

                                [0, 8, 0, 0, 7, 6, 0, 0, 0],
                                [0, 0, 7, 0, 0, 0, 1, 0, 8],
                                [9, 5, 1, 0, 0, 8, 0, 0, 0]])) is True
    assert solve(convertToSets([[9, 0, 0, 0, 0, 8, 0, 0, 0],
                                [0, 0, 0, 0, 3, 2, 0, 0, 0],
                                [6, 8, 0, 9, 0, 1, 0, 7, 0],

                                [8, 0, 9, 5, 2, 0, 0, 3, 0],
                                [2, 0, 0, 0, 0, 0, 0, 0, 5],
                                [0, 4, 0, 0, 9, 3, 7, 0, 8],

                                [0, 2, 0, 3, 0, 9, 0, 6, 4],
                                [0, 0, 0, 2, 8, 0, 0, 0, 0],
                                [0, 0, 0, 6, 0, 0, 0, 0, 3]])) is False
