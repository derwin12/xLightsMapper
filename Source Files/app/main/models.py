import random
import logging
#
# try to determine what each model is IRL
# based on name, pixel count, model type, submodels, layout, faces, appearance (floods)
# check each model from the input model names and mapped to model names, tag them with estimated model name
#
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_match(type, model, fgi, fmi):
    if type == "group":
        val = random.choice(fgi)
    else:
        val = random.choice(fmi)
    logging.debug(f"Groups {fgi}, Models {fmi}")
    logging.info(f"find_match \"{model['name']}\" is mapped to \"{val['name']}\"")
    return val