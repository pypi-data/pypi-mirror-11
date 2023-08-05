#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
'''
sail me
sail me set-acls 'cidr,cidr,cidr'

sail services add [<namespace>/]<repository>[:tag] [namespace/]<service-name>
            --model         Container model
            --number        Number of container to run
            [--link         name:alias]
            [--network      {public|private|<namespace name>}]
            [--network-allow [network:]ip[/mask] Use IPs whitelist]
            [--publish, -p  Publish a container's port to the host]
            [                 format: network:publishedPort:containerPort, network::containerPort, publishedPort:containerPort, containerPort]
            [--gateway      network-input:network-output]
            [--restart {no|always[:<max>]|on-failure[:<max>]}]
            [--volume       /path:size] (Size in GB)
            [--batch        do not attach console on start]
            [--redeploy     if the service already exists, redeploy instead]
	    [--pool <name>  use private hosts pool <name>]
       override docker options:
            --user
            --entrypoint
            --command
            --workdir
            --environment KEY=val
        other options:

sail services ps
sail services inspect [namespace/]service-name
sail services rm [namespace/]service-name
sail services redeploy [namespace/]service-name
            --model         Container model
            [--link         name:alias]
            [--network      {public|private|<namespace name>}]
            [--network-allow [network:]ip[/mask] Use IPs whitelist]
            [--publish, -p  Publish a container's port to the host]
            [                 format: network:publishedPort:containerPort, network::containerPort, publishedPort:containerPort, containerPort]
            [--restart      {no|always[:<max>]|on-failure[:<max>]}]
            [--gateway      network-input:network-output]
            [--volume       /path:size] (Size in GB)
            [--batch        do not attach console on start]
            [--pool <name>  use private hosts pool <name>]
            [--tag  <tag>   deploy from new image version]
       override docker options:
            --user
            --entrypoint
            --command
            --workdir
            --environment KEY=val

sail services scale --number <X> [namespace/]service-name
            [--batch        do not attach console on start]
sail services start [namespace/]service-name
            [--batch        do not attach console on start]
sail services stop [namespace/]service-name
sail services attach [namespace/]service-name
sail services logs [namespace/]service-name
	    [--tail         Return N last lines, before offset]
	    [--head         Return N first lines, after offset]
	    [--offset       Offset result by N line]
	    [--period       Lucene compatible period]

sail services attach-domain [namespace/]service-name domain
            [--pattern URI pattern]
            [--method  HTTP method to route]
sail services detach-domain [namespace/]service-name domain
            [--pattern URI pattern]
            [--method  HTTP method to route]

sail containers ps
sail containers inspect [namespace/]container-name
sail containers attach [namespace/]container-name
sail containers logs [namespace/]container-name
	    [--tail         Return N last lines, before offset]
	    [--head         Return N first lines, after offset]
	    [--offset       Offset result by N line]
	    [--period       Lucene compatible period]

sail repositories list
sail repositories add {hosted|external} [namespace/]repository-name
eail repositories rm [namespace/]repository-name

sail networks list
sail networks add [namespace/]network-name subnet
sail networks range-add [namespace/]network-name ip-from ip-to
sail networks rm [namespace/]network-name subnet

sail compose up <namespace>
    [-f, --file FILE            Specify an alternate fig file (default: docker-compose.yml)]
    [-p, --project-name NAME    Specify an alternate project name (default: directory name)]

sail compose get <namespace>
    [--standard                 Return a standard Docker Compose file]

configuration: (by priority)
    from command line
    from environment
    from .docker/config
    from .dockercfg

common options:
    -h --api-host           Docker index endpoint   [env: SAIL_HOST]
    -u --api-user           Docker index user       [env: SAIL_USER]
    -p --api-password       Docker index password   [env: SAIL_PASSWORD]
'''

import os
import sys
import json
import argparse, argcomplete
from base64 import b64decode
from datetime import datetime
import shlex

from tabulate import tabulate
import requests
import dateutil.parser
import requests.exceptions
import pyaml

ENDPOINT='sailabove.io'
DOCKERCFG='~/.docker/config.json'
DOCKERCFG_OLD='~/.dockercfg'
VERSION='0.5.6'

## Helpers

def ping(url):
    try:
        res = requests.get(url)
    except Exception:
        return False
    else:
        return res.status_code < 400

def expand_registry_url(hostname):
    if hostname.startswith('http:') or hostname.startswith('https:'):
        if '/' not in hostname[9:]:
            hostname = hostname + '/v1'
        return hostname
    if ping('https://' + hostname + '/v1/_ping'):
        return 'https://' + hostname + '/v1'
    return 'http://' + hostname + '/v1'

def parse_repository(repo, default_ns=None):
    column_index = repo.rfind(':')
    if column_index >= 0:
        tag = repo[column_index + 1:]
        repo = repo[:column_index]
    else:
        tag = None
    slash_index = repo.find('/')
    if slash_index >= 0:
        namespace = repo[:slash_index]
        repo = repo[slash_index + 1:]
    else:
        namespace = default_ns
    return namespace, repo, tag

def parse_port_publishing(port):
    '''
    Parse a port publishing parameter
    Format:
        network:publishedPort:containerPort
        network::containerPort,
        publishedPort:containerPort,
        containerPort
    '''

    port = port.split(':', 3)
    container_port = port.pop()
    published_port = container_port
    network = None

    if len(port) > 0:
        published_port = port.pop()
        if not published_port:
            published_port = container_port

    port_config = {
        'published_port': published_port
    }

    if len(port) > 0:
        port_config['network'] = port.pop()

    if '/' not in container_port:
        container_port = container_port + '/tcp'

    return container_port, port_config

def parse_volume(volume):
    '''
    Parse a volume parameter
    Format:
        /data:size
    '''
    try:
        volume_name, volume_size = volume.split(':', 1)
    except ValueError:
        volume_name, volume_size = (volume, 10)

    volume_config = {
        'size': volume_size
    }

    return volume_name, volume_config

