# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the power-supply command.

    :return: the power-supply check.
    """
    return np.Check(
        PowerSupply(args.host, args.token, args.verify_ssl, args.verbose, args.min),
        PowerSupplyAlarmContext('alarm'),
        PowerSupplyInsertedContext('inserted'),
        np.ScalarContext('functional', critical=np.Range("@"+str(args.min-1))),
        PowerSupplySummary()
        )


class PowerSupply(np.Resource):
    """Reads the information about power supplies of the Palo Alto Firewall System."""

    def __init__(self, host, token, verify_ssl, verbose, minimum_powersupplies):
        self.host = host
        self.token = token
        self.ssl_verify = verify_ssl
        self.verbose = verbose
        self.minimum_powersupplies = minimum_powersupplies
        self.functional_powersupplies = 0
        self.cmd = '<show><system><environmentals>' \
                   '</environmentals></system></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.ssl_verify, self.verbose, self.cmd)

    def probe(self):
        """
        :return: a power supply metrics.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        powersupplys = soup.find('power-supply')
        powersupplyslots = powersupplys.find_all("entry")
        self.results = list()

        for entry in powersupplyslots:
            if entry.Inserted.text == "True" and entry.alarm.text == "False":
                self.functional_powersupplies = self.functional_powersupplies + 1

        self.results.append(np.Metric("Functional Power Supplies", self.functional_powersupplies,context="functional"))

        for entry in powersupplyslots:
            if entry.Inserted.text:
                self.results.append(np.Metric("Slot "+entry.slot.text+"-"+entry.description.text+"-"+"Inserted", 1 if entry.Inserted.text == "True" else 0,context="inserted"))

            if entry.alarm.text:
                if entry.alarm.text == "True":
                    if (self.functional_powersupplies >= self.minimum_powersupplies):
                        val = int(np.Warn)
                    else:
                        val = int(np.Critical)
                else:
                    val = int(np.Ok)

                self.results.append(np.Metric("Slot "+entry.slot.text+"-"+entry.description.text+"-"+"Alarm", val,context="alarm"))

        return self.results

class PowerSupplyAlarmContext(np.Context):
    def __init__(self, name, fmt_metric='{name} is {valueunit}',
                 result_cls=np.Result):
        super(PowerSupplyAlarmContext, self).__init__(name, fmt_metric,
                                                   result_cls)
    def performance(self, metric, resource):
        return np.Performance(metric.name, metric.value, metric.uom,
                           None, None, metric.min, metric.max)

    def evaluate(self, metric, resource):
        if metric.value == int(np.Critical):
            return self.result_cls(np.Critical, None, metric)
        elif metric.value == int(np.Warn):
            return self.result_cls(np.Warn, None, metric)
        else:
            return self.result_cls(np.Ok, None, metric)


class PowerSupplyInsertedContext(np.Context):
    def __init__(self, name, fmt_metric='{name} is {valueunit}',
                 result_cls=np.Result):
        super(PowerSupplyInsertedContext, self).__init__(name, fmt_metric,
                                                   result_cls)
    def performance(self, metric, resource):
        return np.Performance(metric.name, metric.value, metric.uom,
                           None, None, metric.min, metric.max)

    def evaluate(self, metric, resource):
      return self.result_cls(np.Ok, None, metric)


class PowerSupplySummary(np.Summary):

    def ok(self, results):
        res = ""
        for alarm in results.by_state[np.Ok]:
            if alarm.metric.context == "functional":
                res = str(alarm.metric.value) + " working power supplies."
        return res

    def problem(self, results):
        s = ""
        power_issues = []
        alarms = []
        minimum = results.first_significant.resource.minimum_powersupplies
        functional = results.first_significant.resource.functional_powersupplies


        if results.most_significant_state == np.Critical:
            for alarm in results.by_state[np.Critical]:
                if alarm.metric.context == "functional":
                    if alarm.metric.value:
                        power_issues.append(alarm.metric.name)
                if alarm.metric.context == "alarm":
                    if alarm.metric.value:
                        alarms.append(alarm.metric.name)

        if results.most_significant_state == np.Warn:
            for alarm in results.by_state[np.Warn]:
                if alarm.metric.context == "alarm":
                    if alarm.metric.value:
                        alarms.append(alarm.metric.name)

        if len(power_issues) > 0:
            if results.most_significant_state == np.Critical:
                s += 'Too few power supplies: ' + str(functional) + " (At least " + str(minimum) + " expected)"

        if len(power_issues) == 0 or results.most_significant_state == np.Warn:
                s += 'Working power supplies: ' + str(functional)

        if len(alarms) > 0:
            if len(s) > 0:
               s += ", "
            s += 'power supplies in alarm state: '
            s += ", ".join(alarms)

        return s
