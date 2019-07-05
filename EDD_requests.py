
import json
import requests

from bs4 import BeautifulSoup as bs


"""
Noxious Weed Data Client

Obtains records of noxious plant species from EDDMapS using API data requests.
Allows export of data in a GIS-friendly format.

Data Sources and Documentation:
Early Detection & Distribution Mapping System:  https://www.eddmaps.org/
API Documentation: https://developers.bugwood.org/
"""


# EDD Occurrences of noxious species
# API Documentation:  https://developers.bugwood.org/Occurrences/
url = 'https://api.bugwood.org/rest/api/occurrence.json'


# State of Utah Noxious Weed List (July 2019)
# source:  https://ag.utah.gov/farmers/plants-industry/noxious-weed-control-resources/state-of-utah-noxious-weed-list/
noxweeds = [
    {'sub': '3400', 'class': '1A', 'name': 'Plumeless thistle', 'sciname': 'Carduus acanthoides'},
    {'sub': '4361', 'class': '1A', 'name': 'Mediterranean sage', 'sciname': 'Salvia aethiopis'},
    {'sub': '4414', 'class': '1A', 'name': 'Common crupina', 'sciname': 'Crupina vulgaris'},
    {'sub': '5103', 'class': '1A', 'name': 'Small bugloss', 'sciname': 'Anchusa arvensis'},
    {'sub': '5281', 'class': '1A', 'name': 'Malta starthistle', 'sciname': 'Centaurea melitensis'},
    {'sub': '6048', 'class': '1A', 'name': 'Spring milletgrass', 'sciname': 'Milium vernale'},
    {'sub': '6158', 'class': '1A', 'name': 'African rue', 'sciname': 'Peganum harmala'},
    {'sub': '6589', 'class': '1A', 'name': 'Ventenata (North Africa grass)', 'sciname': 'Ventenata dubia'},
    {'sub': '6630', 'class': '1A', 'name': 'Syrian beancaper', 'sciname': 'Zygophyllum fabago'},
    {'sub': '3005', 'class': '1B', 'name': 'Garlic mustard', 'sciname': 'Alliaria petiolata'},
    {'sub': '3009', 'class': '1B', 'name': 'Giant reed', 'sciname': 'Arundo donax'},
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
    {'sub': '3405', 'class': '2',  'name': 'Leafy spurge', 'sciname': 'Euphorbia esula'},
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
    {'sub': '6515', 'class': '3',  'name': 'Tamarisk (Saltcedar)', 'sciname': 'Tamarix ramosissima'},
    {'sub': '54552','class': '3',  'name': 'Hoary cress', 'sciname': 'Cardariaspp.'},
    {'sub': '59038','class': '3',  'name': 'Phragmites (Common reed)', 'sciname': 'Phragmites australisssp.'},
    {'sub': '2433', 'class': '4',  'name': 'Cogongrass(Japanese blood grass)', 'sciname': 'Imperata cylindrica'},
    {'sub': '3022', 'class': '4',  'name': 'Russian olive', 'sciname': 'Elaeagnus angustifolia'},
    {'sub': '4408', 'class': '4',  'name': 'Scotch broom', 'sciname': 'Cytisus scoparius'},
    {'sub': '5632', 'class': '4',  'name': 'Myrtle spurge', 'sciname': 'Euphorbia myrsinites'},
    {'sub': '5702', 'class': '4',  'name': 'Dames Rocket', 'sciname': 'Hesperis matronalis'}
]


# list of counties for data request
countyfips = [49003, 49005, 49011, 49023, 49029, 49035, 49039, 49043, 49045, 49049, 49051, 49057]

# 49003 - Box Elder
# 49005 - Cache
# 49011 - Davis
# 49023 - Juab
# 49029 - Morgan
# 49035 - Salt Lake
# 49039 - Sanpete
# 49043 - Summit
# 49045 - Tooele
# 49049 - Utah
# 49051 - Wasatch
# 49057 - Weber


class occurrence:
    """
    Represents the data obtained from EDDMapS for a single species code.
    Methods provide data summary info and export as Python objects or data files.
    """

    def send_request(self, record_start = 0, record_len = 1):
        """
        Sends a GET request to the REST API
        Returns the results as JSON
        """

        payload = {
            'includeonly': 'objectid,SubjectNumber,commonname,WellKnownText,InfestationStatus,ObservationDate,reporter,Density',
            'sub': self.subject,  # EDD Subject ID (plant species)
            'dateFormat': 101,  # SQL Server date format code: mm/dd/yyyy
            'countyfips': countyfips,
            'start': record_start,
            'length': record_len
        }

        # User Agent header
        # Signature requested by Bugwood maintainers to track/contact API users
        headers = {'user-agent': 'Justin Johnson, Utah DNR, jjohnson2@utah.gov'}

        # send the GET request to the REST endpoint
        # store results as a json string
        r = requests.get(url, headers=headers, params=payload)

        # convert the results to a Python dictionary
        return json.loads(r.text)


    def __init__(self, speciescode):

        self.subject = str(speciescode)  # EDDMapS species code

        # store all records received from EDDMapS as an attribute of the object
        # each record is a list within the larger master attribute list
        self.recs = []

        # obtain the basic information about the species from the REST endpoint
        response = self.send_request()

        # list of header names returned from server with data request
        self.cols = response["columns"]

        # total number of records in EDDMapS for this species code
        self.recordCount = response["recordsTotal"]

        # if records exist, request them from the REST service
        if self.recordCount > 0:
            # request records in batches
            # Current API data request limit is 3000 rows per request

            batchsize = 1000 # number of records requested per API call

            for x in range(0, self.recordCount, batchsize):
                # obtain records (in json) between row x and x + batchsize-1
                rec_batch = self.send_request(x, batchsize-1)

                # append the lists of records recieved to the object attribute list
                self.recs += rec_batch["data"]


    def __repr__(self):
        """print the common name and scientific name of species from noxweeds list"""
        for x in noxweeds:
            if x['sub'] == self.subject:
                return f"{x['name']} ({x['sciname']})"


    def count(self):
        """Returns the number of records in the EDDMapS database for this species code"""
        return self.recordCount


    def columns(self):
        """Returns a list of the column headers for the records"""
        return self.cols


    def records(self):
        """Returns all records as a list of lists"""
        return self.recs


    def as_json(self):
        """Returns the species records as JSON string"""
        return json.dumps({"columns": self.cols, "data": self.recs})


    def as_jsonp(self):
        """Returns the species records as JSON string formatted for viewing"""
        return json.dumps(self.as_json(), sort_keys=True, indent=4)


    def as_geojson(self):
        """Returns the species records in a GeoJSON format for use in GIS"""
        # NOTE: Records can contain several geometry types in the same table: (point, polygon, or multipolygon WKT)

        pass


# TEST CODE HERE

d = occurrence(4411)

for x in d.records():
    print(x[3])