def docker_parse_config_old(endpoint, debug):
    '''
    Try hard to load user's credentials from legacy dockercfg confuiguration
    file. Failing is an option
    '''
    path = os.path.expanduser(DOCKERCFG_OLD)

    conf = {
        'USERNAME': None,
        'PASSWORD': None,
    }

    try:
        with open(path) as f:
            parsed = json.load(f)
        if endpoint in parsed:
            auth = b64decode(parsed[endpoint]['auth']).split(':', 1)
            conf['USERNAME'] = auth[0]
            conf['PASSWORD'] = auth[1]
    except IOError:
        if debug:
            print >> sys.stderr, "[WARNING] Failed to read %s" % DOCKERCFG_OLD
    except ValueError:
        if debug:
            print >> sys.stderr, "[WARNING] Failed to parse %s" % DOCKERCFG_OLD

    return conf

def docker_parse_config(endpoint, debug):
    '''
    Try hard to load user's credentials from new docker configuration file.
    Failing is an option
    '''
    path = os.path.expanduser(DOCKERCFG)

    conf = {
        'USERNAME': None,
        'PASSWORD': None,
    }

    try:
        with open(path) as f:
            parsed = json.load(f)

        auths = parsed['auths']
        if endpoint in auths:
            auth = b64decode(auths[endpoint]['auth']).split(':', 1)
            conf['USERNAME'] = auth[0]
            conf['PASSWORD'] = auth[1]
    except IOError:
        if debug:
            print >> sys.stderr, "[WARNING] Failed to read %s" % DOCKERCFG
    except (ValueError, KeyError):
        if debug:
            print >> sys.stderr, "[WARNING] Failed to parse %s" % DOCKERCFG

    return conf

def _print(data):
    if isinstance(data, requests.Response):
        data = data.json()
    print pyaml.dump(data)

def _tabulate(data, headers):
    print(tabulate(data, headers, stralign='left', tablefmt='plain'))

def exit_exc(message, e, args):
    resource_desc = args.func.func_name.split('_')[1:]
    action = resource_desc[1]
    resource = resource_desc[0]
    object_name = getattr(args, resource, '')

    if isinstance(message, dict) and 'message' in message:
        message = message['message']

    print >> sys.stderr, "Failed to %s %s %s: %s" % (action, resource, object_name, message)

    if args.debug and e:
	import traceback
	traceback.print_exc()

    sys.exit(1)

def _console_loop(stream):
    print "Attaching to service console..."
    print "Press Ctrl+C to exit"

    try:
        for line in stream.iter_lines(chunk_size=1):
            print line
    except (KeyboardInterrupt, IOError):
        pass

## API methods

def api_request(args, method, path, data=None, headers=None, display=True, stream=False):
    url = expand_registry_url(args.api_host) + path

    if headers is None:
        headers = {}
    headers.update(json.loads(os.environ.get('SAIL_HEADERS', '{}')))
    headers['User-Agent'] = 'SailAbove CLI/' + VERSION

    kwargs = {
        'stream': stream,
        'headers': headers,
        'auth': (args.api_user, args.api_password),
    }

    if 'headers' in kwargs and 'Content-Type' in kwargs['headers']:
        kwargs['data'] = data
    elif method in ['PUT', 'POST']:
        kwargs['json'] = data
    else:
        kwargs['params'] = data

    if args.debug:
        print 'Request: %s %s' % (method, url)
        print 'Body: %s' %data
        print 'Headers: %s' %headers

    resp = requests.request(method, url, **kwargs)
    resp.raise_for_status()

    if stream:
        return resp

    if resp.headers['content-type'] != 'application/json':
        return resp.text

    if display or args.debug:
        _print(resp)

    return resp.json()

def api_me_show(args):
    return api_request(args, 'GET', '/users')

def api_me_set_acls(args):
    acls = [ip.strip() for ip in args.acl.split(',')]
    return api_request(args, 'PUT', '/user/acl', acls)

def api_app_list(args, display=True):
    return api_request(args, 'GET', '/applications', display=display)

def api_app_inspect(args, display=True):
    return api_request(args, 'GET', '/applications/%s' % args.app, display=display)

def api_app_domain_list(args):
    path = '/applications/%s/attached-domains' % args.app
    domains = api_request(args, 'GET', path, display=False)

    headers = ['DOMAIN', 'SERVICE', 'METHOD', 'PATTERN']
    displayed = []
    for domain, routes in domains.iteritems():
        if not routes:
            displayed.append([domain, '<detached>', '', ''])
        else:
            for route in routes:
                displayed.append([
                    domain,
                    '%s/%s' % (args.app, route['service']),
                    route['method'],
                    route['pattern'],
                ])

    if len(displayed) == 0:
        displayed.append(['', '', '', ''])
    _tabulate(displayed, headers)

def api_app_domain_attach(args):
    path = '/applications/%s/attached-domains/%s' % (args.app, args.domain)
    data = {}
    return api_request(args, 'POST', path, data)

def api_app_domain_detach(args):
    path = '/applications/%s/attached-domains/%s' % (args.app, args.domain)
    return api_request(args, 'DELETE', path)

