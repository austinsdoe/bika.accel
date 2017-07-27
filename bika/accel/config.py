from Products.Archetypes.public import DisplayList
from bika.lims import bikaMessageFactory as _b
from bika.accel import bikaMessageFactory as _

from bika.accel.permissions import *

PROJECTNAME = "bika.accel"

# County THREE LETTER ACRONYMS (TLA), in order to generate IDs
COUNTY_CODES = [
    {"title": "Bomi", "tla": "BOM", "bika_code": "15"},
    {"title": "Bong", "tla": "BON", "bika_code": "01"},
    {"title": "Gbarpolu", "tla": "GBR", "bika_code": "21"},
    {"title": "Grand Bassa", "tla": "GRB", "bika_code": "11"},
    {"title": "Grand Cape Mount", "tla": "GRC", "bika_code": "12"},
    {"title": "Grand Gedeh", "tla": "GRG", "bika_code": "19"},
    {"title": "Grand Kru", "tla": "GRK", "bika_code": "16"},
    {"title": "Lofa", "tla": "LOF", "bika_code": "20"},
    {"title": "Margibi", "tla": "MAR", "bika_code": "17"},
    {"title": "Maryland", "tla": "MAL", "bika_code": "13"},
    {"title": "Montserrado", "tla": "MON", "bika_code": "14"},
    {"title": "Nimba", "tla": "NIM", "bika_code": "09"},
    {"title": "River Gee", "tla": "RGE", "bika_code": "22"},
    {"title": "River Cess", "tla": "RIV", "bika_code": "18"},
    {"title": "Sinoe", "tla": "SIN", "bika_code": "10"},
]
