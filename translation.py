from collections import defaultdict
import ogr2osm
from ogr2osm.osm_geometries import OsmId, OsmBoundary, OsmNode, OsmWay, OsmRelation

class Translation(ogr2osm.TranslationBase):
  def __init__(self):
    self.code_way_map = defaultdict(list)
    self.code_relation_tags = {}
    self.current_layer_name = None
    self.is_boundary = False
    self.is_parcel = False
    self.is_building = False

  def filter_layer(self, layer):
    self.current_layer_name = layer.GetName()

    self.is_boundary = self.current_layer_name and 'boundary' in self.current_layer_name.lower()
    self.is_parcel = self.current_layer_name and 'parcel' in self.current_layer_name.lower()
    self.is_building = self.current_layer_name and 'building' in self.current_layer_name.lower()

    return layer

  def filter_tags(self, attrs):
    if not attrs:
      return

    tags = {}


    # ---=== |CGT LLC specific tags| ===---

    # Boundary tags

    if self.is_boundary:
      if 'from_date' in attrs:
        tags['custom:from_date'] = attrs['from_date']


      if 'to_date' in attrs:
        tags['custom:to_date'] = attrs['to_date']


      if 'area_m2' in attrs:
        tags['custom:area_m2'] = attrs['area_m2']


      if 'length_m' in attrs:
        tags['custom:perimeter_m'] = attrs['length_m']

    if self.is_parcel:
      if 'from_date' in attrs:
        tags['custom:from_date'] = attrs['from_date']

      if 'to_date' in attrs:
        tags['custom:to_date'] = attrs['to_date']


      if 'area_m2' in attrs:
        tags['custom:area_m2'] = attrs['area_m2']


      if 'length_m' in attrs:
        tags['custom:perimeter_m'] = attrs['length_m']

      # ========

      if 'RGN_CC' in attrs:
        tags['custom:rgn_cc'] = attrs['RGN_CC']

      if 'CMM_CC' in attrs:
        tags['custom:cmm_cc'] = attrs['CMM_CC']

      if 'BLK_CC' in attrs:
        tags['custom:blk_cc'] = attrs['BLK_CC']

      if 'PRC_CC' in attrs:
        tags['custom:prc_cc'] = attrs['PRC_CC']

      if 'Code' in attrs:
        tags['custom:code'] = attrs['Code']


    if self.is_building:
      if 'from_date' in attrs:
        tags['custom:from_date'] = attrs['from_date']

      if 'to_date' in attrs:
        tags['custom:to_date'] = attrs['to_date']

      if 'area_m2' in attrs:
        tags['custom:area_m2'] = attrs['area_m2']

      if 'length_m' in attrs:
        tags['custom:perimeter_m'] = attrs['length_m']

      # ========

      if 'RGN_CC' in attrs:
        tags['custom:rgn_cc'] = attrs['RGN_CC']

      if 'CMM_CC' in attrs:
        tags['custom:cmm_cc'] = attrs['CMM_CC']

      if 'BLK_CC' in attrs:
        tags['custom:blk_cc'] = attrs['BLK_CC']

      if 'PRC_CC' in attrs:
        tags['custom:prc_cc'] = attrs['PRC_CC']

      if 'BLD_CC' in attrs:
        tags['custom:bld_cc'] = attrs['BLD_CC']

      if 'code' in attrs:
        tags['custom:code'] = attrs['code']

    return tags

  def process_feature_post(self, osmgeometry, ogrfeature, ogrgeometry):
    if osmgeometry is None:
      return

    if not isinstance(osmgeometry, OsmWay):
      return

    print(f"===============================")
    print(f"osmgeometry: {osmgeometry.tags}")
    print(f"===============================")

    field_name = "Code" if self.is_parcel else "code"
    code = ogrfeature.GetField(field_name)

    if code:
      code = str(code)
      self.code_way_map[code].append(osmgeometry)

      if code not in self.code_relation_tags:
        self.code_relation_tags[code] = {
          'type': 'multipolygon',
          'custom:code': code,
        }

  def process_output(self, osmnodes, osmways, osmrelations):
    for code, ways in self.code_way_map.items():
      members = []

      for way in ways:
        members.append((way, 'outer'))

      relation = OsmRelation(tags = self.code_relation_tags.get(code, {}))
      relation.members = members

      osmrelations.append(relation)
