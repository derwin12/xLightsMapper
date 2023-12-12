import json

def load_data(filename):
    try:
        with open(filename, 'r') as file:
            data = set(tuple(sorted(entry.items())) for entry in json.load(file))
    except FileNotFoundError:
        # If the file doesn't exist, initialize with an empty dictionary
        data = set()
    return data

def save_data(filename, data):
    data_to_save = [dict(entry) for entry in data]
    with open(filename, 'w') as file:
        json.dump(data_to_save, file, indent=2)

def add_model_data(history_data, new_entry):
    # Check if the model name already exists in the data
    entry_key = tuple(sorted(new_entry.items()))
    if entry_key in history_data:
        print(f"Data for '{new_entry}' already exists. Skipping addition.")
    else:
# Add new data under the specified model name
        history_data.add(entry_key)
        print(f"Data added successfully: {new_entry}")

# Example usage
filename = "../seed_data/Output/mapping_history_file.json"

if __name__ == "__main__":
    # Load existing data or initialize with an empty dictionary
    history_data = load_data(filename)

    # Adding data for "modelA"
    model_data = {"model": "Stars", "mapping": "SomeStar", "strand":"", "model_type":"circle", "pixelcount":50}
    add_model_data(history_data, model_data)

    # Adding data for "modelB"
    model_data = {"model": "Stars", "mapping": "SomeStar2", "strand":"", "model_type":"circle","pixelcount":75}
    add_model_data(history_data, model_data)

    # Save the updated data back to the file
    save_data(filename, history_data)