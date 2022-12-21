#!/bin/python3

import sys
import yaml
import pprint as pp
import xml.etree.ElementTree as et
import os
import itertools


def yaml_to_xml(javaclass_name, root_tag_name, rule_list):
    def fill_children_tags(xml_root, yaml):
        if not len(yaml):
            return

        for key, el in yaml.items():
            if key == 'Attributes':
                for attr_key, attr_val in el.items():
                    xml_root.set(attr_key, attr_val)
                continue
            xml_el = et.SubElement(xml_root, key)
            fill_children_tags(xml_el, el)

    root_tag = et.Element(root_tag_name)
    for rule in rule_list:
        attributes = rule['Attributes']
        attributes['javaType'] = javaclass_name
        rule_tag = et.SubElement(
            root_tag, rule['Type'], rule['Attributes'])
        if 'Body' in rule.keys():
            fill_children_tags(rule_tag, rule['Body'])
    return root_tag


def main():
    yaml_path = sys.argv[1]
    xml_path = sys.argv[2]
    root_tag = et.Element('JavaApiMappingRules')
    javaclass_name = os.path.splitext(os.path.basename(yaml_path))[0]

    def grouper(item): return item['Type']

    with open(yaml_path, 'r') as yaml_file:
        all_rules = yaml.load(yaml_file, Loader=yaml.FullLoader)
        for key, group_items in itertools.groupby(all_rules, key=grouper):
            rules = list(group_items)
            if key == 'CallExpressionRule':
                root_tag.append(yaml_to_xml(javaclass_name,
                                            'CallRules.{}'.format(javaclass_name), rules))
            elif key == 'MemberAccessExpressionRule':
                root_tag.append(yaml_to_xml(javaclass_name,
                                            'MemberAccessRules', rules))
            elif key == 'TypeReferenceRule':
                root_tag.append(yaml_to_xml(javaclass_name,
                                            'TypeReferenceRules', rules))

    et.ElementTree(root_tag).write(xml_path)


main()
