import tkinter as tk
from tkinter import filedialog, messagebox
import utils
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import transformations

class DataProcessingGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Data Preprocessing Tool")
        self.window.geometry("1200x700")
        self.center_window()
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
        self.create_stats_display()

    def show_about(self):
        about_window = tk.Toplevel(self.window)
        about_window.title("About")
        about_window.resizable(False, False)
        
        about_text = """
        Data Preprocessing Tool

        A tool for visualizing and transforming data.

        Created by Daniel Stefanian
        github.com/dn-stef"""
        
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
        if self.data is None:
            messagebox.showwarning("No Data", "No data to export.  Please load data first.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.xlsx'):
                    utils.export_data(self.data, file_path, file_type='xlsx')
                    messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
                elif file_path.endswith('.csv'):
                    utils.export_data(self.data, file_path, file_type='csv')
                    messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
                else:
                    messagebox.showerror("Invalid Format", "Please save as . csv or .xlsx only.")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
    
    def create_controls(self):
        tk.Label(self.top_frame, text="Transform Column:", bg="lightgray").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.transform_column_var = tk.StringVar()
        self.transform_column_dropdown = tk.OptionMenu(self.top_frame, self.transform_column_var, "")
        self.transform_column_dropdown.config(width=15)
        self.transform_column_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(self.top_frame, text="Apply Transformation:", bg="lightgray", font=("Arial", 9, "bold")).grid(row=0, column=2, columnspan=3, pady=5, sticky="w", padx=20)
        
        tk.Button(self.top_frame, text="Standardize", command=lambda: self.apply_transform("standardize"), width=10).grid(row=1, column=2, padx=3, pady=2)
        tk.Button(self.top_frame, text="Min-Max", command=lambda: self.apply_transform("min_max"), width=10).grid(row=1, column=3, padx=3, pady=2)
        tk.Button(self.top_frame, text="Log", command=lambda: self.apply_transform("log"), width=10).grid(row=1, column=4, padx=3, pady=2)
        
        tk.Button(self.top_frame, text="Sqrt", command=lambda: self.apply_transform("sqrt"), width=10).grid(row=2, column=2, padx=3, pady=2)
        tk.Button(self.top_frame, text="Inverse", command=lambda: self.apply_transform("inverse"), width=10).grid(row=2, column=3, padx=3, pady=2)
        tk.Button(self.top_frame, text="Exp", command=lambda: self.apply_transform("exp"), width=10).grid(row=2, column=4, padx=3, pady=2)
        
        tk.Label(self.top_frame, text="Left Graph:", bg="lightgray", font=("Arial", 9, "bold")).grid(row=0, column=6, padx=15, sticky="w")
        tk.Label(self.top_frame, text="X:", bg="lightgray").grid(row=1, column=6, padx=(15,2), sticky="e")
        self.left_x_var = tk.StringVar()
        self.left_x_dropdown = tk.OptionMenu(self.top_frame, self.left_x_var, "")
        self.left_x_dropdown.config(width=10)
        self.left_x_dropdown.grid(row=1, column=7, padx=2)
        
        tk.Label(self.top_frame, text="Y:", bg="lightgray").grid(row=2, column=6, padx=(15,2), sticky="e")
        self.left_y_var = tk.StringVar()
        self.left_y_dropdown = tk.OptionMenu(self.top_frame, self.left_y_var, "")
        self.left_y_dropdown.config(width=10)
        self.left_y_dropdown.grid(row=2, column=7, padx=2)
        
        tk.Label(self.top_frame, text="Right Graph:", bg="lightgray", font=("Arial", 9, "bold")).grid(row=0, column=8, padx=15, sticky="w")
        tk.Label(self.top_frame, text="X:", bg="lightgray").grid(row=1, column=8, padx=(15,2), sticky="e")
        self.right_x_var = tk.StringVar()
        self.right_x_dropdown = tk.OptionMenu(self.top_frame, self.right_x_var, "")
        self.right_x_dropdown.config(width=10)
        self.right_x_dropdown.grid(row=1, column=9, padx=2)
        
        tk.Label(self.top_frame, text="Y:", bg="lightgray").grid(row=2, column=8, padx=(15,2), sticky="e")
        self.right_y_var = tk.StringVar()
        self.right_y_dropdown = tk.OptionMenu(self.top_frame, self.right_y_var, "")
        self.right_y_dropdown.config(width=10)
        self.right_y_dropdown.grid(row=2, column=9, padx=2)

    def update_column_dropdowns(self):
        if self.data is not None:
            columns = ["Index"] + list(self.data.columns)
            
            if not hasattr(self, 'original_columns'):
                self.original_columns = list(self.data.columns)

            menu = self.transform_column_dropdown['menu']
            menu.delete(0, 'end')
            for col in self.original_columns:
                menu.add_command(label=col, command=lambda c=col: self.transform_column_var.set(c))
            self.transform_column_var.set(self.original_columns[0])
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

        if left_y != "Index":
            left_stats = utils.get_statistics(y_data_left)
            for key, value in left_stats.items():
                if isinstance(value, (int, float)):
                    self.left_stats_labels[key].config(text=f"{key}: {value:.3f}")
                else:
                    self.left_stats_labels[key].config(text=f"{key}: {value}")
        else:
            for key in self.left_stats_labels:
                self.left_stats_labels[key].config(text=f"{key}: N/A")

        if right_y != "Index":
            right_stats = utils. get_statistics(y_data_right)
            for key, value in right_stats.items():
                if isinstance(value, (int, float)):
                    self.right_stats_labels[key].config(text=f"{key}: {value:.3f}")
                else:
                    self.right_stats_labels[key].config(text=f"{key}: {value}")
        else:
            for key in self. right_stats_labels:
                self.right_stats_labels[key].config(text=f"{key}: N/A")

    def update_graph_dropdowns_only(self):
        columns = ["Index"] + list(self.data.columns)

        left_x_current = self.left_x_var.get()
        left_y_current = self.left_y_var.get()
        right_x_current = self.right_x_var.get()
        right_y_current = self.right_y_var.get()
        
        self.update_dropdown(self.left_x_dropdown, self.left_x_var, columns, self.update_plots)
        self.update_dropdown(self.left_y_dropdown, self.left_y_var, columns, self.update_plots)
        self.update_dropdown(self.right_x_dropdown, self.right_x_var, columns, self.update_plots)
        self.update_dropdown(self.right_y_dropdown, self.right_y_var, columns, self.update_plots)
        
        if left_x_current in columns:
            self.left_x_var.set(left_x_current)
        if left_y_current in columns:
            self.left_y_var.set(left_y_current)
        if right_x_current in columns:
            self.right_x_var.set(right_x_current)
        if right_y_current in columns:
            self.right_y_var.set(right_y_current)
    
    def apply_transform(self, transform_type):
    
        if self.data is None:
            print("No data loaded")
            return
        
        selected_col = self.transform_column_var.get()
        if not selected_col:
            print("No column selected")
            return
        
        try:
            column_data = self.data[selected_col]
            
            if transform_type == "standardize":
                transformed = transformations.standardization(column_data)
                new_col_name = f"{selected_col}_standardized"
            elif transform_type == "min_max":
                transformed = transformations.min_max_scale(column_data)
                new_col_name = f"{selected_col}_minmax"
            elif transform_type == "log":
                transformed = transformations.log_transform(column_data)
                new_col_name = f"{selected_col}_log"
            elif transform_type == "sqrt":
                transformed = transformations.square_root_transform(column_data)
                new_col_name = f"{selected_col}_sqrt"
            elif transform_type == "inverse":
                transformed = transformations.inverse_transform(column_data)
                new_col_name = f"{selected_col}_inverse"
            elif transform_type == "exp":
                transformed = transformations.exponential_transform(column_data)
                new_col_name = f"{selected_col}_exp"
            
            self.data[new_col_name] = transformed
            
            self.update_graph_dropdowns_only()
            
            print(f"Applied {transform_type} to {selected_col} -> {new_col_name}")
            
        except ValueError as e:
            messagebox.showerror("Transformation Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", str(e))

    def center_window(self):
        self.window.update_idletasks()
        
        window_width = 1200
        window_height = 700
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_stats_display(self):
        tk.Label(self.bottom_frame, text="Left Graph Statistics:", bg="lightgray", font=("Arial", 10, "bold")).place(relx=0.25, y=5, anchor="center")
        
        self.left_stats_frame = tk.Frame(self.bottom_frame, bg="lightgray")
        self.left_stats_frame.place(relx=0.25, y=30, anchor="n")
        
        self.left_stats_labels = {}
        stats_keys = ['Count', 'Mean', 'Median', 'Mode', 'Std', 'Min', 'Max', 'Range']
        for i, key in enumerate(stats_keys):
            row = i // 3
            col = i % 3
            label = tk.Label(self.left_stats_frame, text=f"{key}: N/A", bg="lightgray", font=("Arial", 9), width=15, anchor="w")
            label.grid(row=row, column=col, padx=5, pady=2)
            self.left_stats_labels[key] = label
        
        tk.Label(self.bottom_frame, text="Right Graph Statistics:", bg="lightgray", font=("Arial", 10, "bold")).place(relx=0.75, y=5, anchor="center")
        
        self.right_stats_frame = tk.Frame(self.bottom_frame, bg="lightgray")
        self.right_stats_frame.place(relx=0.75, y=30, anchor="n")
        
        self.right_stats_labels = {}
        for i, key in enumerate(stats_keys):
            row = i // 3
            col = i % 3
            label = tk.Label(self.right_stats_frame, text=f"{key}: N/A", bg="lightgray", font=("Arial", 9), width=15, anchor="w")
            label.grid(row=row, column=col, padx=5, pady=2)
            self.right_stats_labels[key] = label