#! /usr/env/python
"""
oriented_hex_lca.py: simple hexagonal Landlab cellular automaton

This file defines the OrientedHexLCA class, which is a sub-class of 
LandlabCellularAutomaton that implements a simple, non-oriented, hex-grid
CA. Like its parent class, OrientedHexLCA implements a continuous-time, stochastic,
pair-based CA. The hex grid has 3 principal directions, rather than 2 for a
raster. Hex grids are often used in CA models because of their symmetry.

Created GT Sep 2014
"""
import warnings

from numpy import zeros
from .landlab_ca import LandlabCellularAutomaton, Transition
import landlab


class OrientedHexLCA(LandlabCellularAutomaton):
    """
    Class OrientedHexLCA implements an oriented hex-grid CellLab-CTS model.
    """
    
    def __init__(self, model_grid, node_state_dict, transition_list,
                 initial_node_states, prop_data=None, prop_reset_value=None):
        """
        OrientedHexLCA constructor: sets number of orientations to 3 and calls
        base-class constructor.
        
        Parameters
        ----------
        model_grid : Landlab ModelGrid object
            Reference to the model's grid
        node_state_dict : dict
            Keys are node-state codes, values are the names associated with
            these codes
        transition_list : list of Transition objects
            List of all possible transitions in the model
        initial_node_states : array of ints (x number of nodes in grid)
            Starting values for node-state grid
        prop_data : array (x number of nodes in grid) (optional)
            Array of properties associated with each node/cell
        prop_reset_value : (scalar; same type as entries in prop_data) (optional)
            Default or initial value for a node/cell property (e.g., 0.0)
        """
        warnings.warn('use of OrientedHexLCA is deprecated. '
                      'Use OrientedHexCTS instead.')
        
        # Make sure caller has sent the right grid type        
        assert (type(model_grid) is landlab.grid.hex.HexModelGrid), \
               'model_grid must be a Landlab HexModelGrid'
               
        # Somehow test to make sure the grid links have been re-oriented to
        # point up/right (-45 to +135 degrees clockwise relative to vertical).
        # Such orientation is ensured when the argument reorient_grid=True is
        # passed to the hex grid constructor.
               
        # Define the number of distinct cell-pair orientations: here 3,
        # representing
        self.number_of_orientations = 3
        
        # Call the LandlabCellularAutomaton.__init__() method to do the rest of
        # the initialization
        super(OrientedHexLCA, self).__init__(model_grid, node_state_dict, 
            transition_list, initial_node_states, prop_data, prop_reset_value)
            

    def setup_array_of_orientation_codes(self):
        """
        Creates and configures an array that contain the orientation code for 
        each active link (and corresponding cell pair).
        
        Parameters
        ----------
        (none)
        
        Returns
        -------
        (none)
        
        Creates
        -------
        self.active_link_orientation : 1D numpy array
        
        Notes
        -----
        This overrides the method of the same name in landlab_ca.py. If the hex
        grid is oriented such that one of the 3 axes is vertical (a 'vertical'
        grid), then the three orientations are:
            0 = vertical (0 degrees clockwise from vertical)
            1 = right and up (60 degrees clockwise from vertical)
            2 = right and down (120 degrees clockwise from vertical)
        If the grid is oriented with one principal axis horizontal ('horizontal'
        grid), then the orientations are:
            0 = up and left (30 degrees counter-clockwise from vertical)
            1 = up and right (30 degrees clockwise from vertical)
            2 = horizontal (90 degrees clockwise from vertical)
        """
        self.active_link_orientation = zeros(self.grid.number_of_active_links, dtype=int)
        for j in range(self.grid.number_of_active_links):
            i = self.grid.active_links[j]
            dy = self.grid.node_y[self.grid.link_tonode[i]]-self.grid.node_y[self.grid.link_fromnode[i]]
            dx = self.grid.node_x[self.grid.link_tonode[i]]-self.grid.node_x[self.grid.link_fromnode[i]]
            if dx <= 0.:
                self.active_link_orientation[j] = 0
            elif dy<=0.:
                self.active_link_orientation[j] = 2
            elif dx>0. and dy>0.:
                self.active_link_orientation[j] = 1
            else:
                assert (False), 'Non-handled link orientation case'


if __name__=='__main__':
    import doctest
    doctest.testmod()
