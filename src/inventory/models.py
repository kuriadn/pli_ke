from django.contrib.gis.db import models
from django.core.validators import *
from django.utils import timezone

class BeaconType(models.Model):
  bcntype = models.CharField(max_length=10, verbose_name='Beacon Type', primary_key=True)
  desc = models.CharField(max_length=30, verbose_name='Description')

  class Meta:
  	unique_together=('bcntype', 'desc')
  	ordering=['bcntype']

  def __str__(self):
  	return str(self.bcntype)

class Datum(models.Model):
  CHOICES = (('horizontal', 'Horizontal'),
  	('vertical', 'Vertical'))
  datum = models.CharField(max_length=10, primary_key=True)
  dtype = models.CharField(max_length=10, choices=CHOICES, verbose_name='Datum Type')
  desc = models.CharField(max_length=50, verbose_name='Description')

  class Meta:
  	unique_together=('datum', 'dtype')
  	ordering=['datum']

  def __str__(self):
  	return self.datum + ' - ' + self.dtype 

class Beacon(models.Model):
  beaconid = models.CharField(max_length=15, verbose_name='Beacon Id.', primary_key=True)
  bcntype = models.ForeignKey(BeaconType, on_delete=models.CASCADE, verbose_name='Beacon Type')
  xcoord = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='X Coordinate', null=True, blank=True)
  ycoord = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Y Coordinate', null=True, blank=True)
  zcoord = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Z Coordinate', null=True, blank=True)
  vdatum = models.CharField(max_length=10, verbose_name='Vertical Datum', default='MSL')
  hdatum = models.CharField(max_length=10, verbose_name='Horizontal Datum', default='Arc1960')
  bcngeom = models.PointField(srid=32737, verbose_name='Geometry', null=True, blank=True)

  class Meta:
  	unique_together = ('beaconid', 'bcntype')
  	ordering = ['beaconid']

  def __str__(self):
  	return str(self.beaconid) + ' - ' + str(self.bcntype)

class Boundary(models.Model):
  bdryid = models.CharField(max_length=10, verbose_name='Boundary Id.', primary_key=True)
  datefixed = models.DateField(verbose_name='Date Fixed', default=timezone.now)
  bearing = models.CharField(max_length=24, null=True, blank=True)
  distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
  bdgeom = models.LineStringField(srid=32737, verbose_name='Geometry', null=True, blank=True)

  class Meta:
    ordering=['bdryid']
    verbose_name_plural = 'Boundaries'

  def __str__(self):
    return self.bdryid + ' - ' + str(self.datefixed)

class BoundaryBeacon(models.Model):
  boundary = models.ForeignKey(Boundary, on_delete=models.CASCADE, verbose_name='Boundary')
  beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE, verbose_name='Beacon')
  order = models.IntegerField()

  class Meta:
    unique_together = ('beacon', 'boundary') 
    ordering = ['boundary', 'order']

  def __str__(self):
    return str(self.boundary) + ' -> ' + str(self.beacon)

class Party(models.Model):
  partyid = models.CharField(max_length=10, verbose_name='Identifier', primary_key=True)
  pname = models.CharField(max_length=30, verbose_name='Name')
  theme = models.CharField(max_length=100)

  class Meta:
    ordering = ['partyid']
    verbose_name_plural = 'parties'

  def __str__(self):
    return self.name 

class Code(models.Model):
  code = models.CharField(max_length=5, verbose_name='Post Code', primary_key=True, 
    validators=[RegexValidator(regex=r'^[0-9]{5}$')])
  post = models.CharField(max_length=15, verbose_name='Post Office')
  town = models.CharField(max_length=15)

  class Meta:
    ordering = ['code']

  def __str__(self):
    return self.code + ' - ' + self.town 

class Address(models.Model):
  party = models.OneToOneField(Party, on_delete=models.CASCADE, primary_key=True)
  phone = models.CharField(max_length=14, verbose_name='Phone No.')
  physical = models.CharField(max_length=50, verbose_name='Physical Address')
  postal = models.CharField(max_length=20, verbose_name='Postal Address')
  code = models.ForeignKey(Code, on_delete=models.CASCADE, verbose_name='Post Code')

  class Meta:
    ordering = ['party']
    verbose_name_plural = 'Addresses'

  def __str__(self):
    return self.party + ': ' + self.postal + '-' + self.code.code + ', ' + self.code.post

