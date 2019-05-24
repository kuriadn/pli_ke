from django.contrib.gis import admin
from django.contrib.gis.geos import GEOSGeometry 
from .models import *


class BeaconTypeAdmin(admin.ModelAdmin):
  fields = ('bcntype', 'desc',)
  list_display = ('bcntype', 'desc',)
  list_filter = ('bcntype', 'desc',)
  search_fields = ('bcntype', 'desc',)
  list_per_page = 10

class DatumAdmin(admin.ModelAdmin):
  fields = ('datum', 'dtype', 'desc',)
  list_display = ('datum', 'dtype', 'desc',)
  list_filter = ('datum', 'dtype', 'desc',)
  search_fields = ('datum', 'dtype', 'desc',)
  list_per_page = 10

class BeaconAdmin(admin.OSMGeoAdmin):
  model = Beacon
  fields = ('beaconid', 'bcntype', 'xcoord', 'ycoord', 'zcoord', 'vdatum', 'hdatum', 'bcngeom',)
  list_display = ('beaconid', 'bcntype', 'xcoord', 'ycoord', 'zcoord', 'vdatum', 'hdatum',)
  list_filter = ('beaconid', 'bcntype', 'xcoord', 'ycoord', 'zcoord', 'vdatum', 'hdatum',)
  search_fields = ('beaconid', 'bcntype', 'xcoord', 'ycoord', 'zcoord', 'vdatum', 'hdatum',)
  list_per_page = 10

class BoundaryAdmin(admin.OSMGeoAdmin):
  model = Boundary 
  fields = ('bdryid', 'datefixed', 'bdgeom',)
  list_display = ('bdryid', 'datefixed',)
  list_filter = ('bdryid', 'datefixed',)
  search_fields = ('bdryid', 'datefixed',)
  list_per_page = 10

class BoundaryBeaconAdmin(admin.ModelAdmin):
  fields = ( 'boundary', 'beacon', 'order',)
  list_display = ('boundary', 'beacon', 'order',)
  list_filter = ('boundary', 'beacon', 'order',)
  search_fields = ('boundary', 'beacon', 'order',)
  list_per_page = 10
  
class PartyAdmin(admin.ModelAdmin):
  fields = ('partyid', 'pname', 'theme',)
  list_display = ('partyid', 'pname', 'theme',)
  list_filter = ('partyid', 'pname', 'theme',)
  search_fields = ('partyid', 'pname', 'theme',)
  list_per_page = 10
  
class CodeAdmin(admin.ModelAdmin):
  fields = ('code', 'post', 'town',)
  list_display = ('code', 'post', 'town',)
  list_filter = ('code', 'post', 'town',)
  search_fields = ('code', 'post', 'town',)
  list_per_page = 10

class AddressAdmin(admin.ModelAdmin):
  fields = ('party', 'phone', 'physical', 'postal', 'code',)
  list_display = ('party', 'phone', 'physical', 'postal', 'code',)
  list_filter = ('party', 'phone', 'physical', 'postal', 'code',)
  search_fields = ('party', 'phone', 'physical', 'postal', 'code',)
  list_per_page = 10

class SpecializationAdmin(admin.ModelAdmin):
  fields = ('specid', 'desc',)
  list_display = ('specid', 'desc',)
  list_filter = ('specid', 'desc',)
  search_fields = ('specid', 'desc',)
  list_per_page = 10

class ProfessionalAdmin(admin.ModelAdmin):
  fields = ('profid', 'regno', 'name', 'spec', 'address',)
  list_display = ('profid', 'regno', 'name', 'spec', 'address',)
  list_filter = ('profid', 'regno', 'name', 'spec', 'address',)
  search_fields = ('profid', 'regno', 'name', 'spec', 'address',)
  list_per_page = 10
  
class LanduseAdmin(admin.ModelAdmin):
  fields = ('luid', 'user',)
  list_display = ('luid', 'user',)
  list_filter = ('luid', 'user',)
  search_fields = ('luid', 'user',)
  list_per_page = 10

