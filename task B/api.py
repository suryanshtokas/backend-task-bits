from typing import Optional

from fastapi import FastAPI, Query

import requests
import json

from taskB import main

# get the final_matrix(rows are defending, columns attacking)
final_matrix, types, name_dict = main()

app = FastAPI()

@app.get("/")
def read_root(
    defender: Optional[str] = Query(None, description="Defender Type"),
    attacker: Optional[str] = Query(None, description="Attacker Type")):

    # if both inputs are given
    if attacker and defender:
        return {
            "attacker": attacker.title(), 
            "defender": defender.title(),
            "multiplier": final_matrix[name_dict[defender.lower()]][name_dict[attacker.lower()]]
        }
    
    # if only defender input given
    elif defender:
        from_attackers = {}
        for i, attacker in enumerate(types):
            from_attackers[attacker.title()] = final_matrix[name_dict[defender.lower()]][i]
        return {
            "defender": defender.title(),
            "from_attackers": from_attackers
        }
    
    # if only attacker input given
    elif attacker:
        to_defenders = {}
        for i, defender in enumerate(types):
            to_defenders[defender.title()] = final_matrix[i][name_dict[attacker.lower()]]
        return {
            "attacker": attacker.title(),
            "to_defenders": to_defenders
        }
    
    # just return default values otherwise i.e. Null
    return {
        "attacker": attacker, "defender": defender
    }


@app.get("/fullmatrix/")
def full_matrix():
    return {"matrix": final_matrix, "name_dict": name_dict, "types": types}