import random
import logging
#

# try to determine what each model is IRL
# based on name, pixel count, model type, submodels, layout, faces, appearance (floods)
# check each model from the input model names and mapped to model names, tag them with estimated model name
#
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# use the mapping file
# use exact match
# use history
# use spelling mistakes
# use partial matches
# determine the prop?
# use size of model
# use single prop to group if found - arch to group of arches
# map group to singles if not found in group
# use base models
# determine outlines/house/outlines etc
# match up flood types
# check repo of props

def find_exact(type, model, fgi, fmi, xLightsImportModelNodes):
    for m in fgi:
        logging.debug(f"Compare {model['name']} with {m['name']}")
        if model['name'].lower() == m['name'].lower():
            logging.info(f"FOUND MATCH! ({type}) {model['name']}")
            return m
    for m in fmi:
        if model['name'].lower() == m['name'].lower():
            logging.info(f"FOUND MATCH! ({type}) {model['name']}")
            return m
    return None


def find_similar(type, model, fgi, fmi):
    """Compare model type to find potential match
        need to do similar groups
    """
    for m in fmi:
        if model['displayas'] == m['displayas']:
            logging.info(f"FOUND SIMILAR! ({type}) {model['name']} ({model['displayas']}) with {m['name']}")
            return m
    return None


def is_matching(target_str, str_list):
    # Convert the target string to lowercase and remove spaces
    target_str_normalized = target_str.lower().replace(" ", "")
    if target_str == "Candy Canes-02":
        logging.info("stop")
    logging.debug(f"is_matching: {target_str}: {target_str_normalized} with {str_list}")
    logging.debug(f'Results {any(target_str_normalized.startswith(s.lower().replace(" ", "")) for s in str_list)}')

    # Check if the normalized target string is a substring of any string in the list
    return any(target_str_normalized.startswith(s.lower().replace(" ", "")) for s in str_list)


def find_pattern(type, model, fgi, fmi):
    """Compare model type to find potential match
        need to do similar groups
    """
    for g in fgi:
        logging.debug(f"Pattern match (group) {g['name']} with {model['name']}")
        if is_matching(model['name'], [g['name']]):
            logging.info(f"FOUND PATTERN! ({type}) {model['name']} with {g['name']}")
            return g
    return None
    for m in fmi:
        logging.debug(f"Pattern match {m['name']} with {model['name']}")
        if is_matching(model['name'], [m['name']]):
            logging.info(f"FOUND PATTERN! ({type}) {model['name']} with {m['name']}")
            return m
    return None

def find_hint(model, xLightsImportModelNodes):
    """
    Search thru the provided hints (.xmap) for a match.
    """

    for index, item in enumerate(xLightsImportModelNodes):
        if item._model == model['name']:
            logging.info(f"FOUND HINT! for {model['name']}")
            return {'name': item._mapping}
    return None

def find_match(type, model, fgi, fmi, xLightsImportModelNodes):
    if type == "group":
        val = find_hint(model, xLightsImportModelNodes)
        if val == None:
            val = find_exact(type, model, fgi, fmi, xLightsImportModelNodes)
            if val == None:
                val = find_similar(type, model, fgi, fmi)
                if val == None:
                    val = random.choice(fgi)
    else:
        val = find_hint(model, xLightsImportModelNodes)
        if val == None:
            val = find_exact(type, model, fgi, fmi, xLightsImportModelNodes)
            if val == None:
                val = find_similar(type, model, fgi, fmi)
                if val == None:
                    val = find_pattern(type, model, fgi, fmi)
                    if val == None:
                        logging.info(f"NOT FOUND! for {model['name']}")
                        val = random.choice(fgi)
    logging.debug(f"Groups {fgi}, Models {fmi}")
    logging.info(f"find_match results: \"{model['name']}\" is mapped to \"{val['name']}\"")
    return val