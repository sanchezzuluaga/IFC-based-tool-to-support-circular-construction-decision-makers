import ifcopenshell
import ifcopenshell.util.element as Element
import pprint
from ifcopenshell.api.material.data import Data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import googlemaps



# function to get the ditances between two points
def get_distance(address_1, address_2):
    gmaps = googlemaps.Client(key=' ') #insert google id client 
    #gets a dictonary 
    my_dist = gmaps.distance_matrix(address_1,address_2)['rows'][0]['elements'][0]
    #entcodes the disctance form the dictonary
    a = my_dist.get("distance")
    # takes the value of the distance matrix
    distance = a.get("value")
    #convertion to km--> value in m from google maps 
    distance = distance/1000 


    return distance

#gets index for matching the cost dataframe with the KBOB of each material
#def1= costdataframe, df2= cubic or square_
def match_cost_df_materials(df1,df2, id_number,index_cubic_square):
    found = False
    for i in range(len(df1)):
        #looks for the id_number or id_numbers in each row of the cost dataframe
        id_numbers_cost = df1.iloc[i,0]

        #checks if the id_number is contained in the dataframe 
        #checks the floats of the ID-numbers of the dataframe cost (the datframe has eihter a lis or a float)
        if  isinstance(id_numbers_cost, (int, float)):
            if id_number == id_numbers_cost:
                #gets the index
                index_cost = i
                #we have found the material
                found = True
                if found : 
                    break
        #for the entries with commas in the ID-numbers         
        else:
            #converts the strings of the id numbers in list
            id_numbers_cost = id_numbers_cost.split(",")
            id_numbers_cost = list(map(float, id_numbers_cost))
            #looks if the id:number is in the list
            if id_number in id_numbers_cost:
                index_cost = i
                # we have found the material
                found = True
            #break if found is true
            if found :
                break
        if  not found :
            index_cost = 1000
 
    return index_cost, found

# getting the dtaframe for reuse, recycle and disposal for  baseline scenario
#df1 = datframe_cubic or square,df2 = dataframe_scenarios 
def get_datframe_reuse_recyle_disposal(df1, df2):
    #saves the values of treuse, recycle, disposal
    reuse_save = []
    recycle_save = []
    disposal_save = []
    for index_cubic_square in range(len(df1)):
        # gets the id_number of the index
        id_number = df1.iloc[index_cubic_square, 1]
        row_scenarios =  df2.loc[df2["ID-Number"]==id_number ]
        reuse_percentage = row_scenarios.iloc[0,3]
        recycle_percentage = row_scenarios.iloc[0,4]
        disposal_percentage = row_scenarios.iloc[0,5]
       

        #disposal for simplicity of the model, either KVA or landfill 
        disposal_percentage = row_scenarios.iloc[0,5]



        #if there is no reuse potential 
        if reuse_percentage == 0:
            # reuse / recycle percentages
            #total quanitties
            quantity_total = df1.iloc[index_cubic_square,2]
            #% quanitties rcycle / disposal 
            quantity_recycle = quantity_total*recycle_percentage
            quantity_disposal = quantity_total*disposal_percentage
            quantity_reuse = 0 
            #save the quantites
            recycle_save.append(quantity_recycle)
            disposal_save.append(quantity_disposal)
            reuse_save.append(quantity_reuse)
        
        else:
            #quantity total reuse materials 
            quantity_total = df1.iloc[index_cubic_square,2]
            #quanitty after reuse 
            quantity_total_disposal = quantity_total*(1-reuse_percentage) 
            quantity_reuse = quantity_total*reuse_percentage
            quantity_recycle = quantity_total_disposal*recycle_percentage
            quantity_disposal = quantity_total_disposal*disposal_percentage
            recycle_save.append(quantity_recycle)
            disposal_save.append(quantity_disposal)
            reuse_save.append(quantity_reuse)
            
    

    #creates dataframes for reuse, recycle and disposal
    #reuse
    dataframe_reuse = df1.copy()
    dataframe_reuse.iloc[:,2] = reuse_save

    #recycle
    dataframe_recycle = df1.copy()
    dataframe_recycle.iloc[:,2] = recycle_save
    #disposal
    dataframe_disposal = df1.copy()
    dataframe_disposal.iloc[:,2] = disposal_save
    return dataframe_reuse, dataframe_recycle, dataframe_disposal 

