# Third party imports
import numpy as np

# Local imports
from gmprocess.metrics.transform.transform import Transform


class FFT(Transform):
    """Class for computing the fast fourier transform."""
    def __init__(self, transform_data, damping=None, period=None, times=None):
        """
        Args:
            transform_data (obspy.core.stream.Stream or numpy.ndarray): Intensity
                    measurement component.
            damping (float): Damping for spectral amplitude calculations.
                    Default is None.
            period (float): Period for spectral amplitude calculations.
                    Default is None.
            times (numpy.ndarray): Times for the spectral amplitude calculations.
                    Default is None.
        """
        super().__init__(transform_data, damping=None, period=None, times=None)
        self.result = self.get_fft()

    def get_fft(self):
        """
        Calculated the fft of each trace's data.

        Returns:
            numpy.ndarray: Computed fourier amplitudes.
        """
        horizontals = self._get_horizontals()
        nfft = len(horizontals[0].data)
        sampling_rate = horizontals[0].stats.sampling_rate
        freqs = np.fft.rfftfreq(nfft, 1 / sampling_rate)
        ft_traces = [freqs]
        for trace in horizontals:
            # the fft scales so the factor of 1/nfft is applied
            spectra = abs(np.fft.rfft(trace.data, n=nfft)) / nfft
            ft_traces += [spectra]
        return ft_traces
