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
import nagiosplugin as np

import check_pa.modules.diskspace
import utils


class TestPowersupply(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_powersupply_ok(self):
        self.min = 1

        f = 'powersupply.xml'
        check = check_pa.modules.powersupply.create_check(self)
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
            assert check.state == np.state.Ok
            assert check.summary_str == '2 working power supplies.'

    @responses.activate
    def test_powersupply_alarm(self):
        self.min = 3

        f = 'powersupply_alarm.xml'
        check = check_pa.modules.powersupply.create_check(self)
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
            assert check.state == np.state.Critical
            assert check.summary_str == 'Too few power supplies: 1 (At least 3 expected), power supplies in alarm state: Slot 1-Power Supply #2-Alarm'

    @responses.activate
    def test_powersupply_fail(self):
        self.min = 3

        f = 'powersupply.xml'
        check = check_pa.modules.powersupply.create_check(self)
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
            assert check.state == np.state.Critical
            assert check.summary_str == 'Too few power supplies: 2 (At least 3 expected)'

    @responses.activate
    def test_powersupply_warn(self):
        self.min = 1

        f = 'powersupply_alarm.xml'
        check = check_pa.modules.powersupply.create_check(self)
        
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
            
            assert check.exitcode == 1
            assert check.state == np.state.Warn
            assert check.summary_str == 'Working power supplies: 1, power supplies in alarm state: Slot 1-Power Supply #2-Alarm'
