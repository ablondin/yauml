# coding=utf-8
r"""
Creating UML diagrams from YAML files.

AUTHORS:

- Alexandre Blondin Massé
- Simon Désaulniers
"""
#************************************************************************************
#  Copyright (C) 2013 Alexandre Blondin Massé <alexandre.blondin.masse@gmail.com    *
#                     Simon Désaulniers <rostydela@gmail.com>                       *
#                                                                                   *
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)  *
#                                                                                   *
#  The full text of the GPLv2 is available at:                                      *
#                                                                                   *
#                  http://www.gnu.org/licenses/                                     *
#************************************************************************************

import yaml, sys
import getopt

template_filename = '../template/template.dot'
# CONSTANTS
VERSION='0.1'
VERSION_INFO='yauml v%s -- A script for generating UML diagrams from YAML file' % VERSION
HELP='yauml [OPTIONS] file\n\
\tfile: The YAML file to convert.\n\
OPTIONS:\n\
\t-t|--template template\n\
\t\tSepcefies the template file (default: %s).\n\
\t-h|--help\n\
\t\tDisplays this help text.' % template_filename
PROGRAM='yauml'


class DotStringBuilder(object):
    r"""
    """
    # Retrieves relations
    RELATION_FORMAT = "  node%s -> node%s;\n"
    CLASS_FORMAT = '  node%s [\n\tlabel = "{%s\n\t|%s|%s}"\n  \n]\n'
    INTERFACE_FORMAT = '  node%s [\n\tlabel = "{\<\<interface\>\>\\n%s\n\t|\\l|%s}"\n  ]\n\n'

    def __init__(self, data):
        self._data = data

    def build_classes(self):
        r"""
        Builds the class ndoes string.
        """
        class_string = ''
        for entity in data:
            if 'class' in entity:
                class_name = make_raw(entity['class'])
        
                attributes = ''
                if 'attributes' in entity:
                    for attribute in entity['attributes']:
                        attributes += '%s\\l' % make_raw(attribute)
                else:
                    attributes += '\\l'
                methods = ''
                if 'methods' in entity:
                    for method in entity['methods']:
                        methods += '%s\\l' % make_raw(method)
                else:
                    methods += '\\l'
                class_string += self.CLASS_FORMAT % (class_name.split()[0], class_name, attributes, methods)

        return class_string

    def build_interfaces(self):
        """
        Builds the interface nodes string.
        """
        interface_string = ''
        for entity in data:
            if 'interface' in entity:
               interface_name = entity['interface']
               
               methods = ''
               if 'methods' in entity:
                   for method in entity['methods']:
                       methods += '%s\\l' % make_raw(method)
               else:
                   methods += '\\l'

               interface_string += self.INTERFACE_FORMAT % (interface_name, interface_name, methods)

        return interface_string

    def build_uses(self):
        r"""
        Builds the "uses" nodes string.
        """
        # Uses
        uses = ''
        for entity in data:
            if 'uses' in entity:
                for parent in entity['uses']:
                    uses += RELATION_FORMAT % (parent, entity['class'].split()[0])
        return uses

    def build_inherits(self):
        r"""
        Builds the "inherits" nodes string.
        """
        # Inheritance
        inheritances = ''
        for entity in data:
            if 'inherits' in entity:
                for parent in entity['inherits']:
                    inheritances += RELATION_FORMAT % (parent, entity['class'].split()[0])
        return inheritances

    def build_is_part_of(self):
        r"""
        Builds the "is part of"  nodes string.
        """
        # Is-part-of
        ispartofs = ''
        for entity in data:
            if 'ispartof' in entity:
                for parent in entity['ispartof']:
                    ispartofs += RELATION_FORMAT % (parent, entity['class'].split()[0])
        return ispartofs

    def build_implements(self):
        r"""
        Builds the "implements" nodes string.
        """
        # Implements
        implements = ''
        for entity in data:
            if 'implements' in entity:
                for parent in entity['implements']:
                    implements += RELATION_FORMAT % (parent, entity['class'].split()[0])
        return implements

def make_raw(s):
    t = ''
    for c in s:
        if c == '<':
            t += '\<'
        elif c == '>':
            t += '\>'
        elif c == '{':
            t += '\{'
        elif c == '}':
            t += '\}'
        else:
            t += c
    return t
   
def getOptions():
    r"""
    Gets all options at command line.
    """
    global template, yaml_filename

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvt:", ["help","version","template="])
    except getopt.GetoptError, err:
        print(str(err))
        print(HELP)
        sys.exit(1)

    for o,a in opts:
        if o in ("-v","--version"):
            print(VERSION_INFO)
            sys.exit(0)
        elif o in ("-h","--help"):
            print(HELP)
            sys.exit(0)
        elif o in ("-t","--template"):
            with open(a, 'r') as template_file: template = template_file.read()
        else:
            assert False
            
    if len(args) < 1:
        print(PROGRAM+': an argument is missing.')
        sys.exit(1)
    
    yaml_filename = args[0]

def main():
    getOptions()

    # Retrieve yaml data
    with open(yaml_filename) as yaml_file: 
        data = yaml.load(yaml_file.read())

    dot_string_builder = DotStringBuilder(data)
    print template % (dot_string_builder.build_classes(), dot_string_builder.build_interfaces(),\
                        dot_string_builder.build_inherits, dot_string_builder.build_is_part_of(),\
                        dot_string_builder.build_uses(), dot_string_builder.build_implements())

if __name__ == "__main__":
    main()