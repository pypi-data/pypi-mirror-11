"""
"""

from .. import react
from . import Widget


class Canvas2D(ui.Widget):
    
    """ A w
    """
    class JS:
        
        def _create_node(self):
            self.node = document.createElement('canvas')
            self._context = ctx = self.node.getContext('2d')
            
            # create tick units
            self._tick_units = []
            for e in range(-10, 10):
                for i in [10, 20, 25, 50]:
                    self._tick_units.append(i*10**e)
        
        @react.connect('actual_size')
        def _update_canvas_size(self, size):
            if size[0] and size[1]:
                self.node.width = size[0]
                self.node.height = size[1]