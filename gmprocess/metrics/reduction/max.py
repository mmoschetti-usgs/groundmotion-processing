# Third party imports
import numpy as np

# Local imports
from gmprocess.metrics.reduction.reduction import Reduction


class Max(Reduction):
    """Class for calculation of maximum value."""
    def __init__(self, reduction_data, bandwidth=None, percentile=None,
            period=None, smoothing=None):
        """
        Args:
            reduction_data (obspy.core.stream.Stream or numpy.ndarray): Intensity
                    measurement component.
            percentile (float): Percentile for rotation calculations. Default
                is None.
            period (float): Period for smoothing (Fourier amplitude spectra)
                    calculations. Default
                        is None.
            smoothing (string): Smoothing type. Default is None.
            bandwidth (float): Bandwidth for the smoothing operation. Default
                    is None.
        """
        super().__init__(reduction_data, bandwidth=None, percentile=None,
                period=None, smoothing=None)
        self.result = self.get_max()

    def get_max(self):
        """
        Performs calculation of maximum value.

        Returns:
            maximums: Dictionary of maximum value for each channel.
        """
        maximums = {}
        for trace in self.reduction_data:
            maximums[trace.stats.channel] = np.abs(trace.max())
        return maximums
