"""
Definition of a class managing general information
on a seismic station taken from the SQL databases initialised by the 
00_setup.py script
"""

from seissuite.ant import (pserrors, psutils)
from seissuite.response.resp import (freq_check, process_response, 
                                     window_overlap)
import obspy
import obspy.core
from obspy import read_inventory
from obspy.xseed.utils import SEEDParserException
import os
import glob
import pickle
from copy import copy
import itertools as it
import numpy as np
import sqlite3 as lite
from obspy.core import UTCDateTime
import datetime as dt

# import CONFIG class initalised in ./configs/tmp_config.pickle
config_pickle = 'configs/tmp_config.pickle'
f = open(name=config_pickle, mode='rb')
CONFIG = pickle.load(f)
f.close()
    
# import variables from initialised CONFIG class.
MSEED_DIR = CONFIG.MSEED_DIR
STATIONXML_DIR = CONFIG.STATIONXML_DIR
DATALESS_DIR = CONFIG.DATALESS_DIR
DATABASE_DIR = CONFIG.DATABASE_DIR
# import response check variables from CONFIG class
RESP_CHECK = CONFIG.RESP_CHECK
RESP_FREQS = CONFIG.RESP_FREQS
RESP_TOL = CONFIG.RESP_TOL
RESP_EFFECT = CONFIG.RESP_EFFECT

