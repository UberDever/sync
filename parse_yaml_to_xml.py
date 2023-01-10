#!/bin/python3

import sys
import yaml
import pprint as pp
import xml.etree.ElementTree as et
import os
import logging
import yaml
import itertools
import argparse
import re

root_tags = {
    'java': 'JavaApiMappingRules',
    'js': 'JsApiMappingRules',
    'ts': 'TsApiMappingRules',
    'as': 'AsApiMappingRules',
}


def yaml_to_xml(classname, root_tag_name, rule_list, language):
    def fill_children_tags(xml_node, yaml):
        if not len(yaml):
            return

        for key, el in yaml.items():
            if key == 'Attributes':
                for attr_key, attr_val in el.items():
                    xml_node.set(attr_key, attr_val)
                continue
            xml_el = et.SubElement(xml_node, key)
            fill_children_tags(xml_el, el)

    root_tag = et.Element(root_tag_name)
    for rule in rule_list:
        attributes = {language + 'Type': classname}
        for k, v in rule['Attributes'].items():
            attributes[k] = v
        rule_tag = et.SubElement(
            root_tag, rule['Type'], attributes)
        if 'Body' in rule.keys():
            fill_children_tags(rule_tag, rule['Body'])
    return root_tag


def main():
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='', required=True)
    parser.add_argument('-o', '--output', help='', required=True)
    parser.add_argument('-v', '--verbose', help='', action='store_true')
    parser.add_argument('-l', '--language', help='',
                        choices=['java', 'js', 'ts', 'as'], required=True)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    yaml_path = args.path
    xml_path = args.output

    root_tag = et.Element(root_tags[args.language])
    classname = os.path.splitext(os.path.basename(yaml_path))[0]

    def grouper(item): return item['Type']

    with open(yaml_path, 'r') as yaml_file:
        all_rules = yaml.load(yaml_file, Loader=yaml.FullLoader)
        for key, group_items in itertools.groupby(all_rules, key=grouper):
            rules = list(group_items)
            if key == 'CallExpressionRule':
                root_tag.append(yaml_to_xml(classname,
                                            'CallRules.{}'.format(classname), rules, args.language))
            elif key == 'MemberAccessExpressionRule':
                root_tag.append(yaml_to_xml(classname,
                                            'MemberAccessRules', rules, args.language))
            elif key == 'TypeReferenceRule':
                root_tag.append(yaml_to_xml(classname,
                                            'TypeReferenceRules', rules, args.language))

    et.ElementTree(root_tag).write(xml_path)


main()
