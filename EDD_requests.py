import re
import json
import requests
import time  # API may need a break between requests

from json import JSONDecodeError

"""
Noxious Weed Data Client

Obtains records of a noxious plant species from EDDMapS using API data requests.
Provides methods to export that data in native JSON and a GIS-friendly GeoJSON format.
"""

# Data Sources and Documentation:
# Early Detection & Distribution Mapping System:  https://www.eddmaps.org/
# API Documentation: https://developers.bugwood.org/


# State of Utah Noxious Weed List
# source:  https://ag.utah.gov/farmers/plants-industry/noxious-weed-control-resources/state-of-utah-noxious-weed-list/


noxweeds = [
    {'sub': '6515', 'class': '3',  'name': 'Tamarisk (Saltcedar)', 'sciname': 'Tamarix ramosissima'},
    {'sub': '59038','class': '3',  'name': 'Phragmites (Common reed)', 'sciname': 'Phragmites australisssp.'},
    {'sub': '3022', 'class': '4',  'name': 'Russian olive', 'sciname': 'Elaeagnus angustifolia'},
    {'sub': '3005', 'class': '1B', 'name': 'Garlic mustard', 'sciname': 'Alliaria petiolata'},
    {'sub': '3009', 'class': '1B', 'name': 'Giant reed', 'sciname': 'Arundo donax'},
    {'sub': '3405', 'class': '2',  'name': 'Leafy spurge', 'sciname': 'Euphorbia esula'},
    {'sub': '3400', 'class': '1A', 'name': 'Plumeless thistle', 'sciname': 'Carduus acanthoides'},
    {'sub': '4361', 'class': '1A', 'name': 'Mediterranean sage', 'sciname': 'Salvia aethiopis'},
    {'sub': '4414', 'class': '1A', 'name': 'Common crupina', 'sciname': 'Crupina vulgaris'},
    {'sub': '5103', 'class': '1A', 'name': 'Small bugloss', 'sciname': 'Anchusa arvensis'},
    {'sub': '5281', 'class': '1A', 'name': 'Malta starthistle', 'sciname': 'Centaurea melitensis'},
    {'sub': '6048', 'class': '1A', 'name': 'Spring milletgrass', 'sciname': 'Milium vernale'},
    {'sub': '6158', 'class': '1A', 'name': 'African rue', 'sciname': 'Peganum harmala'},
    {'sub': '6589', 'class': '1A', 'name': 'Ventenata (North Africa grass)', 'sciname': 'Ventenata dubia'},
    {'sub': '6630', 'class': '1A', 'name': 'Syrian beancaper', 'sciname': 'Zygophyllum fabago'},
    {'sub': '4411', 'class': '1B', 'name': 'Common St. Johnswort', 'sciname': 'Hypericum perforatum'},
    {'sub': '4535', 'class': '1B', 'name': 'Goatsrue', 'sciname': 'Galega officinalis'},
    {'sub': '5061', 'class': '1B', 'name': 'Camelthorn', 'sciname': 'Alhagi maurorum'},
    {'sub': '5215', 'class': '1B', 'name': 'African mustard', 'sciname': 'Brassica tournefortii'},
    {'sub': '5268', 'class': '1B', 'name': 'Purple starthistle', 'sciname': 'Centaurea calcitrapa'},
    {'sub': '5564', 'class': '1B', 'name': 'Blueweed (Vipers bugloss)', 'sciname': 'Echium vulgare'},
    {'sub': '5937', 'class': '1B', 'name': 'Oxeye daisy', 'sciname': 'Leucanthemum vulgare'},
    {'sub': '19655','class': '1B', 'name': 'Japanese knotweed', 'sciname': 'Polygonum cuspidatum'},
    {'sub': '30314','class': '1B', 'name': 'Cutleaf vipergrass', 'sciname': 'Scorzonera laciniata'},
    {'sub': '32051','class': '1B', 'name': 'Elongated mustard', 'sciname': 'Brassica elongata'},
    {'sub': '3047', 'class': '2',  'name': 'Purple loosestrife', 'sciname': 'Lythrum salicaria'},
    {'sub': '3800', 'class': '2',  'name': 'Yellow toadflax', 'sciname': 'Linaria vulgaris'},
    {'sub': '4373', 'class': '2',  'name': 'Squarrose knapweed', 'sciname': 'Centaurea virgata'},
    {'sub': '4390', 'class': '2',  'name': 'Yellow starthistle', 'sciname': 'Centaurea solstitialis'},
    {'sub': '4404', 'class': '2',  'name': 'Rush skeletonweed', 'sciname': 'Chondrilla juncea'},
    {'sub': '4472', 'class': '2',  'name': 'Diffuse knapweed', 'sciname': 'Centaurea diffusa'},
    {'sub': '4587', 'class': '2',  'name': 'Dyers woad', 'sciname': 'Isatis tinctoria'},
    {'sub': '5736', 'class': '2',  'name': 'Black henbane', 'sciname': 'Hyoscyamus niger'},
    {'sub': '5939', 'class': '2',  'name': 'Dalmation toadflax', 'sciname': 'Linaria dalmatica'},
    {'sub': '6507', 'class': '2',  'name': 'Medusahead', 'sciname': 'Taeniatherum caput-medusae'},
    {'sub': '50209','class': '2',  'name': 'Spotted knapweed', 'sciname': 'Centaurea stoebe'},
    {'sub': '2792', 'class': '3',  'name': 'Canada thistle', 'sciname': 'Cirsium arvense'},
    {'sub': '3011', 'class': '3',  'name': 'Musk thistle', 'sciname': 'Carduus nutans'},
    {'sub': '3075', 'class': '3',  'name': 'Perennial Sorghum spp.:Johnson Grass', 'sciname': 'Sorghumhalepense'},
    {'sub': '3937', 'class': '3',  'name': 'Puncturevine (Goathead)', 'sciname': 'Tribulus terrestris'},
    {'sub': '4338', 'class': '3',  'name': 'Field bindweed (Wild Morning-glory)', 'sciname': 'Convolvulusspp.'},
    {'sub': '4365', 'class': '3',  'name': 'Poison hemlock', 'sciname': 'Conium maculatum'},
    {'sub': '4388', 'class': '3',  'name': 'Russian knapweed', 'sciname': 'Acroptilon repens'},
    {'sub': '4432', 'class': '3',  'name': 'Scotch thistle (Cotton thistle)', 'sciname': 'Onopordum acanthium'},
    {'sub': '5038', 'class': '3',  'name': 'Jointed goatgrass', 'sciname': 'Aegilops cylindrica'},
    {'sub': '5484', 'class': '3',  'name': 'Bermudagrass', 'sciname': 'Cynodon dactylon'},
    {'sub': '5502', 'class': '3',  'name': 'Houndstounge', 'sciname': 'Cynoglossum officianale'},
    {'sub': '5579', 'class': '3',  'name': 'Quackgrass', 'sciname': 'Elymus repens'},
    {'sub': '5931', 'class': '3',  'name': 'Perennial pepperweed(Tall whitetop)', 'sciname': 'Lepidium latifolium'},
    {'sub': '6429', 'class': '3',  'name': 'Perennial Sorghum spp.:Sorghumalmum', 'sciname': 'Sorghum almum'},
    {'sub': '54552','class': '3',  'name': 'Hoary cress', 'sciname': 'Cardariaspp.'},
    {'sub': '2433', 'class': '4',  'name': 'Cogongrass(Japanese blood grass)', 'sciname': 'Imperata cylindrica'},
    {'sub': '4408', 'class': '4',  'name': 'Scotch broom', 'sciname': 'Cytisus scoparius'},
    {'sub': '5632', 'class': '4',  'name': 'Myrtle spurge', 'sciname': 'Euphorbia myrsinites'},
    {'sub': '5702', 'class': '4',  'name': 'Dames Rocket', 'sciname': 'Hesperis matronalis'}
]


