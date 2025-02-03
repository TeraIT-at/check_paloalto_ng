

# -*- coding: utf-8 -*-
import argparse
import sys
import nagiosplugin

sys.path.append('modules')

from check_pa.modules import certificate, cluster, throughput, diskspace, useragent, environmental, sessioninfo, thermal, load, powersupply, pppoe, licenses, interface, antivirus, threat, bgp, qos, reports


@nagiosplugin.guarded
def main():  # pragma: no cover
    args = parse_args(sys.argv[1:])
    if args.reset:
        throughput.reset()
    else:
        check = args.func.create_check(args)
        check.main(verbose=args.verbose, timeout=args.timeout)


def parse_args(args):
    parser = argparse.ArgumentParser(description=__doc__)

    connection = parser.add_argument_group('Connection')
    connection.add_argument('-H', '--host',
                            help='PaloAlto Server Hostname',
                            required=True)
    connection.add_argument('-T', '--token',
                            help='Generated Token for REST-API access',
                            required=True)
    connection.add_argument('--verify-ssl',
                            dest='verify_ssl',
                            help='Enable SSL verification (False if disabled or path to CA bundle file)',
                            default=False)

    debug = parser.add_argument_group('Debug')
    debug.add_argument('-v', '--verbose', action='count', default=0,
                       help='increase output verbosity (use up to 3 times, CAUTION: may expose sensitive information!)')
    debug.add_argument('-t', '--timeout', default=10,
                       help='abort check execution after so many seconds (use 0 for no timeout)')
    debug.add_argument('--reset', action='store_true', help='Deletes the cookie file for the throughput check.')

    info = parser.add_argument_group('Info')
    info.add_argument('--version', action='version',
                      version='%(prog)s 0.3.2')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Sub-Parser for command 'diskspace'.
    parser_diskspace = subparsers.add_parser('diskspace',
                                             help='check used diskspace.',
                                             )
    parser_diskspace.add_argument('-w', '--warn',
                                  metavar='WARN', type=int, default=85,
                                  help='Warning if diskspace is greater. '
                                       '(default: %(default)s)')
    parser_diskspace.add_argument('-c', '--crit',
                                  metavar='CRIT', type=int, default=95,
                                  help='Critical if disksace is greater. '
                                       '(default: %(default)s)')

    parser_diskspace.set_defaults(func=diskspace)

    # Sub-Parser for command 'certificates'.
    parser_certificates = subparsers.add_parser(
        'certificates',
        help='check the certificate store for '
             'expiring certificates: Outputs is a warning, '
             'if a certificate is in range.')
    parser_certificates.add_argument(
        '-ex', '--exclude', default='', help='exclude certificates from '
                                             'check by name.')
    parser_certificates.add_argument(
        '-r', '--range',
        metavar='RANGE',
        default='0:20',
        help='''
        Warning if days until certificate expiration is in range:
        Represents a threshold range.
        The general format is "[@][start:][end]
        (default: %(default)s)
        ''')
    parser_certificates.set_defaults(func=certificate)

    # Sub-Parser for command 'licenses'.
    parser_licenses = subparsers.add_parser(
        'licenses',
        help='check the licenses for '
             'expiring licenses: Outputs is a warning, '
             'if a license is in range.')
    parser_licenses.add_argument(
        '-ex', '--exclude', default='', help='exclude licenses from '
                                             'check by name.')

    parser_licenses.add_argument('-w', '--warn',
                                  metavar='WARN', type=int, default=90,
                                  help='Warning if remaining license days is less than.'
                                       '(default: %(default)s)')
    parser_licenses.add_argument('-c', '--crit',
                                  metavar='CRIT', type=int, default=30,
                                  help='Critical if remaining license days is less than.'
                                       '(default: %(default)s)')
    parser_licenses.set_defaults(func=licenses)

    # Sub-Parser for command 'load'.
    parser_load = subparsers.add_parser(
        'load',
        help='check the CPU load.')
    parser_load.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=85,
        help='Warning if CPU load is greater. (default: %(default)s)')
    parser_load.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=95,
        help='Critical if CPU load is greater. (default: %(default)s)')
    parser_load.set_defaults(func=load)

    # Sub-Parser for command 'useragent'.
    parser_useragent = subparsers.add_parser(
        'useragent',
        help='check for running useragents.')
    parser_useragent.add_argument('-A', '--agent',
                            help='Agent name. Exmaple: all',)
    parser_useragent.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=60,
        help='Warning if agent is not responding for a given amount of seconds. (default: %(default)s)')
    parser_useragent.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=240,
        help='Critical if agent is not responding for a given amount of seconds. (default: %(default)s)')
    parser_useragent.set_defaults(func=useragent)

    # Sub-Parser for command 'environmental'.
    parser_environmental = subparsers.add_parser(
        'environmental',
        help='check if an alarm is found.')
    parser_environmental.set_defaults(func=environmental)

    # Sub-Parser for command 'powersupply'.
    parser_powersupply = subparsers.add_parser(
        'powersupply',
        help='check present power supplies.')
    parser_powersupply.add_argument(
    '-m', '--min',
    metavar='MIN', type=int, default=1,
    help='Warning if functional PSU is lower than specified. (default: %(default)s)')
    parser_powersupply.set_defaults(func=powersupply)


    parser_pppoe = subparsers.add_parser(
        'pppoe',
        help='check the pppoe interface.')

    parser_pppoe.add_argument(
        '-i', '--interface',
        help='PA interface name',
        nargs='?',
        required=True,
    )
    parser_pppoe.add_argument(
    '--expect-down',
    action='store_true',
    help='Expect PPPOE session to be down. (default: %(default)s)')

    parser_pppoe.add_argument(
        '-m', '--mtu',
        metavar='MTU', type=int, default=1492, dest="expect_mtu",
        help='Minimum expected MTU (default: %(default)s)')
    parser_pppoe.set_defaults(func=pppoe)

    # Sub-Parser for command 'sessinfo'.
    parser_sessinfo = subparsers.add_parser(
        'sessinfo',
        help='check important session parameters.')
    parser_sessinfo.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=20000,
        help='Warning if number of sessions is greater. (default: %(default)s)')
    parser_sessinfo.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=50000,
        help='Critical if number of sessions is greater. (default: %(default)s)')
    parser_sessinfo.set_defaults(func=sessioninfo)

    # Sub-Parser for command 'thermal'.
    parser_thermal = subparsers.add_parser(
        'thermal',
        help='check the temperature.')
    parser_thermal.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=40,
        help='Warning if temperature is greater. (default: %(default)s)')
    parser_thermal.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=45,
        help='Critical if temperature is greater. (default: %(default)s)')
    parser_thermal.set_defaults(func=thermal)

    # Sub-Parser for command 'throughput'.
    parser_throughput = subparsers.add_parser(
        'throughput',
        help='check the throughput.')

    parser_throughput.add_argument(
        '-i', '--interface',
        help='PA interface name, seperate by comma.',
        nargs='?',
        required=True,
    )
    parser_throughput.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=8000000000,
        help='Warning if throughput is greater. In bps (default: %(default)s)')
    parser_throughput.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=9000000000,
        help='Critical if throughput is greater. In bps (default: %(default)s)')
    parser_throughput.set_defaults(func=throughput)

    # Sub-Parser for command 'interface'.
    parser_interface = subparsers.add_parser(
        'interface',
        help='check the interfaces. If none specified will check all.')

    parser_interface.add_argument(
        '-i', '--interface',
        help='PA interface name. Give names, seperated by comma.',
        nargs='?',
    )

    parser_interface.add_argument(
        '-x', '--exclude',
        help='Exclude interfaces. Give names, seperated by comma.',
        nargs='?',
    )

    parser_interface.set_defaults(func=interface)

    # Sub-Parser for command 'cluster'.
    parser_cluster = subparsers.add_parser(
        'cluster',
        help='check the cluster status.')

    parser_cluster.add_argument(
        '-l', '--localstate',
        help='Expected Local Node Cluster State, either active or passive',
        nargs='?',
        required=True,
    )

    parser_cluster.add_argument(
        '-p', '--peerstate',
        help='Expected Peer Node Cluster State, either active or passive',
        nargs='?',
        required=True,
    )

    parser_cluster.set_defaults(func=cluster)

    # Sub-Parser for command 'antivirus'.
    parser_antivirus = subparsers.add_parser(
        'antivirus',
        help='check antivirus informations.')
    parser_antivirus.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=2,
        help='Warning if antivirus definition date is older. In days (default: %(default)s)')
    parser_antivirus.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=4,
        help='Critical if antivirus definition date is older. In days (default: %(default)s)')
    parser_antivirus.set_defaults(func=antivirus)

    # Sub-Parser for command 'threat'.
    parser_threat = subparsers.add_parser(
        'threat',
        help='check threat informations.')
    parser_threat.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=5,
        help='Warning if threat definition date is older. In days (default: %(default)s)')
    parser_threat.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=10,
        help='Critical if threat definition date is older. In days (default: %(default)s)')
    parser_threat.set_defaults(func=threat)

    # Sub-Parser for command 'threat'.
    parser_bgp = subparsers.add_parser(
        'bgp',
        help='check bgp informations.')
    parser_bgp.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=5,
        help='Warning if bgp routes/peer count is lesser (default: %(default)s)')
    parser_bgp.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=10,
        help='Critical if bgp routes/peer count is lesser (default: %(default)s)')
    parser_bgp.add_argument(
        '-m', '--mode',
        metavar="MODE", type=str,
        help='Mode: routes or peers',
        required=True)
    parser_bgp.add_argument(
        '-p', '--peer',
        metavar="PEER", type=str,
        help='Peer status (name, critical if not Established)',
        required=False)
    parser_bgp.set_defaults(func=bgp)

    # Sub-Parser for command 'qos'
    parser_qos = subparsers.add_parser(
        'qos',
        help='check quality of service.')
    parser_qos.add_argument(
        '-k', '--klass',
        metavar='KLASS', default='all',
        help='Define qos class',
        nargs='?',
       )
    parser_qos.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=8000000,
        help='Warning if qos is higher. In kbps (default: %(default))')
    parser_qos.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=9000000,
        help='Critical if qos is higher. In kbps (default: %(default))')
    parser_qos.set_defaults(func=qos)

    # Sub-Parser for command 'reports'.
    parser_reports = subparsers.add_parser(
        'reports',
        help='get reports values')
    parser_reports.add_argument(
        '-r', '--report',
        metavar="REPORT", type=str,
        help='Report name (ex: top-applications)',
        required=True)
    parser_reports.add_argument(
        '-n', '--name',
        metavar="NAME", type=str,
        help='Value name (ex: name)',
        required=True)
    parser_reports.add_argument(
        '-t', '--type',
        metavar="TYPE", type=str,
        help='Value type (ex: nbsess)',
        required=True)
    parser_reports.set_defaults(func=reports)

    return parser.parse_args(args)


if __name__ == '__main__':  # pragma: no cover
    main()