def api_service_add(args):
    ns, repository, tag = parse_repository(args.repository, args.api_user)
    ns_service, service, _ = parse_repository(args.service, args.api_user)

    if args.entrypoint is not None:
        args.entrypoint = shlex.split(args.entrypoint)
    if args.command is not None:
        args.command = shlex.split(args.command)

    links = {}
    for link in args.link:
        link = link.split(':', 1)
        if len(link) == 1:
            links[link[0]] = link[0]
        else:
            links[link[0]] = link[1]

    networks = {}
    for network in args.network:
        networks[network] = {}

    if args.gateway:
        for gateway in args.gateway:
            gateway = gateway.split(':', 1)
            if len(gateway) != 2:
                exit_exc('Invalid gateway parameter, should be "input:output', None, args)
            if gateway[0] not in networks:
                exit_exc('Not configured input network %s' % gateway[0], None, args)
            if gateway[1] not in networks:
                exit_exc('Not configured input network %s' % gateway[1], None, args)
            if 'gateway_to' not in networks[gateway[0]]:
                networks[gateway[0]]['gateway_to'] = []
            networks[gateway[0]]['gateway_to'].append(gateway[1])

    if args.volume:
        volumes = dict((parse_volume(vol) for vol in args.volume))
    else:
        volumes = None

    params = {
        'namespace': ns,
        'repository': repository,
        'repository_tag': tag,
        'container_model': args.model,
        'container_number': int(args.number),
        'container_user': args.user,
        'container_entrypoint': args.entrypoint,
        'container_command': args.command,
        'container_workdir': args.workdir,
        'container_environment': args.env,
        'container_network': networks,
        'links': links,
        'volumes': volumes,
        'restart_policy': args.restart,
    }

    if args.pool:
	params['pool'] = args.pool

    if args.publish:
        params['container_ports'] = {}
        for port in args.publish:
            port, port_config = parse_port_publishing(port)
            if not port in params['container_ports']:
                params['container_ports'][port] = []
            params['container_ports'][port].append(port_config)

    if args.network_allow:
        for ip in args.network_allow:
            # Normalize
            if ':' in ip:
                network, ip = ip.split(':', 1)
            else:
                network = None

            if not 'container_ports' in params:
                print >> sys.stderr, "[ERROR] To declare a whitelisted IP, you need to explicit publish (-p) the ports of your container"
                return True

            # Add whitelist
            for port, portconfig in params['container_ports'].iteritems():
                for config in portconfig:
                    if config.get('network', None) == network or \
                       None == network or 'network' not in config:
                        if not 'whitelisted_cidrs' in config:
                            config['whitelisted_cidrs'] = []
                        config['whitelisted_cidrs'].append(ip)

    path = '/applications/%s/services/%s?stream' % (ns_service, service)
    try:
        resp = api_request(args, 'POST', path, params, stream=True)
    except Exception as e:
        print e
        raise

    for msg in resp.iter_lines(chunk_size=1):
        msg = json.loads(msg)
        if 'message' in msg:
            print msg.get('message', None)
        elif 'error' in msg:
            # If we are in ensure mode, fallback to redeploy
            if msg.get('error', -1) == 409 and args.redeploy:
                args.tag = tag
                return api_service_redeploy(args)
            return exit_exc(msg.get('error_details'), Exception(msg), args)

    # Spawn stream and start the service
    args.service = ns_service + '/' + service
    return api_service_start(args)

def api_service_delete(args):
    ns, service, _ = parse_repository(args.service, args.api_user)
    path = '/applications/%s/services/%s/' % (ns, service)
    return api_request(args, 'DELETE', path)

def api_service_redeploy(args):
    ns, service, _ = parse_repository(args.service, args.api_user)
    path = '/applications/%s/services/%s/redeploy?stream' % (ns, service)

    if args.entrypoint is not None:
        args.entrypoint = shlex.split(args.entrypoint)
    if args.command is not None:
        args.command = shlex.split(args.command)

    params = {}

    if args.link:
        links = {}
        for link in args.link:
            link = link.split(':', 1)
            if len(link) == 1:
                links[link[0]] = link[0]
            else:
                links[link[0]] = link[1]
        params['links'] = links

    if args.pool:
	params['pool'] = args.pool
    if args.model:
        params['container_model'] = args.model
    if args.user:
        params['container_user'] = args.user
    if args.entrypoint:
        params['container_entrypoint'] = args.entrypoint
    if args.command:
        params['container_command'] = args.command
    if args.workdir:
        params['container_workdir'] = args.workdir
    if args.env:
        params['container_environment'] = args.env
    if args.tag:
	params['repository_tag'] = args.tag
    if args.volume:
        params['volumes'] = dict((parse_volume(vol) for vol in args.volume))

    if args.network:
        networks = {}
        for network in args.network:
            networks[network] = {}
        params['container_network'] = networks

    if args.publish:
        params['container_ports'] = {}
        for port in args.publish:
            port, port_config = parse_port_publishing(port)
            if not port in params['container_ports']:
                params['container_ports'][port] = []
            params['container_ports'][port].append(port_config)

    if args.network_allow:
        for ip in args.network_allow:
            # Normalize
            if ':' in ip:
                network, ip = ip.split(':', 1)
            else:
                network = None

            if not 'container_ports' in params:
                print >> sys.stderr, "[ERROR] To declare a whitelisted IP, you need to explicit publish (-p) the ports of your container"
                return True

            # Add whitelist
            for port, portconfig in params['container_ports'].iteritems():
                for config in portconfig:
                    if config.get('network', None) == network or None == network:
                        if not 'whitelisted_cidrs' in config:
                            config['whitelisted_cidrs'] = []
                        config['whitelisted_cidrs'].append(ip)

    if args.gateway:
        if not 'container_network' in params:
            exit_exc('Network configuration is compulsory to configure gateway', None, args)

        for gateway in args.gateway:
            gateway = gateway.split(':', 1)
            if len(gateway) != 2:
                exit_exc('Invalid gateway parameter, should be "input:output', None, args)
            if gateway[0] not in networks:
                exit_exc('Not configured input network %s' % gateway[0], None, args)
            if gateway[1] not in networks:
                exit_exc('Not configured input network %s' % gateway[1], None, args)
            if 'gateway_to' not in networks[gateway[0]]:
                networks[gateway[0]]['gateway_to'] = []
            params['container_network'][gateway[0]]['gateway_to'].append(gateway[1])

    if not args.batch:
        stream = api_service_attach(args, return_generator=True)

    resp = api_request(args, 'POST', path, params, stream=True)
    status = None
    for msg in resp.iter_lines(chunk_size=1):
        msg = json.loads(msg)
        if 'message' in msg:
            print msg.get('message', None)
        elif 'error' in msg:
            return exit_exc(msg.get('error_details'), Exception(msg), args)
        else:
            print "\nRedeployed service:"
            status = msg['state']
            _print(msg)

    if status not in ['running', 'degraded']:
        print "\nService failed %s to start (%s)." % (args.service, status)
        return

    # Are we done yet ?
    if args.batch:
        return

    return _console_loop(stream)

