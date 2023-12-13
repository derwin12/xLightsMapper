import logging
import re

import xml.etree.ElementTree as ET

from fetchmatch import match_prop

from models import find_match

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class XlightsImportModelNode:
    def __init__(self, model, strand, node, mapping):
        self._model = model
        self._strand = strand
        self._node = node
        self._mapping = mapping


# Mapping pairs

xLightsImportModelNodes = []
# All models from show
DataViewItems = []
model_groups = []
models_info = []
from_models_info = []
mapping_info = []
my_groups_info = []
from_groups_info = []

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def dump_xlights_import_model_nodes():
    for i, mn in enumerate(xLightsImportModelNodes, start=1):
        logging.info(f" ({i}) model {mn._model} mapped to {mn._mapping}")


def read_rgbeffects(xml_file_path, mi, mg):
    logging.info("read_source()")
    root = ET.parse(xml_file_path)

    # Find the modelGroups element
    model_group_elements = root.find(".//modelGroups")
    if model_group_elements is not None:
        for model_group_element in model_group_elements.findall("modelGroup"):
            model_group_name = model_group_element.get("name")
            model_group_models = model_group_element.get("models").split(",") \
                if model_group_element.get("models") else []
            mg.append({"name": model_group_name, "models": model_group_models})

    # Display the extracted modelGroup names and models
    for model_group in mg:
        logging.debug(f"ModelGroup Name: {model_group['name']}")
        logging.debug(f"Models: {model_group['models']}")
    logging.debug(f"============")
    # Extract name and parm1 attributes from models

    models_element = root.find(".//models")
    if models_element is not None:
        for model_element in models_element.findall("model"):

            if model_element.get("DisplayAs") == "Custom":
                PixelCountStr = model_element.get("PixelCount")
#                logging.debug(">>>>>" + model_element.get("name") + " " + model_element.get("DisplayAs") + ">>" + PixelCountStr + "<< " +
 #                             model_element.get("parm1") + ":" + model_element.get("parm2") + ":" + model_element.get("parm3"))
                if PixelCountStr:
                    pixelcount = int(PixelCountStr)
                else:
                    pattern = "(\d+)"
                    PixelStr = model_element.get("CustomModel")
                    matches = re.findall(pattern, PixelStr)
                    pixel_counts = [int(match) for match in matches]
                    # Find the largest pixel count
                    pixelcount = max(pixel_counts)
            else:
                pixelcount = int(model_element.get("parm1")) * int(model_element.get("parm2"))
            model_info = {
                "name": model_element.get("name"),
                "displayas": model_element.get("DisplayAs"), # ModelType
                "parm1": model_element.get("parm1"),
                "parm2": model_element.get("parm2"),
                "parm3": model_element.get("parm3"),
                "pixelcount": pixelcount,
            }
            # Never try to map to Images
            if model_info['displayas'] == "Image":
                continue
            if model_info['displayas'] == "DmxMovingHead3D":
                continue
            mi.append(model_info)

    # Display the extracted information
    for model in mi:
        logging.debug(f"Model Name: {model['name']} " +
                      f"DisplayAs: {model['displayas']} Parm1: {model['parm1']} Parm2: {model['parm2']} " +
                      f"Parm3: {model['parm3']} PixelCount: {model['pixelcount']}")


def find_tab(line):
    for x in range(len(line)):
        if line[x] == '\t':
            first = line[:x]
            line = line[x + 1:]
            return first, line
    return line, ""


def load_xmap_mapping(file_path):
    logging.info("load_xmap_mapping()")

    try:
        with open(file_path, 'r') as file:
            firstline = file.readline().strip()  ## ignore
            count = int(file.readline().strip())
            logging.info("Count = %d" % count)
            # Load in models
            for x in range(count):
                mn = file.readline().strip()
