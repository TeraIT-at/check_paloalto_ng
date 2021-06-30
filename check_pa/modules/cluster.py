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
    check.add(Cluster(args.host, args.token, args.primarystate, args.secondarystate))
    check.add(ClusterContext('alarm'))
    check.add(ClusterSummary())

    return check

class Cluster(np.Resource):
    def __init__(self, host, token, primarystate, secondarystate):
        self.host = host
        self.token = token
        self.primarystate = primarystate
        self.secondarystate = secondarystate
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

        # Check if high availabity is enabled by checking <result><enabled>True</enabled></result>. Return if not enabled to prevent failures.
        ha_enabled = soup.result.enabled.text
        if not ha_enabled:
            _log.debug('High Availability is not enabled')
            yield np.Metric('High Availability is not enabled', True, context='alarm')
            return
        yield np.Metric('High Availability is enabled', False, context='alarm')

        localinfo = soup.find('local-info')
        peerinfo = soup.find('peer-info')

        # Check if the local node is $primarystate by checking <result><group><local-info><state>$primarystate</state></local-info></group></result>
        state = Finder.find_item(localinfo, 'state')
        if state != self.primarystate:
            _log.debug(f'Cluster Primary node status is {state} not {self.primarystate}')
            yield np.Metric(f'Cluster Primary node status is {state} not {self.primarystate}', True, context='alarm')
        yield np.Metric(f'Cluster Primary node status is {state}', False, context='alarm')
        
        # Check if the peer node is $secondarystate by checking <result><group><peer-info><state>$secondarystate</state></peer-info></group></result>
        peerstate = Finder.find_item(peerinfo, 'state')
        if peerstate != self.secondarystate:
            _log.debug(f'Cluster Secondary node status is {peerstate} not {self.secondarystate}')
            yield np.Metric(f'Cluster Secondary node status is {peerstate} not {self.secondarystate}', True, context='alarm')
        yield np.Metric(f'Cluster Secondary node status is {peerstate}', False, context='alarm')

        # Check if configuration synchronization is enabled by checking <result><group><running-sync-enabled>yes</running-sync-enabled></group></result>
        sync_enabled = soup.group.select('running-sync-enabled')[0].text
        if sync_enabled != 'yes':
            _log.debug(f'Cluster Configuration Synchronization is not Enabled')
            yield np.Metric(f'Cluster Configuration Synchronization state is not Enabled', True, context='alarm')
        yield np.Metric(f'Cluster Configuration Synchronization state is Enabled', False, context='alarm')

        # Check if configuration synchronization is synchronized by checking <result><group><running-sync>synchronized</running-sync></group></result>
        sync_state = soup.group.select('running-sync')[0].text
        if sync_state != 'synchronized':
            _log.debug(f'Cluster Configuration Synchronization state is {sync_state} not synchronized')
            yield np.Metric(f'Cluster Configuration Synchronization state is {sync_state} not synchronized', True, context='alarm')
        yield np.Metric(f'Cluster Configuration Synchronization state is {sync_state}', False, context='alarm')

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