import ifcopenshell
import ifcopenshell.util.element as Element
import pprint
from ifcopenshell.api.material.data import Data
import numpy as np
import pandas as pd

#function to get all the materials and all the quantitey into two single lines 
def df_material_quanitty (df, attributes_materials_thickness):
    #create empty data frame to store the data
    d_material =[]
    d_volume = []
    d_kbob = []
    #d_rr = []
    #takeing the material layers that we have in the project
    attributes_material = attributes_materials_thickness[::2]

    #creating the attributes volume in order to find the volumes in the data frame
    attributes_volume = []
    attributes_kbob = []
    #attributes_rr = []

    for i in range(len(attributes_material)):
         attributes_volume.append(f"Quantity {i+1}")
         attributes_kbob.append(f'ID nr. {i+1}')
         #attributes_rr.append(f' RR {i+1}')




    #loop inside the length of the attribute materials
    for i in range(len(attributes_material)):
         #takes from the dataframe_sorted (the dataframe sorted for the chosen IfcType(IfcWall, IfcSlab,etc.)) the data from 
         #each material layer
         a = df[attributes_material[i]]
         #takes from the dataframe_sorted (the dataframe sorted for the chosen IfcType(IfcWall, IfcSlab,etc.)) the data from 
         #the quantity of ech material layer
         b = df[attributes_volume[i]]
         #takes from the dataframe_sorted (the dataframe sorted for the chosen IfcType(IfcWall, IfcSlab,etc.)) the data from 
         #the kbob of each material
         c= df[attributes_kbob[i]]
         #takes from the dataframe_sorted (the dataframe sorted for the chosen IfcType(IfcWall, IfcSlab,etc.)) the data from 
         #the RR of each material
         #d = df[attributes_rr[i]]
        
        
         #converts the taken data to a list
         a = a.values.tolist()
         b = b.values.tolist()
         c = c.values.tolist()
         #d = d.values.tolist()
         #includes all the materials into teh empty list d
         d_material.extend(a)
         d_volume.extend(b)
         d_kbob.extend(c)
         #d_rr.extend(d)
            
    #creates a list to get a list of levels and types
    # multipplying the classes to get the Types alignn with the Materials names and quantities 
    d_classes= []
    for object_class in df["Class"]:
        d_classes.append(object_class)

    d_classes =  d_classes*len(attributes_material)

    
    #multiplying the levels to get the levels 
    d_level=[]
    for level in df["Level"]:
        d_level.append(level)        
    d_level =  d_level*len(attributes_material) 
            
    #creates a dataframe from the list
    d_material = pd.DataFrame(d_material)
    d_volume = pd.DataFrame(d_volume)
    d_kbob = pd.DataFrame(d_kbob)
    #d_rr = pd.DataFrame(d_rr)
    d_classes = pd.DataFrame(d_classes)
    d_level = pd.DataFrame(d_level)
    #merges the lists into a dataframe
    df_material_volume = pd.concat([d_classes, d_level,d_material,d_volume, d_kbob], axis = 1)
    return df_material_volume

#creates a set of all the materials  
def material_set(df): 
    material_set= set()
    #with this loop we go through all  the materials that are included and adds it to the material set 
    for rows in df["Material"]:
        material_set.add(rows)

    #creates a list of the set
    material_set = list(material_set)
    #from the list remove of values zero -->
    return material_set


# gets the total quantity of each material 
def get_total_quantities (material_set, df):

    all_materials = []
    all_quantities= []
    for material in material_set:
        #looks at the material volume data set if the materials are contained 
        contain_material = df[df['Material'].str.contains(material, na =False)]
        #looks at the material volume data set if the volume are contained 
        column_volume = contain_material.filter(like = "Quantity")
        #sums all the volume of the selected material
        tot_volume =  column_volume.sum()
        #converts the to_volume into a float
        tot_volume= float(tot_volume)
        #adds in a list all the materials
        all_materials.append(material)
        #adds in the volume list all the volumes
        all_quantities.append(tot_volume)
        
    return all_materials, all_quantities

#gets the different classes, levels
def get_classes_levels(type,df):
    levels_classes = []
    for level_class in df[type].unique():
        #gets a list of the levels and classes
        levels_classes.append(level_class)
    return levels_classes

# gets the dataframe filtered
def dataframe_filtered_by_input(dataframe, filtered_by_name, input ):
    return dataframe[dataframe[input] == filtered_by_name].dropna(axis=1, how="all")

#converts the names from IFC into KBOB database
def convert_to_KBOB_Materials(df, material_dataframe):
    for i in range(len(df)):
        id_nr = df.iloc[i,4]
        id_nr = float(id_nr)
        #print(id_nr)
        #looks for the rows in the kbob that contains the number id_number
        row_kbob = material_dataframe.loc[material_dataframe["ID-Number"] == id_nr]
        # takes the material of the row of the KBOB
        material = row_kbob["Material"].to_string(index = False)
        df.iloc[i,2] = material
    return df