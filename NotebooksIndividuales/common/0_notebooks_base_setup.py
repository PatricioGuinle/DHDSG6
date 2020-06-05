import os, sys, subprocess
from ipywidgets import Layout, Box, Image, HTML

def popen(cmd):
    try:
        print(f"Running command `{cmd}`... ", end="")
        proc = subprocess.run(
            cmd,
            shell=True,
            check=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("ok")
        return proc.stdout
    except subprocess.CalledProcessError as err:
        print("error\n   ", err.stderr)
        raise

def draw_text_icon(image_path, html_text):
    items_layout = Layout( width='auto')     # override the default width of the button to 'auto' to let the button grow

    box_layout = Layout(display='flex',
                    flex_flow='row',
                    align_items='stretch',
                    border='none',
                    width='100%')

    with open(image_path, "rb") as file:
        image = file.read()
    image_obj = Image(
        value=image,
        format='png'
    )

    html_obj = HTML(
        value=html_text
    )

    items = [image_obj, html_obj]
    box = Box(children=items, layout=box_layout)
    return box


def update_path():
    notebook_base_path = os.getcwd()
    if notebook_base_path not in sys.path:
        sys.path.append(notebook_base_path)
    return


def list_conda_installed_packages():
    output_lines = popen('conda list').split("\n")

    names = []

    for line in output_lines:
        line_clean = " ".join(line.split())
        line_clean_parts = line_clean.split(' ')
        #print(line_clean_parts)
        #print(len(line_clean_parts))
        if len(line_clean_parts) > 1:
            package_version = line_clean_parts[0] + '=' + line_clean_parts[1]
            #print(package_version)
            names.append(package_version)
    
    return(names)

def list_required_packages(requirements_file_path):
    with open(requirements_file_path) as file:
        return file.readlines()

def install_packages(requirements_file_path, channel=None):
    installed = list_conda_installed_packages()    
    required_packages = list_required_packages(requirements_file_path)
    for p in required_packages:
        package_name = p.strip()
        if package_name not in installed:            
            #print(package_name  + ' not installed')
            command = 'conda install --yes '
            if channel:
                command += '-c ' + channel + ' '            
            command += package_name
            print(popen(command))
        else:
            print(package_name + ' already installed' )

def main(arguments):
    
    update_path()
    
    if 'plotly' in arguments:
        print('check plotly dependencies')
        plotly_requirements_file_path = 'common/requirements_plotly.txt'
        try:
            install_packages(plotly_requirements_file_path, channel='plotly')
        except subprocess.CalledProcessError as err:
            pass
    else:
        print('default checking')
        
    requirements_file_path = 'common/requirements.txt'
    try:
        install_packages(requirements_file_path)
    except subprocess.CalledProcessError as err:
        pass

main(sys.argv)

print("Importando librerías ...")
import pandas as pd
import seaborn as sns
import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import chart_studio
import chart_studio.plotly as py
import unicodedata
print("Las librerías has sido importadas con éxito")

pd.set_option('display.max_rows', 300)
pd.set_option('display.width', 5000)