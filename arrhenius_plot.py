import sys
print(sys.path)
from cinf_database.cinfdata import Cinfdata
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import gridspec
import plotly.offline as plotoff
import plotly.plotly as py
import plotly.graph_objs as go


list_of_time_stamps = [
#        '2018-11-29 17:05:07',
#        '2018-11-29 15:42:58',
#        '2018-11-26 14:52:53',
#        '2018-11-22 16:32:52',
#        '2018-11-20 16:50:03',
#        '2018-11-07 18:50:37',
#        '2018-10-31 16:58:48',    
        '2019-01-15 20:29:19',
#        '',
            ]
#timestamp = '2018-11-29 17:05:07' #comment:

class get_data_for_story:

    def __init__(self,setup,timestamps):

        self.setup = setup
        self.db = Cinfdata(
                self.setup,
                use_caching = True,
                grouping_column = 'time'
                )
        self.list_of_time_stamps = timestamps

    def get_data_from_timestamp(self):

        for timestamp in self.list_of_time_stamps:
            self.group_data = self.db.get_data_group(timestamp, scaling_factors=(1E-3, None))
            self.group_meta = self.db.get_metadata_group(timestamp)
            #print(group_data)
            #print([i for key, i in group_meta.items() if 'comment' in i.lower()])
            ## Get a list of labels and group data
            try:
                self.name = self.group_meta[list(self.group_meta.keys())[0]]['Comment']
            except KeyError:
                print('comment with small ')
                self.name = self.group_meta[list(self.group_meta.keys())[0]]['comment']
            print(self.name)
            self.labels = [self.group_meta[key]['mass_label'] for key in self.group_data.keys()]
            self.data = {self.group_meta[key]['mass_label']: self.group_data[key] for key in self.group_data.keys()}
            print('Loaded data from Experiment: "{}"'.format(self.name))

        return self.labels, self.data, self.name
    #print(data)
    #x = [i/1000 for i in spectrum[:,0]]
    #index = np.searchsorted(x, 20)
#    for label in data.keys():
#        print(label)
#        plt.figure()
    #    for i in range(0,int(data[label][-1,0]),3600):
    #        plt.axvspan(i,i+1800, facecolor='b', alpha=0.5)
#        plt.plot(data[label][:,0],data[label][:,1])
#        plt.title(label)
    #    plt.show()
#        plt.close()
    #### RTD plus TC Plot with power ####
ms_data = get_data_for_story(setup='microreactorNG',timestamps=list_of_time_stamps)
labels, data, name = ms_data.get_data_from_timestamp()
print(labels)
RTD_plot = data['RTD temperature']
M44 = data['M44']
TC_plot = data['TC temperature']
min_length= min([len(data['Heater voltage 1'][:,1]), len(data['Heater current 1'][:,1]), len(data['Heater voltage 2'][:,1]), len(data['Heater current 2'][:,1])])
print([len(data['Heater voltage 1'][:,1]), len(data['Heater current 1'][:,1]), len(data['Heater voltage 2'][:,1]), len(data['Heater current 2'][:,1])],min_length)
Total_power = data['Heater voltage 1'][:min_length,1] * data['Heater current 1'][:min_length,1] + data['Heater voltage 2'][:min_length,1] * data['Heater current 2'][:min_length,1]

#print(Total_power)
#fig, ax1 = plt.subplots()
#ax2 = ax1.twinx()
#end_time = -1#5000
#start_index = 0#2000
#ln1 = ax1.plot(M44[start_index:end_time,0],M44[start_index:end_time,1],'red',linestyle = '-', label = 'CO2')#, dashes=(5,5)) 
#ln2 = ax2.plot(TC_plot[start_index:end_time,0],TC_plot[start_index:end_time,1], 'black', linestyle ='--', label= 'Temperature (TC)')
#ax1.plot(M44[start_index:end_time,0],M44[start_index:end_time,1],'red',linestyle = '-', label = 'CO2')#, dashes=(5,5)) 
#ax2.plot(TC_plot[start_index:end_time,0],TC_plot[start_index:end_time,1], 'black', linestyle ='--', label= 'Temperature (TC)')
#ax2.plot(TC_plot[start_index:end_time,0],Total_power[start_index:end_time])

#lns = ln1 + ln2
#all_labels = [l.get_label() for l in lns]
#plt.legend(lns, all_labels)
#ax1.set_xlabel('Time [s]')
#ax1.set_ylabel('SEM current [A]')
#ax2.set_ylabel('Temperature [C]')
#plt.title(name)
#plt.savefig(name+'_T_M44.pdf')
#plt.show()


start = 12050
end = 48000
plots = [x for x in range(start,end,1140)]
#for x in plots:
#    ax2.plot((x,x),(0,100), 'blue')

#plt.savefig(name+'_T_M44_with_arr_blue_lines.pdf')
#plt.show()

temp_time_index = np.searchsorted(TC_plot[:,0],plots[:])
signal_time_index = np.searchsorted(M44[:,0],plots[:])
print(temp_time_index)
Temp_arr = [TC_plot[x,1] for x in temp_time_index]
inverse_temp_arr = [1/T for T in Temp_arr]
M44_signal = [M44[x,1] for x in signal_time_index]
print(Temp_arr)
print(M44_signal)


plt.plot(inverse_temp_arr, M44_signal, '*')
#ax.set_yscale('log')
plt.title('Arrhenius plot AuTi on TiO2, first')
plt.xlabel('Temperature (1/T)')
plt.ylabel('SEM current M44')
plt.yscale('log')
plt.savefig('arrhenius_AuTi_first')
plt.show()
#print(data)
#    prnt = [i for i in data['M44'][0][:]]
#    prnt = data['M44'][:,0]
#print(prnt)
#plt.plot(data[label][]
#plt.plot(x[0:index], spectrum[0:index, 1])
#plt.title(metadata['comment'])
#plt.show()


N = 500
random_x = np.linspace(0, 1, N)
random_y = np.random.randn(N)
trace1 = go.Scatter( x = random_x,y = random_y)

data1 = [trace1]

N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N)+5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N)-5

# Create traces
trace0 = go.Scatter(
    x = random_x,
    y = random_y0,
    mode = 'lines',
    name = 'lines'
)
trace1 = go.Scatter(
    x = random_x,
    y = random_y1,
    mode = 'lines+markers',
    name = 'lines+markers'
)
trace2 = go.Scatter(
    x = random_x,
    y = random_y2,
    mode = 'markers',
    name = 'markers'
)
data = [trace0, trace1, trace2]

#plotoff.plot(data)
