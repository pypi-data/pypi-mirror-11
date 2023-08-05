"""
Created on Apr 19, 2015

@author: brian
"""
from traits.api import HasStrictTraits, provides, Str
from cytoflow.views.i_view import IView
from cytoflow.utility.util import num_hist_bins
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.transforms as mtrans

@provides(IView)
class HexbinView(HasStrictTraits):
    """
    classdocs
    """
    
    id = 'edu.mit.synbio.cytoflow.view.hexbin'
    friend_id = "Hex Bin"
    
    name = Str
    xchannel = Str
    ychannel = Str
    xfacet = Str
    yfacet = Str
    huefacet = Str
    subset = Str
    
    def is_valid(self, experiment):
        """Validate this view against an experiment."""
        if not experiment:
            return False
        
        if not self.xchannel or self.xchannel not in experiment.channels:
            return False
        
        if not self.ychannel or self.ychannel not in experiment.channels:
            return False
        
        if self.xfacet and self.xfacet not in experiment.metadata:
            return False
        
        if self.yfacet and self.yfacet not in experiment.metadata:
            return False
        
        if self.huefacet and self.huefacet not in experiment.metadata:
            return False
        
        if self.subset:
            try:
                experiment.query(self.subset)
            except:
                return False
        
        return True
    
    def plot(self, experiment, **kwargs):
        """Plot a faceted histogram view of a channel"""
        
        #kwargs.setdefault('histtype', 'stepfilled')
        #kwargs.setdefault('alpha', 0.5)
        kwargs.setdefault('edgecolor', 'none')
        #kwargs.setdefault('mincnt', 1)
        #kwargs.setdefault('bins', 'log')
        kwargs.setdefault('antialiased', True)
        
        if not self.subset:
            x = experiment.data
        else:
            x = experiment.query(self.subset)
            
        xmin, xmax = (np.amin(x[self.xchannel]), np.amax(x[self.xchannel]))
        ymin, ymax = (np.amin(x[self.ychannel]), np.amax(x[self.ychannel]))
        # to avoid issues with singular data, expand the min/max pairs
        xmin, xmax = mtrans.nonsingular(xmin, xmax, expander=0.1)
        ymin, ymax = mtrans.nonsingular(ymin, ymax, expander=0.1)
        
        extent = (xmin, xmax, ymin, ymax)
        kwargs.setdefault('extent', extent)
        
        xbins = num_hist_bins(experiment[self.xchannel])
        ybins = num_hist_bins(experiment[self.ychannel])
        bins = np.mean([xbins, ybins])
        
        kwargs.setdefault('bins', bins) # Do not move above.  don't ask.

        g = sns.FacetGrid(x, 
                          col = (self.xfacet if self.xfacet else None),
                          row = (self.yfacet if self.yfacet else None),
                          hue = (self.huefacet if self.huefacet else None))
        
        g.map(plt.hexbin, self.xchannel, self.ychannel, **kwargs)
        
if __name__ == '__main__':
    import cytoflow as flow
    import FlowCytometryTools as fc
    
    import matplotlib as mpl
    mpl.rcParams['savefig.dpi'] = 2 * mpl.rcParams['savefig.dpi']
    
    tube1 = fc.FCMeasurement(ID='Test 1', 
                             datafile='../../cytoflow/tests/data/Plate01/RFP_Well_A3.fcs')

    tube2 = fc.FCMeasurement(ID='Test 2', 
                           datafile='../../cytoflow/tests/data/Plate01/CFP_Well_A4.fcs')
    
    ex = flow.Experiment()
    ex.add_conditions({"Dox" : "float"})
    
    ex.add_tube(tube1, {"Dox" : 10.0})
    ex.add_tube(tube2, {"Dox" : 1.0})
    
    hlog = flow.HlogTransformOp()
    hlog.name = "Hlog transformation"
    hlog.channels = ['V2-A', 'Y2-A', 'B1-A', 'FSC-A', 'SSC-A']
    ex2 = hlog.apply(ex)
    
    hexbin = flow.HexbinView()
    hexbin.name = "Hex"
    hexbin.xchannel = "FSC-A"
    hexbin.ychannel = "SSC-A"
    hexbin.huefacet = 'Dox'
    
    plt.ioff()
    hexbin.plot(ex2)
    plt.show()