# list of counties for data request
countyFIPS = [49003, 49005, 49011, 49023, 49029, 49035, 49039, 49043, 49045, 49049, 49051, 49057]

# 5-digit county FIPS codes:
# 49003 - Box Elder
# 49005 - Cache
# 49011 - Davis *
# 49023 - Juab
# 49029 - Morgan
# 49035 - Salt Lake *
# 49039 - Sanpete
# 49043 - Summit *
# 49045 - Tooele
# 49049 - Utah *
# 49051 - Wasatch *
# 49057 - Weber *


# Get EDD Occurrences from API
# API Documentation:  https://developers.bugwood.org/Occurrences/
# Subject ID lookup:  http://maphelp.eddmaps.org/basics/subject-lookup/

url = 'https://api.bugwood.org/rest/api/occurrence.json'

# payload is a dict of key/value pairs, sent as URL querystring
payload = {
    'includeonly': 'objectid,SubjectNumber,commonname,WellKnownText,InfestationStatus,ObservationDate,reporter,Density', #fieldnames
    'sub': 0,  # EDD Subject ID (plant species)
    'dateFormat': 101,  # SQL Server date format code: mm/dd/yyyy 
    'countyfips': countyFIPS, # list of county FIPS numbers
    'start': 0, # first record in request
    'length': 1 # number of records in request (3000 limit)
    }

