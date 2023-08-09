

import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class PlotWindow:
    def __init__(self, masterframe, size):
        """
        Initialize the PlotWindow object.

        Args:
            masterframe (tkinter.Tk or tkinter.Frame): The parent frame for the plot.
            size (tuple): The size of the plot (width, height).
        """
        self.figure, self.axes = plt.subplots(figsize=size, dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=masterframe)
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.background_color = 'orange'
        self.font_style = {'family': 'Trebuchet MS', 'size': 18}

    def plot_data(self, chart_type):
        """
        Plot the data based on the given chart type.

        Args:
            chart_type (str): The type of chart to plot.
        """
        data = pd.read_csv('SalesDL.csv')
        self.axes.clear()

        if chart_type == 'Category-wise Total Sales':
            print(PlotWindow.plot_data_prod_cat.__doc__)
            plot_w.plot_data_prod_cat(data)


        elif chart_type == 'Sub Category-wise(Bikes) Sales':
            print(PlotWindow.plot_sub_cat.__doc__)
            plot_w.plot_sub_cat(data)

        elif chart_type == 'Month-wise Sales':
            print(PlotWindow.plot_month_wise.__doc__)
            plot_w.plot_month_wise(data)

        elif chart_type == 'State-wise Sales':
            print(PlotWindow.plot_state_wise.__doc__)
            plot_w.plot_state_wise(data)

        elif chart_type == 'Age-wise Sales':
            print(PlotWindow.plot_age_wise.__doc__)
            plot_w.plot_age_wise(data)

        self.axes.set_facecolor(self.background_color)  # Set background color
        self.canvas.draw()

    def plot_data_prod_cat(self,data):
        """
        Category-wise Sales chart is plotted
        """
        group_data = data.groupby('ProductCategory')['Revenue'].sum()
        labels = group_data.index
        values = group_data.values
        self.axes.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        self.axes.set_title('Category-wise Total Sales', **self.font_style)

    def plot_sub_cat(self,data):
        """
        Sub category-wise Sales Chart is plotted
        """
        bikes_data = data[data['ProductCategory'] == 'Bikes']
        group_data = bikes_data.groupby('Sub Category')['Revenue'].sum()
        labels = group_data.index
        values = group_data.values
        self.axes.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        self.axes.set_title('Sub Category-wise(Bikes) Sales ', **self.font_style)

    def plot_month_wise(self,data):
        """
        Month-wise Sales Chart is plotted
        """
        month_order = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        month_data = data.groupby('Month')['Revenue'].sum()
        month_data = month_data.reindex(month_order)
        month_data.plot(kind='line', ax=self.axes)
        self.axes.set_xlabel('Month', **self.font_style)
        self.axes.set_ylabel('Revenue', **self.font_style)
        self.axes.set_title(' Month-wise Sales', **self.font_style)
        self.figure.tight_layout()  # Adjust layout for better visibility of labels
    def plot_state_wise(self,data):
        """
        State-wise Sales Chart is plotted
        """
        state_data = data.groupby('State')['Revenue'].sum()
        state_data.plot(kind='bar', ax=self.axes)
        self.axes.set_xlabel('State', **self.font_style)
        self.axes.set_ylabel('Revenue', **self.font_style)
        self.axes.set_title(' State-wise Sales', **self.font_style)
        self.axes.tick_params(axis='x', rotation=50)  # Rotate x-axis labels for better visibility

        # Add value labels on top of bars
        for index, value in enumerate(state_data.values):
            self.axes.text(index, value, str(round(value, 2)), ha='center', va='bottom', color='blue')
    def plot_age_wise(self,data):
        """
        Age-wise Sales Chart is plotted
        """
        data['AgeGroup'] = pd.cut(data['Customer Age'], bins=[0, 30, 40, 50, 60, 100],
                                  labels=['<=30', '31-40', '41-50', '51-60', '>=61'])
        age_group_data = data.groupby('AgeGroup')['Revenue'].sum()
        labels = age_group_data.index
        values = age_group_data.values
        self.axes.bar(labels, values)
        self.axes.set_xlabel('Age Group', **self.font_style)
        self.axes.set_ylabel('Sales Revenue', **self.font_style)
        self.axes.set_title('Histogram - Age-wise Sales', **self.font_style)
        self.axes.tick_params(axis='x', rotation=0)  # Rotate x-axis labels if needed

    def clear_plot(self):
        self.axes.clear()
        self.canvas.draw()

def plot_data():
    selected_chart = chart_var.get()
    plot_w.plot_data(selected_chart)


