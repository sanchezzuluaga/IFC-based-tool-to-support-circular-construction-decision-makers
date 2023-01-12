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
    gmaps = googlemaps.Client(key='AIzaSyCRB64YI5yfno7EJ0vRlawD4J6sytsd9AI')
    #gets a dictonary 
    my_dist = gmaps.distance_matrix(address_1,address_2)['rows'][0]['elements'][0]
    #entcodes the disctance form the dictonary
    a = my_dist.get("distance")
    # takes the value of the distance matrix
    distance = a.get("value")
    #convertion to km--> value in m from google maps 
    distance = distance/1000 


    return distance 

#function that groups what is going to incineration plant and land_fill --> scenario 0 
# df1 = datframe cubic or dataframe square
def get_quantities_landfill_incineration_smelting(df1):
    #grupping what is goingt to smelting plant/ incineration plant/ landfill TYP B
    land_fill_quantity = []
    incineration_quantity = []
    #smelting_plant_quantity = []

    dataframe_rounded = df1.astype({"KBOB" : "int"})
    for index in range(len(dataframe_rounded)):
        id_number = dataframe_rounded.iloc[index,1]
        #the id_numbers that go to the incineration plant 
        if id_number in (7,10,12, 15):
            quantity_incineration = dataframe_rounded.iloc[index,2]

            incineration_quantity.append(quantity_incineration)
        #to the smelting plant    
#         elif id_number  == 6:
#             quantity_smelting_plant = dataframe_rounded.iloc[index,2]
#             smelting_plant_quantity.append(quantity_smelting_plant)
        # to landfill
        else:
            quantity_land_fill_quanitty = dataframe_rounded.iloc[index,2]
            land_fill_quantity.append(quantity_land_fill_quanitty)





    total_volume_incineration = sum(incineration_quantity)
    #total_volume_smelting_plant = sum(smelting_plant_quantity)
    total_volume_land_fill = sum(land_fill_quantity)

        
        
    return (total_volume_incineration, total_volume_land_fill)  
    #return (total_volume_incineration, total_volume_smelting_plant, total_volume_land_fill)

#function to  get a dataframe of the loose volumes for cubic --> fro the transport
#df1 = total squar / cubic, df2 = cost dataframe
def get_volume_loose_cubic(df1,df2):
    quantities_loose_save = []
    #copy the dataframe
    df_cubic_loose = df1.copy()
    for index_cubic_square in range(len(df_cubic_loose)):
        #id number of the material
        id_number = df_cubic_loose.iloc[index_cubic_square,1]
        #find index_cost, the index in the cost dataframe
        whole_part, decimal = divmod(id_number,1)
        whole_part = int(whole_part)
        if whole_part in (1,2, 5, 7, 10, 12):
            id_number = whole_part
        else:
            id_number = id_number
        index_cost, found  = match_cost_df_materials(df2, df_cubic_loose, id_number, index_cubic_square)
        #append the
        quantity_square_cubic =  df_cubic_loose.iloc[index_cubic_square, 2]
        if not found:
            loose_factor = 1.5
        else:
            loose_factor= df2.iloc[index_cost, 20]
        #makes a quantity loose
        quantity_loose = loose_factor*quantity_square_cubic
        quantities_loose_save.append(quantity_loose)

    # creates the dataframe 
    df_cubic_loose.iloc[0: len(df1),2 ] = quantities_loose_save
    

    return df_cubic_loose


