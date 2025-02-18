import os
import PySimpleGUI as sg
from desample_points import desample_points

def main():
    layout = [
        [sg.Text("Select Source .laz File:"), sg.Input(key="-SOURCE-"), 
         sg.FileBrowse(file_types=(("LAZ Files", "*.laz"),))],
        [sg.Text("Select Output .laz File:"), sg.Input(key="-OUTPUT-"), 
         sg.FileSaveAs(file_types=(("LAZ Files", "*.laz"),))],
        [sg.Text("Sample Fraction (default 0.25):"), sg.Input(default_text="0.25", key="-FRACTION-")],
        [sg.Button("Run Desample"), sg.Button("Exit")]
    ]
    
    window = sg.Window("Desample Points", layout, finalize=True)
    
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        if event == "Run Desample":
            input_file = values["-SOURCE-"]
            output_file = values["-OUTPUT-"]
            try:
                sample_fraction = float(values["-FRACTION-"])
            except Exception as e:
                sg.popup_error("Invalid sample fraction", str(e))
                continue

            if not input_file or not os.path.exists(input_file):
                sg.popup_error("Please select a valid source .laz file.")
                continue

            if not output_file:
                sg.popup_error("Please select a valid output file.")
                continue

            desample_points(input_file, output_file, sample_fraction)
    
    window.close()

if __name__ == "__main__":
    main()