import tkinter as tk
from tkinter import filedialog
import utils
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataProcessingGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Data Preprocessing Tool")
        self.window.geometry("1200x700")
        self.window.resizable(False, False)

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_command(label="Export Data", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)

        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="About", command=self.show_about)

        self.data = None
        self.selected_transform_column = None

        self.top_frame  = tk.Frame(self.window, height=100, bg="lightgrey")
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        self.graph_frame = tk.Frame(self.window, bg="white")
        self.graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_frame = tk.Frame(self.window, height=150, bg="lightgray")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.create_controls()
        self.create_graphs()

    def show_about(self):
        about_window = tk.Toplevel(self.window)
        about_window.title("About")
        about_window.resizable(False, False)
        
        about_text = """
        Data Preprocessing Tool

        A tool for visualizing and transforming data.

        Created by Daniel Stefanian
        github.com/Dn-Stef"""
        
        label = tk.Label(about_window, text=about_text, padx=20, pady=20, justify="left")
        label.pack()
        
        about_window.update()
        about_window.geometry(f"280x{label.winfo_reqheight() + 20}")

    def run(self):
        self.window.mainloop()
    
    def import_data(self):
        file_path = filedialog.askopenfilename(
        title="Select a data file",
        filetypes=[("All supported files", "*.csv *.xlsx"), ("CSV files", "*.csv"), ("Excel files", "*.xlsx")],
        )
        
        if file_path:
            try:
                self.data = utils.import_data(file_path)
                print(f"Loaded data with columns: {list(self.data.columns)}")
                self.update_column_dropdowns()
            except Exception as e:
                print(f"Error loading file: {e}")
    def export_data(self):
        pass # Placeholder for export data functionality
    
    def create_controls(self):
        tk.Label(self.top_frame, text="Transform Column:", bg="lightgray").grid(row=0, column=0, padx=10, pady=5    , sticky="w")
        
        self.transform_column_var = tk.StringVar()
        self.transform_column_dropdown = tk.OptionMenu(self.top_frame, self.transform_column_var, "")
        self.transform_column_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(self.top_frame, text="Apply Transformation:", bg="lightgray", font=("Arial", 9, "bold")).grid(row=1, column=0, columnspan=2, pady=2, sticky="w", padx=5)
        
        tk.Button(self.top_frame, text="Normalize", command=lambda: self.apply_transform("normalize"), width=12).grid(row=2, column=0, padx=5, pady=2, sticky="ew")
        tk.Button(self.top_frame, text="Standardize", command=lambda: self.apply_transform("standardize"), width=12).grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(self.top_frame, text="Min-Max", command=lambda: self.apply_transform("min_max"), width=12).grid(row=2, column=2, padx=5, pady=2, sticky="ew")
        tk.Button(self.top_frame, text="Log", command=lambda: self.apply_transform("log"), width=12).grid(row=2, column=3, padx=5, pady=2, sticky="ew")
        
        tk.Button(self.top_frame, text="Sqrt", command=lambda: self.apply_transform("sqrt"), width=12).grid(row=3, column=0, padx=5, pady=2, sticky="ew")
        tk.Button(self.top_frame, text="Inverse", command=lambda: self.apply_transform("inverse"), width=12).grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        tk.Button(self.top_frame, text="Exp", command=lambda: self.apply_transform("exp"), width=12).grid(row=3, column=2, padx=5, pady=2, sticky="ew")
        
        tk.Label(self.top_frame, text="Left Graph:", bg="lightgray", font=("Arial", 10, "bold")).grid(row=0, column=8, padx=20, pady=5)
        
        self.left_x_var = tk.StringVar()
        self.left_y_var = tk.StringVar()
        
        tk.Label(self.top_frame, text="X:", bg="lightgray").grid(row=1, column=8, padx=5, pady=5)
        self.left_x_dropdown = tk.OptionMenu(self.top_frame, self.left_x_var, "")
        self.left_x_dropdown.grid(row=1, column=9, padx=5, pady=5)
        
        tk.Label(self.top_frame, text="Y:", bg="lightgray").grid(row=2, column=8, padx=5, pady=5)
        self.left_y_dropdown = tk.OptionMenu(self.top_frame, self.left_y_var, "")
        self.left_y_dropdown.grid(row=2, column=9, padx=5, pady=5)
        

        tk.Label(self.top_frame, text="Right Graph:", bg="lightgray", font=("Arial", 10, "bold")).grid(row=0, column=10, padx=20, pady=5)
        
        self.right_x_var = tk.StringVar()
        self.right_y_var = tk.StringVar()
        
        tk.Label(self.top_frame, text="X:", bg="lightgray").grid(row=1, column=10, padx=5, pady=5)
        self.right_x_dropdown = tk.OptionMenu(self.top_frame, self.right_x_var, "")
        self.right_x_dropdown.grid(row=1, column=11, padx=5, pady=5)
        
        tk.Label(self.top_frame, text="Y:", bg="lightgray").grid(row=2, column=10, padx=5, pady=5)
        self.right_y_dropdown = tk.OptionMenu(self.top_frame, self.right_y_var, "")
        self.right_y_dropdown.grid(row=2, column=11, padx=5, pady=5)

    def update_column_dropdowns(self):
        if self.data is not None:
            columns = ["Index"] + list(self.data.columns)
            
            menu = self.transform_column_dropdown['menu']
            menu.delete(0, 'end')
            for col in self.data.columns:
                menu.add_command(label=col, command=lambda c=col: self.transform_column_var.set(c))
            self.transform_column_var.set(self.data.columns[0])
            
            self.update_dropdown(self.left_x_dropdown, self.left_x_var, columns, self.update_plots)
            self.update_dropdown(self.left_y_dropdown, self.left_y_var, columns, self.update_plots)
            
            self.update_dropdown(self.right_x_dropdown, self.right_x_var, columns, self.update_plots)
            self.update_dropdown(self.right_y_dropdown, self.right_y_var, columns, self.update_plots)
            
            self.update_plots()

    def update_dropdown(self, dropdown, var, options, callback=None):
        menu = dropdown['menu']
        menu.delete(0, 'end')
        for option in options:
            menu.add_command(label=option, command=lambda o=option: [var.set(o), callback() if callback else None])
        var.set(options[0])

    def create_graphs(self): 
        self.fig = Figure(figsize=(12, 5))
        self.ax_left = self.fig.add_subplot(121)
        self.ax_right = self.fig.add_subplot(122)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.ax_left.set_title("Left Graph")
        self.ax_right.set_title("Right Graph")
        self.canvas.draw()

    def update_plots(self):
        if self.data is None:
            print("No data loaded")
            return
        
        self.ax_left.clear()
        self.ax_right.clear()
        
        left_x = self.left_x_var.get()
        left_y = self.left_y_var.get()
        right_x = self.right_x_var.get()
        right_y = self.right_y_var.get()
        
        x_data_left = self.data.index if left_x == "Index" else self.data[left_x]
        y_data_left = self.data.index if left_y == "Index" else self.data[left_y]
        self.ax_left.plot(x_data_left, y_data_left)
        self.ax_left.set_xlabel(left_x)
        self.ax_left.set_ylabel(left_y)
        self.ax_left.set_title("Left Graph")
        
        x_data_right = self.data.index if right_x == "Index" else self.data[right_x]
        y_data_right = self.data.index if right_y == "Index" else self.data[right_y]
        self.ax_right.plot(x_data_right, y_data_right)
        self.ax_right.set_xlabel(right_x)
        self.ax_right.set_ylabel(right_y)
        self.ax_right.set_title("Right Graph")
        
        self.canvas.draw()

    