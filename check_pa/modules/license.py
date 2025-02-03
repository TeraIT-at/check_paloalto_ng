# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader, Finder
from datetime import datetime

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the license command.

    :return: the license check.
    """

    check = np.Check()
    check.add(License(args.host, args.token, args.verify_ssl, args.verbose))
    check.add(LicenseContext('alarm'))
    check.add(LicenseSummary())

    return check

class License(np.Resource):
    def __init__(self, host, token, verify_ssl, verbose):
        self.host = host
        self.token = token
        self.ssl_verify = verify_ssl
        self.verbose = verbose
        self.cmd =  '<request><license><info><%2Finfo' \
                   '>' \
                   '<%2Flicense><%2Frequest>'
        self.xml_obj = XMLReader(self.host, self.token, self.ssl_verify, self.verbose, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create load metrics.

        :return: a load metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        licenses = soup.result.licenses
        present = datetime.now()

        for entry in licenses.find_all('entry'):
            name = Finder.find_item(entry, 'description')
            expires = Finder.find_item(entry, 'expires')
            expired = Finder.find_item(entry, 'expired')

            if expired == 'yes':
                yield np.Metric(f'License with name: {name} has expired!', True, context='alarm')
                continue

            if not expires == 'Never':
                delta = datetime.strptime(expires, '%B %d, %Y') - present
                if delta.days < 60:
                    yield np.Metric(f'License with name: {name} will expire in {delta.days} days!', True, context='alarm')
                else:
                    yield np.Metric(f'License with name: {name} will expire in {delta.days} days.', False, context='alarm')



class LicenseContext(np.Context):
    def __init__(self, name, fmt_metric='{name} is {valueunit}',
                 result_cls=np.Result):
        super(LicenseContext, self).__init__(name, fmt_metric,
                                                   result_cls)

    def evaluate(self, metric, resource):
        if not metric.value:
            return self.result_cls(np.Ok, None, metric)
        else:
            return self.result_cls(np.Critical, None, metric)

class LicenseSummary(np.Summary):
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
