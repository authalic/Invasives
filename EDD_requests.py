
import json
import requests

"""
API Data Requests
Early Detection & Distribution Mapping System:  https://www.eddmaps.org/
API Documentation: https://developers.bugwood.org/
"""

# State of Utah Noxious Weed List
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

# API Data Request limits:
# Current limit for records returned per request is 3000

        # Option 1
        # url.start - this is the starting record number.
        # url.length - this is how many records to return.

        # Option2
        # url.rows - number of records to return as a "page".
        # url.page - page number to return.


# EDD Occurrences
# API Documentation:  https://developers.bugwood.org/Occurrences/
url = 'https://api.bugwood.org/rest/api/occurrence.json'

payload = {
    'includeonly': 'objectid,SubjectNumber,commonname,WellKnownText,InfestationStatus,ObservationDate,reporter,Density',
    'sub': 0,  # EDD Subject ID (plant species)
    'dateFormat': 101,  # SQL Server date format code: mm/dd/yyyy
    'countyfips': countyfips,
    'start': 0,
    'length': 1
    }

# User Agent header
# Signature requested by Bugwood maintainers to track/contact API users
headers = {'user-agent': 'Justin Johnson, Utah DNR, jjohnson2@utah.gov'}


class Occurrence:

    def getRecords(self, speciescode):
        """returns a dict containing all records for the species code"""

        payload["sub"] = speciescode
        recordcount = self.recordsTotal  # total record count in feature service
        batchsize = 3000 # max records per Bugwood API call

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

            if offset == 0:
                # first API request, save complete JSON response as dict
                records = json.loads(r.text)
            else:
                # append the contents of the "data" list on each subsequent call
                subsequent = json.loads(r.text)
                records["data"] += subsequent["data"]

        return records


    def __init__(self, speciescode):

        self.subject = str(speciescode)  # species code from Bugwood API subjectnumber

        # update the species code in the API request payload
        payload["sub"] = speciescode

        # request a single record to get the "recordsTotal" value for species
        r = requests.get(url, headers=headers, params=payload)

        # save results as object attribute
        self.recordsTotal = json.loads(r.text)["recordsTotal"]

        # send the request to get all records for species code
        self.records = self.getRecords(speciescode) # stored as a dict


    def __repr__(self):
        """print the common name and scientific name of species from noxweeds list"""
        for x in noxweeds:
            if x['sub'] == self.subject:
                return f"{x['name']} ({x['sciname']})"


    def count(self):
        """Returns the number of records in the EDDMapS database for this species code"""
        return self.recordsTotal


    def as_json(self):
        """Returns the species records as JSON"""

        # TODO:  if the total number of records exceeds the request limit, multiple requests
        # need to be sent, and the responses stored in a list

        return json.dumps(self.records)


    def as_jsonp(self):
        """Returns the species records as JSON formatted for viewing"""
        return json.dumps(self.records, sort_keys=True, indent=4)



# Usage
# import this file as a module
# instantiate a new Occurrence object, using the subjectnumber ('sub' value in the noxweeds list)


# TESTCODE

if __name__ == "__main__":
    o = Occurrence(3937)

    print(o.count())
    print(o.as_jsonp())