def api_service_start(args):
    ns, service, _ = parse_repository(args.service, args.api_user)
    path = '/applications/%s/services/%s/start?stream' % (ns, service)

    if not args.batch:
        stream = api_service_attach(args, return_generator=True)

    print "\nStarting service..."
    resp = api_request(args, 'POST', path, {}, stream=True)

    status = None
    for msg in resp.iter_lines(chunk_size=1):
        msg = json.loads(msg)
        if 'message' in msg:
            print msg.get('message', None)
        elif 'error' in msg:
            return exit_exc(msg.get('error_details'), Exception(msg), args)
        else:
            print "\nService %s/%s running:" % (ns, service)
            status = msg['state']
            _print(msg)

    if status not in ['running', 'degraded']:
        print "\nService failed %s to start (%s)." % (args.service, status)
        return

    # Are we done yet ?
    if args.batch:
        return

    # Spawn stream and start the service
    return _console_loop(stream)

def api_service_stop(args):
    ns, service, _ = parse_repository(args.service, args.api_user)
    path = '/applications/%s/services/%s/stop' % (ns, service)
    return api_request(args, 'POST', path, {})

def api_service_scale(args):
    ns, service, _ = parse_repository(args.service, args.api_user)
    path = '/applications/%s/services/%s/scale?stream' % (ns, service)
    params = {
        'container_number': int(args.number)
    }
    resp = api_request(args, 'POST', path, params, stream=True)

    for msg in resp.iter_lines(chunk_size=1):
        msg = json.loads(msg)
        if 'message' in msg:
            print msg.get('message', None)
        elif 'error' in msg:
            return exit_exc(msg.get('error_details'), Exception(msg), args)

    # Spawn stream and start the service
    return api_service_start(args)

def api_service_ps(args):
    if args.namespace:
        applications = [args.namespace]
    else:
        applications = api_app_list(args, display=False)

    displayed = []
    headers = ['NAME', 'REPOSITORY', 'IMAGE ID', 'STATE', 'CONTAINERS', 'CREATED', 'NETWORK']
    for application in applications:
        path = '/applications/%s/services' % (application)
        services = api_request(args, 'GET', path, display=False)
        for service in services:
            path = '/applications/%s/services/%s' % (application, service)
            service = api_request(args, 'GET', path, display=False)

            ips = []
            for container in service['containers'].values():
                for name, network in container['network'].items():
                    ips.append("%s:%s" % (name, network['ip']))

            displayed.append([
                '%s/%s' % (application, service['name']),
                '%s@%s' % (service['repository'], service['repository_tag']),
                service['image'][:12],
                service['state'].capitalize(),
                service['container_number'],
                dateutil.parser.parse(service['creation_date']).replace(tzinfo=None),
                ', '.join(ips),
            ])

    if len(displayed) == 0:
        displayed.append(['', '', '', '', '', ''])
    _tabulate(displayed, headers)

def api_service_inspect(args):
    ns, service, _ = parse_repository(args.service, args.api_user)
    path = '/applications/%s/services/%s/' % (ns, service)
    return api_request(args, 'GET', path)

def api_service_attach(args, return_generator=False):
    ns, service, _ = parse_repository(args.service, args.api_user)
    path = '/applications/%s/services/%s/attach' % (ns, service)
    r = api_request(args, 'GET', path, stream=True)
    if return_generator:
        return r
    try:
        for line in r.iter_lines(chunk_size=1):
            print line
    except (KeyboardInterrupt, IOError):
        pass

def api_service_logs(args):
    ns, service, _ = parse_repository(args.service, args.api_user)
    req = {}
    if args.tail: req['tail'] = args.tail
    if args.head: req['head'] = args.head
    if args.offset: req['offset'] = args.offset
    if args.period: req['period'] = args.period
    if args.search: req['search'] = args.search
    path = '/applications/%s/services/%s/logs' % (ns, service)
    for line in api_request(args, 'GET', path, req, display=False):
        print ' '.join(line)

def api_service_domain_list(args):
    ns, service, _ = parse_repository(args.service, args.api_user)
    path = '/applications/%s/services/%s/attached-routes' % (ns, service)
    routes = api_request(args, 'GET', path, display=False)

    headers = ['DOMAIN', 'METHOD', 'PATTERN']
    displayed = []
    for route in routes:
        displayed.append([
            route['domain'],
            route['method'],
            route['pattern'],
        ])

    if len(displayed) == 0:
        displayed.append(['', ''])
    _tabulate(displayed, headers)

def api_service_domain_attach(args):
    ns, service, _ = parse_repository(args.service, args.api_user)
    path = '/applications/%s/services/%s/attached-routes/%s' % (ns, service, args.domain)
    data = {
        'pattern': args.pattern,
        'method': args.method,
    }
    return api_request(args, 'POST', path, data)

def api_service_domain_detach(args):
    ns, service, _ = parse_repository(args.service, args.api_user)
    path = '/applications/%s/services/%s/attached-routes/%s' % (ns, service, args.domain)
    data = {
        'pattern': args.pattern,
        'method': args.method,
    }
    return api_request(args, 'DELETE', path, data)

