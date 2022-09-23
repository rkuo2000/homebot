from pykml import parser
import sys
import re

_name = []
_coor = []
kml_file = sys.argv[1]

with open(kml_file) as f:
    doc = parser.parse(f).getroot()
    for e in doc.Document.Folder.Placemark:
        _name.append(e.name)
        coor = e.Point.coordinates.text.split(',')
        _coor.append(coor)
    print(_name[0])
    print(_coor[0])
# Point
    for p in doc.Document.Folder.Folder.Placemark:
        if p.name.text!='Route':
            print(p.name)
            coor = p.Point.coordinates.text.split(',')
            print(coor)
# Route
    for r in doc.Document.Folder.Folder.Placemark:
        if r.name.text=='Route':
            print('Route')
            coor = re.sub('\\n','',r.LineString.coordinates.text)
            coor = re.sub('\\t','',coor)
            cord = coor.split(' ')
            for c in cord:
                cc = c.split(',')
                if cc[0]!='':
                    print(c.split(','))
    print(_name[1])
    print(_coor[1])
