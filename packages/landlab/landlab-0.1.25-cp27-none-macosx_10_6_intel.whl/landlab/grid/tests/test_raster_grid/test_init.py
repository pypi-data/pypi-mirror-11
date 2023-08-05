import numpy as np
from numpy.testing import assert_array_equal
from nose.tools import (assert_equal, assert_raises, raises, assert_true,
                        assert_false)
from nose.tools import with_setup

try:
    from nose.tools import assert_is, assert_is_instance
except ImportError:
    from landlab.testing.tools import assert_is, assert_is_instance

from landlab import RasterModelGrid
from landlab import BAD_INDEX_VALUE as X


def setup_grid():
    """
    These tests use a grid that 4x5 nodes::

     15------16------17------18------19
      |       |       |       |       |
      |       |       |       |       |
      |       |       |       |       |
     10------11------12------13------14
      |       |       |       |       |
      |       |       |       |       |   
      |       |       |       |       |
      5-------6-------7-------8-------9
      |       |       |       |       |
      |       |       |       |       |
      |       |       |       |       |
      0-------1-------2-------3-------4
    """
    from landlab import RasterModelGrid
    globals().update({
        'rmg': RasterModelGrid(4, 5, 1.)
    })


def test_init_with_kwds_classic():
    grid = RasterModelGrid(num_rows=4, num_cols=5, dx=1.)

    assert_equal(grid.number_of_node_rows, 4)
    assert_equal(grid.number_of_node_columns, 5)
    assert_equal(grid.node_spacing, 1)

    grid = RasterModelGrid(3, 7, 2)

    assert_equal(grid.number_of_node_rows, 3)
    assert_equal(grid.number_of_node_columns, 7)
    assert_equal(grid.node_spacing, 2.)


def test_init_new_style():
    grid = RasterModelGrid((4, 5), spacing=2)

    assert_equal(grid.number_of_node_rows, 4)
    assert_equal(grid.number_of_node_columns, 5)
    assert_equal(grid.node_spacing, 2.)

    grid = RasterModelGrid((4, 5))

    assert_equal(grid.number_of_node_rows, 4)
    assert_equal(grid.number_of_node_columns, 5)
    assert_equal(grid.node_spacing, 1.)


def test_spacing_is_float():
    grid = RasterModelGrid((4, 5))
    assert_equal(grid.node_spacing, 1.)
    assert_is_instance(grid.node_spacing, float)

    grid = RasterModelGrid((4, 5), spacing=2)
    assert_equal(grid.node_spacing, 2.)
    assert_is_instance(grid.node_spacing, float)


@with_setup(setup_grid)
def test_grid_dimensions():
    assert_equal(rmg.get_grid_ydimension(), rmg.number_of_node_rows - 1)
    assert_equal(rmg.get_grid_xdimension(), rmg.number_of_node_columns - 1)


def test_grid_dimensions_non_unit_spacing():
    rmg = RasterModelGrid((4, 5), spacing=2.)
    assert_equal(rmg.get_grid_ydimension(), 6.)
    assert_equal(rmg.get_grid_xdimension(), 8.)


@with_setup(setup_grid)
def test_nodes_around_point():
    surrounding_ids = rmg.get_nodes_around_point(2.1, 1.1)
    assert_array_equal(surrounding_ids, np.array([7, 12, 13, 8]))

    surrounding_ids = rmg.get_nodes_around_point(2.1, .9)
    assert_array_equal(surrounding_ids, np.array([2, 7, 8, 3]))


@with_setup(setup_grid)
def test_neighbor_list_with_scalar_arg():
    assert_array_equal(rmg.get_neighbor_list(6), np.array([7, 11, 5, 1]))
    assert_array_equal(rmg.get_neighbor_list(-1), np.array([X, X, X, X]))
    assert_array_equal(rmg.get_neighbor_list(-2), np.array([X, X, X, 13]))


@with_setup(setup_grid)
def test_neighbor_list_with_array_arg():
    assert_array_equal(rmg.get_neighbor_list([6, -1]),
                       np.array([[7, 11, 5, 1], [X, X, X, X]]))


