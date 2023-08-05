from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from collective.address.behaviors import IAddress
from collective.address.vocabulary import get_pycountry_name
from collective.geolocationbehavior.geolocation import IGeolocatable
import json


class VenueView(BrowserView):

    @property
    def data(self):
        context = self.context
        geo = IGeolocatable(context)
        add = IAddress(context)

        title = safe_unicode(getattr(self.context, 'title', u''))
        description = safe_unicode(getattr(self.context, 'description', u''))
        latitude = geo.geolocation.latitude
        longitude = geo.geolocation.longitude
        geo_json = json.dumps([{
            'lat': latitude,
            'lng': longitude,
            'popup': u'<h3>{0}</h3><p>{1}</p>'.format(title, description)
        }])

        return {
            'title': title,
            'description': description,
            'geopoints': geo_json,
            'latitude': latitude,
            'longitude': longitude,
            'street': add.street,
            'zip_code': add.zip_code,
            'city': add.city,
            'country': get_pycountry_name(add.country) or '',
            'notes': add.notes and add.notes.output or '',
        }
