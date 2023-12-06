
def read_source():
    print("read_source()")
def read_destination():
    print("read_destination()")

def process_files():
    read_source("seed_data/SourceA/xlights_rgbeffects.xml")
    read_destination("seed_data/Destination/xlights_rgbeffects.xml")

if __name__ == "__main__":
    print("Starting app")
    process_files()