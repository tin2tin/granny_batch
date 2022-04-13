# Granny Batch
Batch convert a folder of fbx into a new folder of granny friendly fbx files.

## Location
Find the options of the add-on in the sidebar of the 3D View.

## Important:
Please ensure that paths are absolute, by opening the sidebar of the File Browser and uncheck Relative Path. 

![alt text](https://github.com/tin2tin/granny_batch/blob/main/GrannyBatch.png?raw=true)

## What it does:
- The script will open each fbx files in a folder into a new scene.
- Place all objects centered(while keeping offsets) on grid. 
- Add an empty with the name of the fbx file.
- Parent the 3d objects to the empty.
- Save the scene to the output path as fbx.
- Close the new scene.
- Repeat.