def api_container_ps(args):
    if args.namespace:
        applications = [args.namespace]
    else:
        applications = api_app_list(args, display=False)
    displayed = []
    for application in applications:
        path = '/applications/%s/containers' % (application)
        containers = api_request(args, 'GET', path, display=False)
        headers = ['APP', 'SERVICE', 'CONTAINER', 'STATE', 'DEPLOYED']
        for container in containers:
            path = '/applications/%s/containers/%s' % (application, container)
            container = api_request(args, 'GET', path, display=False)
            displayed.append([
                application,
                container['service'],
                container['name'],
                container['state'].capitalize(),
                container['deployment_date'].split('.')[0].replace('T', ' ')
            ])

    if len(displayed) == 0:
        displayed.append(['', '', '', '', '', ''])
    _tabulate(displayed, headers)

def api_container_inspect(args):
    ns, container, _ = parse_repository(args.container, args.api_user)
    path = '/applications/%s/containers/%s/' % (ns, container)
    return api_request(args, 'GET', path)

def api_container_attach(args):
    ns, container, _ = parse_repository(args.container, args.api_user)
    path = '/applications/%s/containers/%s/attach' % (ns, container)
    r = api_request(args, 'GET', path, stream=True)
    try:
        for line in r.iter_lines(chunk_size=1):
            print line
    except (KeyboardInterrupt, IOError):
        pass

def api_container_logs(args):
    ns, container, _ = parse_repository(args.container, args.api_user)
    req = {}
    if args.tail: req['tail'] = args.tail
    if args.head: req['head'] = args.head
    if args.offset: req['offset'] = args.offset
    if args.period: req['period'] = args.period
    path = '/applications/%s/containers/%s/logs' % (ns, container)
    for line in api_request(args, 'GET', path, req, display=False):
        print ' '.join(line)

def api_compose_up(args):
    if args.file is None:
        args.file = os.path.join(args.project_name, 'docker-compose.yml')

    yml_path = os.path.join(args.project_name, args.file)
    try:
        with open(yml_path, 'r') as f:
            compose_payload = f.read()
    except IOError as e:
        exit_exc(yml_path + ': ' + e.strerror, e, args)

    path = '/applications/%s/fig/up?stream' % args.namespace
    headers = {
        'Content-Type': 'application/x-yaml'
    }
    r = api_request(args, 'POST', path, compose_payload, headers=headers, stream=True)
    for msg in r.iter_lines(chunk_size=1):
        msg = json.loads(msg)
        if 'message' in msg:
            if 'object_type' in msg:
                msg['message'] = '[' + msg['object_type'] + '] ' + msg['message']
            print msg['message']
        elif 'error' in msg:
            return exit_exc(msg.get('error_details'), Exception(msg), args)

def api_compose_get(args):
    path = '/applications/%s/fig?standard=%s' % (args.namespace, args.standard)
    r = api_request(args, 'GET', path)
    print r

def api_repository_list(args):
    if args.namespace:
        applications = [args.namespace]
    else:
        applications = api_app_list(args, display=False)
    displayed = []
    headers = ['NAME', 'TAG', 'TYPE', 'PRIVACY', 'SOURCE']
    for application in applications:
        path = '/repositories/%s' % (application)
        repositories = api_request(args, 'GET', path, display=False)
        for repository in repositories:
            path = '/repositories/%s/%s' % (application, repository)
            repository = api_request(args, 'GET', path, display=False)
            tags = repository.get('tags') or ['-']
            for tag in sorted(tags):
                displayed.append([
                    '%s/%s' % (application, repository['name']),
                    tag,
                    repository['type'],
                    repository['privacy'],
                    repository['source'] or '-',
                ])

    if len(displayed) == 0:
        displayed.append(['', '', '', '', '', '', ''])
    _tabulate(displayed, headers)

def api_repository_add(args):
    ns, repository, _ = parse_repository(args.repository, args.api_user)
    path = '/repositories/%s/%s' % (ns, repository)
    params = {
        'namespace': ns,
        'repository': repository,
        'type': args.type,
        'source': args.source,
    }
    return api_request(args, 'POST', path, params)

def api_repository_delete(args):
    ns, repository, _ = parse_repository(args.repository, args.api_user)
    path = '/repositories/%s/%s' % (ns, repository)
    return api_request(args, 'DELETE', path, {})

def api_network_list(args):
    if args.namespace:
        applications = [args.namespace]
    else:
        applications = api_app_list(args, display=False)
    displayed = []
    headers = ['NAME', 'SUBNET']
    for application in applications:
        path = '/applications/%s/networks' % (application)
        networks = api_request(args, 'GET', path, display=False)
        for network in networks:
            path = '/applications/%s/networks/%s' % (application, network)
            network = api_request(args, 'GET', path, display=False)
            displayed.append([
                network['name'],
                network['subnet'] or '-'
            ])

    if len(displayed) == 0:
        displayed.append(['', ''])
    _tabulate(displayed, headers)

def api_network_inspect(args):
    ns, network, _ = parse_repository(args.network, args.api_user)
    path = '/applications/%s/networks/%s' % (ns, network)
    network = api_request(args, 'GET', path, display=False)
    network['ranges'] = api_request(args, 'GET', path + '/ranges', display=False)
    return _print(network)

def api_network_add(args):
    ns, network, _ = parse_repository(args.network, args.api_user)
    path = '/applications/%s/networks/%s' % (ns, network)
    params = {
        'subnet': args.subnet
    }
    return api_request(args, 'POST', path, params)

def api_network_range_add(args):
    ns, network, _ = parse_repository(args.network, args.api_user)
    path = '/applications/%s/networks/%s/ranges/%s-%s' % (
        ns, network, args.ip_from, args.ip_to)
    return api_request(args, 'POST', path, {})

