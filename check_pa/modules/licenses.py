# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np
from datetime import datetime

from check_pa.xml_reader import XMLReader, Finder

_log = logging.getLogger('nagiosplugin')


def get_now():
    return datetime.today()  # pragma: no cover


def create_check(args):
    return np.Check(
        License(args.host, args.token, args.verify_ssl, args.verbose, args.exclude),
        LicenseContext('license',  args.warn, args.crit),
        LicenseSummary(args.warn,args.crit))


class License(np.Resource):
    def __init__(self, host, token, verify_ssl, verbose, exclude):
        self.host = host
        self.token = token
        self.ssl_verify = verify_ssl
        self.verbose = verbose
        self.cmd = '<request><license><info></info></license></request>'
        self.xml_obj = XMLReader(self.host, self.token, self.ssl_verify, self.verbose, self.cmd)
        self.exclude = str(exclude).split(",")

    def probe(self):
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()

        licenses = soup.find_all('entry')

        for license in licenses:
            name = Finder.find_item(license,"feature").strip()
            not_valid_after = Finder.find_item(license,'expires').strip()
            _log.info(name)
            date_object = datetime.strptime(not_valid_after, '%B %d, %Y')
            difference = date_object - get_now()
            _log.debug('License "%s" difference: %s days' % (
                name, difference.days))

            if name not in self.exclude:
                    yield np.Metric(name, int(difference.days),
                                    context='license', uom="days")


class LicenseContext(np.Context):
    def fmt_metric(metric,context):
        if metric.value < 0:
            return "{name} expired since {value} {uom}".format(name=metric.name, value=abs(metric.value), uom=metric.uom, valueunit=metric.valueunit, min=metric.min, max=metric.max)
        else:
            return "{name} expires in {value} {uom}".format(name=metric.name, value=metric.value, uom=metric.uom, valueunit=metric.valueunit, min=metric.min, max=metric.max)

    def __init__(self, name, warn, crit,
                 fmt_metric=fmt_metric,
                 result_cls=np.Result):
        super(LicenseContext, self).__init__(name, fmt_metric, result_cls)
        self.warn = warn
        self.crit = crit

    def evaluate(self, metric, resource):
        if metric.value < self.crit:
            return self.result_cls(np.Critical, None, metric)
        elif metric.value < self.warn:
            return self.result_cls(np.Warn, None, metric)
        else:
            return self.result_cls(np.Ok, None, metric)


class LicenseSummary(np.Summary):
    def __init__(self, warn, crit):
        self.warn = warn
        self.crit = crit

    def ok(self, results):
        l = []
        n = []
        for result in results:
            l.append(result.metric.value)
            n.append(result.metric.name)
        output = 'All licenses ('+','.join(n)+') ok.\n'
        output += 'The next license will expire in %s days.' % min(l)
        return str(output)

    def problem(self, results):
        l = []
        ok = []
        for result in results:
            if result.metric.value < self.warn or result.metric.value < self.crit:
                l.append(str(result))
            else:
                ok.append(str(result))
        output = ", ".join(l)
        if len(ok) > 0:
            output += "\n"+", ".join(ok)
        return str(output)
