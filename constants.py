import os
from pathlib import Path
#from chart_functions import hex_to_rgb
import pandas as pd

DATADir=r"C:\Users\ameil\Documents\GitHub\Historical data by gameweek.csv"
features = ["involvement", "distribution", "goal-threat", "defending", "set-pieces", "kpi-attacking", "kpi-defending","expected"]
teams = pd.DataFrame()
teams["Team"] = ['ARS','AVL','BHA','BUR','CHE','CRY','EVE','FUL','LEE','LEI','LIV','MCI','MUN','NEW','SHU','SOU','TOT','WBA','WHU','WOL']
colours = ["#EE3B3B", "#942257", "#afd6f0", "#631938"
    , "#1c19a8", "#500678", "#3d64e3", "#eff0e9"
    , "#eff0e9", "#4157c4"
    , "#c20245", "#04becf", "#de020a"
    , "#877777", "#e65353", "#ff001e", "#FFFFFF"
    , "#022873", "#70072f", "#f59247"]
dict_team={k:v for k,v in zip(teams["Team"], colours)}
teams["Colours"]=teams['Team'].map(dict_team)
#teams["ColoursRGB"] = teams["Colours"].apply(hex_to_rgb)
columns_used = ['Name',
                'Season',
                'Position', "GW ID",
                'Team',
                'TouchesOpp Half',
                'TouchesFin 3rd',
                'Passes ReceivedOpp Half',
                'Passes ReceivedFin 3rd',
                'FPL Goal Inv',
                'Big Chances Created',
                'Total Assists',
                'Successful Crosses',
                'Pass Completion',
                'Attempts In Box',
                'Attempts On Target',
                'Successful Corners',
                'Headed Attempts from Set Pieces',
                'Form Measure EWM Points',
                'Form Measure EWM Points_Opponent',
                'Opponent',
                'MA Opponent Goals Conceded',
                'MA Opponent Clean Sheets',
                'MA Opponent Shots ConcededIn',
                'MA Opponent Shots ConcededOut',
                'MA Opponent Shots ConcededTotal',
                'MA Opponent Shots ConcededOn Target',
                'MA Opponent Shots ConcededHead',
                'MA Team GoalsTotal',
                'MA Team AttemptsTotal',
                'MA Team AttemptsIn',
                'MA Team AttemptsBCT',
                'MA Team AttemptsSP',
                'MA Team AttemptsBlkd',
                'MA Team AttemptsOn Target',
                'Passes Final Third',
                'Corners Taken',
                'Goal Attempts',
                'Chances Created',
                'Crosses',
                'Penalty Touches',
                'Attacking FPL Points']

rolling = ['TouchesOpp Half',
           'TouchesFin 3rd',
           'Passes ReceivedOpp Half',
           'Passes ReceivedFin 3rd',
           'FPL Goal Inv',
           'Big Chances Created',
           'Total Assists',
           'Successful Crosses',
           'Pass Completion',
           'Attempts In Box',
           'Attempts On Target',
           'Successful Corners',
           'Headed Attempts from Set Pieces', 'Passes Final Third',
           'Corners Taken',
           'Goal Attempts',
           'Chances Created',
           'Crosses',
           'Penalty Touches', "Attacking FPL Points"]