#function to  get a dataframe of the loose volumes for square datframe
#df1 = total squar / cubic, df2 = cost dataframe
def get_volume_loose_square(df1,df2):
    quantities_loose_save = []
    #copy the dataframe
    df_square_loose = df1.copy()
    for index_cubic_square in range(len(df_square_loose)):
        #id number of the material
        id_number = df_square_loose.iloc[index_cubic_square,1]
        #find index_cost, the index in the cost dataframe
        whole_part, decimal = divmod(id_number,1)
        whole_part = int(whole_part)
        if whole_part in (1,2, 5, 7, 10, 12):
            id_number = whole_part
        else:
            id_number = id_number
        index_cost, found  = match_cost_df_materials(df2, df_square_loose, id_number, index_cubic_square)
        #append the
        quantity_square_cubic =  df_square_loose.iloc[index_cubic_square, 2]
        if not found:
            loose_factor = 1.5
        else:
            loose_factor= df2.iloc[index_cost, 20]
        #makes a quantity loose for doors, insulation and windows
        quantity_loose = loose_factor*quantity_square_cubic*0.15
        quantities_loose_save.append(quantity_loose)
        

    # creates the dataframe 
    df_square_loose.iloc[0: len(df1),2 ] = quantities_loose_save
    

    return df_square_loose




#gets index for matvhcin the cost dataframe with the KBOB of each material
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

#gets the cost for demolition and disposal
#df1 = dataframe_total_square or cubic, df2= cost dataframe
def get_costs_scenario_0_demolition_disposal(df1, df2):
    #dictonaries to save the information
    cost_demolition_save = []
    cost_disposal_save = []

    #cost_recycling_save = []
    #index_cubic square = index of datafrae total (qubic /square)
    # inputs function: dataframe_total_cubic, cost dataframe, 
    for index_cubic_square in range(len(df1)):
        id_number = df1.iloc[index_cubic_square, 1]
        #takes the whole part of the decimal 
        whole_part, decimal = divmod(id_number,1)
        whole_part = int(whole_part)
        if whole_part in (1,2, 5, 7, 10, 12):
            id_number = whole_part
        else:
            id_number = id_number

        #df1= dataframe total cubic /square, df2 = cost dataframe, 
        index_cost, found  = match_cost_df_materials(df2, df1, id_number, index_cubic_square)
        #if the material is not in the cost list add zeros to cost list 

        
        if not found: 
            cost_demolition = 0
            cost_disposal = 0
            


        else: 
            #quantity
            quantity = df1.iloc[index_cubic_square, 2 ]
            #cost demolition
            cost_demolition = quantity*df2.iloc[index_cost,6]
            #cost landfill 
            cost_disposal = quantity * df2.iloc[index_cost, 7]
            
        cost_demolition_save.append(cost_demolition)

        cost_disposal_save.append(cost_disposal)
        
        
        
        

        # output a dataframe with the different costs 
        #merges all the lists into one single list
        costs_together = list(zip(cost_demolition_save, cost_disposal_save ))
        #makes a dataframe
        costs_dataframe = pd.DataFrame(costs_together, columns = [ "Cost Demolition", "Cost Disposal"])
    return costs_dataframe 


# gets the cost for transport for scenario 0 
#df1= datframe_total_cubic, df2 = dataframe_total_square, df3 = cost_dataframe, df4 = cost_transport_dataframe
def get_cost_transport_scenario_0 (addres_building, address_landfill, address_incinaration_plant, df1, df2, df3, df4 ):

