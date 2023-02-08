import streamlit as st
import pandas as pd
#import the functions that are created within the project
from tools import functions, functions2, functions3, graphs, cost_functions, environmental_functions
import plotly.express as px
import numpy as np
import googlemaps
import math

#importing all the packages
#KBOB Database
material_dataframe = pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx', sheet_name='Material')
#Cost Dataframe
cost_dataframe  = pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx', header = [0,1] ,sheet_name='Costs')
#Cost transport dataframe
cost_transport_dataframe = pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx', header = [0,1] ,sheet_name='Cost_Transport')
#dataframe scenarios
dataframe_scenarios =  pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx'  ,sheet_name= 'Scenarios')
#dataframe KBOB 
transport_KBOB_dataframe = pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx'  ,sheet_name= 'Transport_EI')  
 
 
#session
sst = st.session_state

#addresses
#addresses
addres_building = "Birmensdorferstrasse 184, 8003 Zurich"
address_landfill = "Langgrütstrasse 184, 8047 Zurich"
address_incinaration_plant = "Langgrütstrasse 134, 8047 Zurich"
addres_concrete_brick = "Langgrütstrasse 184, 8047 Zurich"
addres_glas = "Hochstrasse 108, 8044 Zürich"
addres_metals = "Langgrütstrasse 134, 8047 Zurich"
addres_wood = "Stefano- Franscini, Platz 5, 8049 Zürich"
addres_storage = "Stefano- Franscini, Platz 5, 8049 Zürich"
addres_building = "Birmensdorferstrasse 184, 8003 Zurich"




#stay uploaded (the file stay uploaded if we change among pages)
def stayUploaded_2() :
    #creates a variable which tell us that the File is uploaded 
    sst["FileUpload_2"] = True

def display_adresses():
    #address or default values known 
    page_names_2 = ["Default values", "Addresses known" ] 
    page_2 = st.sidebar.radio('Select an option  ', page_names_2 , index=1) 

    if page_2 == "Default values":
        st.sidebar.write("Default values")

    else:
        addres_building_1= st.sidebar.text_input(label="Address Building", key= "address_building")
        addres_storage_1 = st.sidebar.text_input(label="Address Storage", key= "address_storage")
        addres_incineration_1 = st.sidebar.text_input(label="Address Incineration", key= "address_incineration")
        addres_landfill_1 = st.sidebar.text_input(label="Address Landfill", key= "address_landfill")

















   

