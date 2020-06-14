# Jupyter widgets extension
jupyter labextension install @jupyter-widgets/jupyterlab-manager
# jupyterlab renderer support
jupyter labextension install jupyterlab-plotly@4.6.0 --no-build
# FigureWidget support
jupyter labextension install plotlywidget@4.6.0 --no-build
# Build extensions (must be done to activate extensions since --no-build is used above)
jupyter lab build