#def get_cost_transport_scenario_0 (addres_building, address_landfill, address_smelting_plant, address_incinaration_plant, df1, df2, df3, df4 ):
    distance_land_fill = get_distance(addres_building,address_landfill )
    #distance_smelting_plant = get_distance(addres_building,address_smelting_plant)
    distance_incineration_plant = get_distance(addres_building, address_incinaration_plant)


    # gets the volume loose_cubic, for the trucks 
    volume_loose_cubic = get_volume_loose_cubic(df1, df3)
    # gets the total quantites from cubic (landfill, smelting plant, incineration plant)
    #total_volume_incineration_cubic, total_volume_smelting_plant_cubic, total_volume_land_fill_cubic = get_quantities_landfill_incineration_smelting(volume_loose_cubic) 
    total_volume_incineration_cubic, total_volume_land_fill_cubic = get_quantities_landfill_incineration_smelting(volume_loose_cubic) 

    #get the volumesloose, squares
    volume_loose_square= get_volume_loose_square(df2, df3)
    # gets the total quantites from cubic (landfill, smelting plant, incineration plant)
    #total_volume_incineration_square, total_volume_smelting_plant_suqare, total_volume_land_fill_square = get_quantities_landfill_incineration_smelting(volume_loose_square) 
    total_volume_incineration_square, total_volume_land_fill_square = get_quantities_landfill_incineration_smelting(volume_loose_square) 

    
    #sums all the volumes for landfill, smelting plant and incineration
    total_volume_incineration = total_volume_incineration_cubic + total_volume_incineration_square
    #total_volume_smelting_plant = total_volume_smelting_plant_cubic + total_volume_smelting_plant_suqare
    total_volume_land_fill =total_volume_land_fill_cubic + total_volume_land_fill_square
    
    #gets the capacity and the cost of transport 
    capacity_truck = df4.iloc[2,2]
    cost_transport_one_truck = df4.iloc[2,1]
    #gets the number of trucks  for each station (smelting, incineration, and landfill)
    #incineration plant
    number_of_trucks_incineration =  total_volume_incineration / capacity_truck
    number_of_trucks_incineration = math.ceil(number_of_trucks_incineration)
    total_cost_incineration_transport = number_of_trucks_incineration*distance_incineration_plant*cost_transport_one_truck

    #smelting plant 
    #number_of_trucks_smelting =  total_volume_smelting_plant / capacity_truck
    #number_of_trucks_smelting = math.ceil(number_of_trucks_smelting)
    #total_cost_smelting_transport = number_of_trucks_smelting*distance_smelting_plant*cost_transport_one_truck

    #land_fill
    number_of_trucks_land_fill =  total_volume_land_fill / capacity_truck
    number_of_trucks_land_fill = math.ceil(number_of_trucks_land_fill)
    total_cost_land_fill_transport = number_of_trucks_land_fill*distance_land_fill*cost_transport_one_truck
    
    
    #return total_cost_incineration_transport, total_cost_smelting_transport, total_cost_land_fill_transport 
    return total_cost_incineration_transport, total_cost_land_fill_transport

#gets the total costs
#df1 = dataframe_total_cubic, df2 =dataframe_total_square   df3 = cost_dataframe, df4 = cost_transport_dataframe   
#def get_total_cost_scenario_0(df1, df2, df3, df4, addres_building, address_landfill, address_smelting_plant, address_incinaration_plant):
def get_total_cost_disposal(df1, df2, df3, df4, addres_building, address_landfill, address_incinaration_plant):
    
    #gets the total cost for scenario 0 (demolition--> incineration, smelting plant, disposal)
    costs_demoltion_disposal_cubic =  get_costs_scenario_0_demolition_disposal(df1, df3 )
    costs_demoltion_disposal_square =  get_costs_scenario_0_demolition_disposal(df2, df3 )
    # add the two dataframes datframe square and datframe cubic
    cost_demolition_disposal_total = costs_demoltion_disposal_cubic.add(costs_demoltion_disposal_square, fill_value =0)
    #add the Cost Demolition, Cost Disposal
    cost_demolition_disposal_total =cost_demolition_disposal_total.sum()
    #convert data fram series to frame
    cost_demolition_disposal_total = cost_demolition_disposal_total.to_frame().T
    # copy dataframe to add the transport cost
    cost_scenario_0_total = cost_demolition_disposal_total.copy()
    


    #gets the cost for tranport
    #total_cost_incineration_transport, total_cost_smelting_transport, total_cost_land_fill_transport = get_cost_transport_scenario_0 (addres_building, address_landfill, address_smelting_plant, address_incinaration_plant, df1, df2, df3, df4)
    #total_cost_transport = total_cost_incineration_transport + total_cost_smelting_transport + total_cost_land_fill_transport
    #
    total_cost_incineration_transport, total_cost_land_fill_transport = get_cost_transport_scenario_0 (addres_building, address_landfill, address_incinaration_plant, df1, df2, df3, df4)
    total_cost_transport = total_cost_incineration_transport + total_cost_land_fill_transport

    
    
    # adds the transport to the cost
    cost_scenario_0_total["Cost Transport"] = total_cost_transport
    return cost_scenario_0_total

