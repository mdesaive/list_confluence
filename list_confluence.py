#!/usr/bin/python3

# select content.title, content.contentid, content.parentid from content inner join spaces on content.spaceid = spaces.spaceid where content.content_status = 'current' and content.contenttype = 'PAGE' and spaces.spacekey = 'ITInfra' order by content.contentid into outfile '/tmp/only-content.csv'

import pdb


class Element(object):
    def __init__(self, name, content_id, parent_id):
        self.name = name
        self.content_id = content_id
        self.parent_id = parent_id
        self.parent = None
        self.children = []

    def __str__(self):
        return str(self.name) + " \"" + str(self.content_id) + "\" \"" + \
            str(self.parent_id) + "\" " + str(self.children)


def search_parent_element(element, array_of_elements):
    for tmp_element in array_of_elements[:]:
        # pdb.set_trace()
        if tmp_element.content_id == element.parent_id:
            # pdb.set_trace()
            # print("*** match "  + element.name + " " + tmp_element.name)
            tmp_element.children.append(element)
            return None
    else:
        return element


def print_tree(element, indent):
    print(str(element.content_id) + " " + indent + str(element.name))
    for tmp_element in sorted(element.children, key=lambda elem: elem.name):
        print_tree(tmp_element, indent + "  ")

def print_csv(element, path):
    print(str(element.content_id) + ";" + path + "/" + str(element.name))
    for tmp_element in sorted(element.children, key=lambda elem: elem.name):
        print_csv(tmp_element, path + "/" + str(element.name))


input_file = open("only-content-20160106.csv", "r")
PT_TREE = False
PT_CSV = True

array_of_elements = []
roots = []

for line in input_file:
    array_line = line.split("\t")

    content_name = array_line[0].strip()
    content_id = array_line[1].strip()
    parent_id = array_line[2].strip()

    array_of_elements.append(Element(content_name, content_id, parent_id))

for element in array_of_elements[:]:
    # print(str(element))
    if search_parent_element(element, array_of_elements) is not None:
        roots.append(element)
for root in roots:
    if PT_TREE:
        print_tree(root, "")
    if PT_CSV:
        print_csv(root, "")
