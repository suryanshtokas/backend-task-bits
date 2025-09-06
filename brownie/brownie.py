import requests

pokemon = input("Enter Name of Pokemon: ").title()

# get pokemon data
data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/").json()

# get the final matrix, name_dict and types
matrix = requests.get("http://localhost:8000/fullmatrix/").json()
name_dict = matrix["name_dict"]
types = matrix["types"]
matrix = matrix["matrix"]

# getting the pokemon type(s)
p_type = []
for typ in data["types"]:
    p_type.append(typ["type"]["name"])


# if single type pokemon
if len(p_type) == 1:
    weak_2x = []
    immune = []
    for typ in types:
        if matrix[name_dict[p_type[0]]][name_dict[typ]] == 0:
            immune.append(typ)
        elif matrix[name_dict[p_type[0]]][name_dict[typ]] == 2:
            weak_2x.append(typ)

    print("2x Weaknesses: ", end="")
    print(weak_2x)
    print("Immunities: ", end="")
    print(immune)

# if double type pokemon:
elif len(p_type) == 2:
    # make a combined weakness dict 
    combined_weakness = {}
    for index, typ in enumerate(p_type):
        for key in name_dict.keys():
            if index == 0:
                combined_weakness[key] = matrix[name_dict[typ]][name_dict[key]]
            else:
                combined_weakness[key] *= matrix[name_dict[typ]][name_dict[key]]

    # sort the combined_weaknesses into 4x 2x and immune
    weak_4x = []
    weak_2x = []
    immune = []
    for key in combined_weakness.keys():
        if combined_weakness[key] == 4:
            weak_4x.append(key)
        elif combined_weakness[key] == 2:
            weak_2x.append(key)
        elif combined_weakness[key] == 0:
            immune.append(key)

    print("4x Weaknesses: ", end="")
    print(weak_4x)
    print("2x Weaknesses: ", end="")
    print(weak_2x)
    print("Immunities: ", end="")
    print(immune)          