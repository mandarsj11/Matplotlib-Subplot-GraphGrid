import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md

Bird_Spreadsheet = pd.read_excel('All_Bird_Data.xlsx', sheet_name=None)
All_Bird_input = Bird_Spreadsheet['Data']

location = All_Bird_input['Location'].unique()
bird = All_Bird_input['Bird'].unique()
month = All_Bird_input['Month'].unique()
colour_seq = ['red','blue','green'] #set different color for location line graph

#convert datetime.time to datetime.datetime - time can then be formatted to HH:MM
All_Bird_input = All_Bird_input.assign(date_time=pd.to_datetime(All_Bird_input['Time'], format='%H:%M:%S')) 

fig, axes = plt.subplots(nrows=6,ncols=12, sharey='row', figsize=(72, 42))
plt.style.use('ggplot')
z=0 #counter 
for i in range(len(bird)):
    for j in range(len(month)):
        All_Bird_input_bird = All_Bird_input[(All_Bird_input['Bird']==bird[i])]
        All_Bird_input_month = All_Bird_input[(All_Bird_input['Bird']==bird[i])
                                            & (All_Bird_input['Month']==month[j])]
        sunset = All_Bird_input_month['Sunset'].unique()
        x = [pd.to_datetime(sunset, format='%H:%M:%S'), pd.to_datetime(sunset, format='%H:%M:%S')]
        y = [0,All_Bird_input_bird['Total'].max()]
        for items, col in zip(location, colour_seq):
            All_Bird_input_location = All_Bird_input[(All_Bird_input['Bird']==bird[i])
                                                   & (All_Bird_input['Month']==month[j])
                                                   & (All_Bird_input['Location']==items)]
            axes[i, j].plot(All_Bird_input_location['date_time'],All_Bird_input_location['Total'], marker='.', label=items, color = col,linewidth=2.0)
            #ref link - https://www.unidata.ucar.edu/blogs/developer/entry/simple-plotting-in-python-with
            plt.setp(axes[i,j].xaxis.get_majorticklabels(), rotation=90 ) #X axis major tick label rotation
        axes[i,j].plot(x,y,linestyle='--',label = "Sunset Time",color='black',linewidth=2.0)
        axes[i,j].set(title = bird[i] +' For ' + month[j])
        
        #Modify x axis label - automatically set as 'time'
        x_axis = axes[i,j].axes.get_xaxis()
        x_label = x_axis.get_label()
        x_label.set_text('Bird Arrival Period')
        
        #set x axis interval
        xformatter = md.DateFormatter('%H:%M')
        plt.gcf().axes[z].xaxis.set_major_formatter(xformatter)
        z=z+1
        
fig.suptitle('Rousting pattern for 6 Bird species over one year - Data Source: Abhijit Gandhi and Team', fontsize=30)
fig.subplots_adjust(top=0.95, hspace = 0.3) # to adjust huge blank space between Fig title and subplots

plt.legend(bbox_to_anchor=(-13, 7.60), loc='lower left', borderaxespad=0) #Loc-reference for Legend block: bbox_to_anchor-assuming right bottom corner of fig as (0,0)
fig.savefig('bird_data.pdf', transparent=False, dpi=80, bbox_inches="tight")

#explicitly set tick marks using np arrange - https://intellipaat.com/community/9913/changing-the-tick-frequency-on-x-or-y-axis-in-matplotlib

