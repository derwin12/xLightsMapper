import xml.etree.ElementTree as ET

class xLights_Import_Model_Node:
    def __init__(self, model, strand, node, mapping ):
        self._model = model
        self._strand = strand
        self._node = node
        self._mapping = mapping

xLights_Import_Model_Nodes = []

def dump_xLights_Import_Model_Nodes():
    for i, xLights_Import_Model_Node in enumerate(xLights_Import_Model_Nodes, start=1):
        print(f" ({i}) model {xLights_Import_Model_Node._model} mapped to {xLights_Import_Model_Node._mapping}")

def read_xml_file(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Process the XML data as needed
        for element in root:
            # Access element attributes, text, or other data
            print(f"Element Name: {element.tag}")
            print(f"Element Attributes: {element.attrib}")
            print(f"Element Text: {element.text}")
            print("\n")

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")

def read_source(xml_file_path):
    print("read_source")
    #read_xml_file(xml_file_path)
def read_destination(xml_file_path):
    print("read_destination()")
    #read_xml_file(xml_file_path)

def find_tab(line):
    for x in range(len(line)):
        if line[x] == '\t':
            first = line[:x]
            line = line[x+1:]
            return first, line
    return line, ""

def load_xmap_mapping(file_path):
    print("load_xmap_mapping")

    try:
        with open(file_path, 'r') as file:
            firstline = file.readline().strip() ## ignore
            count = int(file.readline().strip())
            #print("Count = %d" % count)
            for x in range(count):
                mn = file.readline().strip()
#                print("Line:", x, mn.strip())

            line = file.readline().strip()

            while line != "":
                if line.count('\t') == 4:
                    model, line = find_tab(line)
                    strand, line = find_tab(line)
                    node, line = find_tab(line)
                    mapping, line = find_tab(line)
                   # color = wx.Colour(find_tab(line))
                else:
                    model, line = find_tab(line)
                    strand, line  = find_tab(line)
                    node, line = find_tab(line)
                    mapping, line = find_tab(line)

                print(f"model: {model}, strand: {strand}, node: {node}, mapping: {mapping}")
                xLights_Import_Model_Nodes.append( xLights_Import_Model_Node(model, strand, node, mapping))

                line = file.readline().strip()

            dump_xLights_Import_Model_Nodes()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_files():
    read_source("../../../Source Files/seed_data/SourceA/xlights_rgbeffects.xml")
    read_destination("../../../Source Files/seed_data/Destination/xlights_rgbeffects.xml")
    load_xmap_mapping("../../../Source Files/seed_data/SourceA/SourceA.xmap")

def read_prior_maps():
    print("read_prior_maps")

def identify_models():
    print("identify_models")

def output_mapfile():
    print("output_mapfile")

def map_exact():
    print("map_exact")

def map_hints():
    print("map_hints")



    
import os

if __name__ == "__main__":
    print("Starting app")
    current_directory = os.getcwd()
    print(f"Current Directory: {current_directory}")

    process_files()