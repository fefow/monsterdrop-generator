import os
import sys

def resource_path(relative_path):
    """ Devuelve la ruta relativa segun donde este el gui.py """
    
    try:
        base_path = sys._MEIPASS
        
    except AttributeError:
        
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
