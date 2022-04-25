#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_check_paloalto
----------------------------------

Tests for `check_paloalto` modules.
"""

import pytest
import responses
import nagiosplugin.state as state

import check_pa.modules.diskspace
import utils


class TestPPPoE(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_pppoe(self):
        self.interface = "ethernet1/1"
        self.expect_down = False
        self.expect_mtu = 1492

        f = 'pppoe_up.xml'
        check = check_pa.modules.pppoe.create_check(self)
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
            assert check.state == state.Ok
            assert check.summary_str == 'ethernet1/1: PPPoE is UP, PPP is UP, MTU is 1492'

    @responses.activate
    def test_pppoe_expect_down_fail(self):
        self.interface = "ethernet1/1"
        self.expect_down = True
        self.expect_mtu = 1500

        f = 'pppoe_up.xml'
        check = check_pa.modules.pppoe.create_check(self)
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
            assert check.state == state.Critical
            assert check.summary_str == 'ethernet1/1: PPPoE is UP (expected DOWN), PPP is UP (expected DOWN)'

    @responses.activate
    def test_pppoe_expect_mtu_fail(self):
        self.interface = "ethernet1/1"
        self.expect_down = False
        self.expect_mtu = 1500

        f = 'pppoe_up.xml'
        check = check_pa.modules.pppoe.create_check(self)
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
            assert check.state == state.Critical
            assert check.summary_str == 'ethernet1/1: MTU is 1492 (expected >= 1500)'

    @responses.activate
    def test_pppoe_down_ok(self):
        self.interface = "ethernet1/1"
        self.expect_down = True
        self.expect_mtu = 1500

        f = 'pppoe_down.xml'
        check = check_pa.modules.pppoe.create_check(self)
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
            assert check.state == state.Ok