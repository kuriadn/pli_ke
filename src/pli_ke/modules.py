from inventory.models import *
from django.db import connection
from pli_ke.point import *
from pli_ke.angle import *
from pli_ke.traverse import * 

def runsql(sql):
  with connection.cursor() as cursor:
    cursor.execute(sql)

def getcoordinate(sql):
  coord = 0
  with connection.cursor() as cursor:
    cursor.execute(sql)
    coord = cursor.fetchone()
    if 'NoneType' not in str(type(coord[0])):
      coord = round(coord[0], 2)
    else: coord = 0.00
    print (coord)
  return coord

def beacon_geometry(bid, srid):
  qry = Beacon.objects.filter(beaconid=bid)
  if len(qry) > 0:
    pt = Point(qry[0].xcoord, qry[0].ycoord)
    bcngeom = "ST_GeomFromText('Point({0})', {1})".format(pt.toString(), srid)
    sql = "update inventory_beacon set bcngeom = " + bcngeom + " where beaconid = '" + str(bid) + "'"
    runsql(sql)
  else:
    print ('No Beacon found with id: {0}'.format(bid))

def generate_coordinates(bid):
  qry = Beacon.objects.filter(beaconid=bid)
  for q in qry:
    xsql = "select st_x(bcngeom) from inventory_beacon where beaconid='" + bid + "'"
    ysql = "select st_y(bcngeom) from inventory_beacon where beaconid='" + bid + "'"
    zsql = "select st_z(bcngeom) from inventory_beacon where beaconid='" + bid + "'"
    q.xcoord = getcoordinate(xsql)
    q.ycoord = getcoordinate(ysql)
    q.zcoord = getcoordinate(zsql)
    q.save()

def boundary_geometry(bdryid, srid):
  qry = BoundaryBeacon.objects.filter(boundary=bdryid).order_by('order')
  if len(qry) > 0:
    pts = ''
    for q in qry:
      pt = Point(q.beacon.xcoord, q.beacon.ycoord)
      pts += '{0}, '.format(pt.toString())
    pts = pts[0: len(pts) - 2]
    bdrygeom = "ST_GeomFromText('Linestring(" + pts + ")', " + str(srid) + ")"
    sql = "update inventory_boundary set bdgeom = " + bdrygeom + " where bdryid = '" + qry[0].boundary.bdryid + "'"
    runsql(sql)
  else: print ('No boundary beacons found for boundary with id: {0}'.format(bdryid))

def reverse_beacons(bdry):
  bqry = BoundaryBeacon.objects.filter(boundary=bdry).order_by('-order')
  beacons = []
  for bdrybcn in bqry:
#    print (bdrybcn) 
    beacons.append(bdrybcn.beacon) 
  return beacons

def forward_beacons(bdry):
  bqry = BoundaryBeacon.objects.filter(boundary=bdry).order_by('order')
  beacons = []
  for bdrybcn in bqry:
#    print (bdrybcn) 
    beacons.append(bdrybcn.beacon) 
  return beacons

def parcel_geometry(parcel, srid):
  qry = ParcelBoundary.objects.filter(parcel=parcel).order_by('order')
  parcelbeacons = []
  if len(qry) > 0:
    lastbcns = forward_beacons(qry[0].boundary)
    secbcns = forward_beacons(qry[1].boundary)
    if lastbcns[len(lastbcns) - 1] != secbcns[0]: lastbcns = reverse_beacons(qry[0].boundary)
    parcelbeacons.append(lastbcns[0])
#    print(lastbcns)
    for i in range(len(qry) - 1):
      bqrybcns = forward_beacons(qry[i + 1].boundary)
      if lastbcns[len(lastbcns) - 1] != bqrybcns[0]: bqrybcns = reverse_beacons(qry[i + 1].boundary)
      parcelbeacons.append(bqrybcns[0])
      lastbcns = bqrybcns
#      print (bqrybcns)
    parcelbeacons.append(lastbcns[1])
#    print(parcelbeacons)
    pts = ''
    for bcn in parcelbeacons:
      pt = Point(bcn.xcoord, bcn.ycoord)
      pts += '{0}, '.format(pt.toString())
    pts = pts[0: len(pts) - 2]
    parcgeom = "ST_GeomFromText('MultiPolygon(((" + pts + ")))', " + str(srid) + ")"
    sql = "update inventory_parcel set pgeom = " + parcgeom + " where parcelid = '" + parcel.parcelid + "'"
#    print (sql)
    runsql(sql)
   
def generate_bcn_coords():
  beacons = Beacon.objects.filter(xcoord__isnull=True, ycoord__isnull=True, zcoord__isnull=True)
  for beacon in beacons:
    generate_coordinates(beacon.beaconid)

def generate_bcn_geom():
  beacons = Beacon.objects.filter(bcngeom__isnull=True)
  for beacon in beacons:
    beacon_geometry(beacon.beaconid, 32737)

def generate_bdry_geom():
  boundaries = Boundary.objects.filter(bdgeom__isnull=True)
  for bdry in boundaries:
    boundary_geometry(bdry.bdryid, 32737)

def generate_parcel_geom():
  pqry = Parcel.objects.filter(pgeom__isnull=True)
  for parcel in pqry:
    parcel_geometry(parcel, 32737)

def generate_all_geometries():
  generate_bcn_geom()
  generate_bdry_geom()
  generate_parcel_geom()

def dist_bearing(bdry):
  qry = BoundaryBeacon.objects.filter(boundary=bdry).order_by('order')
  if len(qry) > 0:
    pts = []
    for q in qry:
      pts.append(Point(q.beacon.xcoord, q.beacon.ycoord))
    st = pts[0]
    en = pts[len(qry) - 1]
    dx = en.x - st.x
    dy = en.y - st.y 
    dist = distance(dx, dy)
    bear = bearing(dx, dy)
    bdry.distance = dist
    bdry.bearing = bear
    bdry.save()

def generate_dist_bear():
  qry = Boundary.objects.filter(bearing__isnull=True, distance__isnull=True)
  for bdry in qry:
    dist_bearing(bdry)