@with_setup(setup_grid)
def test_neighbor_list_with_no_args():
    expected = np.array([
        [ X,  X,  X,  X], [ X,  6,  X,  X], [ X,  7,  X,  X], [ X,  8,  X,  X],
            [ X,  X,  X,  X],
        [ 6,  X,  X,  X], [ 7, 11,  5,  1], [ 8, 12,  6,  2], [ 9, 13,  7,  3],
            [ X,  X,  8,  X],
        [11,  X,  X,  X], [12, 16, 10,  6], [13, 17, 11,  7], [14, 18, 12,  8],
            [ X,  X, 13,  X],
        [ X,  X,  X,  X], [ X,  X,  X, 11], [ X,  X,  X, 12], [ X,  X,  X, 13],
            [ X,  X,  X,  X]])

    assert_array_equal(rmg.get_neighbor_list(), expected)


@with_setup(setup_grid)
def test_node_x():
    assert_array_equal(rmg.node_x, np.array([0., 1., 2., 3., 4.,
                                             0., 1., 2., 3., 4.,
                                             0., 1., 2., 3., 4.,
                                             0., 1., 2., 3., 4.]))

@with_setup(setup_grid)
def test_node_y():
    assert_array_equal(rmg.node_y, np.array([0., 0., 0., 0., 0.,
                                             1., 1., 1., 1., 1.,
                                             2., 2., 2., 2., 2.,
                                             3., 3., 3., 3., 3.]))


@with_setup(setup_grid)
@raises(ValueError)
def test_node_x_is_immutable():
    rmg.node_x[0] = 0


@with_setup(setup_grid)
@raises(ValueError)
def test_node_y_is_immutable():
    rmg.node_y[0] = 0


@with_setup(setup_grid)
def test_node_axis_coordinates():
    assert_is(rmg.node_axis_coordinates(axis=0).base, rmg.node_y.base)
    assert_is(rmg.node_axis_coordinates(axis=1).base, rmg.node_x.base)
    assert_is(rmg.node_axis_coordinates(axis=-1).base, rmg.node_x.base)
    assert_is(rmg.node_axis_coordinates(axis=-2).base, rmg.node_y.base)


@with_setup(setup_grid)
def test_diagonal_list():
    assert_array_equal(rmg.get_diagonal_list(6), np.array([12, 10, 0, 2]))
    assert_array_equal(rmg.get_diagonal_list(-1), np.array([X, X, 13, X]))
    assert_array_equal(rmg.get_diagonal_list([6, -1]),
                       np.array([[12, 10, 0, 2], [X, X, 13, X]]))
    assert_array_equal(
        rmg.get_diagonal_list(),
        np.array([[6, X, X, X], [7, 5, X, X], [8, 6, X, X],
                    [9, 7, X, X], [X, 8, X, X],
                  [11, X, X, 1], [12, 10,  0,  2], [13, 11,  1,  3],
                    [14, 12,  2,  4], [X, 13, 3, X],
                  [16, X, X, 6], [17, 15,  5,  7], [18, 16,  6,  8],
                    [19, 17,  7,  9], [X, 18, 8, X],
                  [X, X, X, 11], [X, X, 10, 12], [X, X, 11, 13],
                    [X, X, 12, 14], [X, X, 13, X]]))


@with_setup(setup_grid)
def test_diagonal_list_boundary():
    assert_array_equal(rmg.get_diagonal_list(0), np.array([6, X, X, X]))


@with_setup(setup_grid)
def test_is_interior():
    for cell_id in [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 16, 17, 18, 19]:
        assert_false(rmg.is_interior(cell_id))
    for cell_id in [6, 7, 8, 11, 12, 13]:
        assert_true(rmg.is_interior(cell_id))


@with_setup(setup_grid)
def test_get_interior_cells():
    assert_array_equal(rmg.get_core_cell_node_ids(),
                       np.array([6, 7, 8, 11, 12, 13]))


@with_setup(setup_grid)
def test_active_links():
    assert_equal(rmg.number_of_active_links, 17)
    assert_array_equal(rmg.active_links,
                       np.array([1, 2, 3, 6, 7, 8, 11, 12, 13,
                                 19, 20, 21, 22, 23, 24, 25, 26]))


@with_setup(setup_grid)
def test_active_link_fromnode():
    assert_array_equal(rmg.activelink_fromnode,
                       np.array([1, 2, 3, 6, 7, 8, 11, 12, 13,
                                 5, 6, 7, 8, 10, 11, 12, 13]))


