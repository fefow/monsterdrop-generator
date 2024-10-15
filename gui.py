import sys
import time
import threading
from tkinter import messagebox
import customtkinter as ctk

from file_manager import load_item_data, load_monster_data
from logic import generate_result, validate_drop_rate
from utils import resource_path

# Configuración inicial de la interfaz
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class AppItemDropDusius(ctk.CTk):

    def __init__(self):
        
        super().__init__()
        self.terminated = False
        self.setup_window()
        self.init_variables()
        self.show_loading_screen()
        
        if not self.terminated:
            threading.Thread(target=self.load_components).start()

    def setup_window(self):
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.title("MonsterDrop MUDevs S18-S19 - Dusius")
        self.geometry(f"{w//2}x{h-75}+{w//4}+0")
        self.resizable(False, True)
        self.protocol('WM_DELETE_WINDOW', self.terminate)
        try:
            if sys.platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap(resource_path("img/icon.ico")))
        except Exception:
            pass

    def init_variables(self):
            #Variables generales
            self.selected_items, self.monsters = [], []
            self.selected_monster, self.settings_flag = None, False
            self.classType_var = ctk.StringVar(value="0")
            self.default_values = {k: "-1" for k in ["op0", "op1", "op2", "op3", "op4", "op5", "op6", "atr", "minLvl", "maxLvl"]}
            self.default_values.update({"level": "0", "grade": "0", "dur": "0", "classType": "0", "dw": "1", "dk": "1", "fe": "1", "mg": "1", "dl": "1", "su": "1", "rf": "1", "gl": "1", "rw": "1", "sl": "1", "gc": "1", "km": "1", "lm": "1", "ik": "1"})
            self.current_page, self.current_page_monster = 0, 0
            self.items_per_page, self.monsters_per_page = 20, 20
            self.filtered_df, self.filtered_monster_df = None, None
            
            #Elementos que deberian estar en el initialize pero estan definidas aca para evitar errores (ARREGLAR en el futuro)
            self.monsters_list_scroll = ctk.CTkScrollableFrame(self,0,0)
            self.show_more_monsters_button = ctk.CTkButton(self, 0, 0)
            self.show_more_button = ctk.CTkButton(self, 0, 0)
    
    def show_loading_screen(self):
        self.loading_label = ctk.CTkLabel(self, text="Cargando Item.xml y Monster.xml, por favor espere...")
        self.loading_label.pack(padx=60, pady=100)
        self.progress_bar = ctk.CTkProgressBar(self, width=self.winfo_screenwidth() // 2)
        self.progress_bar.pack(padx=50, pady=100)
        self.progress_bar.set(0)

    def terminate(self):
        ''' Terminar programa '''
        if self.terminated == False:
            self.terminated = True
            try:
                self.erase_monsters_list()
                self.destroy()
            except:
                print("Error al cerrar el programa.")
                pass
            sys.exit()
    
    def initialize_main_window(self):
        # Eliminar la pantalla de carga
        self.loading_label.pack_forget()
        self.progress_bar.pack_forget()

        # Configurar grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.create_main_layout()
        
    def create_main_layout(self):

        # Main Frame - Se hizo un main frame para poder scrollear en caso de que la vista supere el ancho de la pantalla
        self.main_frame = ctk.CTkScrollableFrame(master=self, width=(self.winfo_screenwidth()/2))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1) 
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)
        self.main_frame.grid_rowconfigure(5, weight=1)
        self.main_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        self.left_frame = ctk.CTkFrame(master=self.main_frame, width=self.winfo_screenwidth()/2)
        self.left_frame.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.create_left_frame()
        
        self.right_frame = ctk.CTkFrame(self.main_frame, width=self.winfo_screenwidth()/2)
        self.right_frame.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        self.create_right_frame()
        
        self.separator = ctk.CTkFrame(self.main_frame, height=2, fg_color="#333333")  
        self.separator.grid(row=4, column=0, columnspan=8, sticky="ew", pady=10) 
                         
        self.bottom_frame = ctk.CTkFrame(self.main_frame, width=self.winfo_screenwidth())
        self.bottom_frame.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")
        self.create_bottom_frame()
    
    def create_left_frame(self):
        ''' Row 0 - Columna 0 - left frame '''
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_rowconfigure(3, weight=1)
        self.left_frame.grid_rowconfigure(4, weight=1)
        self.left_frame.grid_rowconfigure(5, weight=1)
        
        # ---- Estructura de LEFT FRAME ----
        #  row 0 = [ 0 - filtro item ]
        #  row 1 = [ 0 - button Mostrar menos  | 1 - button mostrar mas ]
        #  row 2 = [ 0 - frame item left - 1 - frame item right ]
        #  row 3 = [ 0 - text items seleccionados ]
        #  row 4 = [ 0 - frame items seleccionados ]
        #  row 5 = [ 0 - button borrar seleccionados ]

        # 0 - 0 filtrar ítems'''
        self.filter_entry = ctk.CTkEntry(self.left_frame, placeholder_text="Buscar en Item.xml", width=200, height=39)
        self.filter_entry.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.filter_entry.bind("<KeyRelease>", self.apply_item_filter)
    
        # 1 - 0 Botón "Mostrar menos"'''
        self.show_back_button = ctk.CTkButton(self.left_frame, text="Mostrar menos", command=self.load_back_items)
        self.show_back_button.grid_forget()

        # 1 - 1 Botón "Mostrar más"'''
        self.show_more_button = ctk.CTkButton(self.left_frame, text="Mostrar más", command=self.load_more_items)
        self.show_more_button.grid(row=1, column=1, padx=10, pady=2, sticky="ne")
        
        # 2 - 0 Frame items izquierda'''
        self.items_left_frame = ctk.CTkScrollableFrame(self.left_frame, height=350)  # Aumentar ancho y alto
        self.items_left_frame.grid(row=2, column=0, padx=2, pady=2)
        
        # 2 - 1 Frame items izquierda'''
        self.items_right_frame = ctk.CTkScrollableFrame(self.left_frame, height=350)  # Reducir ancho
        self.items_right_frame.grid(row=2, column=1, padx=2, pady=2)
        
        # 3 - 0 Labe l Items seleccionados'''
        self.selected_items_label = ctk.CTkLabel(self.left_frame, text="Ítems seleccionados:", height=20)
        self.selected_items_label.grid(row=3, column=0, pady=5)

        # 4 .0 Frame para mostrar los ítems seleccionados'''
        self.selected_items_listbox = ctk.CTkScrollableFrame(self.left_frame, width=(self.winfo_screenwidth()/2-30))
        self.selected_items_listbox.grid(row=4, column=0, columnspan=2, pady=5)

        # 5.0 Botón "Borrar seleccionados"'''
        self.clear_button = ctk.CTkButton(self.left_frame, text="Borrar Items seleccionados", command=self.clear_selection, height=30)
        self.clear_button.grid(row=5, column=0, pady=5)

    def create_right_frame(self):
        ''' Row 0 - Columna 1 - right frame '''
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=1)
        self.right_frame.grid_rowconfigure(3, weight=1)
        self.right_frame.grid_rowconfigure(4, weight=1)
        self.right_frame.grid_rowconfigure(5, weight=1)
        
        # ---- Estructura de RIGHT FRAME ----
        #  row 0 = [ 0 - filtro monstruo ]
        #  row 1 = [ 0 - button mostrar menos  | 1 - button mostrar mas ]
        #  row 2 = [ 0 - frame monstruo ]
        #  row 3 = [ 0 - text monstruo seleccionados ]
        #  row 4 = [ 0 - frame monstruo seleccionados ]
        #  row 5 = [ - nada -]

        # 0 - 0 Entry para filtrar monstruos'''
        self.monster_filter_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Buscar en Monster.xml", width=200, height=30)
        self.monster_filter_entry.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky="nsew")
        self.monster_filter_entry.bind("<KeyRelease>", self.apply_monster_filter)
        
        # 1 - 0 Botón "Mostrar menos" '''
        self.show_back_monsters_button = ctk.CTkButton(self.right_frame, text="Mostrar menos", command=self.load_back_monster)
        self.show_back_monsters_button.grid_forget()
        
        # 1 - 1 Botón "Mostrar más"'''
        self.show_more_monsters_button = ctk.CTkButton(self.right_frame, text="Mostrar más", command=self.load_more_monster)
        self.show_more_monsters_button.grid(row=1, column=1, padx=10, pady=2, sticky="ne")
        
        # 2 - 0 Entry para filtrar monstruos'''
        self.monsters_list_scroll = ctk.CTkScrollableFrame(self.right_frame, width=self.winfo_screenwidth()/2.6, height=500)  # Aumentar ancho y alto
        self.monsters_list_scroll.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # 3 - 0 Label y textbox para monstruo seleccionado'''
        self.selected_monster_label = ctk.CTkLabel(self.right_frame, text="Monstruo Seleccionado:", height=10)
        self.selected_monster_label.grid(row=3, column=0, columnspan=2)

        # 4 - 0 Label y textbox para monstruo seleccionado'''
        self.selected_monster_display = ctk.CTkLabel(self.right_frame, text="- No hay monstruo seleccionado -", height=20, text_color="#eb4034")
        self.selected_monster_display.grid(row=4, column=0, columnspan=2)

        # 5 Frame Drop Rate'''
        self.drop_frame = ctk.CTkFrame(self.right_frame, width=self.winfo_screenwidth()/3, fg_color="transparent")
        self.drop_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.create_drop_frame()    
        
        ''' ROW 1 '''
        # Separador entre el row 0 y el row 1
        separator = ctk.CTkFrame(self.main_frame, height=2, fg_color="#333333")  # Define el grosor y color del separador
        separator.grid(row=1, column=0, columnspan=8, sticky="ew", pady=10) 

        ''' ROW 2 '''
        # Boton de configuracion avanzada 
        self.button_settings = ctk.CTkButton(self.main_frame, text="Config. Avanzada ▼", command=lambda: self.toggle_frame_settings(), fg_color="#222222", hover_color="#111111", width=self.winfo_screenwidth()/2)
        self.button_settings.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")

        ''' ROW 3'''
        # Frame de la configuracion avanzada
        self.settings_frame = ctk.CTkFrame(master=self.main_frame, width=self.winfo_screenwidth()/3.5)
        self.settings_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.settings_frame.grid_forget()
        self.create_settings_frame()
        
    def create_drop_frame(self):
            self.drop_frame.grid_rowconfigure(0, weight=1)
            self.drop_frame.grid_columnconfigure(0, weight=1)

            # ---- Estructura de DROPRATE FRAME ----
            #  row 0 = [ 0 - Label |  1 - Input  ]

            # 5 - 0 Label Drop Rate'''
            self.droprate_label = ctk.CTkLabel(self.drop_frame, text="Drop Rate", height=30)
            self.droprate_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

            # 5 - 1 Label Drop Rate'''
            self.droprate_entry = ctk.CTkEntry(self.drop_frame, placeholder_text="Valor de drop", height=30)
            self.droprate_entry.grid(row=0, column=1, sticky="w", ipadx=5, ipady=5, padx=10, pady=10)
            
    def create_settings_frame(self):      
            self.settings_frame.grid_rowconfigure(0, weight=1)
            self.settings_frame.grid_rowconfigure(1, weight=1)
            self.settings_frame.grid_rowconfigure(2, weight=1)
            self.settings_frame.grid_rowconfigure(3, weight=1)
        
            # ---- Estructura de SETTINGS FRAME ----
            #  row 0 = [ 0 - Boton Cerrar config. ]
            #  row 1 = [ 0 - Frame Settings Internal 1 ]
            #  row 2 = [ 0 - Frame Settings Internal 2 ]
            #  row 0 = [ 0 - Frame Settings Internal 3 ]
  
            # Boton para ocultar el frame de la config. avanzada
            self.setting_button = ctk.CTkButton(self.settings_frame, text="Cerrar Config. Avanzada ▲", command=lambda: self.toggle_frame_settings(), fg_color="#222222", hover_color="#111111", width=self.winfo_screenwidth()/2)
            self.setting_button.grid(row=0, column=0, columnspan=7, sticky="w")
            
            self.settings_internal1_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
            self.settings_internal1_frame.grid(row=1, column=0, sticky="w")
            self.create_settings_internal1_frame()

            self.settings_internal2_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
            self.settings_internal2_frame.grid(row=2, column=0, sticky="w")
            self.create_settings_internal2_frame()

            self.settings_internal3_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
            self.settings_internal3_frame.grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.create_settings_internal3_frame()
            
    def create_settings_internal1_frame(self):
        '''Settings Frame Internal 1 '''
        self.settings_internal1_frame.grid_columnconfigure(0, weight=1)
        self.settings_internal1_frame.grid_columnconfigure(1, weight=1)
        self.settings_internal1_frame.grid_columnconfigure(2, weight=1)
        self.settings_internal1_frame.grid_columnconfigure(3, weight=1)
        self.settings_internal1_frame.grid_columnconfigure(4, weight=1)
        self.settings_internal1_frame.grid_columnconfigure(5, weight=1)
        self.settings_internal1_frame.grid_columnconfigure(6, weight=1)
        self.settings_internal1_frame.grid_columnconfigure(7, weight=1)
        
        # ---- Estructura de SETTINGS INTERNAL 1 FRAME ---- 
        #  row 0 = [ 0 - Level Frame | 1 - Grado | 2 - Atributo | 3 - Duracion | 4 - Min. lvl | 5 - Max. Lvl]
         
        self.level_frame = ctk.CTkFrame(self.settings_internal1_frame, fg_color="transparent")
        self.level_frame.grid(row=0, column=0, padx=5, pady=5)

        # ---- Estructura de LEVEL FRAME ---- 
        #  row 0 = [ 0 - Label | 1 - Select ]
        
        # Label "Level" en la primera columna
        self.level_label = ctk.CTkLabel(self.level_frame, text="Nivel")
        self.level_label.grid(row=0, column=0, padx=5, pady=10)
        
        # OptionMenu con números del 1 al 15
        level_options = [str(i) for i in range(0, 16)]  # Números del 1 al 15
        self.level_option_menu = ctk.CTkOptionMenu(self.level_frame, values=level_options, command=lambda value: self.handle_onchange_default_values("level", value))
        self.level_option_menu.grid(row=0, column=1, padx=0, pady=10)
        
        self.grade_entry = ctk.CTkEntry(self.settings_internal1_frame, placeholder_text="Grado", width=65)
        self.grade_entry.grid(row=0, column=2, padx=5, pady=5)
                        
        self.atr_entry = ctk.CTkEntry(self.settings_internal1_frame, placeholder_text="Atributo", width=65)
        self.atr_entry.grid(row=0, column=3, padx=5, pady=5)
        
        self.dur_entry = ctk.CTkEntry(self.settings_internal1_frame, placeholder_text="Duracion", width=65)
        self.dur_entry.grid(row=0, column=4, padx=5, pady=5)
        
        self.min_entry = ctk.CTkEntry(self.settings_internal1_frame, placeholder_text="Min Lvl", width=65)
        self.min_entry.grid(row=0, column=5, padx=5, pady=5)
        
        self.max_entry = ctk.CTkEntry(self.settings_internal1_frame, placeholder_text="Max Lvl", width=65)
        self.max_entry.grid(row=0, column=6, padx=5, pady=5)
        
        #Frame classType
        self.classType_frame = ctk.CTkFrame(self.settings_internal1_frame, fg_color="transparent")
        self.classType_frame.grid(row=0, column=7)
        self.create_class_type_frame()
    
    def create_class_type_frame(self):
        self.classType_frame.grid_columnconfigure(0, weight=1)
        self.classType_frame.grid_columnconfigure(1, weight=1)
        
        self.classType_label = ctk.CTkLabel(self.classType_frame, text="Hab. por Clase")
        self.classType_label.grid(row=0, column=0, padx=2, pady=2)
        self.classType_option = ctk.CTkOptionMenu(self.classType_frame, values=["0", "1"], variable=self.classType_var, command=self.handle_class_type_change)
        self.classType_option.grid(row=0, column=1)
           
    def create_settings_internal2_frame(self):
        ''' Settings Frame Internal 2 '''
        self.settings_internal2_frame.grid_rowconfigure(0, weight=1)
        self.settings_internal2_frame.grid_columnconfigure(0, weight=1)
        self.settings_internal2_frame.grid_columnconfigure(1, weight=1)
        self.settings_internal2_frame.grid_columnconfigure(2, weight=1)
        self.settings_internal2_frame.grid_columnconfigure(3, weight=1)
        self.settings_internal2_frame.grid_columnconfigure(4, weight=1)
        self.settings_internal2_frame.grid_columnconfigure(5, weight=1)
        self.settings_internal2_frame.grid_columnconfigure(6, weight=1)
        
        # ---- Estructura de SETTINGS INTERNAL 2 FRAME ---- 
        #  row 0 = [ 0 - Option 0 | 1 - Option 1 | 2 - Option 2 | 3 - Option 3 | 4 - Option 4 | 5 - Option 5 | 6 - Option 6 ]
        
        self.option0_entry = ctk.CTkEntry(self.settings_internal2_frame, placeholder_text="Option 0", width=60)
        self.option0_entry.grid(row=0, column=0, padx=1, pady=5)
        
        self.option1_entry = ctk.CTkEntry(self.settings_internal2_frame, placeholder_text="Option 1", width=60)
        self.option1_entry.grid(row=0, column=1, padx=1, pady=5)
        
        self.option2_entry = ctk.CTkEntry(self.settings_internal2_frame, placeholder_text="Option 2", width=60)
        self.option2_entry.grid(row=0, column=2, padx=1, pady=5)
        
        self.option3_entry = ctk.CTkEntry(self.settings_internal2_frame, placeholder_text="Option 3", width=60)
        self.option3_entry.grid(row=0, column=3, padx=1, pady=5)
        
        self.option4_entry = ctk.CTkEntry(self.settings_internal2_frame, placeholder_text="Option 4", width=60)
        self.option4_entry.grid(row=0, column=4, padx=1, pady=5)
        
        self.option5_entry = ctk.CTkEntry(self.settings_internal2_frame, placeholder_text="Option 5", width=60)
        self.option5_entry.grid(row=0, column=5, padx=1, pady=5)
        
        self.option6_entry = ctk.CTkEntry(self.settings_internal2_frame, placeholder_text="Option 6", width=60)
        self.option6_entry.grid(row=0, column=6, padx=1, pady=5)
            
    def create_settings_internal3_frame(self):
        ''' Settings Frame Internal 3 '''
        trueOrFalse = ["1","0"]
        self.settings_internal3_frame.grid_rowconfigure(0, weight=1)
        self.settings_internal3_frame.grid_rowconfigure(1, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(0, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(1, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(2, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(3, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(4, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(5, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(6, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(7, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(8, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(9, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(10, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(11, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(12, weight=1)
        self.settings_internal3_frame.grid_columnconfigure(13, weight=1)
        self.settings_internal3_frame.grid_forget()
        
        # ---- Estructura de SETTINGS INTERNAL 3 FRAME ---- 
        #  row 0 = [ 0 - Lbl DW | 1 - Lbl DK | 2 - Lbl FE | 3 - Lbl MG | 4 - Lbl DL  | 5 - Lbl SU | 6 - Lbl RF | 7 - Lbl GL | 8 - Lbl RW | 9 - Lbl SL | 10 - Lbl GC  | 11 - Lbl KM | 12 - Lbl LM | 13 - Lbl IK]
        #  row 0 = [ 0 - Entry DW | 1 - Entry DK | 2 - Entry FE | 3 - Entry MG | 4 - Entry DL  | 5 - Entry SU | 6 - Entry RF | 7 - Entry GL | 8 - Entry RW | 9 - Entry SL | 10 - Entry GC  | 11 - Entry KM | 12 - Entry LM | 13 - Entry IK]
        
        self.dw_label = ctk.CTkLabel(self.settings_internal3_frame, text="DW")
        self.dw_label.grid(row=0, column=0, padx=2, pady=2)
        self.dw_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("dw", value), width=40, fg_color="#222222")
        self.dw_option.grid(row=1, column=0, padx=5, pady=5)

        self.dk_label = ctk.CTkLabel(self.settings_internal3_frame, text="DK")
        self.dk_label.grid(row=0, column=1, padx=2, pady=2)
        self.dk_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("dk", value), width=40, fg_color="#222222")
        self.dk_option.grid(row=1, column=1, padx=5, pady=5)
        
        self.fe_label = ctk.CTkLabel(self.settings_internal3_frame, text="FE")
        self.fe_label.grid(row=0, column=2, padx=2, pady=2)
        self.fe_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("fe", value), width=40, fg_color="#222222")
        self.fe_option.grid(row=1, column=2, padx=5, pady=5)
        
        self.mg_label = ctk.CTkLabel(self.settings_internal3_frame, text="MG")
        self.mg_label.grid(row=0, column=3, padx=2, pady=2)
        self.mg_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("mg", value), width=40, fg_color="#222222")
        self.mg_option.grid(row=1, column=3, padx=5, pady=5)
        
        self.dl_label = ctk.CTkLabel(self.settings_internal3_frame, text="DL")
        self.dl_label.grid(row=0, column=4, padx=2, pady=2)
        self.dl_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("dl", value), width=40, fg_color="#222222")
        self.dl_option.grid(row=1, column=4, padx=5, pady=5)
        
        self.su_label = ctk.CTkLabel(self.settings_internal3_frame, text="SU")
        self.su_label.grid(row=0, column=5, padx=2, pady=2)
        self.su_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("su", value), width=40, fg_color="#222222")
        self.su_option.grid(row=1, column=5, padx=5, pady=5)
        
        self.rf_label = ctk.CTkLabel(self.settings_internal3_frame, text="RF")
        self.rf_label.grid(row=0, column=6, padx=2, pady=2)
        self.rf_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("rf", value), width=40, fg_color="#222222")
        self.rf_option.grid(row=1, column=6,padx=5, pady=5)
        
        self.gl_label = ctk.CTkLabel(self.settings_internal3_frame, text="GL")
        self.gl_label.grid(row=0, column=7, padx=2, pady=2)
        self.gl_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("gl", value), width=40, fg_color="#222222")
        self.gl_option.grid(row=1, column=7,padx=5, pady=5)
        
        self.rw_label = ctk.CTkLabel(self.settings_internal3_frame, text="RW")
        self.rw_label.grid(row=0, column=8, padx=2, pady=2)
        self.rw_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("rw", value), width=40, fg_color="#222222")
        self.rw_option.grid(row=1, column=8,padx=5, pady=5)
        
        self.sl_label = ctk.CTkLabel(self.settings_internal3_frame, text="SL")
        self.sl_label.grid(row=0, column=9, padx=2, pady=2)
        self.sl_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse,  command=lambda value: self.handle_onchange_default_values("sl", value), width=40, fg_color="#222222")
        self.sl_option.grid(row=1, column=9, padx=5, pady=5)
        
        self.gc_label = ctk.CTkLabel(self.settings_internal3_frame, text="GC")
        self.gc_label.grid(row=0, column=10, padx=2, pady=2)
        self.gc_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("gc", value), width=40, fg_color="#222222")
        self.gc_option.grid(row=1, column=10, padx=5, pady=5)
        
        self.km_label = ctk.CTkLabel(self.settings_internal3_frame, text="KM")
        self.km_label.grid(row=0, column=11, padx=2, pady=2)
        self.km_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("km", value), width=40, fg_color="#222222")
        self.km_option.grid(row=1, column=11, padx=5, pady=5)
        
        self.lm_label = ctk.CTkLabel(self.settings_internal3_frame, text="LM")
        self.lm_label.grid(row=0, column=12, padx=2, pady=2)
        self.lm_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("lm", value), width=40, fg_color="#222222")
        self.lm_option.grid(row=1, column=12, padx=5, pady=5)
        
        self.ik_label = ctk.CTkLabel(self.settings_internal3_frame, text="IK")
        self.ik_label.grid(row=0, column=13, padx=2, pady=2)
        self.ik_option = ctk.CTkOptionMenu(self.settings_internal3_frame, values=trueOrFalse, command=lambda value: self.handle_onchange_default_values("ik", value), width=40, fg_color="#222222")
        self.ik_option.grid(row=1, column=13, padx=5, pady=5)
              
    def create_bottom_frame(self):
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(1, weight=1)
        
        # ---- Estructura de BOTTOM FRAME ----
        #  row 0 = [ 0 - bottom_right frame | 1 - boton generar drop  ] 
        #  row 1 = [ 0 -  resultado frame ]
        #  row 2 = [ 0 -  resultado frame ]

        # 1 - 0 Botón "Generar Drop" '''
        self.generate_button = ctk.CTkButton(self.bottom_frame, text="Generar Drop", command=self.on_generate_result, height=40)
        self.generate_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")
        
        # 0 - 0 Frame para mostrar el resultado generado '''
        self.result_frame = ctk.CTkFrame(self.bottom_frame, width=self.winfo_screenwidth())
        self.result_frame.grid(row=1, column=0, columnspan=2, padx=3, pady=3)
        
        self.result_label = ctk.CTkTextbox(self.result_frame, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.result_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        # 0 - 0 Frame para mostrar el resultado generado '''
        self.bottom_right_frame = ctk.CTkFrame(self.bottom_frame, width=(self.winfo_screenwidth()/2)/3.5, height=30, fg_color="transparent" )
        self.bottom_right_frame.grid_forget()
        
        # ---- Estructura de BOTTOM RIGHT FRAME ----
        #  row 0 = [ 0 - Boton copiar | 1 - Boton borrar  ] 
        
        # Opcional: Botón para copiar el resultado al portapapeles '''
        self.copy_button = ctk.CTkButton(self.bottom_right_frame, text="Copiar resultado", height=30, command=self.copy_to_clipboard, fg_color="#2256b3", hover_color="#2d71eb")
        self.copy_button.grid_forget()
        
         # Creación del botón para borrar el contenido de result_label
        self.clear_button = ctk.CTkButton(self.bottom_right_frame, text="Borrar Resultado", height=30, command=self.clear_result_label, fg_color="#BB0000", hover_color="#e10101")
        self.clear_button.grid_forget()
        
        if self.terminated is not True:
            self.load_thread = threading.Thread(target=self.display_items)
            self.load_thread.start()

            self.load_thread = threading.Thread(target=self.display_monsters)
            self.load_thread.start()

    def load_components(self):
        self.monster_df = load_monster_data(resource_path('xml/Monster.xml'))
        self.items_df = load_item_data(resource_path('xml/Item.xml'))
        for i in range(100):
            time.sleep(0.05)
            self.progress_bar.set(i / 100)
        self.after(100, self.initialize_main_window)

    def erase_monsters_list(self):
        if hasattr(self, 'monsters_list_scroll'):
            for widget in self.monsters_list_scroll.winfo_children():
                widget.destroy()
        else:
            print("No tiene lista de monstruos")
    
    def display_monsters(self):   
        for widget in self.monsters_list_scroll.winfo_children():
            widget.destroy()
        
        if self.filtered_monster_df is not None and not self.filtered_monster_df.empty:
            monsters_to_display = self.filtered_monster_df.iloc[self.current_page_monster * self.monsters_per_page:(self.current_page_monster + 1) * self.monsters_per_page]
        else:
            monsters_to_display = self.monster_df.iloc[self.current_page_monster * self.monsters_per_page:(self.current_page_monster + 1) * self.monsters_per_page]
                    
        monsters_list = monsters_to_display[:20]
        
        cant_monsters = len(monsters_list)

        if cant_monsters == 0 | cant_monsters < 20:
            self.show_more_monsters_button.configure(state=ctk.DISABLED)
        else:
            self.show_more_monsters_button.configure(state=ctk.NORMAL)
        
        if self.current_page_monster > 0:
            self.show_back_monsters_button.grid(row=1, column=0, padx=10, pady=2, sticky="nw")
        else:
            if hasattr(self, 'show_back_monsters_button'):
                self.show_back_monsters_button.grid_forget()
            
        for index, row in monsters_list.iterrows():
            monster_check = ctk.CTkRadioButton(
                                                self.monsters_list_scroll,
                                                text=row['Name'],
                                                variable=ctk.StringVar(value=row['Index']),
                                                command=lambda i=row: self.select_monster(i)
                                                )
            monster_check.pack(fill="x", padx=10, pady=2)
          
    def display_items(self):
        if hasattr(self, 'items_left_frame') and hasattr(self, 'items_right_frame'):
            
            for widget in self.items_left_frame.winfo_children():
                    widget.destroy()
            for widget in self.items_right_frame.winfo_children():
                    widget.destroy()

            if self.filtered_df is not None and not self.filtered_df.empty:
                items_to_display = self.filtered_df.iloc[self.current_page * self.items_per_page:(self.current_page + 1) * self.items_per_page]
            else:
                items_to_display = self.items_df.iloc[self.current_page * self.items_per_page:(self.current_page + 1) * self.items_per_page]

            left_items = items_to_display[:10]
            right_items = items_to_display[10:]
            
            cant_itemsRight = len(right_items)

            if cant_itemsRight == 0 | cant_itemsRight < 10:
                self.show_more_button.configure(state=ctk.DISABLED)
            else:
                self.show_more_button.configure(state=ctk.NORMAL)
                
            if self.current_page > 0: 
                #aca va config. el boton de mostrar menos
                self.show_back_button.grid(row=1, column=0, padx=10, pady=2, sticky="nw")
            else:
                if hasattr(self, 'show_back_button'):
                    self.show_back_button.grid_forget()

            for index, row in left_items.iterrows():
                item_widget = ctk.CTkButton(self.items_left_frame, text=row['Name'], bg_color="#1b1b1b", fg_color="#1b1b1b")
                item_widget.pack(fill="x", padx=10, pady=2)
                item_widget.bind("<Button-1>", lambda e, i=row: self.select_item(e, i))     

            for index, row in right_items.iterrows():
                item_widget = ctk.CTkButton(self.items_right_frame, text=row['Name'], bg_color="#1b1b1b", fg_color="#1b1b1b")
                item_widget.pack(fill="x", padx=10, pady=2)
                item_widget.bind("<Button-1>", lambda e, i=row: self.select_item(e, i))

    def apply_item_filter(self, event=None):

        ''' Función de filtro para ítems '''
        try:
                filter_text = self.filter_entry.get().lower()
                if filter_text:
                    filtered_items = self.items_df[self.items_df['Name'].str.contains(filter_text, case=False, na=False)]
                else:
                    filtered_items  = self.items_df
                self.filtered_df = filtered_items
                self.current_page = 0
                self.display_items()
        except Exception as e:
                print("Error: se produjo un error al filtrar el archivo item.xml \n"+ str(e) )
    
    def apply_monster_filter(self, event=None):

        ''' Función de filtro para monstruos '''
        try:
                filter_text_monster = self.monster_filter_entry.get().lower()
                if filter_text_monster:
                    filtered_monsters = self.monster_df[self.monster_df['Name'].str.contains(filter_text_monster, case=False, na=False)]
                else:
                    filtered_monsters  = self.monster_df
                    
                self.filtered_monster_df = filtered_monsters  
                self.current_page_monster = 0   
                self.display_monsters()  # Limitar a 20 monstruos para mostrar al principio
        except Exception as e:
                print("Error: se produjo un error al filtrar el archivo monster.xml \n"+e)       
        
    def load_more_items(self):
        self.current_page += 1
        self.display_items()
        
    def load_back_items(self):
        self.current_page -= 1
        self.display_items()
        
    def load_more_monster(self):
        self.current_page_monster += 1
        self.display_monsters()
        
    def load_back_monster(self):
        self.current_page_monster -= 1
        self.display_monsters()

    def select_item(self, event, item):
            flag = 0
            for a in self.selected_items:
                if item['Index'] == a['Index'] and item['Name'] == a['Name']:
                    flag = 1

            if flag == 0:
                self.selected_items.append(item)
                # Añadir una etiqueta en el CTkScrollableFrame para mostrar el nombre del ítem seleccionado
                item_label = ctk.CTkLabel(self.selected_items_listbox, text=item['Name'], fg_color="#1b1b1b", text_color="#FFFFFF")
                item_label.pack(fill="x", padx=10, pady=2)
                
    def select_monster(self, monster):
        ''' Activar el radiobutton si es el seleccionado '''
        try:
            
            if hasattr(self, "monsters_list_scroll"):
                for widget in self.monsters_list_scroll.winfo_children():
                    # Accede a la variable del radiobutton y compara con el índice del monstruo '''
                    if widget.cget('value') == monster['Index'] or widget.cget('text') == monster['Name']:
                        widget.select()
                    else:
                        widget.deselect()
                        
        except Exception as e:
            print("Error al seleccionar. \n"+e)
                    
        self.selected_monster = monster
        self.selected_monster_display.configure(text=monster['Name'],text_color="#32a852")
        
    def clear_selection(self):
        ''' Asegúrate de que hay ítems seleccionados '''
        if self.selected_items:
            # Eliminar todas las etiquetas de la lista de seleccionados
            for widget in self.selected_items_listbox.winfo_children():
                widget.destroy()

        # Vaciar la lista de ítems seleccionados '''
        self.selected_items.clear()
    
    def clear_result_label(self):
        self.result_label.delete(1.0, ctk.END)
        self.bottom_right_frame.grid_forget()
        self.copy_button.grid_forget()
        self.clear_button.grid_forget()
    
    def toggle_frame_settings(self):
        if self.settings_flag == False:
            self.button_settings.grid_forget()
            self.settings_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
            self.settings_flag = True
        else:
            self.settings_frame.grid_forget()
            self.button_settings.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
            self.settings_flag = False
    
    def handle_class_type_change(self, choice):
        if choice == "1":
            self.settings_internal3_frame.grid()
            self.default_values["classType"] = 1
        else:
            self.settings_internal3_frame.grid_forget()
            self.default_values["classType"] = 0
    
    def handle_onchange_default_values(self, selected_value, new_value):
        self.default_values[selected_value] = new_value
    
    def update_default_values(self):
            '''ACTUALIZA LOS PARAMETROS DE ENTRY CONFIG. AVANZADA'''
            if self.min_entry.get() != "":
                self.default_values["minLvl"] = self.min_entry.get()
        
            if self.max_entry.get() != "":
                self.default_values["maxLvl"] = self.max_entry.get()
            
            if self.atr_entry.get() != "":
                self.default_values["atr"] = self.atr_entry.get()
            
            if self.grade_entry.get() != "":
                self.default_values["grade"] = self.dur_entry.get()
            
            if self.dur_entry.get() != "":
                self.default_values["dur"] = self.dur_entry.get()
                
            if self.option0_entry.get() != "":
                self.default_values["op0"] = self.option0_entry.get()
                
            if self.option1_entry.get() != "":
                self.default_values["op1"] = self.option1_entry.get()
                
            if self.option2_entry.get() != "":
                self.default_values["op2"] = self.option2_entry.get()
                
            if self.option3_entry.get() != "":
                self.default_values["op3"] = self.option3_entry.get()
                
            if self.option4_entry.get() != "":
                self.default_values["op4"] = self.option4_entry.get()
                
            if self.option5_entry.get() != "":
                self.default_values["op5"] = self.option5_entry.get()
                
            if self.option6_entry.get() != "":
                self.default_values["op6"] = self.option6_entry.get()
             
    def on_generate_result(self):
          
        try:
            # Obtener el valor de la entrada del drop
            drop_rate_str = self.droprate_entry.get()

            # Verificar si el valor de drop no está vacío
            if not drop_rate_str.strip():
                raise ValueError("El campo Drop Rate está vacío.")

            # Verificar si el valor no está vacío
            if self.selected_monster is None or not self.selected_items:
                raise ValueError("No se han seleccionado ítems o monstruos.")
            
            # Parse a integer del string drop
            drop_rate = int(drop_rate_str)
            
            if validate_drop_rate(drop_rate):
                
                self.update_default_values()
                
                result = generate_result(self.selected_monster, self.selected_items, drop_rate, self.default_values)
                self.result_label.insert("1.0", result)
                self.bottom_right_frame.grid(row=0, column=0, padx=0, pady=1, sticky="nsew")
                self.copy_button.grid(row=0, column=0, padx=20, pady=0, sticky="nw")
                self.clear_button.grid(row=0, column=1, padx=20, pady=0, sticky="ne")
                
            else:
                raise ValueError("El valor de drop rate solo acepta de 1 a 100000.")
            
        except ValueError as e:
            messagebox.showwarning("Error Resultado", str(e))
            return
            
    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.result_label.get(1.0, ctk.END))
        messagebox.showinfo("Copiar al portapapeles", "Resultado copiado al portapapeles")