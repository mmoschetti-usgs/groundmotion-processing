# stdlib imports
import importlib
import pkg_resources
import inspect
import os.path
import logging

# local imports
from .fetcher import DataFetcher
from gmprocess.config import get_config


def fetch_data(time, lat, lon,
               depth, magnitude,
               config=None,
               rawdir=None, drop_non_free=True):
    """Retrieve data using any DataFetcher subclass.

    Args:
        time (datetime):
            Origin time.
        lat (float):
            Origin latitude.
        lon (float):
            Origin longitude.
        depth (float):
            Origin depth.
        magnitude (float):
            Origin magnitude.
        radius (float):
            Search radius (km).
        dt (float):
            Search time window (sec).
        ddepth (float):
            Search depth window (km).
        dmag (float):
            Search magnitude window (magnitude units).
        rawdir (str):
            Path to location where raw data will be stored. If not specified,
            raw data will be deleted.
        drop_non_free (bool):
            Option to ignore non-free-field (borehole, sensors on structures, etc.)

     Returns:
        StreamCollection: StreamCollection object.
    """
    if config is None:
        config = get_config()
    fetchers = find_fetchers(lat, lon)
    instances = []
    errors = []
    for fetchname, fetcher in fetchers.items():
        try:
            fetchinst = fetcher(time, lat, lon,
                                depth, magnitude,
                                config=config,
                                rawdir=rawdir, drop_non_free=drop_non_free)
        except Exception as e:
            fmt = 'Could not instantiate Fetcher %s, due to error\n "%s"'
            tpl = (fetchname, str(e))
            msg = fmt % tpl
            logging.warn(msg)
            errors.append(msg)
            continue
        xmin, xmax, ymin, ymax = fetchinst.BOUNDS
        if (xmin < lon < xmax) and (ymin < lat < ymax):
            instances.append(fetchinst)

    efmt = '%s M%.1f (%.4f,%.4f)'
    etpl = (time, magnitude, lat, lon)
    esummary = efmt % etpl
    streams = []
    for fetcher in instances:
        if 'FDSN' in str(fetcher):
            tstreams = fetcher.retrieveData()
            if len(streams):
                streams = streams + tstreams
            else:
                streams = tstreams

        else:
            events = fetcher.getMatchingEvents(solve=True)
            if not len(events):
                msg = 'No event matching %s found by class %s'
                logging.warn(msg % (esummary, str(fetcher)))
                continue
            tstreams = fetcher.retrieveData(events[0])
            if len(streams):
                streams = streams + tstreams
            else:
                streams = tstreams

    if streams is None:
        streams = []
    return (streams, errors)


def find_fetchers(lat, lon):
    """Create a dictionary of classname:class to be used in main().

    Args:
        lat (float): Origin latitude.
        lon (float): Origin longitude.

    Returns:
        dict: Dictionary of classname:class where each class
            is a subclass of shakemap.coremods.base.CoreModule.
    """

    fetchers = {}
    root = os.path.abspath(
        pkg_resources.resource_filename('gmprocess', 'io'))
    for (rootdir, dirs, files) in os.walk(root):
        if rootdir == root:
            continue
        for tfile in files:
            modfile = os.path.join(rootdir, tfile)
            modname = modfile[modfile.rfind(
                'gmprocess'):].replace('.py', '')
            modname = modname.replace(os.path.sep, '.')
            if modname.find('__') >= 0:
                continue
            mod = importlib.import_module(modname)
            for name, obj in inspect.getmembers(mod):
                if name == 'DataFetcher':
                    continue
                if inspect.isclass(obj) and issubclass(obj, DataFetcher):
                    fetchers[name] = obj
    return fetchers