class SurveyPlanAdmin(admin.ModelAdmin):
  fields = ('sid', 'mapdoc', 'locality', 'scale', 'date_prep', 'accuracy', 'plan', 'compno', 'surveyor', 'pdp',)
  list_display = ('sid', 'mapdoc', 'locality', 'scale', 'date_prep', 'accuracy', 'plan', 'compno', 'surveyor', 'pdp',)
  list_filter = ('sid', 'locality', 'scale', 'date_prep', 'surveyor',)
  search_fields = ('sid', 'locality', 'scale', 'date_prep', 'surveyor',)
  list_per_page = 10

class PIDAdmin(admin.ModelAdmin):
  fields = ('sid', 'mapdoc', 'locality', 'scale', 'date_prep', 'src', 'diagram',)
  list_display = ('sid', 'mapdoc', 'locality', 'scale', 'date_prep', 'src', 'diagram',)
  list_filter = ('sid', 'locality', 'scale', 'date_prep', 'src',)
  search_fields = ('sid', 'locality', 'scale', 'date_prep', 'src',)
  list_per_page = 10
  
class RIMAdmin(admin.ModelAdmin):
  fields = ('sid', 'mapdoc', 'locality', 'scale', 'date_prep', 'src', 'sheet',)
  list_display = ('sid', 'mapdoc', 'locality', 'scale', 'date_prep', 'src', 'sheet',)
  list_filter = ('sid', 'locality', 'scale', 'date_prep', 'src',)
  search_fields = ('sid', 'locality', 'scale', 'date_prep', 'src',)
  list_per_page = 10
  
class SpatialUnitAdmin(admin.ModelAdmin):
  fields = ('sunit', 'srid', 'sutype',)
  list_display = ('sunit', 'srid', 'sutype',)
  list_filter = ('sunit', 'srid', 'sutype',)
  search_fields = ('sunit', 'srid', 'sutype',)
  list_per_page = 10

class SourceMapPlanAdmin(admin.ModelAdmin):
  fields = ('sunit', 'plan',)
  list_display = ('sunit', 'plan',)
  list_filter = ('sunit', 'plan',)
  search_fields = ('sunit', 'plan',)
  list_per_page = 10

class SourceMapRIMAdmin(admin.ModelAdmin):
  fields = ('sunit', 'rim',)
  list_display = ('sunit', 'rim',)
  list_filter = ('sunit', 'rim',)
  search_fields = ('sunit', 'rim',)
  list_per_page = 10

class SourceMapPIDAdmin(admin.ModelAdmin):
  fields = ('sunit', 'pid',)
  list_display = ('sunit', 'pid',)
  list_filter = ('sunit', 'pid',)
  search_fields = ('sunit', 'pid',)
  list_per_page = 10

class ParcelAdmin(admin.OSMGeoAdmin):
  model = Parcel
  fields = ('parcelid', 'party', 'locality', 'sunit', 'pgeom',)
  list_display = ('parcelid', 'party', 'locality', 'sunit',)
  list_filter = ('parcelid', 'party', 'locality', 'sunit',)
  search_fields = ('parcelid', 'party', 'locality', 'sunit',)
  list_per_page = 10

class ParcelBoundaryAdmin(admin.ModelAdmin):
  fields = ('parcel', 'boundary', 'order',)
  list_display = ('parcel', 'boundary', 'order',)
  list_filter = ('parcel', 'boundary', 'order',)
  search_fields = ('parcel', 'boundary', 'order',)
  list_per_page = 10

class ParcelUseAdmin(admin.ModelAdmin):
  fields = ('use', 'parcel', 'status', 'start', 'end',)
  list_display = ('use', 'parcel', 'status', 'start', 'end',)
  list_filter = ('use', 'parcel', 'status', 'start', 'end',)
  search_fields = ('use', 'parcel', 'status', 'start', 'end',)
  list_per_page = 10

