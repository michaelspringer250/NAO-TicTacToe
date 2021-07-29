import pickle
import enum

class PType(enum.Enum):
    P1 = 1
    P2 = 2

dictionary_data = {"a": 1, "b": 2}

# a_file = open("regular.pkl", "wb")
# pickle.dump(dictionary_data, a_file)
# a_file.close()

a_file = open("reversewild.pkl", "rb")
output = pickle.load(a_file)

d = dict()

for key in output:
    items = []
    for item in output[key]:
        winner = None
        if item[0] == PType.P1:
            winner = 1
        if item[0] == PType.P2:
            winner = 2
        items.append((winner, item[1], item[2], item[3]))
        d[key] = items

#print(output)
print(d)
#print(output["---------"])
#print(d["---------"])

