#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import subprocess
from subprocess import PIPE

ENV_CONF = '.env'
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

def tojson(s):
    slice = []
    for line in s.splitlines():
        if len(line) > 0 and line[0] != '#':
            slice.append(line)
    return json.loads('\r\n'.join(slice))

def update_feed(feed):
    relayer = json.load(open(RELAYER_CONF, 'r'))
    relayer['feeds'] = [feed]
    json.dump(relayer, open(RELAYER_CONF, 'w'), sort_keys=True, indent=2)

def update_ssb_invite(ssb_invite):
    parser = EnvParser()
    env = parser.load(ENV_CONF)
    env['SSB_INVITE'] = ssb_invite
    parser.dump(env, ENV_CONF)

def main():
    (_, output) = subprocess.Popen('docker-compose up -d ssb', stdout=PIPE, stderr=PIPE).communicate()
    output = str(output, 'utf8')
    if output.find('done') == -1 and output.find('up-to-date') == -1:
        raise(RuntimeError(output))

    (output, stderr) = subprocess.Popen('docker-compose exec ssb ssb-server invite.create 999', stdout=PIPE, stderr=PIPE).communicate()
    if len(stderr) > 0:
        raise(RuntimeError(stderr))
    ssb_invite = str(output, 'utf8').strip().replace('"', '')
    update_ssb_invite(ssb_invite)

    (_, output) = subprocess.Popen('docker-compose up -d feed', stdout=PIPE, stderr=PIPE).communicate()
    output = str(output, 'utf8')
    if output.find('done') == -1 and output.find('up-to-date') == -1:
        raise(RuntimeError(output))

    (output, stderr) = subprocess.Popen('docker-compose exec feed cat /home/omnia/.ssb/secret', stdout=PIPE, stderr=PIPE).communicate()
    if len(stderr) > 0:
        raise(RuntimeError(stderr))
    output = str(output, 'utf8')
    feed = tojson(output)['id']
    update_feed(feed)

    (_, output) = subprocess.Popen('docker-compose up -d relayer', stdout=PIPE, stderr=PIPE).communicate()
    output = str(output, 'utf8')
    if output.find('done') == -1 and output.find('up-to-date') == -1:
        raise(RuntimeError(output))
    
    os.system('docker-compose ps')

if __name__ == '__main__':
    main()