def api_network_delete(args):
    ns, network, _ = parse_repository(args.network, args.api_user)
    path = '/applications/%s/networks/%s' % (ns, network)
    return api_request(args, 'DELETE', path, {})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='OVH Docker as a Service CLI')

    parser.add_argument('-H', '--api-host',
                        help='Docker index host [env: SAIL_HOST] or [%s]' % ENDPOINT,
                        default=None)
    parser.add_argument('-u', '--api-user',
                        help='Docker index user [env: SAIL_USER] or [file: .docker/config]',
                        default=None)
    parser.add_argument('-p', '--api-password',
                        help='Docker index password [env: SAIL_PASSWORD] or [file: .docker/config]',
                        default=None)
    parser.add_argument('--debug', help='Debug the API requests', action='store_true')

    subparsers = parser.add_subparsers()

    # me
    me_parser = subparsers.add_parser('me', help='Account')
    me_sub = me_parser.add_subparsers()

    me_show = me_sub.add_parser('show', help='show acount details')
    me_show.set_defaults(func=api_me_show)

    me_set_acls = me_sub.add_parser('set-acls', help='Set ip based account access restrictions')
    me_set_acls.add_argument('acl', help='"1.2.3.4/24,4.5.6.7/32" form')
    me_set_acls.set_defaults(func=api_me_set_acls)

    # app-list
    app_parser = subparsers.add_parser('apps', help='Applications')
    app_sub = app_parser.add_subparsers()

    app_list = app_sub.add_parser('list', help='List granted apps')
    app_list.set_defaults(func=api_app_list)

    # app-show
    app_inspect = app_sub.add_parser('inspect', help='Details of an app')
    app_inspect.add_argument('app', help='application')
    app_inspect.set_defaults(func=api_app_inspect)

    # app-domain-list
    app_domain_list = app_sub.add_parser('domain-list', help='List domains and routes on the HTTP load balancer')
    app_domain_list.add_argument('app', help='application')
    app_domain_list.set_defaults(func=api_app_domain_list)

    # app-domain-attach
    app_domain_attach = app_sub.add_parser('domain-attach', help='Attach a domain on the HTTP load balancer')
    app_domain_attach.add_argument('app', help='application')
    app_domain_attach.add_argument('domain', help='domain to attach to this application')
    app_domain_attach.set_defaults(func=api_app_domain_attach)

    # app-domain-detach
    app_domain_detach = app_sub.add_parser('domain-detach', help='Detach a domain from the HTTP load balancer')
    app_domain_detach.add_argument('app', help='application')
    app_domain_detach.add_argument('domain', help='domain to detach from this application')
    app_domain_detach.set_defaults(func=api_app_domain_detach)

    # service-add
    service_parser = subparsers.add_parser('services', help='Services')
    service_sub = service_parser.add_subparsers()
    service_add = service_sub.add_parser('add',
                                         help='Add a new docker service')

    service_add.add_argument('repository', help='[namespace/]repository:tag')
    service_add.add_argument('service', help='the new service name')

    service_add.add_argument('--model', help='the containers model',
                             default='x1')
    service_add.add_argument('--pool', help='use dedicated pool')
    service_add.add_argument('--number', help='number of containers to launch',
                             default=1)

    service_add.add_argument('--user', help='override docker user')
    service_add.add_argument('--entrypoint', help='override docker entrypoint')
    service_add.add_argument('--command', help='override docker run command')
    service_add.add_argument('--workdir', help='override docker workdir')
    service_add.add_argument('--restart', help='Docker like restart policy (no, always[:max], on-failure[:max])',
                             default='no')
    service_add.add_argument('-e', '--env', help='override docker environment',
                             action='append', default=[])
    service_add.add_argument('--link', help='link to another service',
                             action='append', default=[])
    service_add.add_argument('-p', '--publish',
        help='publish ports: network:publishedPort:containerPort, network::containerPort, publishedPort:containerPort, containerPort',
        action='append',default=[])
    service_add.add_argument('--network', help='Specify service network {public|private|<namespace name>/<network-name>}. "public" assigns a public IP, "private" selects this namespace\'s private network (default: [public, private])',
                             action='append', default=[])
    service_add.add_argument('--network-allow', help='Use IPs whitelist fo network [network:]ip[/mask][:port]',
                             action='append', default=[])
    service_add.add_argument('--gateway', help='Use service as gateway for a network. e.g. "private:public", will use the service as a gateway for the "private" network to the "public" network.',
                             action='append', default=[])
    service_add.add_argument('--volume', help='Add a persistent volume and mount it, e.g. "/data:42" will create a 42GB persistent volume and mount it in the /data directory. This directory must exist in the Docker image or be a VOLUME.',
                             action='append', default=[])
    service_add.add_argument('--redeploy', action='store_true', help='if the service already exists, redeploy it')
    service_add.add_argument('--batch', action='store_true', help='do not attach console on start')
    service_add.set_defaults(func=api_service_add)

    # service-delete
    service_delete = service_sub.add_parser('rm', help='Delete a docker service')
    service_delete.add_argument('service', help='[namespace/]service name')
    service_delete.set_defaults(func=api_service_delete)

    # service-attach
    service_attach = service_sub.add_parser('attach', help='Attach to the console of the service containers')
    service_attach.add_argument('service', help='[namespace/]service name')
    service_attach.set_defaults(func=api_service_attach)

    # service-logs
    service_logs = service_sub.add_parser('logs', help='Fetch the logs of a service')
    service_logs.add_argument('service', help='[namespace/]service name')
    service_logs.add_argument('--tail', type=int, default=0, help="Return N last lines, before offset. Max: 500. Default:10")
    service_logs.add_argument('--head', type=int, default=0, help="Return N first lines, after offset. Max: 500")
    service_logs.add_argument('--offset', type=int, default=0, help="Offset result by N line")
    service_logs.add_argument('--period', type=str, default="24 hours ago", help="Lucene compatible period")
    service_logs.add_argument('--search', type=str, default="", help="Only return matching lines")
    service_logs.set_defaults(func=api_service_logs)

    # service-list
    service_ps = service_sub.add_parser('ps', help='List docker services')
    service_ps.add_argument('-n', '--namespace', help='the namespace name')
    service_ps.set_defaults(func=api_service_ps)

    service_inspect = service_sub.add_parser('inspect', help='Inspect a docker service')
    service_inspect.add_argument('service', help='[namespace/]service name')
    service_inspect.set_defaults(func=api_service_inspect)

    # service-redeploy
    service_redeploy = service_sub.add_parser('redeploy', help='Redeploy a docker service')
    service_redeploy.add_argument('service', help='[namespace/]service name')
    service_redeploy.add_argument('--model', help='the containers model')
    service_redeploy.add_argument('--pool', help='use dedicated pool')
    service_redeploy.add_argument('--user', help='override docker user')
    service_redeploy.add_argument('--entrypoint', help='override docker entrypoint')
    service_redeploy.add_argument('--command', help='override docker run command')
    service_redeploy.add_argument('--workdir', help='override docker workdir')
    service_redeploy.add_argument('--tag', help='deploy from new image version')
    service_redeploy.add_argument('--restart', help='Docker like restart policy (no, always[:max], on-failure[:max])')
    service_redeploy.add_argument('-e', '--env', help='override docker environment',
                             action='append', default=[])
    service_redeploy.add_argument('--link', help='link to another service',
                             action='append', default=[])
    service_redeploy.add_argument('-p', '--publish',
        help='publish ports: network:publishedPort:containerPort, network::containerPort, publishedPort:containerPort, containerPort',
        action='append',default=[])
    service_redeploy.add_argument('--network', help='Specify service network {public|private|<namespace name>}. "public" assigns a public IP, "private" selects this namespace\'s private network (default: [public, private])',
                             action='append', default=[])
    service_redeploy.add_argument('--network-allow', help='Use IPs whitelist fo network [network:]ip[/mask][:port]',
                             action='append', default=[])
    service_redeploy.add_argument('--gateway', help='Use service as gateway for a network. e.g. "private:public", will use the service as a gateway for the "private" network to the "public" network.',
                             action='append', default=[])
    service_redeploy.add_argument('--volume', help='Add a persistent volume and mount it, e.g. "/data:42" will create a 42GB persistent volume and mount it in the /data directory. This directory must exist in the Docker image or be a VOLUME.',
                             action='append', default=[])
    service_redeploy.add_argument('--batch', action='store_true', help='do not attach console on start')
    service_redeploy.set_defaults(func=api_service_redeploy)

    # service-stop
    service_stop = service_sub.add_parser('stop', help='Stop a docker service')
    service_stop.add_argument('service', help='[namespace/]service name')
    service_stop.set_defaults(func=api_service_stop)

    # service-start
    service_start = service_sub.add_parser('start', help='Start a docker service')
    service_start.add_argument('service', help='[namespace/]service name')
    service_start.add_argument('--batch', action='store_true', help='do not attach console on start')
    service_start.set_defaults(func=api_service_start)

    # service-scale
    service_scale = service_sub.add_parser('scale', help='Scale a docker service')
    service_scale.add_argument('service', help='[namespace/]service name')
    service_scale.add_argument('--number', help='scale to `number` of containers')
    service_scale.add_argument('--batch', action='store_true', help='do not attach console on start')
    service_scale.set_defaults(func=api_service_scale)

    # service-domain-list
    service_attach = service_sub.add_parser('domain-list', help='List domains on the HTTP load balancer')
    service_attach.add_argument('service', help='[namespace/]service name')
    service_attach.set_defaults(func=api_service_domain_list)

    # service-domain-attach
    service_attach = service_sub.add_parser('domain-attach', help='Attach a domain on the HTTP load balancer')
    service_attach.add_argument('service', help='[namespace/]service name')
    service_attach.add_argument('domain')
    service_attach.add_argument('-p', '--pattern', default='/', help='attach for URIs matching pattern')
    service_attach.add_argument('-m', '--method', default='*', help='attach for METHOD requests')
    service_attach.set_defaults(func=api_service_domain_attach)

    # service-domain-detach
    service_detach = service_sub.add_parser('domain-detach', help='Detach a domain from the HTTP load balancer')
    service_detach.add_argument('service', help='[namespace/]service name')
    service_detach.add_argument('domain')
    service_detach.add_argument('-p', '--pattern', default='/')
    service_detach.add_argument('-m', '--method', default='*')
    service_detach.set_defaults(func=api_service_domain_detach)

    # container-list
    container_parser = subparsers.add_parser('containers', help='Containers')
    container_sub = container_parser.add_subparsers()

    # container-list
    container_ps = container_sub.add_parser('ps', help='List docker containers')
    container_ps.add_argument('-n', '--namespace', help='the namespace name')
    container_ps.set_defaults(func=api_container_ps)

    # container-inspect
    container_inspect = container_sub.add_parser('inspect', help='Inspect a docker container')
    container_inspect.add_argument('container', help='[namespace/]container name')
    container_inspect.set_defaults(func=api_container_inspect)

    # container-attach
    container_attach = container_sub.add_parser('attach', help='Attach to a container console')
    container_attach.add_argument('container', help='[namespace/]container name')
    container_attach.set_defaults(func=api_container_attach)

    # container-logs
    container_logs = container_sub.add_parser('logs', help='Fetch the logs of a container')
    container_logs.add_argument('container', help='[namespace/]container name')
    container_logs.add_argument('--tail', type=int, default=0, help="Return N last lines, before offset. Default:10")
    container_logs.add_argument('--head', type=int, default=0, help="Return N first lines, after offset")
    container_logs.add_argument('--offset', type=int, default=0, help="Offset result by N line")
    container_logs.add_argument('--period', type=str, default="24 hours ago", help="Lucene compatible period")
    container_logs.add_argument('--search', type=str, default="", help="Only return matching lines")
    container_logs.set_defaults(func=api_container_logs)

    # compose
    compose_parse = subparsers.add_parser('compose', help='Docker compose')
    compose_sub = compose_parse.add_subparsers()

    # compose-up
    compose_up = compose_sub.add_parser('up', help='Create and start containers')
    compose_up.add_argument('namespace', help='The namespace where to apply the docker compose / fig')
    compose_up.add_argument('-f', '--file',
        help='Specify an alternate compose file (default: docker-compose.yml)')
    compose_up.add_argument('-p', '--project-name',
        help='Specify an alternate project name (default: directory name)', default=os.getcwd())
    compose_up.set_defaults(func=api_compose_up)

    # compose-get
    compose_get = compose_sub.add_parser('get', help='Export Docker compose receipt')
    compose_get.add_argument('namespace', help='The namespace to export as compose file')
    compose_get.add_argument('--standard',
        help='Return only Docker Compose standard properties', action='store_true')
    compose_get.set_defaults(func=api_compose_get)

    # repositories-list
    repository_parser = subparsers.add_parser('repositories', help='Repositories')
    repository_sub = repository_parser.add_subparsers()

    repository_list = repository_sub.add_parser('list',
                                                help='List the docker repository')
    repository_list.add_argument('-n', '--namespace', help='the namespace name')
    repository_list.set_defaults(func=api_repository_list)

    # repositories-add
    repository_add = repository_sub.add_parser('add',
                                               help='Add a new docker repository')
    repository_add.add_argument('type', help='The type of repository {hosted,external}')
    repository_add.add_argument('repository', help='[namespace/]repository')
    repository_add.add_argument('-s', '--source', help='For external repositories, the source (e.g. registry.hub.docker.com/redis)')
    repository_add.set_defaults(func=api_repository_add)

    # repositories-delete
    repository_delete = repository_sub.add_parser('rm',
                                                  help='Delete a repository')
    repository_delete.add_argument('repository', help='[namespace/]repository')
    repository_delete.set_defaults(func=api_repository_delete)

    # networks-list
    network_parser = subparsers.add_parser('networks', help='Networks')
    network_sub = network_parser.add_subparsers()

    network_list = network_sub.add_parser('list',
                                          help='List the docker private networks')
    network_list.add_argument('-n', '--namespace', help='the namespace name')
    network_list.set_defaults(func=api_network_list)

    # networks-inspect
    network_inspect = network_sub.add_parser('inspect',
                                             help='Inspect the docker private networks')
    network_inspect.add_argument('network', help='[namespace/]network')
    network_inspect.set_defaults(func=api_network_inspect)

    # networks-add
    network_add = network_sub.add_parser('add',
                                         help='Add a new private network')
    network_add.add_argument('network', help='[namespace/]network')
    network_add.add_argument('subnet', help='Network subnet')
    network_add.set_defaults(func=api_network_add)

    # networks-range-add
    network_range_add = network_sub.add_parser(
        'range-add', help='Add an allocation range to a private network')
    network_range_add.add_argument('network', help='[namespace/]network')
    network_range_add.add_argument('ip_from', help='IP from')
    network_range_add.add_argument('ip_to', help='IP to')
    network_range_add.set_defaults(func=api_network_range_add)

    # network-delete
    network_delete = network_sub.add_parser('rm', help='Delete a private network')
    network_delete.add_argument('network', help='[namespace/]network name')
    network_delete.set_defaults(func=api_network_delete)

    # load conf: user
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    # compute configuration
    if not args.api_host:
        if 'SAIL_HOST' in os.environ:
            args.api_host = os.environ['SAIL_HOST']
        else:
            args.api_host = ENDPOINT

    # load conf: new file then old file (pre-docker 1.7.0)
    dockercfg = docker_parse_config(args.api_host, args.debug)
    if dockercfg['USERNAME'] is None:
        dockercfg = docker_parse_config_old(args.api_host, args.debug)
    if dockercfg['USERNAME'] is None:
        print >> sys.stderr, "[WARNING] Failed to read credentials from configuration files"

    if not args.api_user:
        if 'SAIL_USER' in os.environ:
            args.api_user = os.environ['SAIL_USER']
        else:
            args.api_user = dockercfg['USERNAME']

    if not args.api_password:
        if 'SAIL_PASSWORD' in os.environ:
            args.api_password = os.environ['SAIL_PASSWORD']
        else:
            args.api_password = dockercfg['PASSWORD']

    if not args.api_user or not args.api_password:
        print >> sys.stderr, "Missing --api-user or --api-password"
        sys.exit(1)

    # start real work
    try:
        args.func(args)
    except KeyboardInterrupt:
        print "Interrupted..."
    except requests.exceptions.HTTPError as e:

        status = e.response.status_code

        if status == 401:
            exit_exc("Authentication failed for user '%s'" % args.api_user, e, args)
        elif status == 403:
            exit_exc("Access denied for user '%s'" % args.api_user, e, args)
        elif status == 404:
            exit_exc("Object not found", e, args)
        elif status < 499 or status == 409:
            exit_exc(e.response.json(), e, args)
        elif status in [501, 502, 503, 504]:
            exit_exc("Service maintenance", e, args)
        else:
            exit_exc("Internal error", e, args)

    except requests.exceptions.ConnectionError as e:
        exit_exc("Error: connection failed.", e, args)
    except requests.exceptions.Timeout as e:
        exit_exc("Error: timeout while waiting for server's response", e, args)
    except requests.exceptions.RequestException as e:
        exit_exc("Error: unknown request error", e, args)
    except Exception as e:
        if 'error_status' in e.message:
            message = e.message['error_status']
        else:
            message = str(e.message)
        exit_exc("Internal CLI error: "+message, e, args)