# getting the dtaframe for reuse, recycle and disposal
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

# this funciton is for reuse, recycle, disposal for scenario 2
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


#df1 =  dataframe_reuse_cubic or square, df2= cost_dataframe, 
def get_cost_deconstruction(df1, df2):
    #delete rows containing zero values
    dataframe_reuse_square_cubic = df1[(df1 != 0).all(1)]
    cost_deconstruction_save = []
    for index_cubic_square in range(len(dataframe_reuse_square_cubic)):
        id_number = dataframe_reuse_square_cubic.iloc[index_cubic_square,1]
        whole_part, decimal = divmod(id_number,1)
        whole_part = int(whole_part)
        #looks id the id_numer is in the whole part
        if whole_part in (1,2, 5, 7, 10, 12):
            id_number = whole_part
        else:
            id_number = id_number

        index_cost, found = match_cost_df_materials(df2, dataframe_reuse_square_cubic, id_number, index_cubic_square)
        if not found: 
            cost_deconstruction = 0
        else:
            quantity = dataframe_reuse_square_cubic.iloc[index_cubic_square, 2 ]
            cost_deconstruction = df2.iloc[index_cost, 16]
            cost_deconstruction = cost_deconstruction * quantity
            cost_deconstruction_save.append(cost_deconstruction)
    cost_deconstruction = sum(cost_deconstruction_save)
    
    return cost_deconstruction


#df1 = dataframe_reuse_cubic, df2= dataframe_reuse_squre, 
def get_cost_transport_storage(df1, df2, cost_dataframe, cost_transport_dataframe,addres_storage, addres_building):
    # get the cost for storing the materials (storage)

    # get the distance 
    distance_storage = get_distance(addres_storage, addres_building)

    # get the volume loose square and cubic
    df1 =df1[(df1 != 0).all(1)] 
    dataframe_reuse_cubic_loose = get_volume_loose_cubic(df1,cost_dataframe)
    dataframe_reuse_square_loose = df2[(df2 != 0).all(1)] 
    dataframe_reuse_square_loose = get_volume_loose_square(df2, cost_dataframe)

    # total quantities square, cubic
    total_volume_storage_cubic = dataframe_reuse_cubic_loose["Volume m3"].sum()
    total_volume_storage_square = dataframe_reuse_square_loose["Area m2"].sum()

    total_volume_storage = total_volume_storage_cubic + total_volume_storage_square

    #capacity of the truck
    capacity_truck = cost_transport_dataframe.iloc[2,2]
    cost_transport_one_truck = cost_transport_dataframe.iloc[2,1]
    #gets the number of trucks for the storage
    number_of_trucks_storage = total_volume_storage / capacity_truck
    number_of_trucks_storage = math.ceil(number_of_trucks_storage)
    total_cost_transport_storage = number_of_trucks_storage*distance_storage*cost_transport_one_truck
    return total_cost_transport_storage

#get total cost reuse
def get_total_cost_reuse(dataframe_reuse_cubic, dataframe_reuse_square,cost_dataframe,cost_transport_dataframe, addres_storage, addres_building ):
    # gets datframe cubic
    
    #costs, get the cost for deconstruction
    cost_deconstruction_square = get_cost_deconstruction(dataframe_reuse_square,cost_dataframe)
    
    cost_deconstruction_cubic = get_cost_deconstruction(dataframe_reuse_cubic, cost_dataframe)
    
    total_cost_deconstruction = cost_deconstruction_cubic + cost_deconstruction_square
   
    
    #gets total cost transport
    total_cost_transport_storage = get_cost_transport_storage(dataframe_reuse_cubic, dataframe_reuse_square, cost_dataframe, cost_transport_dataframe,addres_storage, addres_building)
    
    #creates dataframe
    total_cost = np.array([[total_cost_deconstruction ,total_cost_transport_storage]])
    
    #creates dataframe
    total_cost_deconstruction_transport = pd.DataFrame(total_cost, columns = ['Cost Deconstruction','Cost Transport'])
    

                                    
    return total_cost_deconstruction_transport