def clear():
    plot_w.clear_plot()

def show_distinct_categories():
    data = pd.read_csv('SalesDL.csv')
    distinct_categories = data['ProductCategory'].unique()
    distinct_categories_text = "\n".join(distinct_categories)
    tk.messagebox.showinfo("Categories", distinct_categories_text)


def show_distinct_subcategories():
    data = pd.read_csv('SalesDL.csv')
    distinct_categories = data['ProductCategory'].unique()
    subcategories_by_category = {}

    for category in distinct_categories:
        subcategories = data[data['ProductCategory'] == category]['Sub Category'].unique()
        subcategories_by_category[category] = subcategories

    message_text = ""
    for category, subcategories in subcategories_by_category.items():
        message_text += f"{category}: \nSubcategories: {', '.join(subcategories)}\n\n"

    tk.messagebox.showinfo("Subcategories", message_text)

def show_summary():
    data = pd.read_csv('SalesDL.csv')
    total_sales = data['Revenue'].sum()
    total_profit = data['Profit'].sum()
    summary_text = f"Total Sales: {total_sales}\nTotal Profit: {total_profit}"
    tk.messagebox.showinfo("Summary", summary_text)


import random

def show_subcategory_sales():
    data = pd.read_csv('SalesDL.csv')

    categories = data['ProductCategory'].unique()

    # Generate random colors for each subcategory
    colors = [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in range(len(categories))]

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 15), dpi=100)

    for i, category in enumerate(categories):
        category_data = data[data['ProductCategory'] == category]
        subcategory_data = category_data.groupby('Sub Category')['Revenue'].sum()

        wedges, _, autopct = axes[i].pie(subcategory_data, labels=subcategory_data.index, autopct='%1.1f%%', startangle=50, colors=colors)

        # Increase label font size and adjust label parameters for better visibility
        plt.setp(autopct, fontsize=10, color='white')

        # Set equal aspect ratio to ensure circular shape
        axes[i].axis('equal')

        axes[i].set_title(f'Contribution of Subcategories to Sales ({category})')


    plt.tight_layout()
    plt.show()


root = tk.Tk()    # Creates the main tkinter window
root.configure(bg='white')   # Set background color of the main window
root.title("Sales Analysis with Charts")   # Main title of the window
mainframe = tk.Frame(root)  # Creates a frame inside the main window to hold the plot.
mainframe.grid(row=0, column=0, sticky="nsew")#  Places the mainframe in the first row and first column of the grid layout within the main window.
print(PlotWindow.plot_data.__doc__)   #Prints the docstring of the plot_data() method, which describes its functionality.
plot_w = PlotWindow(mainframe, (8, 6))

buttonframe = tk.Frame(root, bg="white")  #Creates a frame inside the root window to hold the buttons with a white background.
buttonframe.grid(row=1, column=0, sticky="nsew")  #Places the buttonframe in the second row and first column of the grid layout within the root window.
b1 = tk.Button(buttonframe, text="Plot", command=plot_data)  #Creates a button with the label "Plot" and associates it with the plot_data() function
b1.grid(row=1, column= 1, sticky="nsew")
b2 = tk.Button(buttonframe, text="Clear", command=clear)
b2.grid(row=1, column=2, sticky="nsew")
b3 = tk.Button(buttonframe, text="List of Categories", command=show_distinct_categories)
b3.grid(row=1, column=3, sticky="nsew")
b4 = tk.Button(buttonframe, text="List of Subcategories", command=show_distinct_subcategories)
b4.grid(row=1, column=4, sticky="nsew")
b5 = tk.Button(buttonframe, text="Subcategory Sales", command=show_subcategory_sales)
b5.grid(row=1, column=5, sticky="nsew")
b6 = tk.Button(buttonframe, text="Summary of Sales & Profit", command=show_summary)
b6.grid(row=1, column=6, sticky="nsew")
b7 = tk.Button(buttonframe, text="Close", command=root.quit)
b7.grid(row=1, column=8, sticky="nsew")


# Dropdown menu to select chart type
chart_types = ['Month-wise Sales', 'State-wise Sales', 'Age-wise Sales','Category-wise Total Sales', 'Sub Category-wise(Bikes) Sales']
chart_var = tk.StringVar(root)
chart_var.set(chart_types[0])
chart_dropdown = tk.OptionMenu(buttonframe, chart_var, *chart_types)
chart_dropdown.grid(row=1, column=7, sticky="nsew")

root.mainloop()

