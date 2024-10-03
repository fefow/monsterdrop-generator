**MonsterDrop Generator**
*- MuOnline | MuDevs Free Files Season 18.2-2 y 19.2-3* 

Descripción: Programa para generar las lineas de configuración de drop de items en los files de MuDevs S18 y 19.
Para modificar los archivos XML que se encuentran en la dir. 'Data > Item > MonsterDropManager' dentro de los archivos de servidor.

Requiere tener instalado *python* y tener los siguientes paquetes para ejecutarlo correctamente:
  - customtkinter
  - pandas
  - lxml

![imagen](https://github.com/user-attachments/assets/59ae051e-bb4f-41dc-aa5c-c1c00babbd50)

**- Compilarlo**

Dejo un comando de compilacion de ejemplo medio completo para el que quiera tenerlo como ejecutable

  con Pyinstaller:
  
      pyinstaller --noconsole --onefile --noupx --add-data "xml/Monster.xml;xml" --add-data "xml/Item.xml;xml" --add-data "img/icon.ico;img" --icon="img/icon.ico" --version-file="version_file.txt" --specpath=. gui.py

![imagen](https://github.com/user-attachments/assets/4760c7e8-0042-4c3c-ae04-b601da082d30)
