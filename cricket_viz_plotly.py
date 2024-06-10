import pandas as pd
import plotly.graph_objects as go
import streamlit as st
match = 'Data_IND_vs_PAK.csv'


# team_color_mapping = {
#     "MI": ["#2D6AB1", "#123165"],
#     "RCB": ["#7B2226", "#2B2A29"],
#     "DC": ["#031760", "#B9251C"],
#     "CSK": ["#FFCB05", "#2478A7"],
#     "GT": ["#77C7F2", "#0E1A31"],
#     "PBKS": ["#D71920", "#283665"],
#     "LSG": ["#0248BB", "#E58C3C"],
#     "RR": ["#EB83B5", "#033571"],
#     "KKR": ["#29204A", "#ECC542"],
#     "SRH": ["#F26522", "#712324"]
# }

team_color_mapping = {
    "MI": ["#78a5ff", "#133b77"],  # Brighter shade of blue
    "RCB": ["#ff4d4d", "#2B2A29"],  # Brighter shade of red
    "DC": ["#6a7fff", "#B9251C"],  # Brighter shade of blue
    "CSK": ["#FFCB05", "#2478A7"],  # No change
    "GT": ["#77C7F2", "#C0D3E4"],  # No change
    "PBKS": ["#f98181", "#753D51"],  # Brighter shade of red
    "LSG": ["#1f7bff", "#77A4DC"],  # Brighter shade of blue
    "RR": ["#FF85A2", "#FFB2D9"],  # Brighter shade of pink
    "KKR": ["#7951db", "#7E72A8"],  # No change
    "SRH": ["#ff8266", "#FFA94D"],  # Brighter shade of orange
    "IND": ["#78a5ff", "#ff8266"],  # Blue and orange shades for Indian teams
    "IRE": ["#008000", "#0000ff"],  # Green and blue shades for Irish teams
    "NED": ["#FFA500", "#0000FF"],  # Orange and blue shades for Dutch teams
    "NEP": ["#8A2BE2", "#FF0000"], # Violet and red shades for Nepali teams
    "PAK": ["#008000", "#90EE90"]
}


data = pd.read_csv(match)


print(data)

team1 = match.split('_')[1]
team2 = match.split('_')[3].split('.')[0]

# Innings Summary (Bar chart)

inning1 = data[data.innings == 1]
inning2 = data[data.innings == 2]

fig = go.Figure()

inning1_label = f'{team1}: {inning1["cumRuns"].iloc[-1]}/{inning1["totalWickets"].iloc[-1]}'
inning2_label = f'{team2}: {inning2["cumRuns"].iloc[-1]}/{inning2["totalWickets"].iloc[-1]}'

winner = ""

if inning1["cumRuns"].iloc[-1] > inning2["cumRuns"].iloc[-1]:
    winner = team1
    win_by = f'{inning1["cumRuns"].iloc[-1] - inning2["cumRuns"].iloc[-1]} Runs'
else:
    winner = team2
    win_by = f'{10 - inning2["totalWickets"].iloc[-1]} Wickets'

# Add inning 1 data

score_info1 = inning1.apply(lambda row: f"{row['battingTeam']}: {row['cumRuns']}/{row['totalWickets']} ({row['overs']})", axis=1)

fig.add_trace(go.Scatter(x=inning1['ballNumber'], y=inning1['cumRuns'],
                         mode='lines',
                         name=inning1_label,
                         line=dict(color=team_color_mapping[team1][0], width=2),
                         text=score_info1,
                         hoverinfo='text'
                         ))
for i in range(len(inning1)):

    if inning1['isWicket'].iloc[i] == 1:
        wicket_info = f'{inning1.battingTeam.iloc[i]}: {inning1.cumRuns.iloc[i]}/{inning1.totalWickets.iloc[i]} ({inning1.overs.iloc[i]})<br>{inning1.striker.iloc[i]}: {inning1.strikerFinalScore.iloc[i]}'

        fig.add_trace(go.Scatter(x=[inning1['ballNumber'].iloc[i]], y=[inning1['cumRuns'].iloc[i]],
                                 mode='markers',
                                 name=wicket_info,
                                 marker=dict(color=team_color_mapping[team2][1], size=10,
                                             line=dict(color=team_color_mapping[team2][0], width=1)),
                                 text=wicket_info,
                                 hoverinfo='text'))

# Add inning 2 data
score_info2 = inning2.apply(lambda row: f"{row['battingTeam']}: {row['cumRuns']}/{row['totalWickets']} ({row['overs']})", axis=1)

fig.add_trace(go.Scatter(x=inning2['ballNumber'], y=inning2['cumRuns'],
                         mode='lines',
                         name=inning2_label,
                         line=dict(color=team_color_mapping[team2][0], width=2),
                         text=score_info2,
                         hoverinfo='text'
                         ))

