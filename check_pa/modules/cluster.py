# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader, Finder

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the cluster command.

    :return: the cluster check.
    """

    check = np.Check()
    check.add(Cluster(args.host, args.token, args.clusterstate))
    check.add(ClusterContext('alarm'))
    check.add(ClusterSummary())

    return check

class Cluster(np.Resource):
    def __init__(self, host, token, clusterstate):
        self.host = host
        self.token = token
        self.clusterstate = clusterstate
        self.cmd = '<show><high-availability><state><%2Fstate' \
                   '>' \
                   '<%2Fhigh-availability><%2Fshow>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create load metrics.

        :return: a load metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()

        ha_enabled = soup.result.enabled.text

        if not ha_enabled:
            _log.debug('High Availability is not enabled')
            yield np.Metric('High Availability is not enabled', True, context='alarm')
        yield np.Metric('High Availability is enabled', False, context='alarm')


        localinfo = soup.find('local-info')
        state = Finder.find_item(localinfo, 'state')
        if state != self.clusterstate:
            _log.debug(f'High Availability Cluster Status is {state} not {self.clusterstate}')
            yield np.Metric(f'High Availability Cluster Status is {state} not {self.clusterstate}', True, context='alarm')
        yield np.Metric(f'High Availability Cluster Status is {state}', False, context='alarm')

class ClusterContext(np.Context):
    def __init__(self, name, fmt_metric='{name} is {valueunit}',
                 result_cls=np.Result):
        super(ClusterContext, self).__init__(name, fmt_metric,
                                                   result_cls)

    def evaluate(self, metric, resource):
        if not metric.value:
            return self.result_cls(np.Ok, None, metric)
        else:
            return self.result_cls(np.Critical, None, metric)

class ClusterSummary(np.Summary):
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