@with_setup(setup_grid)
def test_active_link_tonode():
    assert_array_equal(rmg.activelink_tonode,
                       np.array([6, 7, 8, 11, 12, 13, 16, 17, 18,
                                 6, 7, 8, 9, 11, 12, 13, 14]))


@with_setup(setup_grid)
def test_active_link_num_inlink():
    assert_array_equal(rmg.node_numactiveinlink,
                       np.array([0, 0, 0, 0, 0,
                                 0, 2, 2, 2, 1,
                                 0, 2, 2, 2, 1,
                                 0, 1, 1, 1, 0]))


@with_setup(setup_grid)
def test_active_link_num_outlink():
    assert_array_equal(rmg.node_numactiveoutlink, np.array([0, 1, 1, 1, 0,
                                                            1, 2, 2, 2, 0,
                                                            1, 2, 2, 2, 0,
                                                            0, 0, 0, 0, 0]))


@with_setup(setup_grid)
def test_active_inlink_matrix():
    assert_array_equal(rmg.node_active_inlink_matrix,
                       np.array([[-1, -1, -1, -1, -1,
                                  -1,  0,  1,  2, -1,
                                  -1,  3,  4,  5, -1,
                                  -1,  6, 7,  8, -1],
                                 [-1, -1, -1, -1, -1,
                                  -1,  9, 10, 11, 12,
                                  -1, 13, 14, 15, 16,
                                  -1, -1, -1, -1, -1]]))


@with_setup(setup_grid)
def test_active_outlink_matrix():
    assert_array_equal(
        rmg.node_active_outlink_matrix,
        np.array([[-1,  0,  1,  2, -1,
                   -1,  3,  4,  5, -1,
                   -1,  6,  7,  8, -1,
                   -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1,
                    9, 10, 11, 12, -1,
                   13, 14, 15, 16, -1,
                   -1, -1, -1, -1, -1]]))


@with_setup(setup_grid)
def test_active_node_links_scalar_interior():
    assert_array_equal(rmg.active_node_links([6]), np.array([[0, 9, 3, 10]]).T)


@with_setup(setup_grid)
def test_active_node_links_scalar_boundary():
    assert_array_equal(rmg.active_node_links([1]),
                       np.array([[-1, -1, 0, -1]]).T)


@with_setup(setup_grid)
def test_active_node_with_array_arg():
    assert_array_equal(rmg.active_node_links([6, 7]),
                       np.array([[0,  9, 3, 10],
                                 [1, 10, 4, 11]]).T)


@with_setup(setup_grid)
def test_active_node_links_with_no_args():
    assert_array_equal(
        rmg.active_node_links(),
        np.array([[-1, -1, -1, -1, -1, -1,  0,  1,  2, -1,
                   -1,  3,  4,  5, -1, -1,  6,  7,  8, -1],
                  [-1, -1, -1, -1, -1, -1,  9, 10, 11, 12,
                   -1, 13, 14, 15, 16, -1, -1, -1, -1, -1],
                  [-1,  0,  1,  2, -1, -1,  3,  4,  5, -1,
                   -1,  6,  7,  8, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1,  9, 10, 11, 12, -1,
                   13, 14, 15, 16, -1, -1, -1, -1, -1, -1]]))


@with_setup(setup_grid)
def test_link_fromnode():
    assert_array_equal(
        rmg.link_fromnode,
        np.array([0, 1, 2, 3, 4, 5, 6, 7,  8,  9, 10, 11, 12, 13, 14,
                  0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18]))


@with_setup(setup_grid)
def test_link_tonode():
    assert_array_equal(
        rmg.link_tonode,
        np.array([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                  1, 2, 3, 4, 6,  7,  8,  9, 11, 12, 13, 14, 16, 17, 18, 19]))


@with_setup(setup_grid)
def test_link_num_inlink():
    assert_array_equal(rmg.node_numinlink,
                       np.array([0, 1, 1, 1, 1,
                                 1, 2, 2, 2, 2,
                                 1, 2, 2, 2, 2,
                                 1, 2, 2, 2, 2]))


