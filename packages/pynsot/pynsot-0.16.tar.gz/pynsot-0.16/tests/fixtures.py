#!/usr/bin/env python

"""
Make dummy data and fixtures and stuff.
"""

import collections
import json
import hashlib
import logging
import pytest
import random
import socket
import struct
from pynsot import client
try:
    import faker
except ImportError:
    print "The 'fake-factory' module is required! (Hint: pip install fake-factory)"
    raise


log = logging.getLogger(__name__)

# Constants and stuff
fake = faker.Factory.create()

# API URL to use for testing.
API_URL = 'http://localhost:8990/api'

#############
# Responses #
#############
# API responses that we're using for request/resposne mocking.
# When authenticating against API
AUTH_RESPONSE = {
    'status':'ok',
    'data': {'auth_token': 'bogus_token'}
}

# When retrieving Sites.
SITES_RESPONSE = {u'data': {u'limit': None,
  u'offset': 0,
  u'sites': [{u'description': u'Production networks and devices.',
    u'id': 1,
    u'name': u'Production'}],
  u'total': 1},
 u'status': u'ok'}

# When retrieving Devices.
DEVICES_RESPONSE = {u'data': {u'devices': [
    {u'attributes': {'owner': 'jathan'}, u'hostname': u'foo-bar1', u'id': 1, u'site_id': 1},
    {u'attributes': {'owner': 'jathan'}, u'hostname': u'foo-bar2', u'id': 2, u'site_id': 1}
    ],
  u'limit': None,
  u'offset': 0,
  u'total': 2},
 u'status': u'ok'}

DEVICE_RETRIEVE = {u'data': {u'device': {u'attributes': {
   u'owner': u'jathan'},
   u'hostname': u'foo-bar1',
   u'id': 1,
   u'site_id': 1}},
 u'status': u'ok'}

DEVICE_UPDATE = {u'data': {u'device': {u'attributes': {u'monitored': u'',
   u'owner': u'jathan'},
   u'hostname': u'foo-bar1',
   u'id': 1,
   u'site_id': 1}},
 u'status': u'ok'}

# Networks
NETWORK_CREATE = {'data': {'network': {'attributes': {'owner': 'jathan'},
   'id': 1,
   'ip_version': '4',
   'is_ip': False,
   'network_address': '10.0.0.0',
   'parent_id': None,
   'prefix_length': 8,
   'site_id': 1}},
 'status': 'ok'}

NETWORK_RETRIEVE = {u'data': {u'network': {u'attributes': {u'owner': u'jathan'},
   u'id': 1,
   u'ip_version': u'4',
   u'is_ip': False,
   u'network_address': u'10.0.0.0',
   u'parent_id': None,
   u'prefix_length': 8,
   u'site_id': 1}},
 u'status': u'ok'}

NETWORK_UPDATE = {u'data': {u'network': {u'attributes': {u'foo': u'bar', u'owner': u'jathan'},
   u'id': 1,
   u'ip_version': u'4',
   u'is_ip': False,
   u'network_address': u'10.0.0.0',
   u'parent_id': None,
   u'prefix_length': 8,
   u'site_id': 1}},
 u'status': u'ok'}


NETWORKS_RESPONSE = {u'data': {u'limit': None,
  u'networks': [
   {u'attributes': {u'owner': u'jathan'},
    u'id': 1,
    u'ip_version': u'4',
    u'is_ip': False,
    u'network_address': u'10.0.0.0',
    u'parent_id': None,
    u'prefix_length': 8,
    u'site_id': 1},
   {u'attributes': {u'owner': u'jathan'},
    u'id': 2,
    u'ip_version': u'4',
    u'is_ip': False,
    u'network_address': u'10.0.0.0',
    u'parent_id': 1,
    u'prefix_length': 24,
    u'site_id': 1}],
  u'offset': 0,
  u'total': 2},
 u'status': u'ok'}

# When retrieving Attributes.
ATTRIBUTE_CREATE = {u'data': {u'attribute': {u'constraints': {u'allow_empty': False,
    u'pattern': u'',
    u'valid_values': []},
   u'description': u'',
   u'display': False,
   u'id': 3,
   u'multi': True,
   u'name': u'multi',
   u'required': False,
   u'resource_name': u'Device',
   u'site_id': 1}},
 u'status': u'ok'}

ATTRIBUTES_RESPONSE = {u'data': {u'attributes': [{u'constraints': {u'allow_empty': True,
     u'pattern': u'',
     u'valid_values': []},
    u'description': u'',
    u'display': False,
    u'id': 2,
    u'multi': False,
    u'name': u'monitored',
    u'required': False,
    u'resource_name': u'Device',
    u'site_id': 1},
   {u'constraints': {u'allow_empty': False,
     u'pattern': u'',
     u'valid_values': []},
    u'description': u'',
    u'display': True,
    u'id': 1,
    u'multi': False,
    u'name': u'owner',
    u'required': False,
    u'resource_name': u'Device',
    u'site_id': 1},
   {u'constraints': {u'allow_empty': False,
    u'pattern': u'',
    u'valid_values': []},
   u'description': u'',
   u'display': False,
   u'id': 3,
   u'multi': True,
   u'name': u'multi',
   u'required': False,
   u'resource_name': u'Device',
   u'site_id': 1}],
  u'limit': None,
  u'offset': 0,
  u'total': 3},
 u'status': u'ok'}

