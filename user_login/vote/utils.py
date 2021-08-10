import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format = 'png')#, transparent = True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize= (4,5))
    plt.title('')
    plt.bar(x,y)
    plt.yscale("linear")
    plt.xticks(rotation=0)
    plt.xlabel('Name')
    plt.ylabel('Count')
    plt.tight_layout()

    graph = get_graph()
    return graph