
# loop through all of the noxious weeds in Utah
# export them to GeoJSON files

# NOTE: There seems to be some limit on the rate/quantity that the
#   server will allow.
# Server stops sending valid records after some point
# time.sleep() may need to be more than 20 seconds


import time
import EDD_requests


for nox in EDD_requests.noxweeds:

    sub = (int(nox["sub"]))
    weed = EDD_requests.Occurrence(sub)

    print(weed.validratio())

    weed.export_GeoJSON(r"output/sub_" + str(sub) + ".json")

    time.sleep(20)  # 20 seconds still doesn't wor