class Specialization(models.Model):
  specid = models.CharField(max_length=4, verbose_name='Speicalization Id.', primary_key=True)
  desc = models.CharField(max_length=20, verbose_name='Description')

  class Meta:
    ordering = ['specid', 'desc']

  def __str__(self):
    return self.desc 

class Professional(models.Model):
  profid = models.CharField(max_length=14, verbose_name='Professional Id.', primary_key=True)
  regno = models.CharField(max_length=14, verbose_name='Registration No.')
  name = models.CharField(max_length=50)
  spec = models.ForeignKey(Specialization, on_delete=models.CASCADE)
  address = models.ForeignKey(Address, on_delete=models.CASCADE)

  class Meta:
    ordering = ['spec', 'profid']

  def __str__(self):
    return self.name + ' - ' + self.spec

class Landuse(models.Model):
  luid = models.CharField(max_length=10, verbose_name='Land use Id.', primary_key=True)
  user = models.CharField(max_length=15, verbose_name='Land use Type')

  class Meta:
    ordering = ['luid']

  def __str__(self):
    return self.user

class Source(models.Model):
  sid = models.CharField(max_length=15, verbose_name='Source Id.', primary_key=True)
  mapdoc = models.RasterField(srid=32737, verbose_name='Map')
  locality = models.CharField(max_length=40)
  scale = models.CharField(max_length=15)
  date_prep = models.DateField(default=timezone.now, verbose_name='Date Prepared')
  surveyor = models.ForeignKey(Professional, on_delete=models.CASCADE)

  class Meta:
    abstract = True
    ordering = ['sid']

  def __str__(self):
    return self.sid + ' - ' + self.locality

class FixedBoundarySource(Source):
  accuracy = models.DecimalField(max_digits=5, decimal_places=4)

  class Meta:
    abstract = True

class GeneralBoundarySource(Source):
  CHOICES = (
    ('mutation', 'Mutation'),
    ('enlargement', 'Enlargement')
    )
  src = models.CharField(max_length=30, choices=CHOICES, verbose_name='Source Document Type')

  class Meta:
    abstract = True

class SurveyPlan(FixedBoundarySource):
  plan = models.CharField(max_length=50, verbose_name='Survey Plan No.')
  compno = models.CharField(max_length=30, verbose_name='Computation File No.')
  pdp = models.CharField(max_length=30, verbose_name='Part Development Plan No.')

  def __str__(self):
    return self.sid + ' - ' + self.plan 

class PID(GeneralBoundarySource):
  diagram = models.CharField(max_length=20)
  class Meta:
    verbose_name = 'PID'
    verbose_name_plural = 'PIDs'

class RIM(GeneralBoundarySource):
  sheet = models.CharField(max_length=20)

  class Meta:
    verbose_name = 'RIM'
    verbose_name_plural = 'RIMs'

class SpatialUnit(models.Model):
  sunit = models.CharField(max_length=10, verbose_name='Spatial Unit', primary_key=True)
  srid = models.IntegerField()
  sutype = models.CharField(max_length=10, verbose_name='Spatial Unit Type')

  class Meta:
    ordering = ['sunit']

  def __str__(self):
    return self.sunit

class SourceMapPlan(models.Model):
  sunit = models.OneToOneField(SpatialUnit, on_delete=models.CASCADE ,verbose_name='Spatial Unit Id.', primary_key=True)
  plan = models.ForeignKey(SurveyPlan, on_delete=models.CASCADE, verbose_name='Survey Plan')

  class Meta:
    ordering = ['sunit']
    verbose_name = 'Source Plan'
    verbose_name_plural = 'Source Plans'

  def __str__(self):
    return self.sunit 

class SourceMapRIM(models.Model):
  sunit = models.OneToOneField(SpatialUnit, on_delete=models.CASCADE ,verbose_name='Spatial Unit Id.', primary_key=True)
  rim = models.ForeignKey(RIM, on_delete=models.CASCADE, verbose_name='RIM')

  class Meta:
    ordering = ['sunit']
    verbose_name = 'Source RIM'
    verbose_name_plural = 'Source RIMs'

  def __str__(self):
    return self.sunit 

class SourceMapPID(models.Model):
  sunit = models.OneToOneField(SpatialUnit, on_delete=models.CASCADE ,verbose_name='Spatial Unit Id.', primary_key=True)
  pid = models.ForeignKey(PID, on_delete=models.CASCADE, verbose_name='PID')

  class Meta:
    ordering = ['sunit']
    verbose_name = 'Source PID'
    verbose_name_plural = 'Source PIDs'

  def __str__(self):
    return self.sunit 


