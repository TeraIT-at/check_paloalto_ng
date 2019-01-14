#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_check_paloalto
----------------------------------

Tests for `check_paloalto` modules.
"""

import pytest
import responses
from nagiosplugin.state import ServiceState

import check_pa.modules.bgp
import utils


class TestBgp(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_bgp_routes_ok(self):
        self.warn = 10
        self.crit = 5
        self.mode = 'routes'

        f = 'bgp_routes.xml'
        check = check_pa.modules.bgp.create_check(self)
        obj = check.resources[0]

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     obj.xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            with pytest.raises(SystemExit):
                check.main(verbose=3)

        assert check.exitcode == 0
        assert check.state == ServiceState(code=0, text='ok')
        assert check.summary_str == 'bgp-routes-count: 12'

    @responses.activate
    def test_bgp_routes_critical(self):
        self.warn = 20
        self.crit = 15
        self.mode = 'routes'

        f = 'bgp_routes.xml'
        check = check_pa.modules.bgp.create_check(self)
        obj = check.resources[0]

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     obj.xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            with pytest.raises(SystemExit):
                check.main(verbose=3)

        assert check.exitcode == 2
        assert check.state == ServiceState(code=2, text='critical')
        assert check.summary_str == 'bgp-routes-count is 12 (outside range @~:15)'
