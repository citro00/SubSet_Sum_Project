import tkinter as tk
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa la GUI dal modulo frontend
from frontend.sub_set_sum_gui import SubsetSumGUI

if __name__ == "__main__":
    root = tk.Tk()
    gui = SubsetSumGUI(root)
    root.mainloop()