#get recycled 
#df1 = dataframe_recycle_cubic or square
def get_cost_demolition_recycle(df1, cost_dataframe):
        #dictonaries to save the information
    cost_demolition_save = []
    cost_recycle_save = []

    #cost_recycling_save = [] 
    for index_cubic_square in range(len(df1)):
        id_number = df1.iloc[index_cubic_square, 1]
        #takes the whole part of the decimal 
        whole_part, decimal = divmod(id_number,1)
        whole_part = int(whole_part)
        if whole_part in (1,2, 5, 7, 10, 12):
            id_number = whole_part
        else:
            id_number = id_number

        #df1= dataframe total cubic /square, df2 = cost dataframe, 
        index_cost, found  = match_cost_df_materials(cost_dataframe, df1, id_number, index_cubic_square)
        #if the material is not in the cost list add zeros to cost list 

        
        if not found: 
            cost_demolition = 0
            cost_recycle = 0
            


        else: 
            #quantity
            quantity = df1.iloc[index_cubic_square, 2 ]
            #cost demolition
            cost_demolition = quantity*cost_dataframe.iloc[index_cost,6]
            #cost landfill 
            cost_recycle = quantity * cost_dataframe.iloc[index_cost, 11]
            
        cost_demolition_save.append(cost_demolition)

        cost_recycle_save.append(cost_recycle)
        
        
        
        

        # output a dataframe with the different costs 
        #merges all the lists into one single list
        costs_together = list(zip(cost_demolition_save, cost_recycle_save ))
        #makes a dataframe
        costs_dataframe = pd.DataFrame(costs_together, columns = [ "Cost Demolition", "Cost Recycle"])
    return costs_dataframe



#df1 = dataframe recycle cubic or  square loose (important!!!! loose)
def get_quantities_recycling_plants(df1):
    #grupping what is goingt to smelting plant/ incineration plant/ landfill TYP B
    recycle_concrete_brick_save = []
    recycle_glas_gypsum_save = []
    recycle_smelting_save = []
    recycle_wood_save = []
    recycle_others_save = []
    
    
    
    #smelting_plant_quantity = []

    dataframe_rounded = df1.astype({"KBOB" : "int"})
    for index in range(len(dataframe_rounded)):
        id_number = dataframe_rounded.iloc[index,1]
        #Recycle concrete and brick --> concrete plant
        if id_number in (1,2):
            recycle_concrete_brick_quantity = dataframe_rounded.iloc[index,2]
            recycle_concrete_brick_save.append(recycle_concrete_brick_quantity)
        #recycle glas
        elif id_number in (3,5):
            recycle_glas_gypsum_quantity = dataframe_rounded.iloc[index,2]
            recycle_glas_gypsum_save.append(recycle_glas_gypsum_quantity)
        #recycle metals
        elif id_number  == 6:
            recycle_smelting_quantity = dataframe_rounded.iloc[index,2]
            recycle_smelting_save.append(recycle_smelting_quantity)
        # wood
        elif id_number in (7,12):
            recycle_wood_quantity = dataframe_rounded.iloc[index,2]
            recycle_wood_save.append(recycle_wood_quantity)
        else:
            recycle_others_quantity = dataframe_rounded.iloc[index,2] 
            recycle_others_save.append(recycle_others_quantity)
            
            




    #total volume plant concrete
    total_volume_recycle_concrete_brick = sum(recycle_concrete_brick_save)
    #total volume glas
    total_volume_recycle_glas_gypsum = sum(recycle_glas_gypsum_save)
    #total volume metals
    total_volume_metals = sum(recycle_smelting_save)
    #total volume wood
    total_volume_wood = sum(recycle_wood_save)
    #total volume others
    total_volume_others = sum(recycle_others_save)
    

        
        
    return total_volume_recycle_concrete_brick, total_volume_recycle_glas_gypsum, total_volume_metals, total_volume_wood, total_volume_others