for i in range(len(inning2)):
    if inning2['isWicket'].iloc[i] == 1:
        wicket_info = f'{inning2.battingTeam.iloc[i]}: {inning2.cumRuns.iloc[i]}/{inning2.totalWickets.iloc[i]} ({inning2.overs.iloc[i]})<br>{inning2.striker.iloc[i]}: {inning2.strikerFinalScore.iloc[i]}'
        fig.add_trace(go.Scatter(x=[inning2['ballNumber'].iloc[i]], y=[inning2['cumRuns'].iloc[i]],
                                 mode='markers',
                                 name=wicket_info,
                                 marker=dict(color=team_color_mapping[team1][1], size=10,
                                             line=dict(color=team_color_mapping[team1][0], width=1.5)),
                                 text=wicket_info,
                                 hoverinfo='text'))


# Add powerplay and middle overs lines
fig.add_shape(type="line",
              x0=38, y0=0, x1=38, y1=inning1['cumRuns'].max() + 10,
              line=dict(color="white", width=1, dash="dash"),
              xref='x', yref='y')
fig.add_shape(type="line",
              x0=94, y0=0, x1=94, y1=inning1['cumRuns'].max() + 10,
              line=dict(color="white", width=1, dash="dash"),
              xref='x', yref='y')
# Powerplay Runs Calculation
inning1_powerplay_runs = None
for i in range(len(inning1)):
    if inning1['overs'].iloc[i] == 5.6:
        inning1_powerplay_runs = f"{inning1.battingTeam.iloc[i]}: {inning1['cumRuns'].iloc[i]}/{inning1['totalWickets'].iloc[i]}"
        break

inning2_powerplay_runs = None
for i in range(len(inning2)):
    if inning2['overs'].iloc[i] == 5.6:
        inning2_powerplay_runs = f"{inning2.battingTeam.iloc[i]}: {inning2['cumRuns'].iloc[i]}/{inning2['totalWickets'].iloc[i]}"
        break

# Middle Overs Runs Calculation
inning1_mid_runs = None
for i in range(len(inning1)):
    if inning1['overs'].iloc[i] == 14.6:
        inning1_mid_runs = f"{inning1.battingTeam.iloc[i]}: {inning1['cumRuns'].iloc[i]}/{inning1['totalWickets'].iloc[i]}"
        break

if inning1_mid_runs is None and len(inning1) > 0:
    inning1_mid_runs = f"{inning1.battingTeam.iloc[-1]}: {inning1['cumRuns'].iloc[-1]}/{inning1['totalWickets'].iloc[-1]}"

inning2_mid_runs = None
for i in range(len(inning2)):
    if inning2['overs'].iloc[i] == 14.6:
        inning2_mid_runs = f"{inning2.battingTeam.iloc[i]}: {inning2['cumRuns'].iloc[i]}/{inning2['totalWickets'].iloc[i]}"
        break

if inning2_mid_runs is None and len(inning2) > 0:
    inning2_mid_runs = f"{inning2.battingTeam.iloc[-1]}: {inning2['cumRuns'].iloc[-1]}/{inning2['totalWickets'].iloc[-1]}"

# Death Overs Runs Calculation
if len(inning1) > 0:
    inning1_death_runs = f"{inning1.battingTeam.iloc[-1]}: {inning1['cumRuns'].iloc[-1]}/{inning1['totalWickets'].iloc[-1]}"

if len(inning2) > 0:
    inning2_death_runs = f"{inning2.battingTeam.iloc[-1]}: {inning2['cumRuns'].iloc[-1]}/{inning2['totalWickets'].iloc[-1]}"




# Add powerplay annotation
fig.add_annotation(x=18, y=0, text=f"Powerplay",
                   showarrow=False, font=dict(color="white", size=12))

fig.add_annotation(x=18, y=125, text=f"{inning1_powerplay_runs}<br>{inning2_powerplay_runs}",
                   showarrow=False, font=dict(color="white", size=16))

# Add middle overs annotation
fig.add_annotation(x=70, y=0, text="Middle Overs",
                   showarrow=False, font=dict(color="white", size=12))

fig.add_annotation(x=70, y=125, text=f"{inning1_mid_runs}<br>{inning2_mid_runs}",
                   showarrow=False, font=dict(color="white", size=16))


# Add death overs annotation
fig.add_annotation(x=110, y= 0, text="Death Overs",
                   showarrow=False, font=dict(color="white", size=12))

fig.add_annotation(x=110, y=125, text=f"{inning1_death_runs}<br>{inning2_death_runs}",
                   showarrow=False, font=dict(color="white", size=16))


# Add layout
fig.update_layout(
    title={
        'text': f'{team1} vs {team2} : Innings Summary<br>{winner} Won By {win_by}',
        'x': 0.4,
        'font': {
            'size': 24  # Increase title font size
        }
    },
    xaxis_title='Balls',
    yaxis_title='Runs',
    plot_bgcolor='#313131',
    paper_bgcolor='#393939',
    font=dict(color="white"),
    legend=dict(font=dict(color="white"))
)
# plt.show()

# Display Plotly plot in Streamlit
st.plotly_chart(fig)
