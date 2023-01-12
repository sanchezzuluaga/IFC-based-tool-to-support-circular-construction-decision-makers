import streamlit as st
import ifcopenshell
import pandas as pd
#import the functions that are created within the project
from tools import functions, functions2, functions3, graphs
import plotly.express as px
import numpy as np

sst = st.session_state





# main function to get the data 
def get_dataframes(material_dataframe):
#functions    
    #gets the data from the ifc file and the max_length layer of all the elements  
    data, pset_attributes, max_length_layers = functions.get_objects_data_by_class(sst.Ifc_file, "IfcBuildingElement")
    #cretaes the first data frame with the properties and the quantties 
    dataframe_properties_quantities = functions.get_pandas_df_1(data,pset_attributes)
    #creates the second dataframe with material thickness and its layers
    dataframe, attributes_materials_thickness = functions.get_pandas_df_2(sst.Ifc_file,max_length_layers, dataframe_properties_quantities) 
    #creates the dataframe with empty values for the volumes --> this will be filled up when calculating the volumes 
    dataframe = functions.get_pandas_df3(attributes_materials_thickness, dataframe)
#functions 2
    # gets the datframes with their respective quantities (divided by IfcClass)
    dataframe_ifc_wall, dataframe_ifc_slab_landing, dataframe_ifc_slab, dataframe_ifc_beam, dataframe_ifc_column, dataframe_ifc_stairflight, dataframe_ifc_window, dataframe_ifc_door, dataframe_ifc_roof =  functions2.insert_quantities_in_dataframe(dataframe, attributes_materials_thickness )
    #merges the dataframes in cubic( e.g IfcWall, IfcSlab)
    dataframe_cubic = pd.concat([dataframe_ifc_wall, dataframe_ifc_slab_landing, dataframe_ifc_slab, dataframe_ifc_beam, dataframe_ifc_column, dataframe_ifc_stairflight, dataframe_ifc_roof])
    dataframe_square = pd.concat([dataframe_ifc_window,dataframe_ifc_door ])
#functions 3
    # gets the in one column all materials in other column all the quantites
    dataframe_cubic_2 = functions3.df_material_quanitty (dataframe_cubic, attributes_materials_thickness)
    dataframe_square_2 = functions3.df_material_quanitty (dataframe_square,attributes_materials_thickness)
    dataframe_cubic_2.columns = ["Class","Level","Material", "Quantity", "KBOB"]
    dataframe_square_2.columns = ["Class","Level","Material", "Quantity", "KBOB"]
    # creates a new data frame to add to the data frame square (This allows the allocation of the KBOB3 to the dataframe)
    #dataframe_square_KBOB2 = pd.DataFrame(0, index=np.arange(len(dataframe_square_2)), columns=["KBOB2"])
    #dataframe_square_2 = pd.concat([dataframe_square_2,dataframe_square_KBOB2 ], axis =1)
    #calculate the elements Doors and windows in the model
    #elements = int(len(dataframe_square_2)/max_length_layers)
    # puts the information of the KBOB of the wall 
    #values = dataframe_square_2.iloc[elements : elements + elements, 4].to_numpy()
    #dataframe_square_2
    #dataframe_square_2.iloc[0: elements, 6] = values
    #remove the whole row if it has a zero value
    dataframe_cubic_2 = dataframe_cubic_2[(dataframe_cubic_2[["Class","Level","Material", "Quantity", "KBOB"]] != 0).all(axis=1)]
    dataframe_square_2 = dataframe_square_2[(dataframe_square_2[["Class","Level","Material", "Quantity", "KBOB"]] != 0).all(axis=1)]
    #change the materials to KBOB materials 
    dataframe_cubic_2 = functions3.convert_to_KBOB_Materials(dataframe_cubic_2,material_dataframe)
    dataframe_square_2 = functions3.convert_to_KBOB_Materials(dataframe_square_2, material_dataframe)
    #creates a dataframe with total quantites per material 
    dataframe_total_per_material_cubic = dataframe_cubic_2.groupby(["Material", "KBOB"])["Quantity"].sum().reset_index(name= "Volume m3") 
    dataframe_total_per_material_square = dataframe_square_2.groupby(["Material","KBOB"])["Quantity"].sum().reset_index(name= "Area m2") 
    #Return the total quantity per material, and the whole dataframe with Classes, KBOB, etc
    return dataframe_total_per_material_cubic, dataframe_total_per_material_square, dataframe_cubic_2, dataframe_square_2

