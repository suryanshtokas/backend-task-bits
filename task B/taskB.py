# Round 2 (Task B)
import requests
import json


def main():

    def get_types():
        data = requests.get("https://pokeapi.co/api/v2/type/").json()
        return data

    types = []
    for typ in get_types()["results"]:
        types.append(typ["name"])

    # removing the unkown,stellar entries
    # since they weren't given in the google doc
    types.pop()
    types.pop() 

    # also making a dictionary to store index value for name
    name_dict = {}
    for i in range(0, len(types)):
        name_dict[types[i]] = i

    # for each type, make a list to store interaction with others
    # with default values as 1 for neutral, then change them
    final_matrix = []
    for typ in types:
        final_matrix.append([1.0]*len(types))

    # now change the defaults in our matrix wherever we have the data
    for index, typ in enumerate(types):
        # only take the damage relations
        typ_data = requests.get(f"https://pokeapi.co/api/v2/type/{typ}/").json()["damage_relations"]

        # immunity (set to 0)
        for i in typ_data["no_damage_from"]:
            final_matrix[index][name_dict[i["name"]]] = 0.0

        # resistances (set to 1/2)
        for i in typ_data["half_damage_from"]:
            final_matrix[index][name_dict[i["name"]]] = 0.5

        # weakness
        for i in typ_data["double_damage_from"]:
            final_matrix[index][name_dict[i["name"]]] = 2.0

    return final_matrix, types, name_dict

# final_matrix, types, name_dict = main()

def print_final(final_matrix):
    for i in final_matrix:
        for j in i:
            print(j, end=" ")
        print()

# print_final(final_matrix)

# the types (up to down and left to right in this order only)
"""
['normal', 'fighting', 'flying', 'poison', 
 'ground', 'rock', 'bug', 'ghost', 'steel', 
 'fire', 'water', 'grass', 'electric', 'psychic', 
 'ice', 'dragon', 'dark', 'fairy']
"""