# this funciton is for reuse, recycle, disposal for the best case scenario
# getting the dtaframe for reuse, recycle and disposal
#df1 = datframe_cubic or square,df2 = dataframe_scenarios 
def get_datframe_reuse_recyle_disposal_2(df1, df2):
    #saves the values of treuse, recycle, disposal
    reuse_save = []
    recycle_save = []
    disposal_save = []
    for index_cubic_square in range(len(df1)):
        # gets the id_number of the index
        id_number = df1.iloc[index_cubic_square, 1]
        row_scenarios =  df2.loc[df2["ID-Number"]==id_number ]
        reuse_percentage = row_scenarios.iloc[0,6]
        recycle_percentage = row_scenarios.iloc[0,7]
        disposal_percentage = row_scenarios.iloc[0,8]
       




        #if there is no reuse potential 
        if reuse_percentage == 0:
            # reuse / recycle percentages
            #total quanitties
            quantity_total = df1.iloc[index_cubic_square,2]
            #% quanitties rcycle / disposal 
            quantity_recycle = quantity_total*recycle_percentage
            quantity_disposal = quantity_total*disposal_percentage
            quantity_reuse = 0 
            #save the quantites
            recycle_save.append(quantity_recycle)
            disposal_save.append(quantity_disposal)
            reuse_save.append(quantity_reuse)
        
        else:
            #quantity total reuse materials 
            quantity_total = df1.iloc[index_cubic_square,2]
            #quanitty after reuse 
            quantity_total_disposal = quantity_total*(1-reuse_percentage) 
            quantity_reuse = quantity_total*reuse_percentage
            quantity_recycle = quantity_total_disposal*recycle_percentage
            quantity_disposal = quantity_total_disposal*disposal_percentage
            recycle_save.append(quantity_recycle)
            disposal_save.append(quantity_disposal)
            reuse_save.append(quantity_reuse)
            
    

    #creates dataframes for reuse, recycle and disposal
    #reuse
    dataframe_reuse = df1.copy()
    dataframe_reuse.iloc[:,2] = reuse_save

    #recycle
    dataframe_recycle = df1.copy()
    dataframe_recycle.iloc[:,2] = recycle_save
    #disposal
    dataframe_disposal = df1.copy()
    dataframe_disposal.iloc[:,2] = disposal_save
    return dataframe_reuse, dataframe_recycle, dataframe_disposal 

#get environmental impact for disposal 
# df1 = dataframe_square_2 or dataframe_total_cubic, 
def get_environmental_impact_disposal(df1,material_dataframe, transport_KBOB_dataframe ):
    environmental_impact_disposal = pd.DataFrame(np.zeros((len(df1), 7)), columns = ["Material", "KBOB", "A1-A3", "A4" , "A5", "C1-C4", "D"])

    for index_cubic_square in range(len(df1)):
        #takes the id_number
        id_number = df1.iloc[index_cubic_square, 1]
        #gets the row of the KBOB
        row_kbob = material_dataframe.loc[material_dataframe["ID-Number"] == id_number]
        #print(row_kbob)
        #start filling the save matrix
        material = df1.iloc[index_cubic_square, 0]
        quantity = df1.iloc[index_cubic_square, 2]
        density = row_kbob.iloc[0,2]                                    

        if density == "-":
            density_production_EoL = 1
            #doors windows 35 kg/m2
            density_door_windows= 35
        else :
            density_production_EoL = row_kbob.iloc[0,2]

        #New !!!!!
        whole_part, decimal = divmod(id_number,1)
        whole_part = int(whole_part)
        
        
        KBOB_production = row_kbob.iloc[0,4]
        KBOB_elimination = row_kbob.iloc[0,5]
        percentage_A5 = row_kbob.iloc[0 ,6]
        #Calculation A1-A3 --> if is Window-->
        #windows
        if whole_part == 5: 
            A1_A3 = quantity*KBOB_production*density_production_EoL*0.3 + 0.7*70*quantity*density_production_EoL
            #weight in tonnes
            weight = density_door_windows*quantity/1000
            A4 = transport_KBOB_dataframe.iloc[13,3]*7*weight
            A5 = A1_A3*percentage_A5
            C1_C4 = quantity*KBOB_elimination*density_production_EoL*0.3  + 0.7*6*quantity*density_production_EoL
        
        #doors
        elif whole_part == 12 :
            A1_A3 = quantity*KBOB_production*density_production_EoL
            #weight in tonnes
            weight = density_door_windows*quantity/1000 
            A4 =  transport_KBOB_dataframe.iloc[13,3]*7*weight
            A5 = A1_A3*percentage_A5
            C1_C4 = quantity*KBOB_elimination*density_production_EoL
        #
        else:
            A1_A3 = quantity*KBOB_production*density_production_EoL
            #weight in tonnes
            weight = density_production_EoL*quantity/1000 
            A4 =  transport_KBOB_dataframe.iloc[13,3]*7*weight
            A5 = A1_A3*percentage_A5
            C1_C4 = quantity*KBOB_elimination*density_production_EoL
            
        


        #creates np array to store the materials
        row_save = np.array([id_number , A1_A3,A4, A5,C1_C4 ])
        #print(type(row_save))
        #save values in save pandas
        environmental_impact_disposal.iloc[index_cubic_square,0] = material
        environmental_impact_disposal.iloc[index_cubic_square, 1 : 6] = row_save
    return environmental_impact_disposal 