# call back function in order for the model to stay loaded in case the page is changed
def stayUploaded() :
    #creates a variable which tell us that the File is uploaded 
    sst["FileUpload"] = True
    #Loads and decodes the ifc file
    sst["Ifc_file"] = ifcopenshell.file.from_string(st.session_state["file"].getvalue().decode("utf-8"))

    #empty data from uploaded file
    #sst["Levels"]= {}

#function to display the tables side by side

def display_qto():
    col1, col2 = st.columns(2)
    with col1:
        st.write("Dataframe Cubic")
        st.write(sst["Dataframe_total_cubic"])



    with col2:
        st.write("Dataframe Area")
        st.write(sst["Dataframe_total_square"])
       

    col3, col4 = st.columns(2)

    with col3:
        st.write("Graph")
        fig_cubic = graphs.get_pie_chart(sst["Dataframe_total_cubic"])
        st.write(fig_cubic)
    
    with col4:
        st.write("Graph")
        fig_area = graphs.get_pie_chart(sst["Dataframe_total_square"])
        st.write(fig_area)
            #gets all the levels among the data 
    levels = functions3.get_classes_levels("Level", sst["dataframe_cubic"])
    #gets the level indicated by the user 
    level_selector = st.selectbox("Select Level", options= levels or[] , key="level_selector")
    

    col5, col6 = st.columns(2)
    with col5:
        st.write("Graph Cubic")
        #filters the data frame
        sst["Dataframe_Filter_Level_Cubic"] = functions3.dataframe_filtered_by_input(sst["dataframe_cubic"],sst.level_selector, "Level")
        #st.write(sst["Dataframe_Filter_Level_Cubic"])
        df_bar_plot_cubic = sst["Dataframe_Filter_Level_Cubic"].groupby(["Class", "Material"])["Quantity"].sum().reset_index(name='Quantity')
        fig_bar_plot_cubic = px.bar(df_bar_plot_cubic, x= "Class", y="Quantity", color="Material", title="Quantites per Level", width= 800, height= 600)
        st.write(fig_bar_plot_cubic)




  
    with col6:
        st.write("Graph Doors and Windows")
        #filters the data frame
        sst["Dataframe_Filter_Level_Square"] = functions3.dataframe_filtered_by_input(sst["dataframe_square"],sst.level_selector, "Level")
        df_bar_plot_square = sst["dataframe_square"].groupby(["Class", "Material"])["Quantity"].count().reset_index(name='Quantity')
        fig_bar_plot_square = px.bar(df_bar_plot_square, x= "Class", y="Quantity", color="Material", title="Quantites per Level", width= 800, height= 600)
        st.write(fig_bar_plot_square)




    
     







def qto(): 
    st.title("Quantity Take-off")     

   
    #uploads the file
    upload_file  = st.file_uploader("Upload IFC file", key = "file", on_change = stayUploaded)

   

    #check if the model is uploaded
    if "FileUpload" in sst and sst["FileUpload"]:
        st.success(f'Model loaded')

    # gets data from KBOB
    material_dataframe = pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx', sheet_name='Material')      
    
    # gets data from ifc
    dataframe_total_cubic, dataframe_total_square, dataframe_cubic_2, dataframe_suqare_2 = get_dataframes(material_dataframe)
    sst["Dataframe_total_cubic"] = dataframe_total_cubic
    sst["Dataframe_total_square"] = dataframe_total_square
    sst["dataframe_cubic"] = dataframe_cubic_2
    sst["dataframe_square"] = dataframe_suqare_2


    

    
    #display in the app
    display_qto()

    #st.write(a)
    









qto()



