#!/bin/python3

import logging
import sys
import pprint as pp
import os
import yaml
import itertools


def rules_from_apis(raw_path):
    filename = os.path.basename(raw_path)
    rules = []
    with open(raw_path, 'r') as raw_file:
        for api in raw_file:
            api = api.replace('\xa0', '\x20').replace(u"\u200B", '').strip()
            paren_i = api.find('(')
            arg_list = api[paren_i+1:-2]
            arguments = arg_list.split(',')
            signature = []
            for arg in arguments:
                last_space = arg.rfind(' ')
                arg_type = arg[:last_space]
                signature.append(arg_type.strip())

            name = api[:paren_i]
            signature = ','.join(signature)

            rule = {}
            rule['Type'] = 'CallExpressionRule'
            rule['Attributes'] = {
                'javaType': filename,
                'javaMethodName': name,
                'javaMethodArgs': signature
            }
            rule['Comment'] = "\n\t{}\n\t==>\n\n".format(api.strip())
            rule['Body'] = {}

            rules.append(rule)
    return rules


def main():
    raw_path = sys.argv[1]
    rules_path = sys.argv[2]
    logging.getLogger().setLevel(logging.INFO)

    rules = rules_from_apis(raw_path)

    def grouper(item): return item['Attributes']['javaMethodName']
    with open(rules_path, 'w+') as yaml_file:
        for key, group_items in itertools.groupby(rules, key=grouper):
            yaml_file.write('#\n# {}.{}\n#\n'.format(
                os.path.basename(raw_path), key))
            yaml.dump(list(group_items), yaml_file, indent=4,
                      encoding='utf-8', sort_keys=False)


main()
