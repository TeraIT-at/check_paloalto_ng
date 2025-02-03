# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader, Finder

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the qos command.

    :return: the qos check.
    """

    return np.Check(
        Qos(args.host, args.token, args.verify_ssl, args.verbose, args.klass),
        np.ScalarContext("qos", args.warn, args.crit),
        QosSummary())


class Qos(np.Resource):
    """
    Will fetch the qos definition date from the REST API and returns
    a warning if the definition date is between the value of warning (e. g. 1)
    and critical (e. g. 2).
    """

    def __init__(self, host, token, verify_ssl, verbose, klass):
        self.host = host
        self.token = token
        self.ssl_verify = verify_ssl
        self.verbose = verbose
        self.klass = klass
        self.cmd = "<show><qos><interface><entry name='ae1'><throughput>0</throughput></entry></interface></qos></show>"
        self.xml_obj = XMLReader(self.host, self.token, self.ssl_verify, self.verbose, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create qos metrics.

        :return: qos metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        results = str(soup.result).split('\n')
        values = []
        for r in results:
            values.append(r.split(" "))
        for v in values:
            try:
                qos_class = int(v[1])
                qos_bitrate = int(v[-2])
                if (str(self.klass) == 'all'): yield np.Metric("Class %s" % qos_class, qos_bitrate, context='qos')
                if (int(self.klass) == int(qos_class)): yield np.Metric("Class %s" % qos_class, qos_bitrate, context='qos')
            except:
                pass

class QosSummary(np.Summary):
    def ok(self, results):
        l = []
        for result in results.results:
            s = '%s: %s kbps' % (result.metric.name, result.metric.value)
            l.append(s)
        output = " - ".join(l)
        return str(output)

