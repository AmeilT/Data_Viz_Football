import numpy as np

title_font="Franklin Gothic Medium"
title_size=14
label_font="Franklin Gothic Medium"
label_size=9
text_colour="w"
back_colour="#020530"

def y_equals_x(data,x,y,axes,colour="g--"):
    a = np.linspace(0, max(data[x].max(),data[y].max()), 20)
    b = np.linspace(0, max(data[x].max(),data[y].max()), 20)
    axes.plot(a,b, colour)