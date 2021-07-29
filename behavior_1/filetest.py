import pickle

dictionary_data = {"a": 1, "b": 2}

a_file = open("data.pkl", "wb")
pickle.dump(dictionary_data, a_file)
a_file.close()

a_file = open("data.pkl", "rb")
output = pickle.load(a_file)
print(output)

t1 = t2 = t3 = 1
print(t1, t2, t3)