import ifcopenshell
import ifcopenshell.util.element as Element
import pprint
from ifcopenshell.api.material.data import Data
import numpy as np
import pandas as pd


#function to extract the materia thickness and material layer
def get_material_thickness(object, max_length_layers):
    Ifc_material_layer_set =Element.get_material(object, should_skip_usage = True)
    #creats a list with the length of the total layers among all the IfcTypes (spaces for material and thickness)
    material_thickness_store  = [0]*max_length_layers*2


    if Ifc_material_layer_set is None:
        # if the IfcElement doesnt have a Material --> for all the materials layers zero values 
            return(material_thickness_store)
        
    else:
        
        
        #all layers = gets a list of all the layers of the IfcElement
        all_layers = Ifc_material_layer_set[0]
        # if the type of all layers is a string we only have information about the material of the layer
        #i.e we dont have information about the thickness 
        #Otherwise we would get a touple with different kind of information
    
    
        
            
        if object.is_a("IfcColumn") or object.is_a("IfcBeam")  == True:
            material = Ifc_material_layer_set[2][0][2][0]
            thickness = 0
            material_thickness_store[0] = material
            material_thickness_store[1] = thickness
            return(material_thickness_store)
            
        elif type(all_layers) == str:
        #we store the data in the list / since there is no thickness we get zero value 
            material = all_layers
            thickness = 0
            material_thickness_store[0] = material
            material_thickness_store[1] = thickness
            return(material_thickness_store)
        
        else:
            for i in range(len(all_layers)):
                # one layer = extracts from all the layers the information of one layer
                one_layer = all_layers[i]
                # the [0][0] outputs the material name 
                material  = one_layer[0][0]
                #the [1] extracts information about the thickness
                thickness = one_layer[1]
                material_thickness_store[i*2] = material
                material_thickness_store[i*2+1]= thickness

            return(material_thickness_store)
        
def layers_name (length_layer):
    layers_set = []
    for i in range(length_layer):
        layers_set.append(f'Material Layer {i+1}')
        layers_set.append(f'Thickness Layer {i+1}')
    layers_set = list(layers_set)
    return(layers_set)
        
def get_length_layers(object):
    length = 1
    Ifc_material_layer_set =Element.get_material(object, should_skip_usage = True)
    if Ifc_material_layer_set is None:
        pass
    else:
        all_layers = Ifc_material_layer_set[0]
        if type(all_layers) == str:
            length = 1
        else:
            length = len(all_layers)
    return length



def get_objects_data_by_class(file, class_type):
    def add_pset_attributes(psets):
        for pset_name, pset_data in psets.items():
            for property_name in pset_data.keys():
                pset_attributes.add(f'{pset_name}.{property_name}')
    

    
    pset_attributes = set()
    objects_data = []
    objects = file.by_type(class_type)
    #max_length initilized the max length of layers that are inside all the elements of the project 
    max_length_layers = 0 
        
    for object in objects:
        psets = Element.get_psets(object, psets_only=True)
        add_pset_attributes(psets)
        qtos = Element.get_psets(object, qtos_only=True)
        add_pset_attributes(qtos)
        objects_data.append({
            "ExpressId": object.id(),
            "GlobalId": object.GlobalId,
            "Class": object.is_a(),
            "PredefinedType": Element.get_predefined_type(object),
            "Name": object.Name,
            "Level": Element.get_container(object).Name
            if Element.get_container(object)
            else "",
            "Type": Element.get_type(object).Name
            if Element.get_type(object)
            else "",

            "QuantitySets": qtos,
            "PropertySets": psets,
        })
        
        actual_length= get_length_layers(object)
        # looking for the maximum of layers among all the elements 
        if actual_length > max_length_layers:
            max_length_layers = actual_length
        
    return objects_data, list(pset_attributes), max_length_layers


def get_attribute_value(object_data, attribute):
    if "." not in attribute:
        return object_data[attribute]
    elif "." in attribute:
        pset_name = attribute.split(".",1)[0]
        prop_name = attribute.split(".",-1)[1]
        if pset_name in object_data["PropertySets"].keys():
            if prop_name in object_data["PropertySets"][pset_name].keys():
                return object_data["PropertySets"][pset_name][prop_name]
            else:
                return None
        if pset_name in object_data["QuantitySets"].keys():
            if prop_name in object_data["QuantitySets"][pset_name].keys():
                return object_data["QuantitySets"][pset_name][prop_name]
            else:
                return None
    else:
        return None
    
# creates a dataframe with the properties and quantities
def get_pandas_df_1(data1,pset_attributes): 
    attributes = ["ExpressId", "GlobalId", "Class", "PredefinedType", "Name", "Level", "Type", ] + pset_attributes

    #getting datas from properties and quantity sets
    pandas_data = []
    for object_data in data1:
        row = []
        for attribute in attributes:
            value = get_attribute_value(object_data, attribute)
            row.append(value)
        pandas_data.append(tuple(row))
        data1 = pd.DataFrame.from_records(pandas_data, columns=attributes) 
    return data1
        
    
def get_pandas_df_2(file, max_length_layers, dataframe_properties_quantities):
    # getting the data foor the materials 
    objects= file.by_type("IfcBuildingElement")
    pandas_data_materials_thickness = []
    for object in objects:
        row = get_material_thickness(object, max_length_layers)
        pandas_data_materials_thickness.append(tuple(row))

    #name of the atributes for the head of the datafram
    attributes_materials_thickness = layers_name(max_length_layers)
    # merging the data with the name of the material layer
    dataframe_materials_thickness = pd.DataFrame.from_records(pandas_data_materials_thickness, columns=attributes_materials_thickness)
    #connecting the data from the quantity sets and the property sets
    return   pd.concat([dataframe_properties_quantities, dataframe_materials_thickness], axis = 1), attributes_materials_thickness           

#adds to the dataframe 2 columns with zero values--> later this values are going to be stored dependning on the material layer   
def get_pandas_df3(attributes_materials_thickness, dataframe):
    #adding a zero dataframe depending on the maximal volumes that are needed, which depend on the material layers
    volume_name = []
    #creates the name of KBOB
    kbob_name = []
    #creates the name of mci 
    #mci_name = []
    
    
    
    
    #creates a dictonary with the maximal length of volumes depending on the layers that are available
    tot_layers = int(len(attributes_materials_thickness)/2)
    for index in range(tot_layers):
        volume_name.append(f'Quantity {index+1}')
        kbob_name.append(f'ID nr. {index+1}')
        #mci_name.append(f' RR {index+1}')
    #adds the names of all properties     
    properties_add =   volume_name + kbob_name          
    #creates a zero value dataframes with the lenght of the data and the maximal entries of volumes hta the dataframe wil have    
    dataframe_volumes = pd.DataFrame(0, index=np.arange(len(dataframe)), columns=properties_add)
    #adds the names of the volumes to the volumes data frame 
    dataframe_volumes = pd.DataFrame.from_records(dataframe_volumes, columns=properties_add)
    #adds the datframe total with the created data frame for the volumes
    dataframe = pd.concat([dataframe, dataframe_volumes], axis = 1)
    return dataframe    




