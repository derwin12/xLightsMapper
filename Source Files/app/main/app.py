import xml.etree.ElementTree as ET

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
    read_xml_file(xml_file_path)
def read_destination(xml_file_path):
    print("read_destination()")
    read_xml_file(xml_file_path)

def process_files():
    read_source("../../../Source Files/seed_data/SourceA/xlights_rgbeffects.xml")
    read_destination("../../../Source Files/seed_data/Destination/xlights_rgbeffects.xml")

import os

if __name__ == "__main__":
    print("Starting app")
    current_directory = os.getcwd()
    print(f"Current Directory: {current_directory}")

    process_files()