# Dummy config data used for testing dotfile and client
CONFIG_DATA = {
    'email': 'jathan@localhost',
    'url': 'http://localhost:8990/api',
    'auth_method': 'auth_token',
    'secret_key': 'MJMOl9W7jqQK3h-quiUR-cSUeuyDRhbn2ca5E31sH_I=',
}


@pytest.fixture
def config():
    return CONFIG_DATA


# Payload used to create Network & Device attributes used for testing.
TEST_ATTRIBUTES = {
    'attributes': [
        {
            'name': 'cluster',
            'resource_name': 'Device',
            'description': 'Device cluster.',
            'constraints': {'allow_empty': True},
        },
        {
            'name': 'foo',
            'resource_name': 'Device',
            'description': 'Foo for Devices.',
        },
        {
            'name': 'owner',
            'resource_name': 'Device',
            'description': 'Device owner.',
        },
        {
            'name': 'cluster',
            'resource_name': 'Network',
            'description': 'Network cluster.',
            'constraints': {'allow_empty': True},
        },
        {
            'name': 'foo',
            'resource_name': 'Network',
            'description': 'Foo for Networks.',
        },
        {
            'name': 'owner',
            'resource_name': 'Network',
            'description': 'Network owner.',
        },
    ]
}

# Phony attributes to randomly generate for testing.
ATTRIBUTE_DATA = {
    'cluster': ['', 'lax', 'iad', 'sjc'],
    'owner': ['jathan', 'bob', 'alice'],
    'foo': ['bar', 'baz', 'spam'],
}

# Used to store Attribute/value pairs
Attribute = collections.namedtuple('Attribute', 'name value')


def generate_attributes(attributes=None, as_dict=True):
    """
    Randomly choose attributes and values for testing.

    :param attributes:
        Dictionary of attribute names and values

    :param as_dict:
        If set return a dict vs. list of Attribute objects
    """
    if attributes is None:
        attributes = ATTRIBUTE_DATA
    attrs = []
    for attr_name, attr_values in attributes.iteritems():
        if random.choice((True, False)):
            attr_value = random.choice(attr_values)
            attrs.append(Attribute(attr_name, attr_value))
    if as_dict:
        attrs = dict(attrs)
    return attrs


def generate_crap(num_items=100):
    """
    Return a list of dicts of {name: description}.

    :param num_items:
        Number of items to generate
    """
    names = set()
    while len(names) < num_items:
        names.add(fake.word().title())
    data = []
    for name in names:
        description = ' '.join(fake.words()).capitalize()
        item = {'name': name, 'description': description}
        data.append(item)
    return data


def populate_sites(site_data):
    """Populate sites from fixture data."""
    api = client.Client('http://localhost:8990/api', email='jathan@localhost')
    results = []
    for d in site_data:
        try:
            result = api.sites.post(d)
        except Exception as err:
            print err, d['name']
        else:
            results.append(result)
    print 'Created', len(results), 'sites.'


def generate_words(num_items=100, title=False, add_suffix=False):
    stuff = set()
    while len(stuff) < num_items:
        things = (fake.word(), fake.first_name(), fake.last_name())
        suffix = str(random.randint(1, 8)) if add_suffix else ''
        word = random.choice(things) + suffix
        if title:
            word = word.title()
        else:
            word = word.lower()
        stuff.add(word)
    return sorted(stuff)


def generate_ipv4():
    """Generate a random IPv4 address."""
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))


def generate_ipv4list(num_items=100, include_hosts=False):
    """
    Generate a list of unique IPv4 addresses. This is a total hack.

    :param num_items:
        Number of items to generate

    :param include_hosts:
        Whether to include /32 addresses
    """
    ipset = set()
    # Keep iterating and hack together cidr prefixes if we detect empty
    # trailing octects. This is so lame that we'll mostly just end up with a
    # bunch of /24 networks.
    while len(ipset) < num_items:
        ip = generate_ipv4()
        if ip.endswith('.0.0.0'):
            prefix = '/8'
        elif ip.endswith('.0.0'):
            prefix = '/16'
        elif ip.endswith('.0'):
            prefix = '/24'
        elif include_hosts:
            prefix = '/32'
        else:
            continue

        ip += prefix
        ipset.add(ip)
    return sorted(ipset)


def generate_hostnames(num_items=100):
    """
    Generate a random list of hostnames.

    :param num_items:
        Number of items to generate
    """
    hostnames = generate_words(num_items, add_suffix=True)
    return hostnames


def generate_devices(num_items=100, with_attributes=True):
    """
    Return a list of dicts for Device creation.

    :param num_items:
        Number of items to generate

    :param with_attributes:
        Whether to include Attributes
    """
    hostnames = generate_hostnames(num_items)

    devices = []
    for hostname in hostnames:
        item = {'hostname': hostname}
        if with_attributes:
            attributes = generate_attributes()
            item['attributes'] = attributes

        devices.append(item)
    return {'devices': devices}


def generate_networks(num_items=100, with_attributes=True):
    """
    Return a list of dicts for Network creation.

    :param num_items:
        Number of items to generate

    :param with_attributes:
        Whether to include Attributes
    """
    ipv4list = generate_ipv4list(num_items)

    networks = []
    for cidr in ipv4list:
        attributes = generate_attributes()
        item = {'cidr': cidr}
        if with_attributes:
            attributes = generate_attributes()
            item['attributes'] = attributes

        networks.append(item)
    return {'networks': networks}
