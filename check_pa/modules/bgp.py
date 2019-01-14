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
        Bgp(args.host, args.token, args.mode, args.peer=None),
        np.ScalarContext('bgp', '@~:%d' % args.warn, '@~:%d' % args.crit),
        BgpSummary())


class Bgp(np.Resource):
    """
    Will fetch the bgp informations (routes and peers) from the REST API and returns
    a warning if the result is lesser the value of warning (e. g. 1)
    and critical (e. g. 2).
    """

    def __init__(self, host, token, mode, peer):
        self.host = host
        self.token = token
        self.mode = mode
        if peer:
            self.peer = peer
            self.cmd = '<show><routing><protocol><bgp><peer><peer-name>%s</peer-name></peer></bgp></protocol></routing></show>' % self.peer
        else:
            self.cmd = '<show><routing><summary></summary></routing></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create bgp metrics.

        :return: bgp metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        result = soup.result
        if self.mode == "routes":
            for item in result.find_all('BGP-Routes'):
                bgp_routes = int(Finder.find_item(item, 'total'))
            _log.info('BGP Routes: %s' % bgp_routes)
            return [np.Metric('bgp-routes-count', bgp_routes, context='bgp')]
        elif self.mode == "peers":
            if self.peer:
                peer_status = Finder.find_item(item, 'status')
                return [np.Metric('peer-status', peer_count, context='bgp')]
            else:
                for item in result.find_all('bgp'):
                    peer_count = int(Finder.find_item(item, 'peer-count'))
                _log.info('BGP Peers: %s' % peer_count)
                return [np.Metric('peer-count', peer_count, context='bgp')]


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