#df1 = dataframe_reuse_cubic, df2= dataframe_reuse_squre, 
def get_cost_transport_recycle(dataframe_recycle_cubic, dataframe_recycle_square, cost_dataframe, cost_transport_dataframe, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood):
    # get the cost for storing the materials (storage)

    # get the distance from a radius 
    distance_recycle_concrete_brick = get_distance(addres_concrete_brick, addres_building)
    distance_recycle_glas = get_distance(addres_glas, addres_building)
    distance_recycle_metals = get_distance(addres_metals, addres_building)
    distance_recycle_wood = get_distance(addres_wood, addres_building)
    distance_recycle_others = 4 
    

    # get the volume loose square and cubic
    #get the zero values away
    dataframe_recycle_cubic_loose = dataframe_recycle_cubic[(dataframe_recycle_cubic != 0).all(1)] 
    dataframe_recycle_cubic_loose = get_volume_loose_cubic(dataframe_recycle_cubic,cost_dataframe)
    #get the zero values away
    dataframe_recycle_square_loose = dataframe_recycle_square[(dataframe_recycle_square != 0).all(1)] 
    dataframe_reuse_square_loose = get_volume_loose_square(dataframe_recycle_square, cost_dataframe)
    
    #gets total volume cubic for each reacycling plant
    total_volume_recycle_concrete_brick_cubic, total_volume_recycle_glas_gypsum_cubic, total_volume_metals_cubic, total_volume_wood_cubic, total_volume_others_cubic = get_quantities_recycling_plants(dataframe_recycle_cubic_loose)
    total_volume_recycle_concrete_brick_square, total_volume_recycle_glas_gypsum_square, total_volume_metals_square, total_volume_wood_square, total_volume_others_square = get_quantities_recycling_plants(dataframe_recycle_square_loose)
    
    
    
    
    #total volumes
    total_volume_recycle_concrete_brick = total_volume_recycle_concrete_brick_cubic + total_volume_recycle_concrete_brick_square
    total_volume_recycle_glas_gypsum = total_volume_recycle_glas_gypsum_cubic + total_volume_recycle_glas_gypsum_square
    total_volume_recycle_metals = total_volume_metals_cubic + total_volume_metals_square
    total_volume_recycle_wood = total_volume_wood_cubic + total_volume_wood_square
    total_volume_recycle_others = total_volume_others_cubic + total_volume_others_square
    
    #concrete_brick
    #capacity of the truck
    capacity_truck = cost_transport_dataframe.iloc[2,2]
    cost_transport_one_truck = cost_transport_dataframe.iloc[2,1]
    
    #gets cost for recycle concrete
    number_of_trucks_recycle_concrete = total_volume_recycle_concrete_brick / capacity_truck
    number_of_trucks_recycle_concrete = math.ceil(number_of_trucks_recycle_concrete)
    total_cost_transport_recycle_concrete = number_of_trucks_recycle_concrete*distance_recycle_concrete_brick*cost_transport_one_truck
    
    #gets cost for glas
    number_of_trucks_recycle_glas = total_volume_recycle_glas_gypsum / capacity_truck
    number_of_trucks_recycle_glas = math.ceil(number_of_trucks_recycle_glas)
    total_cost_transport_recycle_glas = number_of_trucks_recycle_glas*distance_recycle_glas*cost_transport_one_truck
    
    #gets cost for metals
    number_of_trucks_recycle_metal = total_volume_recycle_metals / capacity_truck
    number_of_trucks_recycle_metal = math.ceil(number_of_trucks_recycle_metal)
    total_cost_transport_recycle_metal = number_of_trucks_recycle_metal*distance_recycle_metals*cost_transport_one_truck
    
    # wood
    number_of_trucks_recycle_wood = total_volume_recycle_wood / capacity_truck
    number_of_trucks_recycle_wood = math.ceil(number_of_trucks_recycle_wood)
    total_cost_transport_recycle_wood = number_of_trucks_recycle_wood*distance_recycle_wood*cost_transport_one_truck
    
    # others
    number_of_trucks_recycle_others = total_volume_recycle_others / capacity_truck
    number_of_trucks_recycle_others = math.ceil(number_of_trucks_recycle_others)
    total_cost_transport_recycle_others = number_of_trucks_recycle_others*distance_recycle_others*cost_transport_one_truck
    
    
    total_cost_transport_recycling = total_cost_transport_recycle_concrete + total_cost_transport_recycle_glas+ total_cost_transport_recycle_metal+total_cost_transport_recycle_wood+total_cost_transport_recycle_others
    
    
    
    return total_cost_transport_recycling