def tool2():

    
    
    
    
    
    
    # creating the names of the bottoms
    page_names_1 = ['IFC File available', 'Template available']
    page_1 = st.sidebar.radio('Select an option', page_names_1, index=1)

    # IFC available
    if page_1 == 'IFC File available':
        
        #tabs
        st.sidebar.write("Dataframe  imported from QTO")
        
        tab_titles = ["Environmental Impact", "Cost"]
        tabs = st.tabs(tab_titles)
        #display adresses
        display_adresses() 
        #sst["Dataframe_total_square"]

        #Tab for environmental impact    
        #environmental impact
        with tabs[0]:
            st.title("Environmental Impact")

            #OUTPUTS FROM EACH SCENARIO
            #SCENSRIO 0
            environmental_impact_disposal_cubic_scenario_0 =  environmental_functions.get_environmental_impact_disposal( sst["Dataframe_total_cubic"],material_dataframe, transport_KBOB_dataframe )
            environmental_impact_disposal_square_scenario_0 = environmental_functions.get_environmental_impact_disposal( sst["Dataframe_total_square"],material_dataframe, transport_KBOB_dataframe )
            #gets the total env impact scenario 0 
            environmental_impact_disposal_scenario_0 = pd.concat([environmental_impact_disposal_cubic_scenario_0,environmental_impact_disposal_square_scenario_0 ])
            sst["Environemntal impact disposal scenario 0"] = environmental_impact_disposal_scenario_0
        

            #SCENARIO 1
            environmental_impact_disposal_scenario_1,  environmental_impact_recycle_scenario_1, environmental_impact_reuse_scenario_1 = environmental_functions.get_envrionmental_impact_scenario_1(sst["Dataframe_total_cubic"], sst["Dataframe_total_square"] ,dataframe_scenarios,material_dataframe,addres_building,addres_concrete_brick,addres_glas,addres_metals,addres_wood,transport_KBOB_dataframe,addres_storage)
            environmental_impact_scenario_1 = pd.concat([environmental_impact_disposal_scenario_1,  environmental_impact_recycle_scenario_1, environmental_impact_reuse_scenario_1])
            sst["Environmental impact scenario 1" ] = environmental_impact_scenario_1

            #SCENARIO 2
            environmental_impact_disposal_scenario_2,  environmental_impact_recycle_scenario_2, environmental_impact_reuse_scenario_2 = environmental_functions.get_envrionmental_impact_scenario_2(sst["Dataframe_total_cubic"], sst["Dataframe_total_square"] ,dataframe_scenarios,material_dataframe,addres_building,addres_concrete_brick,addres_glas,addres_metals,addres_wood,transport_KBOB_dataframe,addres_storage)
            environmental_impact_scenario_2 = pd.concat([environmental_impact_disposal_scenario_2,  environmental_impact_recycle_scenario_2, environmental_impact_reuse_scenario_2])
            sst["Environmental impact scenario 2" ] = environmental_impact_scenario_2



                      
        
            #scenario 0 (Worst Case scenario)
            #columns to divide the environemntal impact
            st.header("Worst-case scenario (scenario 0) ")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Total environmental impact:") 
                #sums the dataframe and gets the dotal for the disposal
                sst["Environemntal impact disposal total"] = environmental_functions.df_EI_to_plot(sst["Environemntal impact disposal scenario 0"] )
                #transpose the dataframe to get the total value of  A1-A3 , etc 
                df_bar_plot_disposal_scenario_0 = sst["Environemntal impact disposal total"]
                #plot
                fig_bar_plot_disposal_scenario_0 = px.bar(df_bar_plot_disposal_scenario_0, x= "Stages", y="kg-CO2_eq", title="Environmental impact total", width= 650, height= 600)
                st.write(fig_bar_plot_disposal_scenario_0)



            
            with col2:
                st.write("Environmental impact by material:")
                #gets a list of the materials to get in the selecor
                #materials = environmental_functions.get_materials(sst["Environemntal impact disposal scenario 0"])
                st.markdown("    ")
                st.markdown("    ")
                st.markdown("    ")
                st.markdown("    ")
                st.markdown("    ")
                st.markdown("    ")
                st.markdown("    ")
                st.markdown("    ")
                st.write(sst["Environemntal impact disposal scenario 0"])


            #Base line scenario (Scenario 1)
            st.header("Baseline scenario (scenario 1) ")
            sst["Environemntal impact scenario 1 total"] = environmental_functions.df_EI_to_plot( sst["Environmental impact scenario 1" ] )
            df_bar_plot_scenario_1 = sst["Environemntal impact scenario 1 total"]
            #plot
            fig_bar_plot_scenario_1 = px.bar(df_bar_plot_scenario_1, x= "Stages", y="kg-CO2_eq", title="Environmental impact total", width= 650, height= 600)
            st.write(fig_bar_plot_scenario_1)


            col3, col4, col5 = st.columns(3)
            with col3:
                st.write("Environmental impact disposal:")
                st.write(environmental_impact_disposal_scenario_1)

            with col4:
                st.write("Environmental impact recycle:")
                st.write(environmental_impact_recycle_scenario_1)

            with col5:
                st.write("Environemntal impact reuse:")
                st.write(environmental_impact_reuse_scenario_1)




            
            #Best case scenario (Scenario 2)
            st.header("Best-case scenario (scenario 2) ")
            sst["Environemntal impact scenario 2 total"] = environmental_functions.df_EI_to_plot( sst["Environmental impact scenario 2" ] )
            df_bar_plot_scenario_2 = sst["Environemntal impact scenario 2 total"]
            #plot
            fig_bar_plot_scenario_2 = px.bar(df_bar_plot_scenario_2, x= "Stages", y="kg-CO2_eq", title="Environmental impact total", width= 650, height= 600)
            st.write(fig_bar_plot_scenario_2)


            col6, col7, col8 = st.columns(3)
            with col6:
                st.write("Environmental impact disposal:")
                st.write(environmental_impact_disposal_scenario_2)

            with col7:
                st.write("Environmental impact recycle:")
                st.write(environmental_impact_recycle_scenario_2)

            with col8:
                st.write("Environemntal impact reuse:")
                st.write(environmental_impact_reuse_scenario_2)


                
                





        #Tab for cost
        # COST 
        with tabs[1]:
            st.title("Cost")
            total_costs_scenario_0, total_cost_reuse_1, total_cost_recycle_1, total_cost_disposal_1,  total_cost_reuse_2, total_cost_recycle_2, total_cost_disposal_2  = cost_functions.get_total_cost(sst["Dataframe_total_cubic"], sst["Dataframe_total_square"], cost_dataframe, cost_transport_dataframe, dataframe_scenarios , addres_building, address_landfill, address_incinaration_plant, addres_concrete_brick, addres_glas, addres_metals, addres_wood, addres_storage)     
            
            st.header("Worst-case scenario (scenario 0) ")
            #scenario 0
            sst["Dataframe total cost scenario 0"] =  cost_functions.df_cost_to_plot_scenario_0(total_costs_scenario_0)
            df_bar_plot_cost_scenario_0 = sst["Dataframe total cost scenario 0"]
            #plot
            fig_bar_plot_cost_scenario_0 = px.bar(df_bar_plot_cost_scenario_0, x= "Costs", y="CHF", title="Total cost", width= 800, height= 500)
            st.write(fig_bar_plot_cost_scenario_0)

            st.header("Baseline scenario (scenario 1) ")
            #scenario 1
            #merges all the cost in one dataframe
            total_cost_scenario_1 = pd.concat([total_cost_reuse_1, total_cost_recycle_1, total_cost_disposal_1])
            #fills the non values with zero
            total_cost_scenario_1 = total_cost_scenario_1.fillna(0)
            sst["Dataframe total cost scenario 1"] =  cost_functions.df_cost_to_plot_scenario_1_2(total_cost_scenario_1)
            df_bar_plot_cost_scenario_1 = sst["Dataframe total cost scenario 1"]
            #plot
            fig_bar_plot_cost_scenario_1 = px.bar(df_bar_plot_cost_scenario_1, x= "Costs", y="CHF", title="Total cost", width= 800, height= 500)
            st.write(fig_bar_plot_cost_scenario_1)

            #scenario 2
            st.header("Best-case scenario (scenario 2) ")
            #merges all the cost in one dataframe
            total_cost_scenario_2 = pd.concat([total_cost_reuse_2, total_cost_recycle_2, total_cost_disposal_2])
            #fills the non values with zero
            total_cost_scenario_2 = total_cost_scenario_2.fillna(0)
            sst["Dataframe total cost scenario 2"] =  cost_functions.df_cost_to_plot_scenario_1_2(total_cost_scenario_2)
            df_bar_plot_cost_scenario_2 = sst["Dataframe total cost scenario 2"]
            #plot
            fig_bar_plot_cost_scenario_2 = px.bar(df_bar_plot_cost_scenario_2, x= "Costs", y="CHF", title="Total cost", width= 800, height= 500)
            st.write(fig_bar_plot_cost_scenario_2)




            
            



    #Template availabe 
    else:
        #uploading th Excel file
        display_adresses()
        st.write("Upload excelfile")
        upload_file_2  = st.file_uploader("Upload Template", key = "file_2", on_change = stayUploaded_2, type= ["xlsx"])
        cubic_data_frame = pd.read_excel(upload_file_2 ,sheet_name='Cubic')
        square_data_frame = pd.read_excel(upload_file_2 ,sheet_name='Square')
        tab_titles = ["Environmental Impact", "Cost"]
        tabs = st.tabs(tab_titles)
        with tabs[0]:
            st.title("Environmental Impact")
            st.write(cubic_data_frame)
            st.write(square_data_frame)
        

        #cost 
        with tabs[1]:
            st.title("Cost")  
    














    
    









    











tool2()


                #material_selector = st.selectbox("Select Material", options= materials or[] , key="material_selector")
                #sst["Dataframe Filtered by Material"] = environmental_functions.dataframe_filtered_by_MaterialInput( sst["Environemntal impact disposal scenario 0"],sst.material_selector )
                #sst["Dataframe Filtered by Material"] =  environmental_functions.df_EI_to_plot(sst["Dataframe Filtered by Material"])
                #df_bar_plot_disposal_scenario_0_per_material = sst["Dataframe Filtered by Material"]
                #plot
                #fig_bar_plot_disposal_scenario_0_per_material = px.bar(df_bar_plot_disposal_scenario_0_per_material, x= "Stages", y="kg-CO2_eq", title="Environmental impact material", width= 800, height= 500)

        
                #st.write(fig_bar_plot_disposal_scenario_0_per_material)

