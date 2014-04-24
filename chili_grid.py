from kivy.uix.gridlayout import GridLayout
from kivy.properties import ReferenceListProperty


class ChiliGrid(GridLayout):
    gridsize = ReferenceListProperty(GridLayout.rows, GridLayout.cols)
