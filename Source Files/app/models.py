from match_prop import find_matching_prop
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


def find_model_type(type, model, fgi, fmi):
    """Compare model type to find potential match
        go thru the possible matches to find the best one
    """
    candidates = []
    for m in fmi:
        if model['displayas'] == m['displayas']:
            logging.debug(f"FOUND MODEL TYPE Candidate! ({type}) {model['name']} #{model['pixelcount']} ({model['displayas']}) with {m['name']} #{m['pixelcount']}")
            candidates.append(m)
    if len(candidates) > 0:
        diff = 9999
        candidate = None
        for c in candidates:
            if abs(c['pixelcount'] - model['pixelcount']) < diff:
                candidate = c
                diff = abs(c['pixelcount'] - model['pixelcount'])
        logging.info(f"FOUND MODEL TYPE! ({type}) {model['name']} ({model['displayas']}) with {candidate['name']}")
        # Find one with the closest pixel count
        return candidate
    return None


def is_matching(target_str, str_list):
    # Convert the target string to lowercase and remove spaces
    target_str_normalized = target_str.lower().replace(" ", "")
    logging.debug(f"is_matching: {target_str}: {target_str_normalized} with {str_list}")
    logging.debug(f'Results {any(target_str_normalized.startswith(s.lower().replace(" ", "")) for s in str_list)}')

    # Check if the normalized target string is a substring of any string in the list
    return any(target_str_normalized.startswith(s.lower().replace(" ", "")) for s in str_list)


def find_fuzzy(type, model, fgi, fmi):
    """Compare fuzzy model name to find potential match
        need to do similar groups
    """
    for g in fgi:
        logging.debug(f"Fuzzy match (group) {g['name']} with {model['name']}")
        if is_matching(model['name'], [g['name']]):
            logging.info(f"FOUND FUZZY! ({type}) {model['name']} with {g['name']}")
            return g
    return None
    for m in fmi:
        logging.debug(f"Fuzzy match {m['name']} with {model['name']}")
        if is_matching(model['name'], [m['name']]):
            logging.info(f"FOUND FUZZY! ({type}) {model['name']} with {m['name']}")
            return m
    return None

def find_111(type, model, fgi, fmi):
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
                val = find_model_type(type, model, fgi, fmi)
                if val == None:
                    val = random.choice(fgi)
    else:
        val = find_hint(model, xLightsImportModelNodes)
        if val == None:
            val = find_exact(type, model, fgi, fmi, xLightsImportModelNodes)
            if val == None:
                val = find_model_type(type, model, fgi, fmi)
                if val == None:
                    #+

                    #if model_type is circle ... look for wreath or spinner?
                    #
                    val = find_fuzzy(type, model, fgi, fmi)
                    if val == None:
                        val = find_111(type, model, fgi, fmi)
                        if val == None:
                            logging.info(f"***NOT FOUND .. random! for {model['name']}")
                            val = random.choice(fgi)
    logging.debug(f"Groups {fgi}, Models {fmi}")
    logging.info(f"find_match results: \"{model['name']}\" is mapped to \"{val['name']}\"")
    return val