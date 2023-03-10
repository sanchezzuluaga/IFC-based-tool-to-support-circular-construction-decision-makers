# IFC-based tool to calculate environmental and cost impacts to support Swiss decision-makers of the circular construction
## Description

A user-friendly IFC-tool was developed that simultaneously calculates the environmental benefits and costs related to reusing/recycling materials. To assist stakeholders of the circular construction in making better-informed decisions.
The tool should serve to demonstrate to users:
+ At early design stages adopt strategies that facilitate easy deconstruction, highlighting how maximizing materials' reuse potential can significantly reduce environmental impacts.
+ The advantages of reusing and recycling materials at the end-of-life stage of buildings.
+ The benefits of reusing materials over recycling.

The tool is divided into two interfaces. The first interface includes the quantity take-off. After uploading the IFC file the tool extracts the bill of quantities. The second interface encompasses the calculation of the environmental and cost impacts. 

The program was developed for a Master’s Thesis at ETH Zurich under the supervision of Dr. Meliha Honic and Brandon Byers (Chair of Circular Engineering for Architecture). 

## Installation

1. Install Anaconda for the Python environment (https://www.anaconda.com/)
2.  Open Anaconda and create an environment with the following packages (to install packages in Anaconda: https://docs.anaconda.com/anaconda/user-guide/tasks/install-packages/):
+ streamlit
+ ifcopenshell
+ pandas
+ plotly.express
+ numpy
+ googlemaps
+ math
+ matplotlib.pyplot
+ pprint
3. In the "tools" folder under environmental_functions.py and cost_functions.py the "get_distance" function needs a google id client, please get one and insert it where the command key = "" is (https://www.balbooa.com/gridbox-documentation/how-to-get-google-client-id-and-client-secret).
4. In the file "2_Environmental_Impact_&_Cost.py" and "3_KBOB_overview.py" under the folder "pages", insert the full path (under "filepath") where the "Database.xlsx" is stored.
5. To run the tool open Anaconda --> Environments --> Select the created environment (Step 2) --> Press the play  button  of the created environmen --> Open terminal --> enter the following command: streamlit run "direction" (the "direction" needs to be replaced by the file direction where the Homepage.py is located) e.g.: 

(streamlit run C:\Users\simon\Dropbox\01_Master_Thesis\05_Python\App\Homepage.py)

6. The program runs and can be used

## Instructions to generate the BIM model
To connect the database with the IFC file shared parameters need to be created( In Revit: https://www.youtube.com/watch?v=MGZo8Ue2sq0). The parameters need to be named KBOBX, where X is the number of the material. If there is a multi-layer element the X needs to increase depending on the number of layers of the element. The value of the shared parameter is the Id. number of the Swiss KBOB database.

### Multi-layer elements:
For walls, the X in KBOBX needs to increase from the outside to the inside. For roofs and slabs the X in KBOBX needs to increase from the top to the bottom.  

<img width="198" alt="Wall" src="https://user-images.githubusercontent.com/122563486/217525946-44814ffc-d2b2-4a60-96a1-f3977cdb42d5.png">
<img width="189" alt="Slab_Roof" src="https://user-images.githubusercontent.com/122563486/217529924-5c43e988-978e-4ae4-bdc9-b33d816650a5.png">

### Single-layer elements:

For single-layer elements  only KBOB1 and the value of the Id. number need to be modelled. For the windows only the Id. number of the frame is needed. 

## Instruction to correctly extract the IFC file and use the tool

IfcMaterial (https://standards.buildingsmart.org/IFC/DEV/IFC4_3/RC1/HTML/schema/ifcmaterialresource/lexical/ifcmaterial.htm):
+ The multi-layer elements need to be extracted in the IfcMultiLayerSet
+ Columns and beams elements need to be extracted as IfcMaterialProfile
+ Doors and Windows need to be extractes as IfcMaterialConstituentSet

Export the IFC file as a IFC4. In Revit export it  as IFC4 Design Tranfer View. The shared paramters need to be also exported --> In Revit: File--> Moodify set up --> Property sets --> Export Revit Property Sets.

In addition, the property and quantity sets need to be stored in the right way as outlined by the IFC documentation (https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/).

## Files overview 
+ Data: the database for calculating the cost and environmental impacts can be found.
+ Pages: the different interfaces of the tool: Quantity take-off, Environmental impact and cost, and KBOB overview (for the user to see the Id. number to be inserted in the BIM model)
+ tools: all the functions for the different tools
+ template: template to upload in case no IFC file is available
