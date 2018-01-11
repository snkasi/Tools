#!/usr/bin/env python
# Version 2.0 for deb-solution

import json
import yaml
import os
from optparse import OptionParser


def deunicodify_hook(pairs):
    '''to solve a problem, which json.loads always return unicode string'''
    new_pairs = []
    for key, value in pairs:
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        if isinstance(value, list):
            new_value = []
            for v in value:
                if isinstance(v, unicode):
                    v = v.encode('utf-8')
                new_value.append(v)
            value = new_value
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        new_pairs.append((key, value))
    return dict(new_pairs)


def set_dict(tdict, key, value):
    if isinstance(value, basestring):
        try:
            value = int(value)
        except ValueError:
            if str(value).lower() == 'false':
                value = False
            elif str(value).lower() == 'true':
                value = True
            elif str(value).lower() == 'null':
                value = None
            else:
                value = str(value)
    key_path = str(key).split('.')
    sdict = tdict
    for tkey in key_path[:-1]:
        if tkey not in sdict:
            sdict[tkey] = {}
        sdict = sdict[tkey]
    sdict[key_path[-1]] = value


def pop_dict(tdict, key):
    key_path = str(key).split('.')
    sdict = tdict
    for tkey in key_path[:-1]:
        if tkey in key_path:
            sdict = sdict[tkey]
        else:
            print '"%s" is not exist!' % str(tkey)
    try:
        sdict.pop(key_path[-1])
    except KeyError:
        print '"%s" is not exist!' % str(key)


def get_config_from_json(json_path, json_config):
    try:
        f = open(json_path, 'r')
        json_content = f.read()
        f.close()
        json_content = json.loads(
            json_content, object_pairs_hook=deunicodify_hook)
        result = json_content
        json_config_at = json_config.split('@')
        if len(json_config_at) > 1:
            json_config = json_config_at[0]
            index = int(json_config_at[-1])
        else:
            index = None
        for key in json_config.split('.'):
            result = result[key]
        if isinstance(index, int):
            result = result[index]
    except Exception as ex:
        print 'load json file error', ex
        result = None
    return result


def main(options):
    try:
        path = options.path
        f = open(path, 'r')
        content = f.read()
        f.close()

        content_dict = yaml.load(content)

        if options.set_config:
            params = str(options.set_config).split(';')
            for param in params:
                kv = param.split('=')
                if len(kv) == 2:
                    key, value = kv[0], kv[1]
                    if value == '@Invoke' and options.json_config:
                        value = get_config_from_json(
                            options.json_path, options.json_config)
                    set_dict(content_dict, key, value)
                else:
                    print '"%s" is not a Key-Value string!' % str(param)
        if options.del_config:
            params = str(options.del_config).split(';')
            for param in params:
                try:
                    pop_dict(content_dict, param)
                except:
                    print '"%s" is not exist!' % str(param)

        if options.reset_config:
            tdict = json.dumps(options.reset_config)
            content_dict = tdict

        f = open(path, 'w')
        f.write(yaml.dump(content_dict, default_flow_style=False))
        f.close()

    except Exception as ex:
        print str(ex)

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(base_dir, 'config.yaml')

    optparser = OptionParser()
    optparser.add_option('-p', '--path', dest='path',
                         help='path of yaml file', default=config_file)
    optparser.add_option('-s', '--set', dest='set_config',
                         default=None, help='set config, example: redis.host=127.0.0.1;')
    optparser.add_option('-d', '--delete', dest='del_config',
                         default=None, help='del config, example: redis.host;')
    optparser.add_option('-r', '--reset', dest='reset_config', default=None,
                         help='reset config, json, example: {"redis":{"host":"127.0.0.1", "port":6379}}')
    optparser.add_option('-j', '--jsonpath', dest='json_path', default='/etc/env.json',
                         help='json file path, example: /etc/env.json')
    optparser.add_option('-c', '--configread', dest='json_config', default=None,
                         help='which config from json file, example: env.pubredis.hosts[0]')

    options, args = optparser.parse_args()

    main(options)
