# Default configuration file for eagle_automation.

import sys
import glob

if 'darwin' == sys.platform:
    eagle_bin = glob.glob('/Applications/EAGLE*/EAGLE.app/Contents/MacOS/EAGLE')[-1]
    open_bin = '/usr/bin/open'
elif 'linux' == sys.platform:
    eagle_bin = glob.glob('/usr/local/eagle*/bin/eagle')[-1]
    open_bin = '/usr/bin/xdg-open'
elif 'win32' == sys.platform:
    eagle_bin = 'c:/program files/EAGLE*/eagle.exe'
    open_bin = 'start'

# LAYERS dictionary provides mapping between Eagle layers and export layers (as
# used by "eagleexport").
#
# Each export layer consists of one or more Eagle layers and usually
# corresponds to one mask (copper, silkscreen, paste, etc.)
#
# Layer properties:
#
# 'layers' : List of Eagle layers to include on this export layer.
#
# 'pp_id'  : Numerical Eagle layer ID for components placed on this layer. Used
#            when exporting pick&place data.
#
# 'mirror' : Whether to mirror this layer on export.
class Config:
    LAYERS = {
        'topassembly': {
            'layers': ['tPlace', 'tNames', 'tDocu'],
            'pp_id': 1,
        },

        'topsilk': {
            'layers': ['tPlace', 'tNames'],
        },

        'toppaste': {
            'layers': ['tCream'],
        },

        'topmask': {
            'layers': ['tStop'],
        },

        'topcopper': {
            'layers': ['Top', 'Pads', 'Vias'],
        },

        'bottomcopper': {
            'layers': ['Bottom', 'Pads', 'Vias'],
            'mirror': True,
        },

        'bottommask': {
            'layers': ['bStop'],
            'mirror': True,
        },

        'bottompaste': {
            'layers': ['bCream'],
            'mirror': True,
        },

        'bottomsilk': {
            'layers': ['bPlace', 'bNames'],
            'mirror': True,
        },

        'bottomassembly': {
            'layers': ['bPlace', 'bNames', 'bDocu'],
            'mirror': True,
            'pp_id': 16,
        },

        'outline': {
            'layers': ['Milling'],
        },

        'measures': {
            'layers': ['DrillLegend', 'Measures'],
        },

        'drills': {
            'layers': ['Drills', 'Holes'],
        },
    }

# Eagle layer names to always include when exporting documentation formats (e.g. PDF)
#
# These layers are usually used to add dimensions, frames, signatures, etc. to
# all exported pages.
    DOCUMENT_LAYERS = ['Dimension', 'Document']

# Path to Eagle binary to use.
    EAGLE = eagle_bin

# DPI for bitmap exports.
    DPI = 400

# General OS-wide open file utility
    OPEN = open_bin