#get environmnetal impact fo recycle
#df1 = dataframe cubic or square recycle, 
def get_environmental_impact_recycle(df1,material_dataframe, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood,transport_KBOB_dataframe, dataframe_scenarios):    
    #since the environemntal impact for reuse and recacle are the same
    #we are getting the matrix environmental impact disposal 
    environmental_impact_recycle = get_environmental_impact_disposal(df1,material_dataframe, transport_KBOB_dataframe)
    #convert al the values to float

    #iteration to know the id number of the dataframe recycle cubic or square
    for index_cubic_square in range(len(df1)):
        id_number = df1.iloc[index_cubic_square, 1]
        row_kbob = material_dataframe.loc[material_dataframe["ID-Number"] == id_number]
        row_scenarios = dataframe_scenarios.loc[dataframe_scenarios["ID-Number"] == id_number] 
        density = row_kbob.iloc[0,2]
        
        
        #match Id. number and dataframe
        
        #factors R1, R2 and Qs/Qp
        R1= row_scenarios.iloc[0,12]
        R2 = row_scenarios.iloc[0,13]
        Qs_Qp = row_scenarios.iloc[0,14]
        #factor production (A1-A3) (1-R1/1-R2/2*Qs/Qp)
        factor_EC_EF_A1_A3 = 1 - R1/2 - R2/2*Qs_Qp
        #print(factor_EC_EF_A1_A3)
        
        #factor EoL (C1-C4)
        factor_EC_EF_EoL = 1 - R1/2 - R2/2
        
        #factor D
        factor_EC_EF_D = R1/2 + R2/2
        
        
        #getting the id_number_whole part
        id_number_whole, decimal = divmod(id_number,1)
        id_number_whole = int(id_number_whole)

        if density == "-":
            #assuming windoows and doors weight 35 kg/m2
            density = 35
        else :
            density = row_kbob.iloc[0,2]
        
        #module A1-A3
        A1_A3_old = environmental_impact_recycle.iloc[index_cubic_square, 2]
        A1_A3_new = A1_A3_old*factor_EC_EF_A1_A3
        environmental_impact_recycle.iloc[index_cubic_square, 2]= A1_A3_new 
        
        #module C1-C4
        C1_C4_old = environmental_impact_recycle.iloc[index_cubic_square, 5]
        C1_C4_new = C1_C4_old*factor_EC_EF_EoL
        environmental_impact_recycle.iloc[index_cubic_square, 5] = C1_C4_new    
        
        #module D
        distance = get_distance_recycle( id_number_whole, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood) 
        quantity = df1.iloc[index_cubic_square, 2]
        #calculate the weight in tonnes
        weight = density*quantity/1000
        #multiply environmental impact transport *weight * distance
        D1 = transport_KBOB_dataframe.iloc[13,3]*weight*(distance + 7)
        A5 = environmental_impact_recycle.iloc[index_cubic_square, 4]
        D2 = 2*A5
        D = (D1+D2)*factor_EC_EF_D 
        environmental_impact_recycle.iloc[index_cubic_square,6] = D
    return environmental_impact_recycle
#gets distance for recylcing
#df1 = dataframe_reuse_cubic, df2= dataframe_reuse_squre, 
def get_distance_recycle( id_number, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood):
    #gets the distance depending on the     
    #Recycle concrete and brick --> concrete plant
    if id_number in (1,2):
        distance = get_distance(addres_concrete_brick, addres_building)
    #recycle glas
    elif id_number in (3,5):
        distance = get_distance(addres_glas, addres_building)
    #recycle metals
    elif id_number  == 6:
        distance = get_distance(addres_metals, addres_building)
    # wood
    elif id_number in (7,12):
        distance = get_distance(addres_wood, addres_building)
        
    else:
        distance = 7 
    
    return distance