@with_setup(setup_grid)
def test_link_num_outlink():
    assert_array_equal(rmg.node_numoutlink, np.array([2, 2, 2, 2, 1,
                                                      2, 2, 2, 2, 1,
                                                      2, 2, 2, 2, 1,
                                                      1, 1, 1, 1, 0]))


@with_setup(setup_grid)
def test_node_inlink_matrix():
    assert_array_equal(rmg.node_inlink_matrix,
                       np.array([[-1, -1, -1, -1, -1,
                                   0,  1,  2,  3,  4,
                                   5,  6,  7,  8,  9,
                                  10, 11, 12, 13, 14],
                                 [-1, 15, 16, 17, 18,
                                  -1, 19, 20, 21, 22,
                                  -1, 23, 24, 25, 26,
                                  -1, 27, 28, 29, 30]]))


@with_setup(setup_grid)
def test_node_outlink_matrix():
    assert_array_equal(rmg.node_outlink_matrix,
                       np.array([[ 0,  1,  2,  3,  4,
                                  5,  6,  7,  8,  9,
                                  10, 11, 12, 13, 14,
                                  -1, -1, -1, -1, -1],
                                 [15, 16, 17, 18, -1,
                                  19, 20, 21, 22, -1,
                                  23, 24, 25, 26, -1,
                                  27, 28, 29, 30, -1]]))


@with_setup(setup_grid)
def test_node_links_with_scalar_interior():
    assert_array_equal(rmg.node_links([6]),
                       np.array([[1, 19, 6, 20]]).T)


@with_setup(setup_grid)
def test_node_links_with_scalar_boundary():
    assert_array_equal(rmg.node_links([1]), np.array([[-1, 15, 1, 16]]).T)


@with_setup(setup_grid)
def test_node_links_with_array_arg():
    assert_array_equal(rmg.node_links([6, 7]),
                       np.array([[1, 19, 6, 20], [2, 20, 7, 21]]).T)


@with_setup(setup_grid)
def test_node_links_with_no_args():
    assert_array_equal(
        rmg.node_links(),
        np.array([[-1, -1, -1, -1, -1,  0,  1,  2,  3,  4,
                    5,  6,  7,  8,  9, 10, 11, 12, 13, 14],
                  [-1, 15, 16, 17, 18, -1, 19, 20, 21, 22,
                   -1, 23, 24, 25, 26, -1, 27, 28, 29, 30],
                  [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
                   10, 11, 12, 13, 14, -1, -1, -1, -1, -1],
                  [15, 16, 17, 18, -1, 19, 20, 21, 22, -1,
                   23, 24, 25, 26, -1, 27, 28, 29, 30, -1]]))


@with_setup(setup_grid)
def test_link_face():
    assert_array_equal(rmg.link_face, np.array([X, 0, 1, 2, X,
                                                X, 3, 4, 5, X,
                                                X, 6, 7, 8, X,
                                                X, X, X, X,
                                                9, 10, 11, 12,
                                                13, 14, 15, 16,
                                                X, X, X, X]))


@with_setup(setup_grid)
def test_grid_coords_to_node_id_with_scalar():
    assert_equal(rmg.grid_coords_to_node_id(3, 4), 19)


@with_setup(setup_grid)
def test_grid_coords_to_node_id_with_array():
    assert_array_equal(rmg.grid_coords_to_node_id((3, 2), (4, 1)),
                       np.array([19, 11]))


@with_setup(setup_grid)
def test_grid_coords_to_node_id_outside_of_grid():
    assert_raises(ValueError, rmg.grid_coords_to_node_id, 5, 0)


@with_setup(setup_grid)
def test_create_diagonal_list():
    rmg.create_diagonal_list()

    assert_array_equal(
        rmg.get_diagonal_list(),
        np.array([[6, X, X, X], [7, 5, X, X], [8, 6, X, X],
                    [9, 7, X, X], [X, 8, X, X],
                  [11, X, X, 1], [12, 10,  0,  2], [13, 11,  1,  3],
                    [14, 12,  2,  4], [X, 13, 3, X],
                  [16, X, X, 6], [17, 15,  5,  7], [18, 16,  6,  8],
                    [19, 17,  7,  9], [X, 18, 8, X],
                  [X, X, X, 11], [X, X, 10, 12], [X, X, 11, 13],
                    [X, X, 12, 14], [X, X, 13, X]]))
