#
# A script to generate the (simple and composite) intents dataset.
#


import itertools
import json
import random
import sys


all_intent_examples = {}
MAX_INTENTS = 400  # Use this to change the size of the dataset
INTENT_DESCRIPTOR = 'intent_descriptor.json'


# AVOID -> , : = ( ) in text when using entity extraction


def create_flow_unicast():
    label = 'create_flow'
    intent_examples = []

    endpoints = [
        '10.0.0.1',
        '219.41.0.9',
        '74.0.0.6',
        'host1',
        'host 37',
        'h1',
        'h49',
        'Host ABC1_2',
        'Host 19',
        'core switch',
        'switch s1_b2',
        's1',
        's37',
        's_9',
        'AB:cd:12:e3:f4:5e',
        'A01b2c3d4e5f',
    ]

    for src in endpoints:
        for tgt in endpoints:
            if tgt == src:
                continue

            r = random.random()

            if r < 0.01:
                continue

            if random.random() < 0.5:
                intent_examples.append('transfer packets from [{}](source) to [{}](target) '
                                       'at a rate [not less than](operator:GTE) [100 kilobits/s](qos)'
                                       .format(src, tgt))
            else:
                intent_examples.append('send packets from [{}](source) to [{}](target) '
                                       'at a rate [not less than](operator:GTE) [100 kilobits/s](qos)'
                                       .format(src, tgt))
            intent_examples.append('configure service from [{}](source) to [{}](target) at [0.5 MBps](qos)'
                                   .format(src, tgt))
            if random.random() < 0.5:
                intent_examples.append('add flow from [{}](source) to [{}](target) with [0.5 MBps](qos)'
                                       .format(src, tgt))
            else:
                intent_examples.append('create flow from [{}](source) to [{}](target) at [0.5 MBps](qos)'
                                       .format(src, tgt))
            intent_examples.append('create the following flow: [{}](source) [{}](target) [0.5 MBps](qos)'
                                   .format(src, tgt))
            intent_examples.append('allow communication between [{}](source) and [{}](target)'.format(src, tgt))
            intent_examples.append('files to be sent to [{}](target) from [{}](source)'.format(tgt, src))
            intent_examples.append('allocate flows from [{}](source) to [{}](target)'.format(src, tgt))
            if random.random() < 0.75:
                intent_examples.append('create a flow from [{}](source) to [{}](target) as target'
                                       .format(src, tgt))
            else:
                intent_examples.append('creat a flow from [{}](source) to [{}](target) as target'
                                       .format(src, tgt))
            intent_examples.append('create a flow with [{}](source) as source and [{}](target) as target'
                                   .format(src, tgt))
            intent_examples.append('set up a flow between [{}](source) & [{}](target)'.format(src, tgt))
            intent_examples.append('route traffic from [{}](source) to [{}](target) with [minimum](operator:GTE) '
                                   'bandwidth of [2.1 mbps](qos)'
                                   .format(src, tgt))
            intent_examples.append('create a flow between [{}](source) and [{}](target) with '
                                   '[at least](operator:GTE) [1Gbps](qos)'
                                   .format(src, tgt))
            intent_examples.append('install a flow from [{}](source) to [{}](target) with [at most](operator:LTE) '
                                   'bandwidth of [20.2 KB/s](qos)'
                                   .format(src, tgt))
            intent_examples.append('add a route between [{}](source) & [{}](target)'.format(src, tgt))
            intent_examples.append('create a shortest path from [{}](source) to [{}](target) and '
                                   'let the packets flow'
                                   .format(src, tgt))
            intent_examples.append('install rules for [{}](source) & [{}](target) communication'.format(src, tgt))

    # -> doesn't get recognized
    # print('[10.0.0.1](source) -> [100.1.15.2](target)')
    # print('[Host_1](source) -> [host2](target)')
    # print('[ab:cd:ef:10:07:11](source) -> [a1:b2:c3:d4:e5:f6](target)')

    # No entity intent_examples
    intent_examples.append('can you please create a flow')
    intent_examples.append('install a flow')
    intent_examples.append('please do a flow allocation for me')
    intent_examples.append('hey there! I need a flow')
    intent_examples.append('create a flow')
    intent_examples.append('create one service')
    intent_examples.append('setup flow')
    intent_examples.append('set up a service')
    intent_examples.append('allocate this flow')
    intent_examples.append('create a flo from 100.1.1.2 to 215.94.18.3')

    intent_examples.append('setup flo')
    intent_examples.append('creat flow')
    intent_examples.append('add flows')
    intent_examples.append('flow frm')

    random.shuffle(intent_examples)
    intent_examples = intent_examples[:MAX_INTENTS]
    all_intent_examples[label] = intent_examples
    return intent_examples


