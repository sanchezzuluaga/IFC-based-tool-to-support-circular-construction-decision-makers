import matplotlib.pyplot as plt
import plotly.express as px



# pie chart 
def get_pie_chart(dataframe):
     materials =  dataframe.iloc[:,0]
     quantities =  dataframe.iloc[:,2]
     fig = px.pie(dataframe, values= quantities, names = materials )
     return(fig)
