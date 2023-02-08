# IFC-based tool to calculate environmental and cost impacts 
## Description

A user-friendly tool was developed that simultaneously calculates the environmental benefits and costs related to reusing/recycling materials. To assist stakeholders of the circular construction in making better-informed decisions.
The tool should serve to demonstrate to users:
+ At early design stages adopt strategies that facilitate easy deconstruction, highlighting how maximizing materials' reuse potential can significantly reduce environmental impacts.
+ The advantages of reusing and recycling materials at the end-of-life stage of buildings.
+ The benefits of reusing materials over recycling.

The tool is divided into two interfaces. The first interface includes the quantity take-off. After uploading the IFC file the tool extracts the bill of quantities. The second interface encompasses the calculation of the environmental and cost impacts. 

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
3. In the tools folder under environmental_functions.py and cost_functions.py the get_distance function needs a google id client, please get one and insert it where the command key = "" is 
4. To run the tool go to anaconda. Press the play botton of the created environment (step 2) --> Open terminal --> enter the following command : streamlit run "direction" (the "direction" needs to be replaced by the file direction wehre the Homepage.py is located e.g.: 
streamlit run C:\Users\simon\Dropbox\01_Master_Thesis\05_Python\App\Homepage.py)
5. The programm runs and can be used

## Model BIM
To connect the database with the IFC file shared parameters to 
