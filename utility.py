import pickle


def save_data(f_name, obj):
    with open(f_name + ".pickle", 'wb') as f_op:
        pickle.dump(obj, f_op, protocol=pickle.HIGHEST_PROTOCOL)
    print("Saved the data")


def load_data(f_name):
    with open(f_name + ".pickle", 'rb') as f_op:
        obj = pickle.load(f_op)
        return obj



