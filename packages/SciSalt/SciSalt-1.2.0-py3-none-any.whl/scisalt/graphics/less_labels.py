import numpy as _np

def less_labels(ax,x_fraction=0.5,y_fraction=0.5):
	nbins = _np.size(ax.get_xticklabels())
	ax.locator_params(nbins=_np.floor(nbins*x_fraction),axis='x')

	nbins = _np.size(ax.get_yticklabels())
	ax.locator_params(nbins=_np.floor(nbins*y_fraction),axis='y')
