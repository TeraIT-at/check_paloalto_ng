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
        PowerSupply(args.host, args.token),
        PowerSupplyAlarmContext('alarm'),
        PowerSupplyInsertedContext('inserted'),
        np.ScalarContext('functional', critical=np.Range("@"+str(args.min-1))),
        PowerSupplySummary(args.min)
        )


class PowerSupply(np.Resource):
    """Reads the information about power supplies of the Palo Alto Firewall System."""

    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.cmd = '<show><system><environmentals>' \
                   '</environmentals></system></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        :return: a power supply metrics.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        powersupplys = soup.find('power-supply')
        powersupplyslots = powersupplys.find_all("entry")
        functional = 0

        for entry in powersupplyslots:
            if entry.Inserted.text:
                yield np.Metric("Slot "+entry.slot.text+"-"+entry.description.text+"-"+"Inserted", 1 if entry.Inserted.text == "True" else 0,context="inserted")

            if entry.alarm.text:
                yield np.Metric("Slot "+entry.slot.text+"-"+entry.description.text+"-"+"Alarm", 1 if entry.alarm.text == "True" else 0,context="alarm")

            if entry.Inserted.text == "True" and entry.alarm.text == "False":
                functional = functional + 1

        yield np.Metric("Functional Power Supplies", functional,context="functional")

            

from pprint import pprint

class PowerSupplyAlarmContext(np.Context):
    def __init__(self, name, fmt_metric='{name} is {valueunit}',
                 result_cls=np.Result):
        super(PowerSupplyAlarmContext, self).__init__(name, fmt_metric,
                                                   result_cls)
    def performance(self, metric, resource):
        return np.Performance(metric.name, metric.value, metric.uom,
                           None, True, metric.min, metric.max)

    def evaluate(self, metric, resource):
        if metric.value == 1:
            return self.result_cls(np.Critical, None, metric)
        else:
            return self.result_cls(np.Ok, None, metric)


class PowerSupplyInsertedContext(np.Context):
    def __init__(self, name, fmt_metric='{name} is {valueunit}',
                 result_cls=np.Result):
        super(PowerSupplyInsertedContext, self).__init__(name, fmt_metric,
                                                   result_cls)
    def performance(self, metric, resource):
        return np.Performance(metric.name, metric.value, metric.uom,
                           False, None, metric.min, metric.max)

    def evaluate(self, metric, resource):
      return self.result_cls(np.Ok, None, metric)


class PowerSupplySummary(np.Summary):
    def __init__(self, minsupplies):
        self.minsupplies = minsupplies


    def ok(self, results):
        res = ""
        for alarm in results.by_state[np.Ok]:
            if alarm.metric.context == "functional":
                res = str(alarm.metric.value) + " working power supplies."
        return res

    def problem(self, results):
        s = ""
        l = []
        for alarm in results.by_state[np.Critical]:
            s += 'Too few Power Supplies: '
            if alarm.metric.value:
                l.append(alarm.metric.name + " is " + str(alarm.metric.value))
        s += ', '.join(l)
        s += ". (At least " + str(self.minsupplies) + " expected)"
        return s