def get_total_cost_recycle(dataframe_recycle_cubic,dataframe_recycle_square,cost_dataframe,cost_transport_dataframe, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood):
    #gets cost for demolition 
    cost_demolition_and_recycling_square = get_cost_demolition_recycle(dataframe_recycle_square, cost_dataframe)
    cost_demolition_and_recycling_cubic = get_cost_demolition_recycle(dataframe_recycle_cubic, cost_dataframe )
    # adds the two cost_demolition and recycling dataframes, the data is still per material
    cost_demolition_and_recycling = cost_demolition_and_recycling_square.add(cost_demolition_and_recycling_cubic, fill_value=0)
    #gets the total of each olumn
    cost_demolition = cost_demolition_and_recycling["Cost Demolition"].sum()
    cost_recycle = cost_demolition_and_recycling["Cost Recycle"].sum()
    #gets total cost transport
    total_cost_transport_recycle = get_cost_transport_recycle(dataframe_recycle_cubic, dataframe_recycle_square, cost_dataframe, cost_transport_dataframe, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood)
    # generates array of cost demolition, recycle and transport
    total_cost = np.array([[cost_demolition, cost_recycle,total_cost_transport_recycle]])
    total_cost_recycle = pd.DataFrame(total_cost, columns = ["Cost Demolition", "Cost Recycle", "Cost Transport"])
    return total_cost_recycle 


