#!/bin/bash

selected_directory=$(zenity  --file-selection --directory --width=475 --height=550 --title="Select the specific directory to make the KSH files." --filename="/home/pmccrone/python/src/CSVMaker/")

# Check if a directory was selected (user didn't click Cancel
if [ -n "$selected_directory" ]; then
        echo $selected_directory
        #echo "You selected: $selected_directory"
	CORRAL=($selected_directory)
else
	echo "No directory selected"
fi

