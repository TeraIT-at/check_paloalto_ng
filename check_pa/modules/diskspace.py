# -*- coding: utf-8 -*-

import logging
import re

import nagiosplugin as np

from check_pa.xml_reader import XMLReader

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the diskspace command.

    :return: the diskspace check.
    """
    return np.Check(
        DiskSpace(args.host, args.token, args.verify_ssl, args.verbose),
        np.ScalarContext('diskspace', args.warn, args.crit),
        DiskSpaceSummary())


class DiskSpace(np.Resource):
    """Reads the used disk space of the Palo Alto Firewall System."""

    def __init__(self, host, token, verify_ssl, verbose):
        self.host = host
        self.token = token
        self.ssl_verify = verify_ssl
        self.verbose = verbose
        self.cmd = '<show><system><disk-space><%2Fdisk-space><%2Fsystem' \
                   '><%2Fshow>'
        self.xml_obj = XMLReader(self.host, self.token, self.ssl_verify, self.verbose, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create disk space metrics.

        :return: a disk space metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        available_disks = re.findall('((sda\d.?)|(md\d.?)|(mmcblk\dp\d.?)|(nvme\dn\dp\d.*?))(?=/)', soup.result.string)

        for disk in available_disks:
            _log.debug("disk: "+str(disk))
            diskname = re.findall('((sda\d)|(mmcblk\dp\d)|(md\d)|(nvme\dn\dp\d))', disk[0])[0][0]
            diskname = str(diskname)
            _log.debug("name: "+str(diskname))
            percent = int(re.findall('([0-9]+%)', disk[0])[0].replace("%", ""))
            _log.debug("percent: "+str(percent))
            yield np.Metric(diskname, percent, '%', context='diskspace')


class DiskSpaceSummary(np.Summary):
    """Create status line from results."""

    def ok(self, results):
        l = []
        for sda in results.results:
            s = '%s: %s%%' % (sda.metric.name, sda.metric.value)
            l.append(s)
        _log.debug('Disk/Partition count: %d' % len(l))
        output = ", ".join(l)
        return str(output)

    def problem(self, results):
        return '%s' % (str(results.first_significant))
