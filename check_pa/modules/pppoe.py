# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    :return: the pppoe check.
    """
    return np.Check(
        PPPoEInterface(args.host, args.token, args.verify_ssl, args.verbose, args.interface, args.expect_down, args.expect_mtu),
        PPPoEStateContext('pppoe-state'),
        PPPoEStateContext('ppp-state'),
        PPPoEMTUContext('mtu'),
        PPPoESummary(args.expect_down, args.expect_mtu, args.interface)
        )


class PPPoEInterface(np.Resource):
    """Reads the information about a pppoe interface of the Palo Alto Firewall System."""

    def __init__(self, host, token, verify_ssl, verbose, interface_name, expect_down, expect_mtu):
        self.host = host
        self.token = token
        self.ssl_verify = verify_ssl
        self.verbose = verbose
        self.interface_name = interface_name
        self.expect_down = expect_down
        self.expect_mtu = expect_mtu
        self.cmd = '<show><pppoe><interface>' + str(self.interface_name) + '</interface></pppoe></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.ssl_verify, self.verbose, self.cmd)


    def probe(self):
        """
        :return: a pppoe interface metrics.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        interface = soup.find("interface").text
        pppoe_state = soup.find("pppoe-state").text
        ppp_state = soup.find("ppp-state").text
        mtu = soup.find("link-mtu").text

        yield np.Metric(interface+"-pppoe-pppoe-state", 1 if (pppoe_state and pppoe_state == "Connected") else 0,context="pppoe-state")
        yield np.Metric(interface+"-pppoe-ppp-state", 1 if (ppp_state and ppp_state == "Connected") else 0,context="ppp-state")
        yield np.Metric(interface+"-pppoe-mtu", int(mtu),context="mtu")



class PPPoEMTUContext(np.Context):
    def __init__(self, name,
                 result_cls=np.Result):
        super(PPPoEMTUContext, self).__init__(name, None,
                                                   result_cls)
    def performance(self, metric, resource):
        return np.Performance(metric.name, metric.value, metric.uom,
                           None, resource.expect_mtu, metric.min, metric.max)

    def evaluate(self, metric, resource):
        if resource.expect_down:
            return self.result_cls(np.Ok, None, metric)

        return self.result_cls(np.Critical if (metric.value < resource.expect_mtu) else np.Ok, None, metric)


class PPPoEStateContext(np.Context):
    def __init__(self, name, fmt_metric='{name} is {valueunit}',
                 result_cls=np.Result):
        super(PPPoEStateContext, self).__init__(name, fmt_metric,
                                                   result_cls)
    def performance(self, metric, resource):
        return np.Performance(metric.name, metric.value, metric.uom,
                           None, True, metric.min, metric.max)

    def evaluate(self, metric, resource):
        if metric.value == 1:
            return self.result_cls(np.Critical if resource.expect_down == True else np.Ok, None, metric)
        else:
            return self.result_cls(np.Ok if resource.expect_down == True else np.Critical, None, metric)

class PPPoESummary(np.Summary):
    def __init__(self, expect_down, expect_mtu, interface):
        self.expect_down = expect_down
        self.expect_mtu = expect_mtu
        self.interface = interface

    def ok(self, results):
        s = self.interface + ": "
        l = []
        for result in results.by_state[np.Ok]:
            if result.context.name == "pppoe-state":
                l.append("PPPoE is " + ("UP" if result.metric.value == 1 else "DOWN"))
            if result.context.name == "ppp-state":
                l.append("PPP is " + ("UP" if result.metric.value == 1 else "DOWN"))
            if result.context.name == "mtu":
                l.append("MTU is " + str(result.metric.value))

        s += ', '.join(l)
        return s

    def problem(self, results):
        s = self.interface + ": "
        l = []
        for result in results.by_state[np.Critical]:
            if result.context.name == "pppoe-state":
                l.append("PPPoE is " + ("UP" if result.metric.value == 1 else "DOWN") + " (expected " + ("DOWN" if self.expect_down else "UP") + ")")
            if result.context.name == "ppp-state":
                l.append("PPP is " + ("UP" if result.metric.value == 1 else "DOWN") + " (expected " + ("DOWN" if self.expect_down else "UP") + ")")
            if result.context.name == "mtu":
                l.append("MTU is " + str(result.metric.value) + " (expected >= " + str(self.expect_mtu) + ")")

        s += ', '.join(l)
        return s