#gets environmental impact for reuse
#df1= dataframe reuse cubic or dataframe reuse square
def get_environmental_impact_reuse(df1,material_dataframe,transport_KBOB_dataframe,addres_building, addres_storage, dataframe_scenarios):    
    #gets the environmental impact
    environmental_impact_reuse = get_environmental_impact_disposal(df1,material_dataframe, transport_KBOB_dataframe)
    #print(environmental_impact_reuse)
    #divides the pandas dataframe by scalar
    #print(environmental_impact_reuse)
    for index_cubic_square in range(len(environmental_impact_reuse)):
        id_number = environmental_impact_reuse.iloc[index_cubic_square, 1]
        row_kbob = material_dataframe.loc[material_dataframe["ID-Number"] == id_number]
        row_scenarios = dataframe_scenarios.loc[dataframe_scenarios["ID-Number"] == id_number]
        density = row_kbob.iloc[0,2]
        
        
        #match Id. number and dataframe
        
        #factors R1, R2 and Qs/Qp
        R1= row_scenarios.iloc[0,9]
        R2 = row_scenarios.iloc[0,10]
        Qs_Qp = row_scenarios.iloc[0,11]
        #factor production (A1-A3) (1-R1/1-R2/2*Qs/Qp)
        factor_EC_EF_A1_A3 = 1 - R1/2 - R2/2*Qs_Qp
        
        
        #factor EoL (C1-C4)
        factor_EC_EF_EoL = 1 - R1/2 - R2/2
        
        #factor D
        factor_EC_EF_D = R1/2 + R2/2
        
        #getting the id_number_whole part
        id_number_whole, decimal = divmod(id_number,1)
        id_number_whole = int(id_number_whole)

        if density == "-":
            #assuming windoows and doors weight 35 kg/m2
            density = 35
        else :
            density = row_kbob.iloc[0,2]

       
        #module A1-A3
        A1_A3_old = environmental_impact_reuse.iloc[index_cubic_square, 2]
        A1_A3_new = A1_A3_old*factor_EC_EF_A1_A3
        environmental_impact_reuse.iloc[index_cubic_square, 2]= A1_A3_new 
        
        #module C1-C4
        C1_C4_old = environmental_impact_reuse.iloc[index_cubic_square, 5]
        C1_C4_new = C1_C4_old*factor_EC_EF_EoL
        environmental_impact_reuse.iloc[index_cubic_square, 5] = C1_C4_new    
        
        #module D
        distance = get_distance(addres_storage, addres_building)
        quantity = df1.iloc[index_cubic_square, 2]
        #calculate the weight in tonnes
        weight = density*quantity/1000
        #multiply environmental impact transport *weight * distance
        D1 = transport_KBOB_dataframe.iloc[13,3]*weight*(distance + 7) 
        A5 = environmental_impact_reuse.iloc[index_cubic_square, 4]
        D2 = 2*A5
        D = (D1+D2)*factor_EC_EF_D 
        environmental_impact_reuse.iloc[index_cubic_square,6] = D
    return environmental_impact_reuse

#get environmental impact baseline scenario scenario 
def get_envrionmental_impact_scenario_1(dataframe_total_cubic, dataframe_total_square ,dataframe_scenarios,material_dataframe,addres_building,addres_concrete_brick,addres_glas,addres_metals,addres_wood,transport_KBOB_dataframe,addres_storage):

    #gets dataframe cubic
    dataframe_reuse_cubic_1, dataframe_recycle_cubic_1, dataframe_disposal_cubic_1 = get_datframe_reuse_recyle_disposal(dataframe_total_cubic, dataframe_scenarios )
    #gets data frame sqaure
    dataframe_reuse_square_1, dataframe_recycle_square_1, dataframe_disposal_square_1 = get_datframe_reuse_recyle_disposal(dataframe_total_square, dataframe_scenarios)
    
    ##Disposal 
    environmental_impact_disposal_cubic = get_environmental_impact_disposal(dataframe_disposal_cubic_1, material_dataframe, transport_KBOB_dataframe) 
    #environmental impact disposal square
    environmental_impact_disposal_square = get_environmental_impact_disposal(dataframe_disposal_square_1, material_dataframe, transport_KBOB_dataframe)
    #merges the disposal 
    environmental_impact_disposal = pd.concat([environmental_impact_disposal_cubic,environmental_impact_disposal_square])
    ## Recycle
    #environmental impact recycle cubic
    environmental_impact_recycle_cubic = get_environmental_impact_recycle(dataframe_recycle_cubic_1,material_dataframe, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood,transport_KBOB_dataframe,dataframe_scenarios )
    #environemntal impact recycle square
    environmental_impact_recycle_square = get_environmental_impact_recycle(dataframe_recycle_square_1,material_dataframe, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood,transport_KBOB_dataframe, dataframe_scenarios )
    #merges environmental impact recycle
    environmental_impact_recycle =  pd.concat([environmental_impact_recycle_cubic,environmental_impact_recycle_square])
    #reuse
    # environmental impact reuse  cubic
    environmental_impact_reuse_cubic = get_environmental_impact_reuse(dataframe_reuse_cubic_1,material_dataframe,transport_KBOB_dataframe,addres_building, addres_storage, dataframe_scenarios)
    environmental_impact_reuse_square = get_environmental_impact_reuse(dataframe_reuse_square_1,material_dataframe,transport_KBOB_dataframe,addres_building, addres_storage, dataframe_scenarios)
    #merges environmental impact reuse
    environmental_impact_reuse = pd.concat([environmental_impact_reuse_cubic,environmental_impact_reuse_square])

    return  environmental_impact_disposal,  environmental_impact_recycle, environmental_impact_reuse