def get_total_cost(dataframe_total_cubic, dataframe_total_square, cost_dataframe, cost_transport_dataframe, dataframe_scenarios , addres_building, address_landfill, address_incinaration_plant, addres_concrete_brick, addres_glas, addres_metals, addres_wood, addres_storage):
        #scenario 0 (Disposal)
    #totalcosts_scenario_0 = get_total_cost_scenario_0(dataframe_total_cubic, dataframe_total_square, cost_dataframe, cost_transport_dataframe , addres_building, address_landfill, address_smelting_plant, address_incinaration_plant)
    total_costs_scenario_0 = get_total_cost_disposal(dataframe_total_cubic, dataframe_total_square, cost_dataframe, cost_transport_dataframe , addres_building, address_landfill, address_incinaration_plant)

    #####
    #scenario 1 (Baseline scenario)
    #gets the % of the reuse/recycle/disposal
    #gets dataframe cubic
    dataframe_reuse_cubic_1, dataframe_recycle_cubic_1, dataframe_disposal_cubic_1 = get_datframe_reuse_recyle_disposal(dataframe_total_cubic, dataframe_scenarios )
    #gets data frame sqaure
    dataframe_reuse_square_1, dataframe_recycle_square_1, dataframe_disposal_square_1 = get_datframe_reuse_recyle_disposal(dataframe_total_square, dataframe_scenarios)
    
    #Reuse total cost
    total_cost_reuse_1 = get_total_cost_reuse(dataframe_reuse_cubic_1, dataframe_reuse_square_1,cost_dataframe,cost_transport_dataframe, addres_storage, addres_building)

    #Recycle total cost
    total_cost_recycle_1 =   get_total_cost_recycle(dataframe_recycle_cubic_1,dataframe_recycle_square_1,cost_dataframe,cost_transport_dataframe, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood)

    #Disposal total cost
    total_cost_disposal_1 = get_total_cost_disposal(dataframe_disposal_cubic_1, dataframe_disposal_square_1, cost_dataframe, cost_transport_dataframe , addres_building, address_landfill, address_incinaration_plant)

    ####Scenario 2
    #gets dataframe cubic
    dataframe_reuse_cubic_2, dataframe_recycle_cubic_2, dataframe_disposal_cubic_2 = get_datframe_reuse_recyle_disposal_2(dataframe_total_cubic, dataframe_scenarios)
    #gets data frame sqaure
    dataframe_reuse_square_2, dataframe_recycle_square_2, dataframe_disposal_square_2 = get_datframe_reuse_recyle_disposal_2(dataframe_total_square, dataframe_scenarios)
    #Reuse total cost
    total_cost_reuse_2 = get_total_cost_reuse(dataframe_reuse_cubic_2, dataframe_reuse_square_2,cost_dataframe,cost_transport_dataframe, addres_storage, addres_building)

    #Recycle total cost
    total_cost_recycle_2 =   get_total_cost_recycle(dataframe_recycle_cubic_2,dataframe_recycle_square_2,cost_dataframe,cost_transport_dataframe, addres_building, addres_concrete_brick, addres_glas,addres_metals, addres_wood)

    #Disposal total cost
    total_cost_disposal_2 = get_total_cost_disposal(dataframe_disposal_cubic_2, dataframe_disposal_square_2, cost_dataframe, cost_transport_dataframe , addres_building, address_landfill, address_incinaration_plant)

    return total_costs_scenario_0, total_cost_reuse_1, total_cost_recycle_1, total_cost_disposal_1,  total_cost_reuse_2, total_cost_recycle_2, total_cost_disposal_2 



#functio to get the cost plot for scenario 0
def df_cost_to_plot_scenario_0(df):
    a = df[["Cost Demolition", "Cost Disposal", "Cost Transport"]].sum().to_frame() 
    
    row_labels_2 = {"Cost Demolition": 0,
              "Cost Disposal": 1,
              "Cost Transport": 2,
    }
    
    a.rename(index=row_labels_2, inplace = True)
    x = ["Cost Demolition", "Cost Disposal", "Cost Transport"]
    c = pd.DataFrame(data= x, columns=["Costs"])
    d = pd.concat([a,c], axis=1)
    d = d.rename(columns={0:"CHF"})
    df_output = d
    return df_output

#function to get the cost plot for scenario 1 and scenario 2

def df_cost_to_plot_scenario_1_2(df):
    
    a = df[["Cost Deconstruction", "Cost Transport", "Cost Demolition", "Cost Recycle", "Cost Disposal"]].sum().to_frame()
    
    row_labels = {"Cost Deconstruction": 0,
              "Cost Transport": 1,
              "Cost Demolition": 2,
              "Cost Recycle":3,
              "Cost Disposal":4
    }
    
    a.rename(index=row_labels, inplace = True)
    x = ["Cost Deconstruction", "Cost Transport", "Cost Demolition", "Cost Recycle", "Cost Disposal"]
    c = pd.DataFrame(data= x, columns=["Costs"])
    d = pd.concat([a,c], axis=1)
    d = d.rename(columns={0:"CHF"})
    df_output = d
    return df_output


    