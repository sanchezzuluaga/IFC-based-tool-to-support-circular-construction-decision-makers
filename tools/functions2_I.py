import ifcopenshell
import ifcopenshell.util.element as Element
import pprint
from ifcopenshell.api.material.data import Data
import numpy as np
import pandas as pd

def insert_quantities_in_dataframe(dataframe, attributes_materials_thickness):    
    #initialize all dataframes, if a data frame is empty after the loop --> we can still merge it, otherwise error will appear
    dataframe_ifc_wall = pd.DataFrame()
    dataframe_ifc_slab_landing = pd.DataFrame()
    dataframe_ifc_slab = pd.DataFrame()
    dataframe_ifc_beam = pd.DataFrame()
    dataframe_ifc_column = pd.DataFrame() 
    dataframe_ifc_stairflight = pd.DataFrame() 
    dataframe_ifc_window = pd.DataFrame()
    dataframe_ifc_door =  pd.DataFrame()
    dataframe_ifc_stair = pd.DataFrame()
    dataframe_ifc_roof = pd.DataFrame()
    
    classes = get_classes(dataframe)
    
    # For loop sorts the  
    for clas in classes:

        attributes_thickness = attributes_materials_thickness[1::2]
        #gets the volumes of the walls and its layers 
        if clas == "IfcWall":
            dataframe_ifc_wall = dataframe[dataframe["Class"] == "IfcWall"]
            
            #funciton for walls iterates along all the layers and multiplies NetSideAre with thickness of the layer
            for index, layer in enumerate(attributes_thickness):
                #quantities
                NetSideArea = dataframe_ifc_wall.filter(like = "WallBaseQuantities.NetSideArea")
                NetSideArea = NetSideArea.to_numpy()
                thickness = dataframe_ifc_wall.filter(like = layer)
                thickness = thickness.to_numpy()
                dataframe_ifc_wall[f"Quantity {index +1}"] = NetSideArea*thickness
             ### New Begin   
                # KBOB id nr 
                id_nr = dataframe_ifc_wall.filter(like = f"KBOB{index +1}").to_numpy()
                dataframe_ifc_wall[f'ID nr. {index+1}'] = id_nr
                #MCI
                #mci = dataframe_ifc_wall.filter(like = f"MC{index +1}").to_numpy()
                #dataframe_ifc_wall[f' RR {index+1}'] = mci


        #gets the volumes of the slabs   
        elif clas == "IfcSlab":

            #Landings from stairs, the landings are slabs but are Predefined as LANDING
            dataframe_ifc_slab_landing =dataframe[(dataframe["Class"] == "IfcSlab") & (dataframe["PredefinedType"] == "LANDING" )] 

            if dataframe_ifc_slab_landing.empty:
                pass
            else :
            #Quantities
                dataframe_ifc_stair = dataframe[dataframe["Class"] == "IfcStair"]
                volume = dataframe_ifc_slab_landing.filter(like="SlabBaseQuantities.GrossVolume")
                dataframe_ifc_slab_landing[f"Quantity {1}"] = volume
                #getting the KBOB
                id_nr = dataframe_ifc_stair.filter(like = f"KBOB{1}").to_numpy()
                dataframe_ifc_slab_landing[f'ID nr. {1}'] = id_nr
                # MCI
                #mci = dataframe_ifc_stair.filter(like = f"MC{1}").to_numpy()
                #dataframe_ifc_slab_landing[f' RR {1}'] = id_nr


            # looking and slabs whichh are not landning 
            dataframe_ifc_slab = dataframe[(dataframe["Class"] == "IfcSlab") & ~(dataframe["PredefinedType"] == "LANDING" )]            
            #gets the volumes of the slab and its layers 
            for index, layer in enumerate(attributes_thickness):
                GrossArea = dataframe_ifc_slab.filter(like = "SlabBaseQuantities.GrossArea")
                GrossArea = GrossArea.to_numpy()
                thickness = dataframe_ifc_slab.filter(like = layer)
                thickness = thickness.to_numpy()
                dataframe_ifc_slab[f"Quantity {index +1}"] = GrossArea*thickness
                # KBOB id nr 
                id_nr = dataframe_ifc_slab.filter(like = f"KBOB{index +1}").to_numpy()
                dataframe_ifc_slab[f'ID nr. {index+1}'] = id_nr
                #MCI
                #mci = dataframe_ifc_slab.filter(like = f"MC{index +1}").to_numpy()
                #dataframe_ifc_slab[f' RR {index+1}'] = mci

        elif clas ==  "IfcRoof":
            dataframe_ifc_roof = dataframe[dataframe["Class"] == "IfcRoof"]
            for index, layer in enumerate(attributes_thickness):
                #quantities
                Area = dataframe_ifc_roof.filter(like = "Dimensions.Area")
                Area = Area.to_numpy()
                thickness = dataframe_ifc_roof.filter(like = layer)
                thickness = thickness.to_numpy()
                dataframe_ifc_roof[f"Quantity {index +1}"] = Area*thickness
                id_nr = dataframe_ifc_roof.filter(like = f"KBOB{index +1}").to_numpy()
                dataframe_ifc_roof[f'ID nr. {index+1}'] = id_nr 
        
        
        #gets the volumes of the beams
        elif clas == "IfcBeam":
            dataframe_ifc_beam = dataframe[dataframe["Class"] == "IfcBeam"] 
            volume = dataframe_ifc_beam.filter(like = "BeamBaseQuantities.GrossVolume").to_numpy()
            dataframe_ifc_beam[f"Quantity {1}"] =   volume
            #getting the KBOB
            id_nr = dataframe_ifc_beam.filter(like = f"KBOB{1}").to_numpy()
            dataframe_ifc_beam[f'ID nr. {1}'] = id_nr
                # MCI
            #mci = dataframe_ifc_beam.filter(like = f"MC{1}").to_numpy()
            #dataframe_ifc_beam[f' RR {1}'] = mci

        #gets the volumes of the columns
        elif clas =="IfcColumn":
            dataframe_ifc_column = dataframe[dataframe["Class"] == "IfcColumn"] 
            volume = dataframe_ifc_column.filter(like = "ColumnBaseQuantities.NetVolume").to_numpy()
            dataframe_ifc_column[f"Quantity {1}"] =   volume
            #getting the KBOB
            id_nr = dataframe_ifc_column.filter(like = f"KBOB{1}").to_numpy()
            dataframe_ifc_column[f'ID nr. {1}'] = id_nr
                # MCI
            #mci = dataframe_ifc_column.filter(like = f"MC{1}").to_numpy()
            #dataframe_ifc_column[f' RR {1}'] = mci
        
        
        #gets the volumes 
        elif clas == "IfcStairFlight":
            dataframe_ifc_stairflight = dataframe[dataframe["Class"] == "IfcStairFlight"]
            volume = dataframe_ifc_stairflight.filter(like = "StairFlightBaseQuantities").to_numpy() 
            dataframe_ifc_stairflight[f"Quantity {1}"] =   volume
            # a = KBOB stair, b = MCI stair 
            a = dataframe_ifc_stair.iloc[0,:].filter(like = f"KBOB{1}").to_numpy()
            #b = dataframe_ifc_stair.iloc[0,:].filter(like = f"MC{1}").to_numpy()    
            c = np.array([a[0]]).tolist()
            # creates a dataframe with the KBOB and MCI values for each stairflight 
            kbob = []
            for i in range(len(dataframe_ifc_stairflight)):   
                kbob.append(c)
            kbob = tuple(kbob)    
        
            columns = ["Kbob"]
            kbob_mci_dataframe_stairflight = pd.DataFrame.from_records(kbob, columns= columns)
            dataframe_ifc_stairflight[[f'ID nr. {1}']] = kbob_mci_dataframe_stairflight.to_numpy()

        elif clas == "IfcWindow":
            #function for windows
            dataframe_ifc_window = dataframe[dataframe["Class"] == "IfcWindow"] 
            area = dataframe_ifc_window.filter(like = "WindowBaseQuantities.Area").to_numpy()
            dataframe_ifc_window[f"Quantity {1}"] =   area
            dataframe_ifc_window[f"Material Layer {1}"] =   "Window"
            #For Windows two KBOB values and one MCI
            id_nr_1 = dataframe_ifc_window.filter(like = f"KBOB{1}").to_numpy()
            dataframe_ifc_window[f'ID nr. {1}'] = id_nr_1
            id_nr_2 = dataframe_ifc_window.filter(like = f"KBOB{2}").to_numpy()
            dataframe_ifc_window[f'ID nr. {2}'] = id_nr_2
            # MCI
            #mci = dataframe_ifc_window.filter(like = f"MC{1}").to_numpy()
            #dataframe_ifc_window[f' RR {1}'] = mci


        elif clas == "IfcDoor":
            dataframe_ifc_door = dataframe[dataframe["Class"] == "IfcDoor"]
            area = dataframe_ifc_door.filter(like = "DoorBaseQuantities.Area").to_numpy() 
            dataframe_ifc_door[f"Quantity {1}"] =   area
            dataframe_ifc_door[f"Material Layer {1}"] =   "Door"
            #Getting the KBOB and the MCI
            #For Doors two KBOB values and one MCI
            id_nr_1 = dataframe_ifc_door.filter(like = f"KBOB{1}").to_numpy()
            dataframe_ifc_door[f'ID nr. {1}'] = id_nr_1
            id_nr_2 = dataframe_ifc_door.filter(like = f"KBOB{2}").to_numpy()
            dataframe_ifc_door[f'ID nr. {2}'] = id_nr_2
            # MCI
            #mci = dataframe_ifc_door.filter(like = f"MC{1}").to_numpy()
            #dataframe_ifc_door[f' RR {1}'] = mci

        else:
            pass
    return dataframe_ifc_wall, dataframe_ifc_slab_landing, dataframe_ifc_slab, dataframe_ifc_beam, dataframe_ifc_column, dataframe_ifc_stairflight, dataframe_ifc_window, dataframe_ifc_door, dataframe_ifc_roof

def get_classes(dataframe):
    classes  =[]
    for object_class in dataframe["Class"].unique():
        classes.append(object_class)
    return classes