#get environmental impact best-case scenario
def get_envrionmental_impact_scenario_2(dataframe_total_cubic, dataframe_total_square ,dataframe_scenarios,material_dataframe,addres_building,addres_concrete_brick,addres_glas,addres_metals,addres_wood,transport_KBOB_dataframe,addres_storage):

    #gets dataframe cubic
    dataframe_reuse_cubic_2, dataframe_recycle_cubic_2, dataframe_disposal_cubic_2 = get_datframe_reuse_recyle_disposal_2(dataframe_total_cubic, dataframe_scenarios )
    #gets data frame sqaure
    dataframe_reuse_square_2, dataframe_recycle_square_2, dataframe_disposal_square_2 = get_datframe_reuse_recyle_disposal_2(dataframe_total_square, dataframe_scenarios)
    
    ##Disposal 
    environmental_impact_disposal_cubic = get_environmental_impact_disposal(dataframe_disposal_cubic_2, material_dataframe, transport_KBOB_dataframe) 
    #environmental impact disposal square
    environmental_impact_disposal_square = get_environmental_impact_disposal(dataframe_disposal_square_2, material_dataframe, transport_KBOB_dataframe)
    #merges the disposal 
    environmental_impact_disposal = pd.concat([environmental_impact_disposal_cubic,environmental_impact_disposal_square])
    ## Recycle
    #environmental impact recycle cubic
    environmental_impact_recycle_cubic = get_environmental_impact_recycle(dataframe_recycle_cubic_2,material_dataframe, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood,transport_KBOB_dataframe,dataframe_scenarios)
    #environemntal impact recycle square
    environmental_impact_recycle_square = get_environmental_impact_recycle(dataframe_recycle_square_2,material_dataframe, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood,transport_KBOB_dataframe,dataframe_scenarios)
    #merges environmental impact recycle
    environmental_impact_recycle =  pd.concat([environmental_impact_recycle_cubic,environmental_impact_recycle_square])
    #reuse
    # environmental impact reuse  cubic
    environmental_impact_reuse_cubic = get_environmental_impact_reuse(dataframe_reuse_cubic_2,material_dataframe,transport_KBOB_dataframe,addres_building, addres_storage, dataframe_scenarios)
    environmental_impact_reuse_square = get_environmental_impact_reuse(dataframe_reuse_square_2,material_dataframe,transport_KBOB_dataframe,addres_building, addres_storage, dataframe_scenarios)
    #merges environmental impact reuse
    environmental_impact_reuse = pd.concat([environmental_impact_reuse_cubic,environmental_impact_reuse_square])

    return  environmental_impact_disposal,  environmental_impact_recycle, environmental_impact_reuse


#gets the different classes, levels
def get_materials(df):
    materials = []
    for index in range(len(df)):
        material= df.iloc[index,0]
        materials.append(material)
    return materials 



# gets the dataframe filtered by material
def dataframe_filtered_by_MaterialInput(dataframe, input):
    mask = dataframe["Material"].str.contains(input)
    filtered = dataframe.loc[mask]
    return filtered

#restructure the dataframe to be plotted
def df_EI_to_plot(df):
    
    a = df[["A1-A3", "C1-C4"]].sum().to_frame()
    
    row_labels = {"A1-A3": 0,
              "C1-C4": 1,
    }
    
    a.rename(index=row_labels, inplace = True)
    x = ["A1-A3","C1-C4"]
    c = pd.DataFrame(data= x, columns=["Stages"])
    d = pd.concat([a,c], axis=1)
    d = d.rename(columns={0:"kg-CO2_eq"})
    df_output = d
    return df_output