def allocate_optimally():
    label = 'allocate_batch'
    intent_examples = []

    # Optimal allocation of a set of flows would consist of several source, target, and QoS entities.
    # This intent has no associated entity, it recognizes based on the text. 
    # Actual source, target, and QoS entities are to be
    # identified separately perhaps using a series of regular expressions.
    
    endpoints = [
        [('97.81.54.60', '19.71.82.41', '71.0.2.101',), ('210.0.0.11', '110.0.0.4', '30.0.0.11',),],
        [('210.0.0.11', '110.0.0.4', '30.0.0.11',), ('97.81.54.60', '19.71.82.41', '71.0.2.101',),],
        [('200.23.56.28', '200.14.57.72', '201.21.26.88',), ('H_21', 'H_22', 'H_34'),],
        [('H_21', 'H_22', 'H_34'), ('200.23.56.28', '200.14.57.72', '201.21.26.88',),],
        [('s81', 's22', 's24',), ('s1', 's1', 's35',),],
        [('s4_h1', 's4_h2', 's10_h1',), ('s22_h32', 's9_h78', 's11_h11',),],
        [('s1', 's1', 's35',), ('s4_h1', 's4_h2', 's10_h1',),],
        [('s22_h32', 's9_h78', 's11_h11',), ('s81', 's22', 's24',),],
        [('switch s12', 'switch s12', 'switch s3',), ('switch s29', 'switch s30', 'switch s39',),],
        [('host1', 'host2', 'host3',), ('host15', 'host2', 'host11',),],
        [(12, 8, 101,), (9, 197, 34)],
        [('AB:cd:12:e3:f4:5e', 'cc:08:12:23:f4:e1', 'c0:1d:a2:43:f1:69',), ('AB:cd:12:e3:f4:2e', 'cc:08:12:43:f4:e1', 'c0:1d:a2:43:f1:89',),],
        [('h64', 'h101', 'h5',), ('h32', 'h303', 'h40',),],
    ]

    for src, tgt in endpoints:
            intent_examples.append('allocate the following flows:  '
                                   'source [{}](source) to target [{}](target) having rate [100 kilobits/s](qos)  '
                                   'source [{}](source) to target [{}](target) having rate [200 kilobits/s](qos) '
                                   'source [{}](source) to target [{}](target) rate [135.79 kilobits/s](qos) '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('allocate the following flows:  '
                                   'src [{}](source) tgt [{}](target) rate [10.40 KBit/s](qos) '
                                   'src [{}](source) tgt [{}](target) rate [20.50 KBit/s](qos) '
                                   'src [{}](source) tgt [{}](target) rate [13.79 KBit/s](qos) '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('optimally allocate the following:  '
                                   'src [{}](source) tgt [{}](target) [10.40](qos) '
                                   'src [{}](source) tgt [{}](target) [20.50](qos) '
                                   'src [{}](source) tgt [{}](target) [13.79](qos) '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('batch install:  '
                                   'from [{}](source) to [{}](target) such that bandwidth is [70 kilobits/s](qos) '
                                   'from [{}](source) to [{}](target) such that bandwidth is [100 kilobits/s](qos) '
                                   'from [{}](source) to [{}](target) such that bandwidth is [300 kilobits/s](qos) '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('[{}](source) | [{}](target) | [100 kilobits/s](qos)  '
                                   '[{}](source) | [{}](target) | [200 kilobits/s](qos)  '
                                   '[{}](source) | [{}](target) | [345 kilobits/s](qos)  '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('send data from '
                                   '[{}](source) [{}](target) [2](qos)  '
                                   '[{}](source) [{}](target) [5](qos)  '
                                   '[{}](source) [{}](target) [11](qos)  '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('[{}](source), [{}](target), [43](qos)  '
                                   '[{}](source), [{}](target), [19](qos)  '
                                   '[{}](source), [{}](target), [56](qos)  '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('install these  '
                                   '[{}](source) [{}](target) [8](qos)  '
                                   '[{}](source) [{}](target) [7](qos)  '
                                   '[{}](source) [{}](target) [23](qos)  '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('add these flows  '
                                   '[{}](source), [{}](target) '
                                   '[{}](source), [{}](target) '
                                   '[{}](source), [{}](target) '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('[{}](source) to [{}](target) '
                                   '[{}](source) to [{}](target) '
                                   '[{}](source) to [{}](target) '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('optimally create the flows from given sources to destinations  '
                                   '[{}](source), [{}](target), [1.2 mbps](qos) '
                                   '[{}](source), [{}](target), [4.7 mbps](qos) '
                                   '[{}](source), [{}](target), [6.9 mbps](qos) '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('optimize the following allocations: '
                                   '[{}](source), [{}](target), [2](qos)  '
                                   '[{}](source), [{}](target), [5](qos)  '
                                   '[{}](source), [{}](target), [11](qos)  '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('allow communication '
                                   '[{}](source) [{}](target) b/w [201.2 KB/s](qos) '
                                   '[{}](source) [{}](target) b/w [300.5 KB/s](qos) '
                                   '[{}](source) [{}](target) b/w [190 KB/s](qos)'
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('configure these services '
                                   'origin [{}](source), destination [{}](target), data rate [1Gbps](qos) '
                                   'origin [{}](source), destination [{}](target), data rate [11Gbps](qos) '
                                   'origin [{}](source), destination [{}](target), data rate [12.5Gbps](qos)'
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('optimally install  '
                                   '[{}](source), [{}](target), [1 Mbps](qos) '
                                   '[{}](source), [{}](target), [20 Kbps](qos) '
                                   '[{}](source), [{}](target), [1123.4 Mb/s](qos)'
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('Can you find an optimal allocation for these services?  '
                                   's [{}](source) d [{}](target) b [6 mbps](qos) '
                                   's [{}](source) d [{}](target) b [11 mbps](qos) '
                                   's [{}](source) d [{}](target) b [1.3 mbps](qos) '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('solve this optimalm flow allocation problem  '
                                   '[{}](source), [{}](target), [22 mbps](qos) '
                                   '[{}](source), [{}](target), [14 mbps](qos) '
                                   '[{}](source), [{}](target), [39 mbps](qos) '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('use optimal resources to enable this set of flows  '
                                   '[{}](source), [{}](target), [.43](qos)  '
                                   '[{}](source), [{}](target), [.19](qos)  '
                                   '[{}](source), [{}](target), [.56](qos)  '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('allocate bandwidth paths for these '
                                   '[{}](source), [{}](target), [21](qos)  '
                                   '[{}](source), [{}](target), [5.8](qos)  '
                                   '[{}](source), [{}](target), [32.5](qos)  '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))
            intent_examples.append('do a network wide flow optimsation  '
                                   '[{}](source), [{}](target), [2](qos)  '
                                   '[{}](source), [{}](target), [5](qos)  '
                                   '[{}](source), [{}](target), [11](qos)  '
                                   .format(src[0], tgt[0], src[1], tgt[1], src[2], tgt[2]))


    # -> doesn't get recognized
    # print('[10.0.0.1](source) -> [100.1.15.2](target)')
    # print('src=[Host_1](source) tgt=[host2](target)')
    # print('[ab:cd:ef:10:07:11](source) -> [a1:b2:c3:d4:e5:f6](target)')

    # No entity intent_examples
    intent_examples.append('can you please create a batch of flows?')
    intent_examples.append('install a set of flows')
    intent_examples.append('hey there! I need to configure a few services')
    intent_examples.append('optimally install flows')
    intent_examples.append('configure services optimally')
    intent_examples.append('set up these services')
    intent_examples.append('allocate flows')
    intent_examples.append('add flows')

    intent_examples.append('add flowz')
    intent_examples.append('create shortest paths')

    random.shuffle(intent_examples)
    intent_examples = intent_examples[:MAX_INTENTS]
    all_intent_examples[label] = intent_examples
    return intent_examples


def apply_filter():
    label = 'apply_filter'
    intent_examples = []
    endpoints = [
        '10.0.0.1',
        '219.41.0.9',
        '74.0.0.6',
        'host1',
        'host 37',
        'h1',
        'h49',
        'Host ABC1_2',
        'Host 19',
        'core switch',
        'switch s1_b2',
        's1',
        's37',
        's_9',
        'AB:cd:12:e3:f4:5e',
        'A01b2c3d4e5f',
    ]

    for src in endpoints:
        for tgt in endpoints:
            if tgt == src:
                continue

            intent_examples.append('[open](action:ALLOW) [HTTPS](port:443) between [{}](source) and [{}](target)'
                                   .format(src, tgt))
            intent_examples.append('from [{}](source) to [{}](target), [https](port:443)'
                                   .format(src, tgt))
            intent_examples.append('[{}](source) and [{}](target) [should not be able](action:DENY) to access '
                                   '[websites](port:80)'
                                   .format(src, tgt))
            intent_examples.append('[{}](source) and [{}](target) [should be able](action:ALLOW) to access '
                                   '[websites](port:80)'
                                   .format(src, tgt))
            intent_examples.append('for host [{}](source), [close](action:DENY) TCP [port 443](port:443)'
                                   .format(src))
            intent_examples.append('[allow](action:ALLOW) [{}](source) and [{}](target) to communicate via '
                                   'UDP [port 500](port:500)'
                                   .format(src, tgt))
            intent_examples.append('[block](action:DENY) [apache server](port:80) at host [{}](source)'
                                   .format(src))
            intent_examples.append('[Drop](action:DENY) all packets from [port 23](port:23) at [{}](source)'
                                   .format(src))
            intent_examples.append('let [web traffic](port:80) pass between [{}](source) and [{}](target)'
                                   .format(src, tgt))
            intent_examples.append('[Allow](action:ALLOW) ICMP [ping](port:7) for host [{}](source)'
                                   .format(src))
            intent_examples.append('[allow](action:ALLOW) [{}](source) and [{}](target) to [ping](port:7) each other'
                                   .format(src, tgt))
            intent_examples.append('[enable](action:ALLOW) [ping](port:7) from [{}](source) to [{}](target) '
                                   'for troubleshooting'
                                   .format(src, tgt))
            intent_examples.append('run [web server](port:80) at [{}](source) and let [{}](target) '
                                   '[access it](action:ALLOW)'
                                   .format(src, tgt))
            intent_examples.append('[web service](port:80) [should be accessible](action:ALLOW) by [{}](source) '
                                   'and [{}](target)'
                                   .format(src, tgt))
            intent_examples.append('[ping service](port:7) [should be accessible](action:ALLOW) by [{}](source) '
                                   'and [{}](target)'
                                   .format(src, tgt))

    intent_examples.append('[allow](action:ALLOW) [http](port:80)')
    intent_examples.append('[allow](action:ALLOW) [web traffic](port:80)')
    intent_examples.append('[do not allow](action:DENY) any [web traffic](port:80)')
    intent_examples.append('[Enable](action:ALLOW) [ping](port:7)')
    intent_examples.append('[allow](action:ALLOW) the hosts to [ping](port:7)')
    intent_examples.append('[disable](action:DENY) ICMP [ping](port:7)')
    intent_examples.append('the hosts [should have](action:ALLOW) [web access](port:80)')
    intent_examples.append('[open](action:ALLOW) [websites](port:80)')

    random.shuffle(intent_examples)
    intent_examples = intent_examples[:MAX_INTENTS-3]
    intent_examples.append('only [websites](port:80) are [allowed](action:ALLOW)')
    intent_examples.append('and only [Web](port:80) is [allowed](action:ALLOW)')
    intent_examples.append('only [ping](port:7) is [enabled](action:ALLOW)')
    all_intent_examples[label] = intent_examples
    return intent_examples


def remove_flow():
    label = 'remove_flow'
    intent_examples = []

    endpoints = [
        '10.0.0.1',
        '219.41.0.9',
        '74.0.0.6',
        'host1',
        'host 37',
        'h1',
        'h49',
        'Host ABC1_2',
        'Host 19',
        'core switch',
        'switch s1_b2',
        's1',
        's37',
        's_9',
        'AB:cd:12:e3:f4:5e',
        'A01b2c3d4e5f',
    ]


    for src in endpoints:
        for tgt in endpoints:
            if tgt == src:
                continue

            intent_examples.append('remove flow from [{}](source) to [{}](target) '.format(src, tgt))
            intent_examples.append('remove the route from [{}](source) to [{}](target) '.format(src, tgt))
            intent_examples.append('halt communication between [{}](source) and [{}](target) '.format(src, tgt))
            intent_examples.append('stop packets from [{}](source) to [{}](target) '.format(src, tgt))
            intent_examples.append('delete [{}](source) to [{}](target) flow'.format(src, tgt))
            intent_examples.append('delete [{}](source) to [{}](target) packet path'.format(src, tgt))
            intent_examples.append('rm flow between [{}](source) & [{}](target) '.format(src, tgt))
            intent_examples.append('del flow [{}](source) to [{}](target)'.format(src, tgt))
            intent_examples.append('del flow [{}](source) & [{}](target)'.format(src, tgt))
            intent_examples.append('disallow communication between [{}](source) and [{}](target)'.format(src, tgt))
            intent_examples.append('uninstall [{}](source) to [{}](target) route'.format(src, tgt))
            intent_examples.append('delete flow between [{}](source) and [{}](target) '.format(src, tgt))
            intent_examples.append('deallocate [{}](source) to [{}](target)'.format(src, tgt))
            intent_examples.append('unallocate [{}](source) to [{}](target) communication'.format(src, tgt))
            intent_examples.append('uninstall the flow between [{}](source) & [{}](target) '.format(src, tgt))
            intent_examples.append('uninstall the path between [{}](source) & [{}](target) '.format(src, tgt))
            intent_examples.append('deactivate flow between [{}](source) & [{}](target) '.format(src, tgt))

    # No entity intent_examples
    intent_examples.append('can you please remove a flow?')
    intent_examples.append('uninstall a flow')
    intent_examples.append('please delete a flow')
    intent_examples.append('hey there! I need to deallocate a flow')
    intent_examples.append('undo flow')
    intent_examples.append('remove flow')
    intent_examples.append('rm flo frm')
    intent_examples.append('delete flo')

    random.shuffle(intent_examples)
    intent_examples = intent_examples[:MAX_INTENTS]
    all_intent_examples[label] = intent_examples
    return intent_examples


def stop():
    label = 'stop'
    intent_examples = [
        '/stop',
        'stop',
        'bye',
        'Thanks',
        'quit',
        'q',
        'exit'
    ]

    all_intent_examples[label] = intent_examples
    return intent_examples


def unsupported_intent():
    label = 'unsupported_intent'
    intent_examples = [
        'set up multicast',
        'set up a multicast flow',
        'set up a multicast service',
        'enable multi casting among',
        'allow multicasting among hosts',
        'join multicast group',
        'leave multicast group',
        'create a multi-cast group',
        'create geocast',
        'set up a geocast flow',
        'allow geocast between 10.0.0.1 and 10.0.0.2',
        'provide geo-casting service',
        'install geocasting',
        'set up VLAN',
        'create a V-LAN',
        'enable vxlan',
        'how to VxLAN',
        'assign multicast',
        'add to a multimedia multicast group',
        'install a virtual LAN',
        'initiate virtual area network',
        'set up a VPN',
        'connect to virtual network',
        'login to virtual private network',
        'join vpn',
        'create a VLAN for multicast',
        'tunnel traffic',
        'create a tunnel',
        'enable tunneling',
        'set up a tunnel',
        'take down this network',
        'how can I hack into you',
    ]

    all_intent_examples[label] = intent_examples
    return intent_examples


if __name__ == '__main__':
    #
    # - Create a unicast flow
    # - Remove a flow
    # - Apply filter (port filtering)
    # - Optimally allocate a bunch of flows
    #
    
    create_flow_unicast()
    allocate_optimally()
    apply_filter()
    remove_flow()

    COMPOSITE2 = True
    COMPOSITE3 = COMPOSITE2 and False

    for key in all_intent_examples.keys():
        print('\n## intent:{}'.format(key))
        sys.stdout.write('- ')
        print('\n- '.join(all_intent_examples[key]))
        print('')

    skip_composition = {'stop', 'unsupported_intent'}
    keys = set(all_intent_examples.keys())
    keys = keys.difference(skip_composition)

    # Not all k-composite intents are supported
    supported_intents = json.loads(open(INTENT_DESCRIPTOR, 'r').read())

    for intent in supported_intents:
        madeof = supported_intents[intent].get('madeof', [])
        degree = len(madeof)
        if COMPOSITE2 and degree == 2:
            key1, key2 = madeof[0], madeof[1]
            composite = '{}+{}'.format(key1, key2)
            
            list1, list2, = all_intent_examples[key1], all_intent_examples[key2]

            print('\n## intent:{}'.format(composite))
            for element in random.sample(set(itertools.product(list1, list2)), MAX_INTENTS):
                r = random.random()
                
                if r < 0.20:
                    print('- {}  {}'.format(element[0], element[1]))
                elif r < 0.40:
                    print('- {} and also {}'.format(element[0], element[1]))
                elif r < 0.60:
                    print('- {} . In addition, {}'.format(element[0], element[1]))
                elif r < 0.80:
                    print('- {} as well as {}'.format(element[0], element[1]))
                else:
                    print('- {} and ensure that {}'.format(element[0], element[1]))
            print('')
            

    COMPOSITE2 = False
    
    # 2-composition
    if COMPOSITE2:
        for key in itertools.combinations(keys, 2):
            key1, key2 = key
            composite = '{}+{}'.format(key1, key2)
            print(composite)
            if composite not in supported_intents:
                continue
            
            list1, list2, = all_intent_examples[key1], all_intent_examples[key2]

            print('\n## intent:{}'.format(composite))
            for element in random.sample(set(itertools.product(list1, list2)), MAX_INTENTS):
                print('- {}'.format(' '.join(element)))
            print('')

    # 3-composition
    if COMPOSITE3:
        for key in itertools.combinations(keys, 3):
            key1, key2, key3 = key
            composite = '{}+{}+{}'.format(key1, key2, key3)
            if composite not in supported_intents:
                continue
            
            list1, list2, = all_intent_examples[key1], all_intent_examples[key2]

            print('\n## intent:{}'.format(composite))
            for element in random.sample(set(itertools.product(list1, list2, list3)), MAX_INTENTS):
                print('- {}'.format(' '.join(element)))
            print('')



