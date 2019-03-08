#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pycontrol.pycontrol as pc
import os

host = 'xxx.xxx.xxx.xxx'
user = 'xxxxxx'
password = 'xxxxxx'

def lb(wsdls):
    wsdl_dir = os.path.abspath(os.path.dirname(__file__)) + '/wsdl'

    return pc.BIGIP(
        hostname = host,
        username = user,
        password = password,
        fromurl = False,
        directory = wsdl_dir,
        wsdls = wsdls
    )

def get_vs_list():
    bigip = lb(['LocalLB.VirtualServer'])
    vs = bigip.LocalLB.VirtualServer
    return vs.get_list()

def get_pool_list():
    bigip = lb(['LocalLB.Pool'])
    p = bigip.LocalLB.Pool
    return p.get_list()

def set_pool_member_state_enable(pool_name, members):
    bigip = lb(['LocalLB.Pool'])
    p = bigip.LocalLB.Pool

    ms = []
    ss = []
    for m in members:
        member = p.typefactory.create('Common.AddressPort')
        member.address = m['name']
        member.port = int(m['port'])
        ms.append(member)
        state = p.typefactory.create('Common.EnabledState').STATE_ENABLED
        ss.append(state)
    member_seq = p.typefactory.create('Common.AddressPortSequence')
    member_seq.item = ms
    member_seq_seq = p.typefactory.create('Common.AddressPortSequenceSequence')
    member_seq_seq.item = member_seq

    ses_seq = p.typefactory.create('Common.EnabledStateSequence')
    ses_seq.item = ss
    ses_seq_seq = p.typefactory.create('Common.EnabledStateSequenceSequence')
    ses_seq_seq.item = ses_seq

    p.set_member_session_enabled_state([pool_name], member_seq_seq, ses_seq_seq)

def set_pool_member_state_disable(pool_name, members):
    bigip = lb(['LocalLB.Pool'])
    p = bigip.LocalLB.Pool

    ms = []
    ss = []
    for m in members:
        member = p.typefactory.create('Common.AddressPort')
        member.address = m['name']
        member.port = int(m['port'])
        ms.append(member)
        state = p.typefactory.create('Common.EnabledState').STATE_DISABLED
        ss.append(state)
    member_seq = p.typefactory.create('Common.AddressPortSequence')
    member_seq.item = ms
    member_seq_seq = p.typefactory.create('Common.AddressPortSequenceSequence')
    member_seq_seq.item = member_seq

    ses_seq = p.typefactory.create('Common.EnabledStateSequence')
    ses_seq.item = ss
    ses_seq_seq = p.typefactory.create('Common.EnabledStateSequenceSequence')
    ses_seq_seq.item = ses_seq

    p.set_member_session_enabled_state([pool_name], member_seq_seq, ses_seq_seq)

def get_node_list():
    bigip = lb(['LocalLB.NodeAddressV2'])
    node = bigip.LocalLB.NodeAddressV2
    return node.get_list()

def create_node(node_name, ip, limits=0):
    bigip = lb(['LocalLB.NodeAddressV2'])
    node = bigip.LocalLB.NodeAddressV2
    try:
        node.create([node_name], [ip], [limits])
    except:
        raise

def delete_node(node_name):
    bigip = lb(['LocalLB.NodeAddressV2'])
    node = bigip.LocalLB.NodeAddressV2
    try:
        node.delete_node_address([node_name])
    except:
        raise

def get_node_address(node_name):
    bigip = lb(['LocalLB.NodeAddressV2'])
    node = bigip.LocalLB.NodeAddressV2
    return node.get_address([node_name])

if __name__ == '__main__':
    print "===== Disable node ====="
    set_pool_member_state_disable('Pool_xxxx', [{'name':'xxxx', 'port':80}])

    print "===== Enable node ====="
    set_pool_member_state_enable('Pool_xxxx', [{'name':'xxxx', 'port':80}])

    print "===== VirtualServer ====="
    print get_vs_list()

    print "===== Pool ====="
    print get_pool_list()

    print "===== Node ====="
    print get_node_list()

    print "===== Create Node ====="
    create_node('pycontrol_node', '192.168.50.101')
    print "===== Node Address ====="
    print get_node_address('pycontrol_node')

    #print "===== Delete Node ====="
    #delete_node('pycontrol_node')

    print "===== Node ====="
    print get_node_list()