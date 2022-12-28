#!/bin/python3

import logging
import sys
import pprint as pp
import os
import yaml
import itertools
import argparse
import re
from collections import namedtuple

g_language = None


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


class Converter(object):
    Rule = namedtuple('Rule', ['Type', 'Attributes', 'Body'])

    def _class(self: str, ark_symbol: str) -> Rule:
        logging.info('Parsing %s', ark_symbol)

        return self.Rule('TypeReferenceRule', {
            'arktsName': ark_symbol,
        }, [])

    def _member(self, language_symbol: str, ark_symbol: str) -> Rule:
        symbol = language_symbol.split(' ')[-1]
        logging.info(f'{symbol} -> {ark_symbol}')

        return self.Rule('MemberAccessExpressionRule', {
            self.language + 'MemberName': symbol,
            'arktsName': ark_symbol
        }, [])

    def _method(self, language_symbol: str, ark_symbol: str) -> Rule:
        logging.info(f'{language_symbol} -> {ark_symbol}')
        symbol = language_symbol

        paren_i = symbol.find('(')
        arg_list = symbol[paren_i+1:-2]
        arguments = arg_list.split(',')
        signature = []
        for arg in arguments:
            last_space = arg.rfind(' ')
            arg_type = arg[:last_space]
            signature.append(arg_type.strip())

        name = symbol[:paren_i].split()[-1]
        signature = ','.join(signature)
        return self.Rule('CallExpressionRule', {
            self.language + 'MethodName': name,
            self.language + 'MethodArgs': signature
        }, [])

    def __init__(self, data_path, language, ark_symbol):
        HEADING_RE = re.compile(r'^#+ (.*)\n')
        SYMBOL_RE = re.compile(r'^#+ ' + ark_symbol + r'\n')

        self.language = language

        with open(data_path, 'r') as data_file:
            for line in data_file:
                if re.match(SYMBOL_RE, line):
                    logging.info(f'Processing symbol: {line.strip()}')
                    break
            table_lines = []
            for line in data_file:
                if '|' in line:
                    table_lines.append(line.strip())
                elif re.match(HEADING_RE, line):
                    break

            table_body = table_lines[2:]

            for entry in table_body:
                entry = entry.strip('|')
                entry_fields = [e.strip() for e in entry.split('|')]

                if len(entry_fields) == 0:
                    continue

                entry_type = entry_fields[0]
                language_symbol = entry_fields[1]
                ark_symbol = entry_fields[2]
                status = entry_fields[3]

                if status == 'Done':
                    ark_symbol = 'Same'

                if entry_type == 'Class':
                    self.rules.append(self._class(ark_symbol))
                elif entry_type == 'Member':
                    self.rules.append(self._member(
                        language_symbol, ark_symbol))
                elif entry_type == 'Method':
                    self.rules.append(self._method(
                        language_symbol, ark_symbol))
                else:
                    raise Exception(f'Unknown entry type: {entry_type}')

    def dump(self, output_file):
        rules = [rule._asdict() for rule in self.rules]
        with open(output_file, 'w+') as yaml_file:
            yaml.dump(rules, yaml_file, indent=4,
                      encoding='utf-8', sort_keys=False)
        logging.info(f'Wrote rules to {output_file}')

    language = None
    rules = []


def main():
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='', required=True)
    parser.add_argument('-o', '--output', help='')
    parser.add_argument('-v', '--verbose', help='', action='store_true')
    parser.add_argument('-l', '--language', help='',
                        choices=['java', 'js', 'ts', 'as'], required=True)
    parser.add_argument('-s', '--symbol', help='', required=True)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    data_path = args.path
    output_file = args.output

    if not output_file:
        output_file = args.symbol + '.yaml'

    converter = Converter(data_path, args.language, args.symbol)
    converter.dump(output_file)


main()