# User-Agent header
# Requested by Bugwood maintainers to track/contact API users
headers = {'user-agent': 'Justin Johnson, Utah DNR, jjohnson2@utah.gov'}

errorlog = "errors.txt"


class Occurrence:
    """
    Records of an invasive species occurrence from:
    Early Detection and Distribution Mapping System (EDDMapS)
    Center for Invasive Species and Ecosystems Health
    University of Georgia
    """

    def getRecords(self, speciescode):
        """returns a dict from BugwoodAPI containing all records for the species code"""

        payload["sub"] = speciescode
        recordcount = self.recordsTotal  # total record count in feature service
        batchsize = 3000 # max records per Bugwood API call
        APIrecords = {} # store the processed API JSON dict record string #ugly

        print("Species: " + str(speciescode))

        # send request to Bugwood API
        # use batches, if total record count exceeds 3,000

        for offset in range(0, recordcount, batchsize):

            # print the record range requested by current call
            if offset + batchsize <= recordcount:
                print(str(offset) + " - " + str(offset + batchsize))
            else:
                print(str(offset) + " - " + str(recordcount))
                payload["length"] = recordcount - offset

            # send the GET request to the REST endpoint
            payload["start"] = offset
            r = requests.get(url, headers=headers, params=payload)

            # rest a bit, before sending next request, to avoid overloading API server
            time.sleep(5) # seconds

            if offset == 0:
                # first API request, save complete JSON response as dict
                APIrecords = json.loads(r.text)
            else:
                # append the contents of the "data" list on each subsequent call
                subsequent = json.loads(r.text)
                APIrecords["data"] += subsequent["data"]

        return APIrecords


    def __init__(self, speciescode):
        """
        Constructor:
        Requires a numeric Subject ID code for the desired plant species
        Subject ID lookup:  http://maphelp.eddmaps.org/basics/subject-lookup/
        """

        self.subject = str(speciescode)  # species code from Bugwood API subject id number

        # update the species code in the API request payload
        payload["sub"] = speciescode

        # request a single record to get the "recordsTotal" value for species
        r = requests.get(url, headers=headers, params=payload)

        # save record count as attribute, to be used later in requesting all records
        self.recordsTotal = json.loads(r.text)["recordsTotal"]

        # send the request to get all records for species code
        # if any valid records were found, store internally as a dict
        self.records = self.getRecords(speciescode)

        # number of records with properly formatted spatial information
        # (still... may not be a valid location)
        if self.records:
            self.validRecords = len(self.records["data"])
        else:
            self.validRecords = 0


    def __repr__(self):
        """print the common name and scientific name of species from noxweeds list"""

        for x in noxweeds:
            if x['sub'] == self.subject:
                return f"{x['name']} ({x['sciname']})"


    def count(self):
        """Returns the number of records in the EDDMapS database for this species code"""
        if self.records:
            return self.recordsTotal


    def validcount(self):
        """Returns the number of records from the EDDMapS API request with a valid spatial feature"""
        if self.records:
            return self.validRecords


    def validratio(self):
        """Returns a string indicating the ratio of valid records to total records"""
        if self.records:
            return str(self.validcount()) + r"/" + str(self.count()) + " valid records"
        else:
            return "No valid records"


    def as_JSON(self):
        """Returns the EDDMapS species records as JSON
        No changes or corrections are made to the data returned from the API
        Errors may exist in spatial data.
        To export for geospatial use, use as_GeoJSON()"""

        if self.records:
            return json.dumps(self.records)
        else:
            return ""


    def export_JSON(self, filename):
        """Exports records to a JSON file"""

        with open(filename, 'w') as file:
            file.write(self.as_JSON())


    def as_JSONPretty(self):
        """Returns the species records as JSONP formatted for human readability"""
        
        if self.records:
            return json.dumps(self.records, sort_keys=False, indent=4)
        else:
            return ""


    def export_JSONPretty(self, filename):
        """Exports a prettified JSON file, formatted for human readability
        Note: File sizes will be larger when JSONPretty() is used. 
        If formatting is not required use the export_JSON() method"""

        with open(filename, 'w') as file:
            file.write(self.as_JSONPretty())


    def reformat(self, geom):
        """Helper function: changes coordinate pair string(s) from WKT to GeoJSON
        Don't call directly. Use as_GeoJSON()"""

        # Split the WKT geometry string into a tuple of string fields
        # (geometry type, geometry coordinates)
        #  NOTE: input data from EDDMapS is not consistently and properly formatted
        #  eg. there may, or may not, be a space between geom and ()
        #      coordinates have been found with numbers outside parentheses
        # some string hacks are required in order to get data into usable format
        # records that cannot be rescued are skipped

        # geom is the WKT geometry
        # examples: "POINT(-112.213747 41.892975)", "POINT (-111.9223893 40.6292995)"
        
        # split at first parenthesis
        g = geom.split( '(', maxsplit=1 )

        # get the geometry type (Point, LineString, Polygon)
        # strip any extra spaces and convert case to title
        geomtype = g[0].strip().title() 

        # NOTE: the correct spelling of "Linestring" in GeoJSON spec is "LineString"
        # alternate spelling appears in some EDDMapS records
        if geomtype == "Linestring":
            geomtype = "LineString"

        # restore opening parenthesis, which was lost splitting string earlier #ugly
        coords = '(' + g[1]

        # RE matches lat/lon coordinate strings, with the format: "-111.9415 41.26219"
        c = re.compile(r'-\d+.\d+\s\d+.\d+')  #NW global quadrant coordinates only

        # get a list of coordinate pairs in the current geometry using the RE module
        # Point has a single pair, LineString and Polygon will have more
        coordlist = c.findall(coords)

        # change the format of the coordinate pairs
        #   from:  "-111.941542 41.2621659"     <-- WKT
        #     to:  "[-111.941542, 41.2621659]"  <-- GeoJSON
        for coord in coordlist:
            # replace whitespace(s) delimeter with a comma
            # add square brackets around coordinate pair
            newcoord = '[' + re.sub(r'[ ]+', ', ', coord) + ']'
            coords = coords.replace(coord, newcoord)

            #TODO:  rename the coords variable, since it contains a list below

        # replace all remaining parentheses in coordinate string with square brackets
        coords = coords.replace('(', '[')
        coords = coords.replace(')', ']')


        # convert the coordinates from a string to a JSON array (Python list)
        # Point features seem to add extra square brackets: [[-111.941542, 41.2621659]]

        # NOTE: The following if..else is an ugly workaround
        # TODO: find out where the extra brackets are coming from

        # ERROR in WKT
        # Apparently, bad WKT can be uploaded to EDDMapS through their web portal
        # check for JSONDecodeError when converting from WKT string to dict using json.loads()

        try:  
            JSONgeom = json.loads(coords)
            # at this point, the coordinate string is a Python dict

            if geomtype == "Point":
                # the point is stored in a list inside a list: [[lon, lat]]
                # extract the inner list 
                coords = JSONgeom[0] 
            else:
                coords = JSONgeom
            
        except JSONDecodeError:
            # badly formatted WKT... log it, skip it

            with open(errorlog, "a") as log:
                log.write(coords + "\n")


        # return a tuple containing reformatted (for GeoJSON) geometry type and coordinates
        return (geomtype, coords)


    def as_GeoJSON(self):
        """
        Converts a dict of species records to properly formatted GeoJSON string
        for input into QGIS or ArcGIS
        """

        if not self.records:
            return ""

        # GeoJSON Linter  http://geojsonlint.com/

        # Geometries in EED Data
        # stored as WKT
        # 3 geometry types found (so far): ('POINT', 'POLYGON', 'LINESTRING')
        # if another geom is used in the EDDMapS, ie 'MULTIPOINT' or 'MULTIPOLYGON',
        # it should work in the code below, but hasn't been tested

        # GeoJSON FeatureCollection
        # dict containing all of the records reformatted for GeoJSON dump
        collection = {
            "type": "FeatureCollection",
            "features": []
        }

        # list of columns returned from API, should match the list sent in API request
        cols = self.records["columns"]

        # extract list of records from dict
        data = self.records["data"]

        for record in data:
            # create a dict of column names for key/value pairs, for GeoJSON format
            properties = {col: "" for col in cols}

            # for each record, populate the properties dict with values from record
            for x in range(len(cols)):
                # use 'range' to maintain order of matching between cols and record
                properties[cols[x]] = record[x]

            # new feature dict for current record (see GeoJSON format specification)
            feat = {
                "type": "Feature", 
                "geometry": {
                    "type": "",
                    "coordinates": ""
                    }, 
                "properties": properties
                }
            
            # populate the value of the feat["geometry"["coordinates"] key
            # with a list of coordinates

            if 'wellknowntext' in cols:
                # there is a wellknowntext attribute in the data returned from EDDMapS

                # NOTE: some values returned from EDDMapS do not contain anything in the
                # wellknowntext field, and cannot be mapped. They are skipped here.

                if feat["properties"]["wellknowntext"]:
                    # the wellknowntext attribute is not an empty string

                    wkt = feat["properties"]["wellknowntext"]

                    # send the WKT geometry to be reformatted into GeoJSON
                    geofmts = self.reformat(wkt)

                    feat["geometry"]["type"] = geofmts[0] # Geometry type string
                    feat["geometry"]["coordinates"] = geofmts[1] # Geometry coordinate list

                    # remove the old WKT property from the properties dict
                    # it is now stored in the geometry dict
                    properties.pop("wellknowntext")

                    # append the current feature to the features list in the FeatureCollection dict
                    collection["features"].append(feat)
                else:
                    # no spatial data for this feature... log it, skip it

                    with open(errorlog, "a") as log:
                        log.write(str(feat) + "\n")

        return json.dumps(collection, indent=4)


    def export_GeoJSON(self, filename):
        """Exports records to a GeoJSON file"""

        with open(filename, 'w') as file:
            file.write(self.as_GeoJSON())


# TESTCODE

if __name__ == "__main__":
    o = Occurrence(5702) #

    print(o.validratio())

    o.export_JSON("test1.json")
    o.export_JSONPretty("test1_pretty.json")
    o.export_GeoJSON("test1_geo.json")
    o.export_GeoJSON(r"output/sub_" + str(o.subject) + ".json")
