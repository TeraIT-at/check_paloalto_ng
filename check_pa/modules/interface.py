# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader, Finder

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the interface command.

    :return: the interface check.
    """
    check = np.Check()
    if args.interface:
        interfaces = str(args.interface).split(",")
        check.add(Interface(args.host, args.token, args.verify_ssl, args.verbose, interfaces=interfaces))
    elif args.exclude:
        exclude_interfaces = str(args.exclude).split(",")
        check.add(Interface(args.host, args.token, args.verify_ssl, args.verbose, exclude_interfaces=exclude_interfaces))
    else:
        check.add(Interface(args.host, args.token, args.verify_ssl))

    check.add(InterfaceContext('alarm'))
    check.add(InterfaceSummary())

    return check

class Interface(np.Resource):
    def __init__(self, host, token, verify_ssl, verbose, interfaces=None, exclude_interfaces=None):
        self.host = host
        self.token = token
        self.ssl_verify = verify_ssl
        self.verbose = verbose
        self.interfaces = interfaces
        self.exclude_interfaces = exclude_interfaces

        self.cmd =  '<show><interface>all' \
                   '<%2Finterface><%2Fshow>'
        self.xml_obj = XMLReader(self.host, self.token, self.ssl_verify, self.verbose, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create load metrics.

        :return: a load metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        interfaces = soup.result.hw

        for entry in interfaces.find_all('entry'):
            name = Finder.find_item(entry, 'name')
            state = Finder.find_item(entry, 'state')
            duplex = Finder.find_item(entry, 'duplex')

            if (self.interfaces and name not in self.interfaces) or (self.exclude_interfaces and name in self.exclude_interfaces):
                continue

            if state == 'down':
                yield np.Metric(f'Interface with name: {name} is down!', True, context='alarm')
                continue
            else:
                yield np.Metric(f'Interface with name: {name} is up', False, context='alarm')

            if duplex != 'full':
                yield np.Metric(f'Interface with name: {name} is not full duplex, but only: {duplex}', True, context='alarm')
            else:
                yield np.Metric(f'Interface with name: {name} is full duplex', False, context='alarm')


class InterfaceContext(np.Context):
    def __init__(self, name, fmt_metric='{name} is {valueunit}',
                 result_cls=np.Result):
        super(InterfaceContext, self).__init__(name, fmt_metric,
                                                   result_cls)

    def evaluate(self, metric, resource):
        if not metric.value:
            return self.result_cls(np.Ok, None, metric)
        else:
            return self.result_cls(np.Critical, None, metric)

class InterfaceSummary(np.Summary):
    def ok(self, results):
        return 'No alarms found.'

    def problem(self, results):
        s = 'Alarm(s) found: '
        l = []
        for alarm in results.results:
            if alarm.metric.value:
                l.append(alarm.metric.name)
        s += ', '.join(l)
        return s
