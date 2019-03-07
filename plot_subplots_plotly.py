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
        '2019-02-26 23:19:22',
#        '',
            ]
#timestamp = '2018-11-29 17:05:07'
for timestamp in list_of_time_stamps:
    db = Cinfdata('microreactorNG',
                  use_caching = True,
                  grouping_column = 'time',
                  )
    group_data = db.get_data_group(timestamp, scaling_factors=(1E-3, None))
    group_meta = db.get_metadata_group(timestamp)
    #print(group_data)
    #print([i for key, i in group_meta.items() if 'comment' in i.lower()])
    ## Get a list of labels and group data
    try:
        name = group_meta[list(group_meta.keys())[0]]['Comment']
    except KeyError:
        print('comment with small ')
        name = group_meta[list(group_meta.keys())[0]]['comment']
    print(name)
    labels = [group_meta[key]['mass_label'] for key in group_data.keys()]
    data = {group_meta[key]['mass_label']: group_data[key] for key in group_data.keys()}
    print('Loaded data from Experiment: "{}"'.format(name))
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
    RTD_plot = data['RTD temperature']
    TC_plot = data['TC temperature']
    min_length= min([len(data['Heater voltage 1'][:,1]), len(data['Heater current 1'][:,1]), len(data['Heater voltage 2'][:,1]), len(data['Heater current 2'][:,1])])
    print([len(data['Heater voltage 1'][:,1]), len(data['Heater current 1'][:,1]), len(data['Heater voltage 2'][:,1]), len(data['Heater current 2'][:,1])],min_length)
    Total_power = data['Heater voltage 1'][:min_length,1] * data['Heater current 1'][:min_length,1] + data['Heater voltage 2'][:min_length,1] * data['Heater current 2'][:min_length,1]

    print(Total_power)
    for k, v in data.items():
        print(k)
    print(data['M44'][:,0])
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    end_time = 5000
    start_index = 0#2000
    ax1.plot(RTD_plot[start_index:end_time,0],RTD_plot[start_index:end_time,1],'black',linestyle = '-')#, dashes=(5,5)) 
    ax1.plot(TC_plot[start_index:end_time,0],TC_plot[start_index:end_time,1], 'grey', linestyle ='-')
    ax2.plot(TC_plot[start_index:end_time,0],Total_power[start_index:end_time])
    plt.title(name)
    plt.savefig(name+'_first.pdf')
    #plt.show()
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
random_y0 = np.random.randn(N)+45
random_y1 = np.random.randn(N)+3
random_y2 = np.random.randn(N)+15
random_y3= np.random.randn(N)+1
# Create traces
traceRTD = go.Scatter(
        x = data['RTD temperature'][:,0],#random_x,
        y = data['RTD temperature'][:,1],#,random_y0,
    mode = 'lines',
    name = 'RTD Temperature'
)
traceTC = go.Scatter(
    x = data['TC temperature'][:,0],#random_x,
    y = data['TC temperature'][:,1],#,random_y0,
    mode = 'lines',
    name = 'TC Temperature',
    xaxis='x',
    yaxis='y'
)
tracePress = go.Scatter(
    x = data['Reactor pressure'][:,0],#random_x,
    y = data['Reactor pressure'][:,1],#,random_y0,
    mode = 'lines',
    name = 'Reactor Pressure',
    xaxis='x',
    yaxis='y2'
)
#gas = {'M2':, M15:, M18:, M28:, M31:, M32:, M40:, M44:, M46:}
gas = ['M2', 'M15', 'M18', 'M28', 'M31', 'M32', 'M40', 'M44', 'M46']
traceM2 = go.Scatter(
    x = data['M2'][:,0],#random_x,
    y = data['M2'][:,1],#,random_y0,
    mode = 'lines',
    name = 'H2 (M2)',
    xaxis='x',
    yaxis='y3'
)
traceM15 = go.Scatter(
    x = data['M15'][:,0],#random_x,
    y = data['M15'][:,1],#,random_y0,
    mode = 'lines',
    name = 'CH4 (M15)',
    xaxis='x',
    yaxis='y4'
)
traceM18 = go.Scatter(
    x = data['M18'][:,0],#random_x,
    y = data['M18'][:,1],#,random_y0,
    mode = 'lines',
    name = 'H2O (M18)',
    xaxis='x',
    yaxis='y3'
)
traceM28 = go.Scatter(
    x = data['M28'][:,0],#random_x,
    y = data['M28'][:,1],#,random_y0,
    mode = 'lines',
    name = 'CO (M28)',
    xaxis='x',
    yaxis='y4'
)
traceM31 = go.Scatter(
    x = data['M31'][:,0],#random_x,
    y = data['M31'][:,1],#,random_y0,
    mode = 'lines',
    name = 'CH3OH (M31)',
    xaxis='x',
    yaxis='y3'
)
traceM32 = go.Scatter(
    x = data['M32'][:,0],#random_x,
    y = data['M32'][:,1],#,random_y0,
    mode = 'lines',
    name = 'O2 (M32)',
    xaxis='x',
    yaxis='y4'
)
traceM40 = go.Scatter(
    x = data['M40'][:,0],#random_x,
    y = data['M40'][:,1],#,random_y0,
    mode = 'lines',
    name = 'Ar (M40)',
    xaxis='x',
    yaxis='y4'
)
traceM44 = go.Scatter(
    x = data['M44'][:,0],#random_x,
    y = data['M44'][:,1],#,random_y0,
    mode = 'lines',
    name = 'CO2 (M44)',
    xaxis='x',
    yaxis='y3'
)
traceM46 = go.Scatter(
    x = data['M46'][:,0],#random_x,
    y = data['M46'][:,1],#,random_y0,
    mode = 'lines',
    name = 'CO2?, Myresyre? (M46)',
    xaxis='x',
    yaxis='y3'
)
trace2 = go.Scatter(
    x = random_x,
    y = random_y2,
    mode = 'markers',
    name = 'markers',
    xaxis='x2',
    yaxis='y5'
)
trace3 = go.Scatter(
    x = random_x,
    y = random_y1,
    mode = 'markers',
    name = 'markers_2',
    xaxis='x',
    yaxis='y2'
)
trace4 = go.Scatter(
    x = random_x,
    y = random_y1,
    mode = 'markers',
    name = 'markers_2',
    xaxis='x',
    yaxis='y4'
)
trace5 = go.Scatter(
    x = random_x,
    y = random_y1,
    mode = 'markers',
    name = 'markers_2',
    xaxis='x',
    yaxis='y2'
)
data_plot = [traceRTD, traceTC, tracePress, traceM2, traceM18,
        traceM28, traceM32, traceM40, traceM44,]

layout = go.Layout(
         xaxis=dict(
             domain=[0, 1]#0.45]
             ),
         yaxis=dict(
             domain=[0, 0.30],
             showgrid=False,
             zeroline=False,
             ticks='inside',
             ),
         yaxis2=dict(
             domain=[0, 0.30],
             overlaying='y',
             side='right',
             showgrid=False,
             zeroline=False,
             ticks='outside',
             ),
         yaxis3=dict(
             domain=[0.32, 1],
             type='log',
             showgrid=False,
             zeroline=False,
             ticks='outside',
             exponentformat='power',
             ),
         yaxis4=dict(
             domain=[0.32, 1],
             overlaying='y3',
             side='right',
             type='log',
             showgrid=False,
             zeroline=False,
             ticks='outside',
             exponentformat='e',
             ),
#         xaxis2=dict(
#             domain=[0.55, 1],
#             ),
#         yaxis5=dict(
#             domain=[0, 1],
#             anchor='x2',
#             ),
        )

fig = go.Figure(data=data_plot, layout=layout)
plotoff.plot(fig, filename='triple_plot')
