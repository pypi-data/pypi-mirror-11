# coding=utf-8
"""
"""
from __future__ import absolute_import

from abilian.i18n import _
from abilian.web import nav
from flask import g, Blueprint as BaseBlueprint, abort

from . import security
from .models import Community
from .presenters import CommunityPresenter


class Blueprint(BaseBlueprint):
  """
  Blueprint for community based views.

  It sets g.community and perform access verification for the traversed
  community.
  """
  _BASE_URL_PREFIX = '/communities'
  _ROUTE_PARAM = '<string:community_id>'

  def __init__(self, *args, **kwargs):
    url_prefix = kwargs.get('url_prefix', '')

    if kwargs.pop('set_community_id_prefix', True):
      if (not url_prefix) or url_prefix[0] != '/':
        url_prefix = '/' + url_prefix
      url_prefix = self._ROUTE_PARAM + url_prefix

    if not url_prefix.startswith(self._BASE_URL_PREFIX):
      if (not url_prefix) or url_prefix[0] != '/':
        url_prefix = '/' + url_prefix
      url_prefix = self._BASE_URL_PREFIX + url_prefix

    if url_prefix[-1] == '/':
      url_prefix = url_prefix[:-1]
    kwargs['url_prefix'] = url_prefix

    BaseBlueprint.__init__(self, *args, **kwargs)
    self.url_value_preprocessor(pull_community)
    self.before_request(check_access)


def check_access():
  if hasattr(g, 'community'):
    # communities.index is not inside a community, for example
    security.check_access(g.community)


def pull_community(endpoint, values):
  """
  url_value_preprocessor function
  """
  g.nav['active'] = 'section:communities'
  g.breadcrumb.append(
    nav.BreadcrumbItem(label=_(u'Communities'),
                       url=nav.Endpoint('communities.index')))

  try:
    slug = values.pop('community_id')
    community = Community.query.filter(Community.slug == slug).first()
    if community:
      g.community = CommunityPresenter(community)
      wall_url = nav.Endpoint('wall.index', community_id=community.slug)
      breadcrumb_item = nav.BreadcrumbItem(label=community.name,
                                           url=wall_url)
      g.breadcrumb.append(breadcrumb_item)
    else:
      abort(404)
  except KeyError:
    pass
