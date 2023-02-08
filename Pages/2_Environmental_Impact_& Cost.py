import streamlit as st
import pandas as pd
#import the functions that are created within the project
from tools import graphs, cost_functions, environmental_functions, quantity_takeoff_1, quantity_takeoff_2, quantity_takeoff_3
import plotly.express as px
import numpy as np
import googlemaps
import math

#comments:
#scanrio 0 = worst-case scenario, scenario 1 = baseline scenario, scenario 2 = best-case scenario 
#cubic dataframe = volume dataframe, square dataframe = area dataframe 

#importing the database
#KBOB Database materials
#basePath = "C:/User/" # replace this string with the base directory of the repository
#material_dataframe = pd.read_excel('Data/Database.xlsx', sheet_name='Material')
material_dataframe = pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx', sheet_name='Material')
#Cost Dataframe
cost_dataframe  = pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx', header = [0,1] ,sheet_name='Costs')
#Cost transport dataframe
cost_transport_dataframe = pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx', header = [0,1] ,sheet_name='Cost_Transport')
#dataframe scenarios
dataframe_scenarios =  pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx'  ,sheet_name= 'Scenarios')
#dataframe KBOB transport
transport_KBOB_dataframe = pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx'  ,sheet_name= 'Transport_EI')  
 
 
#session
sst = st.session_state






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
        address = dict()
        address["building"] = "Birmensdorferstrasse 533, 8055 Zürich"
        address["landfill"] = "Toblerstrasse 44, 8044 Zürich"
        address["incineration plant"] = "Toblerstrasse 44, 8044 Zürich"
        address["concrete_brick"] = "Toblerstrasse 44, 8044 Zürich"
        address["glass"] = "Toblerstrasse 44, 8044 Zürich"
        address["metals"] = "Toblerstrasse 44, 8044 Zürich"
        address["wood"]  = "Toblerstrasse 44, 8044 Zürich"
        address["storage"]  = "Toblerstrasse 44, 8044 Zürich"

        if address["building"] and address["landfill"] and address["incineration plant"] and address["concrete_brick"] and address["glass"] and address["metals"] and address["wood"] and  address["storage"] :
            defined = True
        else:
            defined = False






    else:
        #define all the addresses
        address = dict()

        address["building"] = st.sidebar.text_input(
            label="Address building",
            key= "address_building")

        address["landfill"] = st.sidebar.text_input(
            label="Address landfill",
            key= "address_landfill")

        address["incineration plant"] = st.sidebar.text_input(
            label="Address incineration plant ",
            key= "address_incineration_plant")    

        address["concrete_brick"] = st.sidebar.text_input(
            label="Address concrete brick",
            key= "address_concrete_brick")

        address["glass"] = st.sidebar.text_input(
            label="Address glass",
            key= "address_glas")        
                
        address["metals"] = st.sidebar.text_input(
            label="Address metals",
            key= "address_metals")

        address["wood"]  = st.sidebar.text_input(
            label="Address wood",
            key= "address_wood")
        
        address["storage"]  = st.sidebar.text_input(
            label="Address storage",
            key= "address_storage")
        
    



        if address["building"] and address["landfill"] and address["incineration plant"] and address["concrete_brick"] and address["glass"] and address["metals"] and address["wood"] and  address["storage"] :
            defined = True
        else:
            defined = False

    return defined, address








   

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
        defined, address = display_adresses()  
        #sst["Dataframe_total_square"]

        if defined:
            #Tab for environmental impact    
            #environmental impact
            with tabs[0]:
                st.title("Environmental Impact")

                #OUTPUTS FROM EACH SCENARIO INCLUDING A4-A5 and D
                #SCENSRIO 0
                environmental_impact_disposal_cubic_scenario_0 =  environmental_functions.get_environmental_impact_disposal(sst["Dataframe_total_cubic"],material_dataframe, transport_KBOB_dataframe )
                environmental_impact_disposal_square_scenario_0 = environmental_functions.get_environmental_impact_disposal( sst["Dataframe_total_square"],material_dataframe, transport_KBOB_dataframe )
                #gets the total env impact scenario 0 
                environmental_impact_disposal_scenario_0 = pd.concat([environmental_impact_disposal_cubic_scenario_0,environmental_impact_disposal_square_scenario_0 ])
                sst["Environemntal impact disposal scenario 0"] = environmental_impact_disposal_scenario_0
            

                #SCENARIO 1
                environmental_impact_disposal_scenario_1,  environmental_impact_recycle_scenario_1, environmental_impact_reuse_scenario_1 = environmental_functions.get_envrionmental_impact_scenario_1(sst["Dataframe_total_cubic"], sst["Dataframe_total_square"] ,dataframe_scenarios,material_dataframe,address["building"],address["concrete_brick"],address["glass"],address["metals"],address["wood"],transport_KBOB_dataframe,address["storage"])
                environmental_impact_scenario_1 = pd.concat([environmental_impact_disposal_scenario_1,  environmental_impact_recycle_scenario_1, environmental_impact_reuse_scenario_1])
                sst["Environmental impact scenario 1" ] = environmental_impact_scenario_1

                #SCENARIO 2
                environmental_impact_disposal_scenario_2,  environmental_impact_recycle_scenario_2, environmental_impact_reuse_scenario_2 = environmental_functions.get_envrionmental_impact_scenario_2(sst["Dataframe_total_cubic"], sst["Dataframe_total_square"] ,dataframe_scenarios,material_dataframe,address["building"],address["concrete_brick"],address["glass"],address["metals"],address["wood"],transport_KBOB_dataframe, address["storage"])
                environmental_impact_scenario_2 = pd.concat([environmental_impact_disposal_scenario_2,  environmental_impact_recycle_scenario_2, environmental_impact_reuse_scenario_2])
                sst["Environmental impact scenario 2" ] = environmental_impact_scenario_2

                ## Dataframe without A4-A5, D --> for displaying in the interface
                # SCENARIO 0-Worst case scenario
                sst["Environemntal impact disposal scenario 0_A-C"] = sst["Environemntal impact disposal scenario 0"].loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                #SCENARIO 1- BAseline scenario
                environmental_impact_disposal_scenario_1_A_C = environmental_impact_disposal_scenario_1.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                environmental_impact_recycle_scenario_1_A_C =  environmental_impact_recycle_scenario_1.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                environmental_impact_reuse_scenario_1_A_C = environmental_impact_reuse_scenario_1.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                #SCENARIO 2- BEstcase scenario
                environmental_impact_disposal_scenario_2_A_C = environmental_impact_disposal_scenario_2.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                environmental_impact_recycle_scenario_2_A_C = environmental_impact_recycle_scenario_2.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                environmental_impact_reuse_scenario_2_A_C = environmental_impact_reuse_scenario_2.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]

                #Total dataframes
                sst["Environemntal impact disposal total"] = environmental_functions.df_EI_to_plot(sst["Environemntal impact disposal scenario 0"] )
                sst["Environemntal impact scenario 1 total"] = environmental_functions.df_EI_to_plot( sst["Environmental impact scenario 1" ] )
                sst["Environemntal impact scenario 2 total"] = environmental_functions.df_EI_to_plot( sst["Environmental impact scenario 2" ] )

                #Output of total environmental impact

                sum_worst_case_scenario = sst["Environemntal impact disposal total"]['kg-CO2_eq'].sum()
                sum_baseline_scenario = sst["Environemntal impact scenario 1 total"]['kg-CO2_eq'].sum()
                sum_bestcase_scenario =  sst["Environemntal impact scenario 2 total"]['kg-CO2_eq'].sum()
                #summary scenario 
                summary_df = pd.DataFrame([[int(sum_worst_case_scenario),int(sum_baseline_scenario) , int(sum_bestcase_scenario)]], columns=['Worstcase (kg-CO2-eq)', 'Baseline (kg-CO2-eq)', 'Bestcase (kg-CO2-eq)'])
                summary_df = summary_df.applymap(lambda x: "{:,}".format(x).replace(',', "'") if isinstance(x, (int, float)) else x)
                st.title("Overview")
                st.write(summary_df)
                

                


                        
            
                #scenario 0 (Worst Case scenario)
                #columns to divide the environemntal impact
                st.header("Worst-case scenario: all materials disposed (0% Reuse, 0% Recycle) ")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Total environmental impact:") 
                    #sums the dataframe and gets the dotal for the disposal
                    #sst["Environemntal impact disposal total"] = environmental_functions.df_EI_to_plot(sst["Environemntal impact disposal scenario 0"] )
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
                    st.write( sst["Environemntal impact disposal scenario 0_A-C"])


                #Base line scenario (Scenario 1)
                st.header("Baseline scenario: based on the reuse potential, the materials are then recycled/disposed at the average rate of Switzerland ")
                #sst["Environemntal impact scenario 1 total"] = environmental_functions.df_EI_to_plot( sst["Environmental impact scenario 1" ] )
                df_bar_plot_scenario_1 = sst["Environemntal impact scenario 1 total"]
                #plot
                fig_bar_plot_scenario_1 = px.bar(df_bar_plot_scenario_1, x= "Stages", y="kg-CO2_eq", title="Environmental impact total", width= 650, height= 600)
                st.write(fig_bar_plot_scenario_1)


                col3, col4, col5 = st.columns(3)
                with col3:
                    st.write("Environmental impact disposal:")
                    st.write(environmental_impact_disposal_scenario_1_A_C)

                with col4:
                    st.write("Environmental impact recycle:")
                    st.write(environmental_impact_recycle_scenario_1_A_C)

                with col5:
                    st.write("Environemntal impact reuse:")
                    st.write(environmental_impact_reuse_scenario_1_A_C )




                
                #Best case scenario (Scenario 2)
                st.header("Best-case scenario: if a mataterial have a reuse potential, the material is reused 100%, otherwise is recycled 100% ")
                #sst["Environemntal impact scenario 2 total"] = environmental_functions.df_EI_to_plot( sst["Environmental impact scenario 2" ] )
                df_bar_plot_scenario_2 = sst["Environemntal impact scenario 2 total"]
                #plot
                fig_bar_plot_scenario_2 = px.bar(df_bar_plot_scenario_2, x= "Stages", y="kg-CO2_eq", title="Environmental impact total", width= 650, height= 600)
                st.write(fig_bar_plot_scenario_2)


                col6, col7, col8 = st.columns(3)
                with col6:
                    st.write("Environmental impact disposal:")
                    st.write(environmental_impact_disposal_scenario_2_A_C)

                with col7:
                    st.write("Environmental impact recycle:")
                    st.write(environmental_impact_recycle_scenario_2_A_C)

                with col8:
                    st.write("Environemntal impact reuse:")
                    st.write(environmental_impact_reuse_scenario_2_A_C)


                    
                    





            #Tab for cost
            # COST 
            with tabs[1]:
                st.title("Cost")
                total_costs_scenario_0, total_cost_reuse_1, total_cost_recycle_1, total_cost_disposal_1,  total_cost_reuse_2, total_cost_recycle_2, total_cost_disposal_2  = cost_functions.get_total_cost(sst["Dataframe_total_cubic"], sst["Dataframe_total_square"], cost_dataframe, cost_transport_dataframe, dataframe_scenarios , address["building"], address["landfill"], address["incineration plant"], address["concrete_brick"],address["glass"], address["metals"], address["wood"], address["storage"])     
                
                
                #OTTAL COST
                # WORST CASE SCENARIO (scenario0 )
                sst["Dataframe total cost scenario 0"] =  cost_functions.df_cost_to_plot_scenario_0(total_costs_scenario_0)

                # BASELINE SCENARIO (scenario 1)
                #merges all the cost in one dataframe
                total_cost_scenario_1 = pd.concat([total_cost_reuse_1, total_cost_recycle_1, total_cost_disposal_1])
                #fills the non values with zero
                total_cost_scenario_1 = total_cost_scenario_1.fillna(0)
                sst["Dataframe total cost scenario 1"] =  cost_functions.df_cost_to_plot_scenario_1_2(total_cost_scenario_1)


                #BEST CASE SCENARIO (scenario 2)
                total_cost_scenario_2 = pd.concat([total_cost_reuse_2, total_cost_recycle_2, total_cost_disposal_2])
                #fills the non values with zero
                total_cost_scenario_2 = total_cost_scenario_2.fillna(0)
                sst["Dataframe total cost scenario 2"] =  cost_functions.df_cost_to_plot_scenario_1_2(total_cost_scenario_2)

                #OVERVIEW OF COSTS
                sum_worst_case_scenario_cost =sst["Dataframe total cost scenario 0"] ['CHF'].sum()
                sum_baseline_scenario_cost = sst["Dataframe total cost scenario 1"]['CHF'].sum()
                sum_bestcase_scenario_cost =  sst["Dataframe total cost scenario 2"]['CHF'].sum()
                #summary scenario 
                summary_cost_df = pd.DataFrame([[int(sum_worst_case_scenario_cost),int(sum_baseline_scenario_cost) , int(sum_bestcase_scenario_cost)]], columns=['Worstcase (CHF)', 'Baseline (CHF)', 'Bestcase (CHF)'])
                summary_cost_df = summary_cost_df.applymap(lambda x: "{:,}".format(x).replace(',', "'") if isinstance(x, (int, float)) else x)
                st.title("Overview")
                st.write(summary_cost_df)
                
                
                st.header("Worst-case scenario: All materials disposed (0% Reuse, 0% Recycle) ")
                #scenario 0
                df_bar_plot_cost_scenario_0 = sst["Dataframe total cost scenario 0"]
                #plot
                fig_bar_plot_cost_scenario_0 = px.bar(df_bar_plot_cost_scenario_0, x= "Costs", y="CHF", title="Total cost", width= 800, height= 500)
                st.write(fig_bar_plot_cost_scenario_0)

                st.header("Baseline scenario: Based on the reuse potential, the materials are then recycled/disposed at the average rate of Switzerland ")
                #scenario 1
                df_bar_plot_cost_scenario_1 = sst["Dataframe total cost scenario 1"]
                #plot
                fig_bar_plot_cost_scenario_1 = px.bar(df_bar_plot_cost_scenario_1, x= "Costs", y="CHF", title="Total cost", width= 800, height= 500)
                st.write(fig_bar_plot_cost_scenario_1)

                #scenario 2
                st.header("Best-case scenario (scenario 2) ")
                #merges all the cost in one dataframe
                df_bar_plot_cost_scenario_2 = sst["Dataframe total cost scenario 2"]
                #plot
                fig_bar_plot_cost_scenario_2 = px.bar(df_bar_plot_cost_scenario_2, x= "Costs", y="CHF", title="Total cost", width= 800, height= 500)
                st.write(fig_bar_plot_cost_scenario_2)
        else:
            st.warning("Please insert the addresses")
            st.stop()




            
            



    #Template availabe 
    else:
        #uploading th Excel file
        st.write("Upload excelfile")
        upload_file_2  = st.file_uploader("Upload Template", key = "file_2", on_change = stayUploaded_2, type= ["xlsx"])
        sst["Dataframe_total_cubic"] = pd.read_excel(upload_file_2 ,sheet_name='Cubic')
        sst["Dataframe_total_square"] = pd.read_excel(upload_file_2 ,sheet_name='Square')
        defined, address = display_adresses()  
        tab_titles = ["Environmental Impact", "Cost"]
        tabs = st.tabs(tab_titles)
        #sst["Dataframe_total_square"]

        if defined:
            #Tab for environmental impact    
            #environmental impact
            with tabs[0]:
                st.title("Environmental Impact")

                #OUTPUTS FROM EACH SCENARIO INCLUDING A4-A5 and D
                #SCENSRIO 0
                environmental_impact_disposal_cubic_scenario_0 =  environmental_functions.get_environmental_impact_disposal(sst["Dataframe_total_cubic"],material_dataframe, transport_KBOB_dataframe )
                environmental_impact_disposal_square_scenario_0 = environmental_functions.get_environmental_impact_disposal( sst["Dataframe_total_square"],material_dataframe, transport_KBOB_dataframe )
                #gets the total env impact scenario 0 
                environmental_impact_disposal_scenario_0 = pd.concat([environmental_impact_disposal_cubic_scenario_0,environmental_impact_disposal_square_scenario_0 ])
                sst["Environemntal impact disposal scenario 0"] = environmental_impact_disposal_scenario_0
            

                #SCENARIO 1
                environmental_impact_disposal_scenario_1,  environmental_impact_recycle_scenario_1, environmental_impact_reuse_scenario_1 = environmental_functions.get_envrionmental_impact_scenario_1(sst["Dataframe_total_cubic"], sst["Dataframe_total_square"] ,dataframe_scenarios,material_dataframe,address["building"],address["concrete_brick"],address["glass"],address["metals"],address["wood"],transport_KBOB_dataframe,address["storage"])
                environmental_impact_scenario_1 = pd.concat([environmental_impact_disposal_scenario_1,  environmental_impact_recycle_scenario_1, environmental_impact_reuse_scenario_1])
                sst["Environmental impact scenario 1" ] = environmental_impact_scenario_1

                #SCENARIO 2
                environmental_impact_disposal_scenario_2,  environmental_impact_recycle_scenario_2, environmental_impact_reuse_scenario_2 = environmental_functions.get_envrionmental_impact_scenario_2(sst["Dataframe_total_cubic"], sst["Dataframe_total_square"] ,dataframe_scenarios,material_dataframe,address["building"],address["concrete_brick"],address["glass"],address["metals"],address["wood"],transport_KBOB_dataframe, address["storage"])
                environmental_impact_scenario_2 = pd.concat([environmental_impact_disposal_scenario_2,  environmental_impact_recycle_scenario_2, environmental_impact_reuse_scenario_2])
                sst["Environmental impact scenario 2" ] = environmental_impact_scenario_2

                ## Dataframe without A4-A5, D --> for displaying in the interface
                # SCENARIO 0-Worst case scenario
                sst["Environemntal impact disposal scenario 0_A-C"] = sst["Environemntal impact disposal scenario 0"].loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                #SCENARIO 1- BAseline scenario
                environmental_impact_disposal_scenario_1_A_C = environmental_impact_disposal_scenario_1.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                environmental_impact_recycle_scenario_1_A_C =  environmental_impact_recycle_scenario_1.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                environmental_impact_reuse_scenario_1_A_C = environmental_impact_reuse_scenario_1.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                #SCENARIO 2- BEstcase scenario
                environmental_impact_disposal_scenario_2_A_C = environmental_impact_disposal_scenario_2.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                environmental_impact_recycle_scenario_2_A_C = environmental_impact_recycle_scenario_2.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]
                environmental_impact_reuse_scenario_2_A_C = environmental_impact_reuse_scenario_2.loc[:,["Material","KBOB","A1-A3", "C1-C4"]]

                #Total dataframes
                sst["Environemntal impact disposal total"] = environmental_functions.df_EI_to_plot(sst["Environemntal impact disposal scenario 0"] )
                sst["Environemntal impact scenario 1 total"] = environmental_functions.df_EI_to_plot( sst["Environmental impact scenario 1" ] )
                sst["Environemntal impact scenario 2 total"] = environmental_functions.df_EI_to_plot( sst["Environmental impact scenario 2" ] )

                #Output of total environmental impact

                sum_worst_case_scenario = sst["Environemntal impact disposal total"]['kg-CO2_eq'].sum()
                sum_baseline_scenario = sst["Environemntal impact scenario 1 total"]['kg-CO2_eq'].sum()
                sum_bestcase_scenario =  sst["Environemntal impact scenario 2 total"]['kg-CO2_eq'].sum()
                #summary scenario 
                summary_df = pd.DataFrame([[int(sum_worst_case_scenario),int(sum_baseline_scenario) , int(sum_bestcase_scenario)]], columns=['Worstcase (kg-CO2-eq)', 'Baseline (kg-CO2-eq)', 'Bestcase (kg-CO2-eq)'])
                summary_df = summary_df.applymap(lambda x: "{:,}".format(x).replace(',', "'") if isinstance(x, (int, float)) else x)
                st.title("Overview")
                st.write(summary_df)
                

                


                        
            
                #scenario 0 (Worst Case scenario)
                #columns to divide the environemntal impact
                st.header("Worst-case scenario: all materials disposed (0% Reuse, 0% Recycle) ")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Total environmental impact:") 
                    #sums the dataframe and gets the dotal for the disposal
                    #sst["Environemntal impact disposal total"] = environmental_functions.df_EI_to_plot(sst["Environemntal impact disposal scenario 0"] )
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
                    st.write( sst["Environemntal impact disposal scenario 0_A-C"])


                #Base line scenario (Scenario 1)
                st.header("Baseline scenario: based on the reuse potential, the materials are then recycled/disposed at the average rate of Switzerland ")
                #sst["Environemntal impact scenario 1 total"] = environmental_functions.df_EI_to_plot( sst["Environmental impact scenario 1" ] )
                df_bar_plot_scenario_1 = sst["Environemntal impact scenario 1 total"]
                #plot
                fig_bar_plot_scenario_1 = px.bar(df_bar_plot_scenario_1, x= "Stages", y="kg-CO2_eq", title="Environmental impact total", width= 650, height= 600)
                st.write(fig_bar_plot_scenario_1)


                col3, col4, col5 = st.columns(3)
                with col3:
                    st.write("Environmental impact disposal:")
                    st.write(environmental_impact_disposal_scenario_1_A_C)

                with col4:
                    st.write("Environmental impact recycle:")
                    st.write(environmental_impact_recycle_scenario_1_A_C)

                with col5:
                    st.write("Environemntal impact reuse:")
                    st.write(environmental_impact_reuse_scenario_1_A_C )




                
                #Best case scenario (Scenario 2)
                st.header("Best-case scenario: if a mataterial have a reuse potential, the material is reused 100%, otherwise is recycled 100% ")
                #sst["Environemntal impact scenario 2 total"] = environmental_functions.df_EI_to_plot( sst["Environmental impact scenario 2" ] )
                df_bar_plot_scenario_2 = sst["Environemntal impact scenario 2 total"]
                #plot
                fig_bar_plot_scenario_2 = px.bar(df_bar_plot_scenario_2, x= "Stages", y="kg-CO2_eq", title="Environmental impact total", width= 650, height= 600)
                st.write(fig_bar_plot_scenario_2)


                col6, col7, col8 = st.columns(3)
                with col6:
                    st.write("Environmental impact disposal:")
                    st.write(environmental_impact_disposal_scenario_2_A_C)

                with col7:
                    st.write("Environmental impact recycle:")
                    st.write(environmental_impact_recycle_scenario_2_A_C)

                with col8:
                    st.write("Environemntal impact reuse:")
                    st.write(environmental_impact_reuse_scenario_2_A_C)


                    
                    





            #Tab for cost
            # COST 
            with tabs[1]:
                st.title("Cost")
                total_costs_scenario_0, total_cost_reuse_1, total_cost_recycle_1, total_cost_disposal_1,  total_cost_reuse_2, total_cost_recycle_2, total_cost_disposal_2  = cost_functions.get_total_cost(sst["Dataframe_total_cubic"], sst["Dataframe_total_square"], cost_dataframe, cost_transport_dataframe, dataframe_scenarios , address["building"], address["landfill"], address["incineration plant"], address["concrete_brick"],address["glass"], address["metals"], address["wood"], address["storage"])     
                
                
                #OTTAL COST
                # WORST CASE SCENARIO (scenario0 )
                sst["Dataframe total cost scenario 0"] =  cost_functions.df_cost_to_plot_scenario_0(total_costs_scenario_0)

                # BASELINE SCENARIO (scenario 1)
                #merges all the cost in one dataframe
                total_cost_scenario_1 = pd.concat([total_cost_reuse_1, total_cost_recycle_1, total_cost_disposal_1])
                #fills the non values with zero
                total_cost_scenario_1 = total_cost_scenario_1.fillna(0)
                sst["Dataframe total cost scenario 1"] =  cost_functions.df_cost_to_plot_scenario_1_2(total_cost_scenario_1)


                #BEST CASE SCENARIO (scenario 2)
                total_cost_scenario_2 = pd.concat([total_cost_reuse_2, total_cost_recycle_2, total_cost_disposal_2])
                #fills the non values with zero
                total_cost_scenario_2 = total_cost_scenario_2.fillna(0)
                sst["Dataframe total cost scenario 2"] =  cost_functions.df_cost_to_plot_scenario_1_2(total_cost_scenario_2)

                #OVERVIEW OF COSTS
                sum_worst_case_scenario_cost =sst["Dataframe total cost scenario 0"] ['CHF'].sum()
                sum_baseline_scenario_cost = sst["Dataframe total cost scenario 1"]['CHF'].sum()
                sum_bestcase_scenario_cost =  sst["Dataframe total cost scenario 2"]['CHF'].sum()
                #summary scenario 
                summary_cost_df = pd.DataFrame([[int(sum_worst_case_scenario_cost),int(sum_baseline_scenario_cost) , int(sum_bestcase_scenario_cost)]], columns=['Worstcase (CHF)', 'Baseline (CHF)', 'Bestcase (CHF)'])
                summary_cost_df = summary_cost_df.applymap(lambda x: "{:,}".format(x).replace(',', "'") if isinstance(x, (int, float)) else x)
                st.title("Overview")
                st.write(summary_cost_df)
                
                
                st.header("Worst-case scenario: All materials disposed (0% Reuse, 0% Recycle) ")
                #scenario 0
                df_bar_plot_cost_scenario_0 = sst["Dataframe total cost scenario 0"]
                #plot
                fig_bar_plot_cost_scenario_0 = px.bar(df_bar_plot_cost_scenario_0, x= "Costs", y="CHF", title="Total cost", width= 800, height= 500)
                st.write(fig_bar_plot_cost_scenario_0)

                st.header("Baseline scenario: Based on the reuse potential, the materials are then recycled/disposed at the average rate of Switzerland ")
                #scenario 1
                df_bar_plot_cost_scenario_1 = sst["Dataframe total cost scenario 1"]
                #plot
                fig_bar_plot_cost_scenario_1 = px.bar(df_bar_plot_cost_scenario_1, x= "Costs", y="CHF", title="Total cost", width= 800, height= 500)
                st.write(fig_bar_plot_cost_scenario_1)

                #scenario 2
                st.header("Best-case scenario (scenario 2) ")
                #merges all the cost in one dataframe
                df_bar_plot_cost_scenario_2 = sst["Dataframe total cost scenario 2"]
                #plot
                fig_bar_plot_cost_scenario_2 = px.bar(df_bar_plot_cost_scenario_2, x= "Costs", y="CHF", title="Total cost", width= 800, height= 500)
                st.write(fig_bar_plot_cost_scenario_2)
        else:
            st.warning("Please insert the addresses")
            st.stop()













    
    









    











tool2()

