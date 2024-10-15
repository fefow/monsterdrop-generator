from lxml import etree
import pandas as pd


def load_monster_data(file_path):
    """
    Carga los datos del archivo Monster.xml en un DataFrame y lo devuelve.
    
    Parámetros:
        file_path (str): La ruta al archivo Monster.xml.

    Retorna:
        pd.DataFrame: Un DataFrame con los datos de monstruos.
    """
    try:
        
        context = etree.iterparse(file_path, events=('end',), tag='Monster')
        
        monsters = []

        for event, elem in context:
            monsters.append({
                'Index': elem.get('Index'),
                'Name': elem.get('Name')
            })
            elem.clear()
            
        return pd.DataFrame(monsters)
    
    except Exception as e:
        
        print(f"Error al cargar el archivo Monster.xml: {str(e)}")
        
        return pd.DataFrame() 
    

    
                            
def load_item_data(file_path):
    """
    **Carga los datos del archivo Item.xml en un DataFrame y lo devuelve.**
    
    Parámetros:
        *file_path (str): La ruta al archivo Item.xml.*

    Retorna:
        *pd.DataFrame: Un DataFrame con los datos de monstruos.*
    """
    try:
        
        context = etree.iterparse(file_path, events=('end',), tag='Item')
        
        items = []

        for event, elem in context:
            items.append({
                'Section': elem.getparent().get('Index'),
                'Index': elem.get('Index'),
                'Name': elem.get('Name')
            })
            elem.clear()
            
        return pd.DataFrame(items)
    
    except Exception as e:
        
        print(f"Error al cargar el archivo Item.xml: {str(e)}")
        
        return pd.DataFrame() 
