

def highpass_filter(st, filter_order=5, number_of_passes=2):
    """
    Highpass filter.

    Args:
        st (StationStream):
            Stream of data.
        filter_order (int):
            Filter order.
        number_of_passes (int):
            Number of passes.

    Returns:
        StationStream: Filtered streams.
    """
    if not st.passed:
        return st

    for tr in st:
        tr = highpass_filter_trace(tr, filter_order, number_of_passes)

    return st


def highpass_filter_trace(tr, filter_order=5, number_of_passes=2):
    """
    Highpass filter.

    Args:
        tr (StationTrace):
            Stream of data.
        filter_order (int):
            Filter order.
        number_of_passes (int):
            Number of passes.

    Returns:
        StationTrace: Filtered trace.
    """
    if number_of_passes == 1:
        zerophase = False
    elif number_of_passes == 2:
        zerophase = True
    else:
        raise ValueError("number_of_passes must be 1 or 2.")

    freq_dict = tr.getParameter('corner_frequencies')
    freq = freq_dict['highpass']
    tr.filter(type="highpass",
              freq=freq,
              corners=filter_order,
              zerophase=zerophase)
    tr.setProvenance(
        'highpass_filter',
        {
            'filter_type': 'Butterworth',
            'filter_order': filter_order,
            'number_of_passes': number_of_passes,
            'corner_frequency': freq
        }
    )
    return tr


def lowpass_filter(st, filter_order=5, number_of_passes=2):
    """
    Lowpass filter.

    Args:
        st (StationStream):
            Stream of data.
        filter_order (int):
            Filter order.
        number_of_passes (int):
            Number of passes.

    Returns:
        StationStream: Filtered streams.
    """
    if not st.passed:
        return st

    for tr in st:
        tr = lowpass_filter_trace(tr, filter_order, number_of_passes)

    return st


def lowpass_filter_trace(tr, filter_order=5, number_of_passes=2):
    """
    Lowpass filter.

    Args:
        tr (StationTrace):
            Stream of data.
        filter_order (int):
            Filter order.
        number_of_passes (int):
            Number of passes.

    Returns:
        StationTrace: Filtered trace.
    """
    if number_of_passes == 1:
        zerophase = False
    elif number_of_passes == 2:
        zerophase = True
    else:
        raise ValueError("number_of_passes must be 1 or 2.")

    freq_dict = tr.getParameter('corner_frequencies')
    freq = freq_dict['lowpass']
    tr.filter(type="lowpass",
              freq=freq,
              corners=filter_order,
              zerophase=zerophase)
    tr.setProvenance(
        'lowpass_filter',
        {
            'filter_type': 'Butterworth',
            'filter_order': filter_order,
            'number_of_passes': number_of_passes,
            'corner_frequency': freq
        }
    )
    return tr
