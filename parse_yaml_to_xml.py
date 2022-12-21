#!/bin/python3

import sys
import yaml
import pprint as pp
import xml.etree.ElementTree as et
import os


def yaml_to_xml(javaclass_name, yaml_obj):
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

    callexpr_tag = et.Element('CallRules.{}'.format(javaclass_name))
    for yaml_rule in yaml_obj:
        rule_tag = et.SubElement(
            callexpr_tag, yaml_rule['Type'], yaml_rule['Attributes'])
        fill_children_tags(rule_tag, yaml_rule['Body'])
        # rule_tag.append(et.Comment(yaml_rule['Comment']))
    return callexpr_tag


def main():
    yaml_path = sys.argv[1]
    xml_path = sys.argv[2]
    javaclass_name = os.path.splitext(os.path.basename(yaml_path))[0]
    with open(yaml_path, 'r') as yaml_file:
        yaml_obj = yaml.load(yaml_file, Loader=yaml.FullLoader)
        xml = yaml_to_xml(javaclass_name, yaml_obj)
    et.ElementTree(xml).write(xml_path)


main()
