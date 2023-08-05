# -*- coding: utf-8 -*-
#
# This file is part of CERN Service XML
# Copyright (C) 2015 CERN.
#
# CERN Service XML is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Service document tests."""

from __future__ import absolute_import, print_function, unicode_literals

from datetime import datetime
from decimal import Decimal
from os.path import dirname, join

import pytest
from cernservicexml import ServiceDocument, Status
from cernservicexml._compat import StringIO, long_type
from lxml import etree

schema = etree.XMLSchema(file=join(dirname(__file__), 'xsls_schema.xsd'))


def validate_xsd(xmlstr):
    """Assert if xml is valid according to XSD schema."""
    schema.assertValid(etree.parse(StringIO(xmlstr)))
    return True


def test_creation_simple():
    """Test creation of a service document."""
    doc = ServiceDocument('myserviceid')
    assert doc.service_id == 'myserviceid'
    assert isinstance(doc.timestamp, datetime)
    assert doc.status == Status.available

    assert validate_xsd(doc.to_xml())
    assert doc.to_xml() == \
        '<serviceupdate xmlns="http://sls.cern.ch/SLS/XML/update">' \
        '<id>myserviceid</id>' \
        '<status>available</status>' \
        '<timestamp>{0}</timestamp>' \
        '</serviceupdate>'.format(doc.timestamp.isoformat())

    dt = datetime(2015, 1, 1, 0, 0, 0)
    doc = ServiceDocument('anotherid', timestamp=dt,
                          status=Status.degraded)

    assert doc.to_xml() == \
        '<serviceupdate xmlns="http://sls.cern.ch/SLS/XML/update">' \
        '<id>anotherid</id>' \
        '<status>degraded</status>' \
        '<timestamp>2015-01-01T00:00:00</timestamp>' \
        '</serviceupdate>'
    assert validate_xsd(doc.to_xml())


def test_availablity_to_status():
    """Test creation of a service document."""
    dt = datetime(2015, 1, 1, 0, 0, 0)
    doc = ServiceDocument('anotherid', timestamp=dt, availability=99)
    assert doc.status == Status.available
    assert doc.availability == 99
    assert validate_xsd(doc.to_xml())

    doc = ServiceDocument('anotherid', timestamp=dt, availability=60)
    assert doc.status == Status.degraded
    assert doc.availability == 60
    assert validate_xsd(doc.to_xml())

    doc = ServiceDocument('anotherid', timestamp=dt, availability=20)
    assert doc.status == Status.unavailable
    assert doc.availability == 20
    assert validate_xsd(doc.to_xml())

    with pytest.raises(AssertionError):
        doc = ServiceDocument('anid', timestamp=dt, status=Status.unavailable,
                              availability=20)

    doc = ServiceDocument('anotherid', timestamp=dt, status='available')
    assert doc.status == Status.available
    assert doc.availability == 100
    assert validate_xsd(doc.to_xml())

    doc = ServiceDocument('anotherid', timestamp=dt, status='degraded')
    assert doc.status == Status.degraded
    assert doc.availability == 50
    assert validate_xsd(doc.to_xml())

    doc = ServiceDocument('anotherid', timestamp=dt, status='unavailable')
    assert doc.status == Status.unavailable
    assert doc.availability == 0
    assert validate_xsd(doc.to_xml())


def test_creation_attrs():
    """Test non-mandatory attributes."""
    dt = datetime(2015, 1, 1, 0, 0, 0)
    doc = ServiceDocument(
        'myid',
        timestamp=dt,
        availabilitydesc='My description',
        contact='info@example.org',
        webpage='http://example.org',
        availabilityinfo='Extra info',
    )

    assert doc.to_xml() == \
        '<serviceupdate xmlns="http://sls.cern.ch/SLS/XML/update">' \
        '<id>myid</id>' \
        '<status>available</status>' \
        '<timestamp>2015-01-01T00:00:00</timestamp>' \
        '<availabilitydesc>My description</availabilitydesc>' \
        '<contact>info@example.org</contact>' \
        '<webpage>http://example.org</webpage>' \
        '<availabilityinfo>Extra info</availabilityinfo>' \
        '</serviceupdate>'
    assert validate_xsd(doc.to_xml())


def test_outofbounds():
    """Test out of bounds values."""
    with pytest.raises(AssertionError):
        ServiceDocument(None)
    with pytest.raises(AssertionError):
        ServiceDocument(1234)
    with pytest.raises(AssertionError):
        ServiceDocument('id', timestamp='1234')
    with pytest.raises(AssertionError):
        ServiceDocument('id', status=100)
    with pytest.raises(AssertionError):
        ServiceDocument('id', status='not-a-status')
    doc = ServiceDocument('id')
    with pytest.raises(AssertionError):
        doc.add_numericvalue(1234, 'val')
    with pytest.raises(AssertionError):
        doc.add_numericvalue('name', 1234, desc=1234)
    with pytest.raises(AssertionError):
        doc.add_numericvalue('name', 'astring', desc=1234)
    # Remove in v0.3 (availability removed)
    with pytest.raises(AssertionError):
        ServiceDocument('id', availability=-1)
    with pytest.raises(AssertionError):
        ServiceDocument('id', availability=101)
    with pytest.raises(AssertionError):
        ServiceDocument('id', availability='100')


def test_numericvalue():
    """Test adding numeric data to service."""
    dt = datetime(2015, 1, 1, 0, 0, 0)
    doc = ServiceDocument('myid', timestamp=dt)
    doc.add_numericvalue('val1', 1234)
    doc.add_numericvalue('val2', 12.34)
    doc.add_numericvalue('val3', Decimal("0.1"))
    doc.add_numericvalue('val4', Decimal("0.1") + Decimal("0.2"))
    doc.add_numericvalue('val5', 1234, desc="a desc")
    doc.add_numericvalue('val6', long_type(1234))

    assert doc.to_xml() == \
        '<serviceupdate xmlns="http://sls.cern.ch/SLS/XML/update">' \
        '<id>myid</id>' \
        '<status>available</status>' \
        '<timestamp>2015-01-01T00:00:00</timestamp>' \
        '<data>' \
        '<numericvalue name="val1">1234</numericvalue>' \
        '<numericvalue name="val2">12.34</numericvalue>' \
        '<numericvalue name="val3">0.1</numericvalue>' \
        '<numericvalue name="val4">0.3</numericvalue>' \
        '<numericvalue desc="a desc" name="val5">1234</numericvalue>' \
        '<numericvalue name="val6">1234</numericvalue>' \
        '</data>' \
        '</serviceupdate>'
    assert validate_xsd(doc.to_xml())
