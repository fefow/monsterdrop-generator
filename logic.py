#logic.py 
import customtkinter as ctk

def generate_result(selected_monster, selected_items, drop_rate, default_values):
    """Genera el string del resultado basado en los ítems y monstruos seleccionados."""
    results = []
    
    for item in selected_items:
        section = int(item['Section'])
        index = int(item['Index'])
        name = item['Name']
        monster_class = selected_monster['Index']
        
        result_string = (
            f'<MonsterDrop MonsterClass="{monster_class}" MonsterElement="-1" '
            f'Index="{(section * 512 + index)}" Level="{default_values["level"]}" '
            f'Grade="{default_values["grade"]}" Option0="{default_values["op0"]}" '
            f'Option1="{default_values["op1"]}" Option2="{default_values["op2"]}" '
            f'Option3="{default_values["op3"]}" Option4="{default_values["op4"]}" '
            f'Option5="{default_values["op5"]}" Option6="{default_values["op6"]}" '
            f'Attribute="{default_values["atr"]}" Duration="{default_values["dur"]}" '
            f'DropRate="{drop_rate}" Name="{name}" RequireMinLevel="{default_values["minLvl"]}" '
            f'RequireMaxLevel="{default_values["maxLvl"]}" RequireClassType="{default_values["classType"]}" '
            f'DW="{default_values["dw"]}" DK="{default_values["dk"]}" FE="{default_values["fe"]}" '
            f'MG="{default_values["mg"]}" DL="{default_values["dl"]}" SU="{default_values["su"]}" '
            f'RF="{default_values["rf"]}" GL="{default_values["gl"]}" RW="{default_values["rw"]}" '
            f'SL="{default_values["sl"]}" GC="{default_values["gc"]}" KM="{default_values["km"]}" '
            f'LM="{default_values["lm"]}" IK="{default_values["ik"]}" />\n'
        )
        results.append(result_string)

    return "".join(results)


def validate_drop_rate(drop_rate):
    try:
        if 0 < drop_rate <= 100000:
            return True
        else:
            raise ValueError
    except ValueError:
        return False