class StationSQL:
    """
    Class to hold general station info: name, network, channel,
    base dir, month subdirs and coordinates.
    """

    def __init__(self, name, network, channel, filename, basedir=None,
                 subdirs=None, coord=None):
        """
        @type name: str
        @type network: str
        @type channel: str
        @type filename: str or unicode
        @type basedir: str or unicode
        @type subdirs: list of str or unicode
        @type coord: list of (float or None)

        """
        self.name = name
        self.network = network
        self.channel = channel  # only one channel allowed (should be BHZ)
        self.file = filename
        self.basedir = basedir
        self.subdirs = subdirs if subdirs else []
        self.coord = coord if coord else (None, None)

    def __repr__(self):
        """
        e.g. <BL.10.NUPB>
        """
        return '<Station {0}.{1}.{2}>'.format(self.network, self.channel, 
                                              self.name)

    def __str__(self):
        """
        @rtype: unicode
        """
        # General infos of station
        s = [u'Name    : {0}'.format(self.name),
             u'Network : {0}'.format(self.network),
             u'Channel : {0}'.format(self.channel),
             u'File    : {0}'.format(self.file),
             u'Base dir: {0}'.format(self.basedir),
             u'Subdirs : {0}'.format(self.subdirs),
             u'Lon, Lat: {0}, {1}'.format(*self.coord)]
        return u'\n'.join(s)
        
    def getpath(self, starttime, endtime):
        """
        Gets path to mseed file using initialised SQL timeline database
        @type starttime: L{UTCDateTime} or L{datetime} or L{date}
        @type endtime: L{UTCDateTime} or L{datetime} or L{date}

        @rtype: unicode
        """

        starttime, endtime = UTCDateTime(starttime), UTCDateTime(endtime)
        
        import_start = starttime.timestamp
        #import_end = endtime.timestamp
        
        #connect SQL database
        database_name = os.path.join(DATABASE_DIR, 'timeline.db')

        if not os.path.exists(database_name):
            raise Exception("Database doesn't exist")
        
        conn = lite.connect(database_name)
        #print "conn: ", conn
        
        c = conn.cursor()
        extrema = []
        for row in c.execute('''SELECT * FROM 
                             file_extrema ORDER BY station'''):
            extrema.append(row)
        
        # make sure that this test works! 
        code = '{}.{}.{}'.format(self.network, self.name, self.channel)
    
        file_paths = c.execute('''SELECT file_path FROM 
                             file_extrema WHERE starttime <= ? 
                             AND endtime >= ? AND station = ? LIMIT 1''', 
                             (import_start, import_start, code))        
        
        output_path = []
        for file_path in file_paths: output_path.append(file_path)
        if len(output_path) > 0:
            return str(output_path[0][0])


        # close database
        conn.close() 
        
    def dist(self, other):
        """
        Geodesic distance (in km) between stations, using the
        WGS-84 ellipsoidal model of the Earth

        @type other: L{Station}
        @rtype: float
        """
        lon1, lat1 = self.coord
        lon2, lat2 = other.coord
        return psutils.dist(lons1=lon1, lats1=lat1, lons2=lon2, lats2=lat2)

    # =================
    # Boolean operators
    # =================
    BOOLATTRS = ['name', 'network', 'channel']

    def __eq__(self, other):
        """
        @type other: L{Station}
        """
        return all(getattr(self, att) == getattr(other, att) for att in self.BOOLATTRS)

    def __ne__(self, other):
        """
        @type other: L{Station}
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """
        @type other: L{Station}
        """
        return ([getattr(self, att) for att in self.BOOLATTRS] <
                [getattr(other, att) for att in self.BOOLATTRS])

    def __le__(self, other):
        """
        @type other: L{Station}
        """
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        """
        @type other: L{Station}
        """
        return not self.__le__(other)

    def __ge__(self, other):
        """
        @type other: L{Station}
        """
        return not self.__lt__(other)


def get_stats(filepath, channel='BHZ', fast=True):
    """
    Returns stats on channel *channel* of stations
    contained in *filepath*, as a dict:

    {`station name`: {'network': xxx, 'firstday': xxx, 'lastday': xxx},
     ...
    }

    Raises an Exception if a station name appears in several networks.

    @rtype: dict from str to dict
    """

    if fast:
        # todo: write low level function inspired of obspy.mseed.util._getRecordInformation
        raise NotImplementedError
    else:
        # reading file (header only) as a stream
        st = obspy.core.read(filepath, headonly=True)

        # selecting traces whose channel is *channel*
        traces = [t for t in st if t.stats['channel'] == channel]

        # getting unique station names
        stations = set(t.stats['station'] for t in traces)

        # getting network, first day and last day of each station
        stationstats = {}
        for stationname in stations:
            # traces of station
            stationtraces = [t for t in traces if t.stats['station'] == stationname]

            # network of station
            networks = set(t.stats['network'] for t in stationtraces)
            if len(networks) > 1:
                # a station name cannot appear in several networks
                s = "Station {} appears in several networks: {}"
                raise Exception(s.format(stationname, networks))
            network = list(networks)[0]

            # first and last day of data
            firstday = min(t.stats['starttime'].date for t in stationtraces)
            lastday = max(t.stats['endtime'].date for t in stationtraces)

            # appending stats
            stationstats[stationname] = {
                'network': network,
                'firstday': firstday,
                'lastday': lastday
            }

    return stationstats
    
def get_coords(dataless_inventories, xml_inventories, USE_STATIONXML):
    
    coordinates = set((c['longitude'], c['latitude']) for inv in dataless_inventories)
    if USE_STATIONXML:
        coordinates = coordinates.union((s.longitude, s.latitude) \
                                        for inv in xml_inventories)
                                            
    return coordinates
    
    
def get_stationsSQL(SQL_db, xml_inventories=(), 
                    dataless_inventories=(), networks=None, 
                    startday=None, endday=None, coord_tolerance=1E-4,
                    verbose=False):
    """
    Gets the list of stations from miniseed files, and
    extracts information from StationXML and dataless
    inventories.

    @type SQL_db: str or unicode path file to SQL database create_database.py
    @type xml_inventories: list of L{obspy.station.inventory.Inventory}
    @type dataless_inventories: list of L{obspy.xseed.parser.Parser})
    @type networks: list of str
    @type startday: L{datetime.date}
    @type endday: L{datetime.date}
    @rtype: list of L{Station}
    """
    
    if verbose:
        print "Scanning stations in SQL database: \n", SQL_db

    # initializing list of stations by scanning name of miniseed files
    stations = []
    print SQL_db
    if not os.path.exists(SQL_db):
        raise Exception("Database doesn't exist. Please \
re-run create_database in seissuite.database")

    # connect the database
    conn = lite.connect(SQL_db)
    # create cursor object
    c = conn.cursor()
    
    extrema = []
    for row in c.execute('''SELECT * FROM 
                         file_extrema ORDER BY station'''):
        extrema.append(row)
        #code = '{}.{}'.format(self.network, self.name)
        #print code
        #print starttime
        #print endtime
    database = c.execute('''SELECT * FROM file_extrema''')
    # quickly extract and flatten SQL query output into a python list object
    database = list(database.fetchall())

    # close timeline.db database
    conn.close() 
    
    # open the response database if it exists
    resp_SQL = os.path.join(DATABASE_DIR, 'response.db')
    
    if RESP_CHECK and not os.path.exists(resp_SQL):
        raise Exception('There is no response databse but RESP_CHECK = True')
        
    # connect the response database
    conn = lite.connect(resp_SQL)
    # create cursor object
    c = conn.cursor()
    
    subdir_len = len(database)

    for row in database:
        code, starttime, endtime, file_path = row
        starttime, endtime = UTCDateTime(starttime), UTCDateTime(endtime)

        # check if times are within the run time limits set but only run 
        # this check if the start and end run times of the programme aren't
        # automatic
        year, month, day = str(starttime.date).split('-')
        subdir = os.path.basename(file_path)
        
        network, name, channel = code.split('.')[0:3]
        
        # search response instrument database if RESP_CHECK is True
        resp_code = code.replace('.', '_')

        if networks and network not in networks:
            continue

        # looking for station in list
        try:
            match = lambda s: [s.network, s.name, s.channel] ==\
            [network, name, channel]
            station = next(s for s in stations if match(s))
            
        except StopIteration:
        # =====================================================================
        # Remove channels outside of the acceptible instrument freq. response
        # ===================================================================== 
            if RESP_CHECK:
                overlap = process_response(resp_code)
                if overlap >= RESP_TOL:
                    # appending new station, with current subdir
                    station = StationSQL(name=name, network=network, 
                                         channel=channel,
                                         filename=file_path)                
                    stations.append(station)
                else:
                    continue
            else:
                # appending new station, with current subdir
                station = StationSQL(name=name, network=network, 
                                     channel=channel,
                                     filename=file_path)                
                stations.append(station)

        else:
            # appending subdir to list of subdirs of station
            station.subdirs.append(subdir)

    if verbose:
        print 'Found {0} stations'.format(len(stations))

    # adding lon/lat of stations from inventories
    if verbose:
        print "Inserting coordinates to stations from inventories"

    for sta in copy(stations):
        # coordinates of station in dataless inventories
        coords_set = set((c['longitude'], c['latitude']) for
                          inv in dataless_inventories for c 
                          in inv.getInventory()['channels']
                          if c['channel_id'].split('.')[:2]
                          == [sta.network, sta.name])
        # coordinates of station in xml inventories
        coords_set = coords_set.union((s.longitude, s.latitude) for 
                                       inv in xml_inventories for net 
                                       in inv for s in net.stations
                                       if net.code == sta.network 
                                       and s.code == sta.name)
        if not coords_set:
            # no coords found: removing station
            if verbose:
                print "WARNING: skipping {}. No coords found".format(repr(sta))
            stations.remove(sta)
        elif len(coords_set) == 1:
            # one set of coords found
            sta.coord = list(coords_set)[0]
        else:
            # several sets of coordinates: calculating max diff
            lons = [lon for lon, _ in coords_set]
            lons_combinations = list(it.combinations(lons, 2))
            lats = [lat for _, lat in coords_set]
            lats_combinations = list(it.combinations(lats, 2))
            maxdiff_lon = np.abs(np.diff(lons_combinations)).max()
            maxdiff_lat = np.abs(np.diff(lats_combinations)).max()
            if maxdiff_lon <= coord_tolerance and maxdiff_lat <= coord_tolerance:
                # coordinates differences are within tolerance:
                # assigning means of coordinates
                if verbose:
                    s = ("{} has several sets of coords within "
                         "tolerance: assigning mean coordinates")
                    print s.format(repr(sta))
                sta.coord = (np.mean(lons), np.mean(lats))
            else:
                # coordinates differences are not within tolerance:
                # removing station
                if verbose:
                    s=("WARNING: skipping {} with several sets of coords not "
                     "within tolerance (max lon diff = {}, max lat diff = {})")
                    print s.format(repr(sta), maxdiff_lon, maxdiff_lat)
                stations.remove(sta)

    # close response.db database
    conn.close() 
    
    return stations, subdir_len


def get_stationxml_inventories(stationxml_dir=STATIONXML_DIR, verbose=False):
    """
    Reads inventories in all StationXML (*.xml) files
    of specified dir

    @type stationxml_dir: unicode or str
    @type verbose: bool
    @rtype: list of L{obspy.station.inventory.Inventory}
    """
    inventories = []

    # list of *.xml files
    flist = glob.glob(pathname=os.path.join(stationxml_dir, "*.xml"))

    if verbose:
        if flist:
            print "Reading inventory in StationXML file:",
        else:
            s = u"Could not find any StationXML file (*.xml) in dir: {}!"
            print s.format(stationxml_dir)

    for f in flist:
        if verbose:
            print os.path.basename(f),
        inv = read_inventory(f, format='stationxml')
        inventories.append(inv)

    if flist and verbose:
        print

    return inventories


def get_dataless_inventories(dataless_dir=DATALESS_DIR, verbose=False):
    """
    Reads inventories in all dataless seed (*.dataless) and
    pickle (*.pickle) files of specified dir

    @type dataless_dir: unicode or str
    @type verbose: bool
    @rtype: list of L{obspy.xseed.parser.Parser}
    """
    inventories = []

    # list of *.dataless files
    flist = glob.glob(pathname=os.path.join(dataless_dir, "*.dataless"))

    if verbose:
        if flist:
            print "Reading inventory in dataless seed file:",
        else:
            s = u"Could not find any dalatess seed file (*.dataless) in dir: {}!"
            print s.format(dataless_dir)

    for f in flist:
        if verbose:
            print os.path.basename(f),
        inv = obspy.xseed.Parser(f)
        inventories.append(inv)

    # list of *.pickle files
    flist = glob.glob(pathname=os.path.join(dataless_dir, "*.pickle"))

    if flist and verbose:
        print "\nReading inventory in pickle file:",

    for f in flist:
        if verbose:
            print os.path.basename(f),
        f = open(f, 'rb')
        inventories.extend(pickle.load(f))
        f.close()

    if flist and verbose:
        print

    return inventories


def get_paz(channelid, t, inventories):
    """
    Gets PAZ from list of dataless (or pickled dict) inventories
    @type channelid: str
    @type t: L{UTCDateTime}
    @type inventories: list of L{obspy.xseed.parser.Parser} or dict
    @rtype: dict
    """

    for inv in inventories:
        try:
            if hasattr(inv, 'getPAZ'):
                paz = inv.getPAZ(channelid, t)
            else:
                assert channelid == inv['channelid']
                assert not inv['startdate'] or t >= inv['startdate']
                assert not inv['enddate'] or t <= inv['enddate']
                paz = inv['paz']
        except (SEEDParserException, AssertionError):
            continue
        else:
            return paz
    else:
        # no matching paz found
        raise pserrors.NoPAZFound('No PAZ found for channel ' + channelid)


def load_pickled_stations(pickle_file):
    """
    Loads pickle-dumped stations

    @type pickle_file: str or unicode
    @rtype: list of L{Station}
    """
    pickle_stations = []
    f = open(pickle_file, 'rb')
    while True:
        try:
            s = pickle.load(f)
        except EOFError:
            f.close()
            break
        except Exception as err:
            f.close()
            raise err
        else:
            pickle_stations.append(s)
    return pickle_stations