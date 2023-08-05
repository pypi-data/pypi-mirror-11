from __future__ import division

if __name__ == '__main__':
    from traits.etsconfig.api import ETSConfig
    ETSConfig.toolkit = 'qt4'

    import os
    os.environ['TRAITS_DEBUG'] = "1"

from traits.api import HasStrictTraits, Str, provides
import matplotlib.pyplot as plt
from cytoflow.views.i_view import IView
from cytoflow.utility.util import num_hist_bins
import numpy as np
import seaborn as sns

@provides(IView)
class HistogramView(HasStrictTraits):
    """Plots a one-channel histogram
    
    Attributes
    ----------
    name : Str
        The HistogramView name (for serialization, UI etc.)
    
    channel : Str
        the name of the channel we're plotting
    
    xfacet : Str 
        the conditioning variable for multiple plots (horizontal)
    
    yfacet : Str
        the conditioning variable for multiple plots (vertical)
    
    huefacet : Str
        the conditioning variable for multiple plots (color)
        
    subset : Str
        a string passed to pandas.DataFrame.query() to subset the data before 
        we plot it.
        
        .. note: Should this be a param instead?
    """
    
    # traits   
    id = "edu.mit.synbio.cytoflow.view.histogram"
    friendly_id = "Histogram" 
    
    name = Str
    channel = Str
    xfacet = Str
    yfacet = Str
    huefacet = Str
    subset = Str
    
    def plot(self, experiment, **kwargs):
        """Plot a faceted histogram view of a channel"""
        
        kwargs.setdefault('histtype', 'stepfilled')
        kwargs.setdefault('alpha', 0.5)
        kwargs.setdefault('antialiased', True)

        if not self.subset:
            x = experiment.data
        else:
            x = experiment.query(self.subset)
            
        num_bins = num_hist_bins(x[self.channel])
        xmin = np.amin(x[self.channel])
        xmax = np.amax(x[self.channel])
        bin_width = (xmax - xmin) / num_bins
        bins = np.arange(xmin, xmax, bin_width)
        kwargs.setdefault('bins', bins) 

        g = sns.FacetGrid(x, 
                          col = (self.xfacet if self.xfacet else None),
                          row = (self.yfacet if self.yfacet else None),
                          hue = (self.huefacet if self.huefacet else None),
                          legend_out = False)
        
        g.map(plt.hist, self.channel, **kwargs)
        g.add_legend()
        
    def is_valid(self, experiment):
        """Validate this view against an experiment."""
        if not experiment:
            return False
        
        if self.channel not in experiment.channels:
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
    
if __name__ == '__main__':
   
    plt.ioff()
    p = plt.figure(1)

    tips = sns.load_dataset("tips")
    g = sns.FacetGrid(tips, col="time", fig_kws={"num" : 1})
    
    plt.show()