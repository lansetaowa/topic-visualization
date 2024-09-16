# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 21:21:39 2024

@author: elisa
"""

import pandas as pd
import prince
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.sans-serif'] = ['SimHei'] # Or any other Chinese characters
plt.rcParams['axes.unicode_minus'] = False

class Correspondence_Viz():
    
    def __init__(self, value_var, dim_var, input_df):
        '''
        value_var: variable that has specific values, usually "keywords" in Social Listening analysis
        dim_var: variable that contains dimension，possibly "quarter", "month" or "brand"
        '''
        self.value_var = value_var
        self.dim_var = dim_var
    
    def table_for_ca(self, input_df):
        
        table_for_ca = input_df 
        table_for_ca.columns.rename(self.value_var, inplace=True)
        table_for_ca.index.rename(self.dim_var, inplace=True)

        return table_for_ca
    
    def fit_ca(self, ca_df):

        ca = prince.CA(n_components=2,
               n_iter=10,
               copy=True,
               check_input=True,
               engine='scipy',
               random_state=42)

        ca = ca.fit(ca_df)

        row_coord = ca.row_coordinates(ca_df)
        col_coord = ca.column_coordinates(ca_df)

        row_coord.reset_index(inplace=True)
        col_coord.reset_index(inplace=True)

        row_coord.columns = ['index','x','y']
        col_coord.columns = ['index','x','y']

        row_coord['name'] = self.dim_var
        col_coord['name'] = self.value_var

        ca_results = pd.concat([row_coord, col_coord])
        ca_results.reset_index(inplace=True)
        ca_results.drop('level_0', inplace=True, axis=1)

        return ca_results
    
    def visualize_ca(self, ca_results, chart_title, output_dir, output_name):

        x = ca_results["x"].astype(float)
        y = ca_results["y"].astype(float)
        c = ca_results["name"]
        l = ca_results['index']

        # Create a figure with the desired size
        fig, ax = plt.subplots(figsize=(12, 12))

        # Create a scatter plot with different colors and shapes for the points
        colors = {self.dim_var: 'red', self.value_var: 'blue'}
        shapes = {self.dim_var: 'o', self.value_var: '^'}

        for i in set(c):
            plt.scatter(x[c==i], y[c==i], 
                        color=colors[i], marker=shapes[i], label=str(i), alpha=0.8)

        # Add labels to each point
        for i, txt in enumerate(l):
            plt.annotate(txt, (x[i], y[i]), fontsize = 12)

        # ax.set_xlim(-0.5, 0.8)
        # ax.set_ylim(-0.5, 0.8)

        # Add a title, axis labels, and legend
        plt.title(chart_title)
        plt.xlabel("Column X")
        plt.ylabel("Column Y")
        plt.legend()

        plt.savefig(output_dir + '\\' + output_name + '.svg', format='svg')
        plt.savefig(output_dir + '\\' + output_name +'.png', format='png')

    def visualize_ca_axislim(self, ca_results, chart_title, 
                             xlim, ylim,
                             output_dir, output_name):
        '''
        xlim, ylim: list of two floats
        '''
        x = ca_results["x"].astype(float)
        y = ca_results["y"].astype(float)
        c = ca_results["name"]
        l = ca_results['index']

        # Create a figure with the desired size
        fig, ax = plt.subplots(figsize=(12, 12))

        # Create a scatter plot with different colors and shapes for the points
        colors = {self.dim_var: 'red', self.value_var: 'blue'}
        shapes = {self.dim_var: 'o', self.value_var: '^'}

        for i in set(c):
            plt.scatter(x[c==i], y[c==i], 
                        color=colors[i], marker=shapes[i], label=str(i), alpha=0.8)

        # Add labels to each point
        for i, txt in enumerate(l):
            plt.annotate(txt, (x[i], y[i]), fontsize = 14)

        ax.set_xlim(xlim[0], xlim[1])
        ax.set_ylim(ylim[0], ylim[1])

        # Add a title, axis labels, and legend
        plt.title(chart_title)
        plt.xlabel("Column X")
        plt.ylabel("Column Y")
        plt.legend()

        plt.savefig(output_dir + '\\' + output_name + '.svg', format='svg')
        plt.savefig(output_dir + '\\' + output_name +'.png', format='png')