class ValuationAdmin(admin.ModelAdmin):
  fields = ('valid', 'bookno', 'parcel', 'value', 'valuer',)
  list_display = ('valid', 'bookno', 'parcel', 'value', 'valuer',)
  list_filter = ('valid', 'bookno', 'parcel', 'value', 'valuer',)
  search_fields = ('valid', 'bookno', 'parcel', 'value', 'valuer',)
  list_per_page = 10

class RestrictionAdmin(admin.ModelAdmin):
  fields = ('rid', 'restriction', 'date_lodged',)
  list_display = ('rid', 'restriction', 'date_lodged',)
  list_filter = ('rid', 'restriction', 'date_lodged',)
  search_fields = ('rid', 'restriction', 'date_lodged',)
  list_per_page = 10

class RightAdmin(admin.ModelAdmin):
  fields = ('rid', 'right', 'date_lodged',)
  list_display = ('rid', 'right', 'date_lodged',)
  list_filter = ('rid', 'right', 'date_lodged',)
  search_fields = ('rid', 'right', 'date_lodged',)
  list_per_page = 10

class ResponsibilityAdmin(admin.ModelAdmin):
  fields = ('rid', 'Responsibility', 'date_lodged',)
  list_display = ('rid', 'Responsibility', 'date_lodged',)
  list_filter = ('rid', 'Responsibility', 'date_lodged',)
  search_fields = ('rid', 'Responsibility', 'date_lodged',)
  list_per_page = 10

class RegisterAdmin(admin.ModelAdmin):
  fields = ('regid', 'parcel', 'regtype', 'regdate', 'juris',)
  list_display = ('regid', 'parcel', 'regtype', 'regdate', 'juris',)
  list_filter = ('regid', 'parcel', 'regtype', 'regdate', 'juris',)
  search_fields = ('regid', 'parcel', 'regtype', 'regdate', 'juris',)
  list_per_page = 10

class RightRegisterAdmin(admin.ModelAdmin):
  fields = ('register', 'right',)
  list_display = ('register', 'right',)
  list_filter = ('register', 'right',)
  search_fields = ('register', 'right',)
  list_per_page = 10

class RestrictionRegisterAdmin(admin.ModelAdmin):
  fields = ('register', 'rest',)
  list_display = ('register', 'rest',)
  list_filter = ('register', 'rest',)
  search_fields = ('register', 'rest',)
  list_per_page = 10

class ResponsibilityRegisterAdmin(admin.ModelAdmin):
  fields = ('register', 'resp',)
  list_display = ('register', 'resp',)
  list_filter = ('register', 'resp',)
  search_fields = ('register', 'resp',)
  list_per_page = 10

admin.site.register(BeaconType, BeaconTypeAdmin)
admin.site.register(Datum, DatumAdmin)
admin.site.register(Beacon, BeaconAdmin)
admin.site.register(Boundary, BoundaryAdmin)
admin.site.register(BoundaryBeacon, BoundaryBeaconAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Professional, ProfessionalAdmin)
admin.site.register(Landuse, LanduseAdmin)
admin.site.register(SurveyPlan, SurveyPlanAdmin)
admin.site.register(PID, PIDAdmin)
admin.site.register(RIM, RIMAdmin)
admin.site.register(SpatialUnit, SpatialUnitAdmin)
admin.site.register(SourceMapPlan, SourceMapPlanAdmin)
admin.site.register(SourceMapRIM, SourceMapRIMAdmin)
admin.site.register(SourceMapPID, SourceMapPIDAdmin)
admin.site.register(Parcel, ParcelAdmin)
admin.site.register(ParcelUse, ParcelUseAdmin)
admin.site.register(ParcelBoundary, ParcelBoundaryAdmin)
admin.site.register(Valuation, ValuationAdmin)
admin.site.register(Right, RightAdmin)
admin.site.register(Restriction, RestrictionAdmin)
admin.site.register(Responsibility, ResponsibilityAdmin)
admin.site.register(Register, RegisterAdmin)
admin.site.register(RightRegister, RightRegisterAdmin)
admin.site.register(ResponsibilityRegister, ResponsibilityRegisterAdmin)
admin.site.register(RestrictionRegister, RestrictionRegisterAdmin)
