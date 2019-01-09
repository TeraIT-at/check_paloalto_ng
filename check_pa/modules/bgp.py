# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader, Finder

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the bgp command.

    :return: the bgp check.
    """
    return np.Check(
        Bgp(args.host, args.token),
        np.ScalarContext('bgp-routes-count'),
        BgpSummary())


class Bgp(np.Resource):
    """
    Will fetch the antivirus definition date from the REST API and returns
    a warning if the definition date is between the value of warning (e. g. 1)
    and critical (e. g. 2).
    """

    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.cmd = '<show><routing><summary></summary></routing></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create antivirus metrics.

        :return: antivirus metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        result = soup.result
        for item in result.find_all('BGP-Routes'):
            bgp_routes = Finder.find_item(item, 'total')
        _log.info('BGP Routes: %s' % bgp_routes)

        return [np.Metric('bgp-routes-count', bgp_routes, context='bgp-routes-count')]


class BgpSummary(np.Summary):
    def ok(self, results):
        l = []
        for result in results.results:
            s = '%s: %s' % (result.metric.name, result.metric.value)
            _log.debug('Add result %r', s)
            l.append(s)
        _log.debug('Result count: %d' % len(l))
        output = ", ".join(l)
        return str(output)
