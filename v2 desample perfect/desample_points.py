import os
import laspy
import numpy as np
import PySimpleGUI as sg

def desample_points(input_file, output_file, sample_fraction=0.25):
    # Check if the input file exists before attempting to read it.
    if not os.path.exists(input_file):
        sg.popup_error("Error: Input file does not exist", f"{input_file}")
        return

    # Read the input .laz file
    try:
        lp = laspy.read(input_file)
    except Exception as e:
        sg.popup_error("Error reading file", f"{e}")
        return

    total_points = len(lp.points)
    if total_points == 0:
        sg.popup_error("Input file contains no points.")
        return

    # Calculate the number of points to sample.
    sample_size = int(total_points * sample_fraction)
    
    # Select indices evenly distributed across the entire dataset.
    indices = np.linspace(0, total_points - 1, sample_size).astype(int)
    
    # Extract the sampled points.
    sampled_points = lp.points[indices]
    
    # Create a new LAS data object and then copy header's scale and offset.
    try:
        new_las = laspy.create(
            point_format=lp.header.point_format,
            file_version=lp.header.version
        )
        # Preserve the scale and offset settings.
        new_las.header.scales = lp.header.scales
        new_las.header.offsets = lp.header.offsets
        # Assign the sampled points to the new LAS object.
        new_las.points = sampled_points
        new_las.write(output_file, do_compress=True)
        sg.popup("Desampling Complete", f"Saved {sample_size} points to {output_file}.")
    except Exception as e:
        sg.popup_error("Error writing output file", f"{e}")