class Parcel(models.Model):
  parcelid = models.CharField(max_length=15, verbose_name='Parcel Id.', primary_key=True)
  party = models.ForeignKey(Party, on_delete=models.CASCADE, null=True, blank=True )
  locality = models.CharField(max_length=15, null=True, blank=True)
  sunit = models.ForeignKey(SpatialUnit, on_delete=models.CASCADE, verbose_name='Spatial Unit', null=True, blank=True)
  origin = models.TextField(max_length=200, null=True, blank=True)
  pgeom = models.MultiPolygonField(srid=32737, verbose_name='Geometry', null=True, blank=True)

  class Meta:
    ordering = ['parcelid', 'locality']

  def __str__(self):
    return self.parcelid

class ParcelBoundary(models.Model):
  parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
  boundary = models.ForeignKey(Boundary, on_delete=models.CASCADE)
  order = models.IntegerField()

  class Meta:
    ordering = ['parcel', 'order']
    verbose_name = 'Parcel Boundary'
    verbose_name_plural = 'Parcel Boundaries'

  def __str__(self):
    return str(self.parcel) + ' => ' + str(self.boundary) 

class ParcelUse(models.Model):
  use = models.OneToOneField(Landuse, on_delete=models.CASCADE)
  parcel = models.OneToOneField(Parcel, on_delete=models.CASCADE)
  status = models.CharField(max_length=10, verbose_name='Status of Use')
  start = models.DateField(verbose_name='Start Date', default=timezone.now)
  end = models.DateField(verbose_name='End Date', default=timezone.now)
  planner = models.ForeignKey(Professional, on_delete=models.CASCADE)

  class Meta:
    ordering = ['use', 'parcel', 'start']

  def __str__(self):
    return self.parcel.parcelid + ' - ' + self.use.user

class Valuation(models.Model):
  valid = models.CharField(max_length=10, verbose_name='Valuation Id.', primary_key=True)
  bookno = models.CharField(max_length=15, verbose_name='Book No.')
  parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
  value = models.DecimalField(max_digits=10, decimal_places=2)
  valuer = models.ForeignKey(Professional, on_delete=models.CASCADE)

  class Meta:
    ordering = ['valid']

  def __str__(self):
    return self.valid + ' - ' + self.parcel

class RRRR(models.Model):
  rid = models.CharField(max_length=20, verbose_name='RRR Id.', primary_key=True)
  date_lodged = models.DateField(default=timezone.now, verbose_name='Date Lodged')

  class Meta:
    abstract = True
    ordering = ['rid']

  def __str__(self):
    return self.rid + ' - ' + self.date_lodged

class Restriction(RRRR):
  restriction = models.CharField(max_length=50)

class Responsibility(RRRR):
  Responsibility = models.CharField(max_length=50)

  class Meta:
    verbose_name_plural = 'Responsibilities'

class Right(RRRR):
  right = models.CharField(max_length=50)

class Register(models.Model):
  regid = models.CharField(max_length=15, verbose_name='Register Id', primary_key=True)
  parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
  regtype = models.CharField(max_length=15, verbose_name='Type of Registration')
  regdate = models.DateField(default=timezone.now, verbose_name='Date of Registration')
  juris = models.CharField(max_length=20, verbose_name='Applicable Jurisdiction')

  class Meta:
    ordering = ['regid']

  def __str__(self):
    return self.regid + ' - ' + self.parcel

class RightRegister(models.Model):
  register = models.ForeignKey(Register, on_delete=models.CASCADE, verbose_name='Register') 
  right = models.ForeignKey(Right, on_delete=models.CASCADE, verbose_name='Rights')

  class Meta:
    ordering = ['register']

  def __str__(self):
    return self.register + ' - ' + self.right

class RestrictionRegister(models.Model):
  register = models.ForeignKey(Register, on_delete=models.CASCADE, verbose_name='Register') 
  rest = models.ForeignKey(Restriction, on_delete=models.CASCADE, verbose_name='Restriction')

  class Meta:
    ordering = ['register']

  def __str__(self):
    return self.register + ' - ' + self.rest
    
class ResponsibilityRegister(models.Model):
  register = models.ForeignKey(Register, on_delete=models.CASCADE, verbose_name='Register') 
  resp = models.ForeignKey(Responsibility, on_delete=models.CASCADE, verbose_name='Responsibility')

  class Meta:
    ordering = ['register']

  def __str__(self):
    return self.register + ' - ' + self.rest
    