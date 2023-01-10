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


class Converter(object):
    Rule = namedtuple('Rule', ['Type', 'Attributes', 'Body'])

    def rule_hash(self, rule: Rule) -> str:
        return rule.Type + ':' + ':'.join(v for v in rule.Attributes.values() if len(v) > 0)

    def _class(self, language_symbol: str, ark_symbol: str) -> Rule:
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

        handlers = {
            'Method': self._method,
            'Constructor': self._method,
            'Member': self._member,
            'Module': self._class,
        }

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

                if status == 'Done' or status == 'TODO':
                    continue

                if entry_type in handlers:
                    rule = handlers[entry_type](language_symbol, ark_symbol)
                    self.rules.append(rule)
                else:
                    raise Exception('Unknown entry type: ' + entry_type)

    def dump(self, output_file):
        rules = [dict({'Hash': self.rule_hash(rule)}, **rule._asdict())
                 for rule in self.rules]
        try:
            with open(output_file, 'r') as yaml_file:
                existing_rules = yaml.load(yaml_file)
        except:
            with open(output_file, 'w+') as yaml_file:
                yaml.dump(rules, yaml_file, indent=4,
                          encoding='utf-8', sort_keys=False)
            logging.info(f'Wrote rules to {output_file}')
            return

        expanded_rules = existing_rules
        for rule in rules:
            if any(rule['Hash'] == r['Hash'] for r in existing_rules):
                continue
            else:
                expanded_rules.append(rule)

        with open(output_file, 'w+') as yaml_file:
            yaml.dump(expanded_rules, yaml_file, indent=4,
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
