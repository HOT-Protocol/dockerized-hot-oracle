#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import click

ENV_CONF = '.env'
FEED_CONF = 'config/feed.conf'
RELAYER_CONF = 'config/relayer.conf'

class Pair(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

class EnvParser(object):
    def load(self, filename):
        lines = []
        with open(filename, 'r') as f:
            lines = f.readlines()
            f.close()

        result = dict()
        for line in lines:
            slice = line.strip().split('=', 2)
            if len(slice) != 2:
                continue
            result[slice[0]] = slice[1]
        return result

    def dump(self, obj, filename):
        f = open(filename, 'w')
        for key in obj:
            value = obj[key]
            f.write(key+'='+value+'\n')
        f.close()

@click.command()
@click.option('--network', prompt='1. Please choice network', type=click.Choice(['mainnet', 'ropsten', 'kovan', 'rinkeby', 'goerli']))
@click.option('--oracle', prompt='2. Please enter oracle address', default='0x', show_default=True)
@click.option('--infurakey', prompt='3. Please enter your <INFURAKEY>(https://infura.io)')
@click.option('--keystore', prompt='4. Please enter wallet keystore')
@click.option('--password', prompt='5. Please enter keystore unlock password')
def generate(network, oracle, infurakey, keystore, password):
    parser = EnvParser()
    env = parser.load(ENV_CONF)
    keyobject = json.loads(keystore)
    address = '0x'+keyobject['address']
    feed = json.load(open(FEED_CONF, 'r'))
    relayer = json.load(open(RELAYER_CONF, 'r'))

    env['ETH_NET'] = network
    env['ETH_KEY'] = keystore
    env['ETH_FROM'] = address
    env['INFURAKEY'] = infurakey
    env['ETH_PASSWORD'] = password
    feed['ethereum']['from'] = address
    feed['ethereum']['network'] = network
    relayer['ethereum']['from'] = address
    relayer['ethereum']['network'] = network
    relayer['pairs']['HOTGBP']['oracle'] = oracle

    parser.dump(env, ENV_CONF)
    json.dump(feed, open(FEED_CONF, 'w'), sort_keys=True, indent=2)
    json.dump(relayer, open(RELAYER_CONF, 'w'), sort_keys=True, indent=2)
    print('\nSuccessful!!!')

if __name__ == '__main__':
    generate()