#                print("Line:", x, mn)
                DataViewItems.append(mn)

            logging.info(f"Total Models loaded {len(DataViewItems)}")
            line = file.readline().strip()

            # Load in Mappings
            while line != "":
                if line.count('\t') == 4:
                    model, line = find_tab(line)
                    strand, line = find_tab(line)
                    node, line = find_tab(line)
                    mapping, line = find_tab(line)
                    # color = wx.Colour(find_tab(line))
                else:
                    model, line = find_tab(line)
                    strand, line = find_tab(line)
                    node, line = find_tab(line)
                    mapping, line = find_tab(line)

                #                print(f"model: {model}, strand: {strand}, node: {node}, mapping: {mapping}")
                xLightsImportModelNodes.append(XlightsImportModelNode(model, strand, node, mapping))
                line = file.readline().strip()

        logging.info(f"Total Lines loaded {len(xLightsImportModelNodes)}")
    except FileNotFoundError:
        logging.error(f"File '{file_path}' not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def create_mapping():
    logging.info("create_mapping()")
# just for fun map something from source groups to dest groups
    for group in my_groups_info:
        mappedNode = find_match("group", group, from_groups_info, from_models_info, xLightsImportModelNodes)
        mappingnode = {
            'model': group['name'],
            'strand': "",
            'node': "",
            'mapping': mappedNode['name']
        }
        mapping_info.append(mappingnode)
# just for fun map something from source to dest
    for model in models_info:
        mappedNode = find_match("model", model, from_groups_info, from_models_info, xLightsImportModelNodes)
        if mappedNode:
            mappingnode = {
                'model': model['name'],
                'strand': "",
                'node': "",
                'mapping': mappedNode['name']
            }
            mapping_info.append(mappingnode)


def save_xmap_mapping(file_path):
    logging.info("save_xmap_mapping()")

    with open(file_path, 'w') as file:
        file.write('false\n')
# Count
        file.write(str(len(mapping_info)) + '\n')
        # Dump out all models

# To Do: only dump models that were mapped
        for group in my_groups_info:
            file.write(f"{group['name']}\n")
        for model in models_info:
            file.write(f"{model['name']}\n")
        # Dump out all mapped models maps
        for model_node in mapping_info:
            if model_node['mapping'] != "":
                file.write(f"{model_node['model']}" +
                           "\t" + model_node['strand'] +
                           "\t" +
                           "\t" + model_node['mapping'] +
                           "\t" + "white" +
                           "\n")
            else:
                file.write(f'{model_node._model}' +
                           "\t" +
                           "\t" +
                           "\t" + model_node._mapping +
                           "\t" + "white" +
                           "\n")


def dump_models():
    logging.info("dump_models")
    for model in models_info:
        logging.info(f"Source Model: {model['name']}")


def dump_from_models():
    logging.info("dump_from_models")
    for model in from_models_info:
        logging.info(f"From Model: {model['name']}")


def process_files():
    read_rgbeffects("../seed_data/DestinationB/xlights_rgbeffects.xml",
                    models_info, my_groups_info)
    read_rgbeffects("../seed_data/SourceB/xlights_rgbeffects.xml",
                    from_models_info, from_groups_info)
    #dump_models()
    #dump_from_models()
    load_xmap_mapping("../seed_data/SourceB/SourceB.xmap")
    load_xmap_history()
    #if we loaded some xmap_hints
    if len(xLightsImportModelNodes) > 0:
        save_xmap_history()
    create_mapping()
    save_xmap_mapping("../seed_data/Output/generated.xmap")


def load_xmap_history():
    logging.info("load_xmap_history()")


def save_xmap_history():
    logging.info("save_xmap_history()")


def find_element(array, target):
    """
    Find the index of the target element in the array.

    Parameters:
    - array (list): The input array.
    - target: The element to find in the array.

    Returns:
    - int: The index of the target element, or -1 if not found.
    """
    try:
        index = array.index(target)
        return index
    except ValueError:
        return -1


def update_element(array, index, new_value):
    """
    Update the element at the specified index in the array.

    Parameters:
    - array (list): The input array.
    - index (int): The index of the element to update.
    - new_value: The new value to assign to the element.

    Returns:
    - list: The updated array.
    """
    if 0 <= index < len(array):
        array[index] = new_value
        return array
    else:
        print("Index out of range.")
        return array


def read_prior_maps():
    logging.info("read_prior_maps")


def identify_models():
    logging.info("identify_models")


def output_mapfile():
    logging.info("output_mapfile")


def map_exact():
    logging.info("map_exact")


def map_hints():
    print("map_hints")
# scan through xLightsImportModelNodes and make the mappings


if __name__ == "__main__":
    print("Starting app")
    model_type_to_search = "Circle"
    pixel_count_to_search = 200

    matching_prop = match_prop(model_type_to_search, pixel_count_to_search)
    if matching_prop:
        print(
            f"Match found: Name={matching_prop.name}, "
            f"Pixelcount={matching_prop.pixelcount}, "
            f"Modeltype={matching_prop.modeltype}")
    else:
        print("No match found.")

    process_files()
