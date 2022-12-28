#!/bin/python3

import logging
import sys
import pprint as pp
import os
import yaml
import itertools
import argparse


def parse_fields(data_path, out_path):
    rules = []
    with open(data_path, 'r') as data_file:
        for line in data_file:
            if '# Fields' in line:
                break
        for field in data_file:
            field = field.strip()
            if not len(field):
                continue
            if '#' in field:
                break

            rule = {}
            rule['Type'] = 'MemberAccessExpressionRule'
            rule['Attributes'] = {
                'javaMemberName': field,
                'arktsName': ""
            }
            rules.append(rule)
    with open(out_path, 'a') as yaml_file:
        yaml_file.write('#\n# Fields {}\n#\n'.format(
            os.path.basename(data_path)))
        yaml.dump(rules, yaml_file, indent=4,
                  encoding='utf-8', sort_keys=False)


def rules_from_apis(data_path):
    rules = []
    with open(data_path, 'r') as data_file:
        for line in data_file:
            if '# API' in line:
                break

        for api in data_file:
            api = api.replace('\xa0', '\x20').replace(u"\u200B", '').strip()
            if not len(api):
                continue
            if '#' in api:
                break

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
                'javaMethodName': name,
                'javaMethodArgs': signature
            }
            # rule['Comment'] = "\n\t{}\n\t==>\n\n".format(api.strip())
            rule['Body'] = {}

            rules.append(rule)
    return rules


def parse_api(data_path, out_path):
    rules = rules_from_apis(data_path)
    def grouper(item): return item['Attributes']['javaMethodName']
    with open(out_path, 'w+') as yaml_file:
        for key, group_items in itertools.groupby(rules, key=grouper):
            yaml_file.write('#\n# {}.{}\n#\n'.format(
                os.path.splitext(os.path.basename(data_path))[0], key))
            yaml.dump(list(group_items), yaml_file, indent=4,
                      encoding='utf-8', sort_keys=False)


def add_typeref(out_path):
    with open(out_path, 'a') as yaml_file:
        yaml.dump([{
            'Type': 'TypeReferenceRule',
            'Attributes': {
                'arktsName': ""
            }
        }], yaml_file, indent=4,
            encoding='utf-8', sort_keys=False)


def parse_markdown(data_path, language, symbol):
    import markdown as md

    symbol_headline = '### ' + symbol
    with open(data_path, 'r') as data_file:
        for line in data_file:
            if symbol_headline in line:
                break
        table_lines = []
        for line in data_file:
            if '|' in line:
                table_lines.append(line)
            elif line.startswith('#'):
                break
        table = md.markdown(''.join(table_lines))
        print(table)


def main():
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='', required=True)
    parser.add_argument('-o', '--output', help='')
    parser.add_argument('-v', '--verbose', help='', action='store_true')
    parser.add_argument('-l', '--language', help='')
    parser.add_argument('-s', '--symbol', help='', required=True)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    data_path = args.path
    out_path = args.output

    parsed = parse_markdown(data_path, args.language, args.symbol)


main()
