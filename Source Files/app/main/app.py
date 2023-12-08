import logging
import xml.etree.ElementTree as ET


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
dest_models_info = []

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def dump_xlights_import_model_nodes():
    for i, mn in enumerate(xLightsImportModelNodes, start=1):
        logging.info(f" ({i}) model {mn._model} mapped to {mn._mapping}")


def read_rgbeffects(xml_file_path, mi):
    logging.info("read_source()")
    root = ET.parse(xml_file_path)

    # Find the modelGroups element
    model_group_elements = root.find(".//modelGroups")
    if model_group_elements is not None:
        for model_group_element in model_group_elements.findall("modelGroup"):
            model_group_name = model_group_element.get("name")
            model_group_models = model_group_element.get("models").split(",") if model_group_element.get("models") else []
            model_groups.append({"name": model_group_name, "models": model_group_models})

    # Display the extracted modelGroup names and models
    for model_group in model_groups:
        logging.debug(f"ModelGroup Name: {model_group['name']}")
        logging.debug(f"Models: {model_group['models']}")

    # Extract name and parm1 attributes from models

    models_element = root.find(".//models")
    if models_element is not None:
        for model_element in models_element.findall("model"):
            model_info = {
                "name": model_element.get("name"),
                "displayas": model_element.get("DisplayAs"),
                "parm1": model_element.get("parm1"),
                "parm2": model_element.get("parm2"),
                "parm3": model_element.get("parm3"),
                "pixelcount": int(model_element.get("parm1")) * int(model_element.get("parm2")),
            }
            mi.append(model_info)

    # Display the extracted information
    for model in mi:
        logging.debug(f"Model Name: {model['name']}")
        logging.debug(f"DisplayAs: {model['displayas']}")
        logging.debug(f"Parm1: {model['parm1']}")
        logging.debug(f"Parm2: {model['parm2']}")
        logging.debug(f"Parm3: {model['parm3']}")
        logging.debug(f"PixelCount: {model['pixelcount']}")
def read_destination(xml_file_path):
    logging.info("read_destination()")


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


def save_xmap_mapping(file_path):
    logging.info("save_xmap_mapping()")

    with open(file_path, 'w') as file:
        file.write('false\n')
        file.write(str(len(DataViewItems)) + '\n')
        # Dump out all mapped models

        for model_model in DataViewItems:
            file.write(f'{model_model}\n')
        # Dump out all mapped models maps
        for model_node in xLightsImportModelNodes:
            if model_node._mapping != "":
                file.write(f'{model_node._model}' +
                           "\t" + model_node._strand +
                           "\t" +
                           "\t" + model_node._mapping +
                           "\t" + "white" +
                           "\n")
            else:
                file.write(f'{model_node._model}' +
                           "\t" +
                           "\t" +
                           "\t" + model_node._mapping +
                           "\t" + "white" +
                           "\n")


def process_files():
    read_rgbeffects("../../../Source Files/seed_data/SourceC/xlights_rgbeffects.xml",  models_info)
    read_rgbeffects("../../../Source Files/seed_data/Destination/xlights_rgbeffects.xml", dest_models_info)
    #load_xmap_mapping("../../../Source Files/seed_data/SourceA/SourceA.xmap")
    #save_xmap_mapping("../../../Source Files/seed_data/Output/generated.xmap")


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


if __name__ == "__main__":
    print("Starting app")
    process_files()
