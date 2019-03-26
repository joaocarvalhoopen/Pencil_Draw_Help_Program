# Pencil Draw Help Program
This is a program to help artists who draw with pencil from colored photos (graphite / charcoal / sanguine). The technique used is tone building. <br>

## License
MIT open source

## Description
* This program takes a color or gray photo, transforms it into gray. 
* Then expands the dynamic range of the photo to occupy all the 0 to 255 value range. 
* Then asks the user for the number of independent values or tones and subdivide the image into different tones.
* It then shows them in a cumulative order, so that the user builds value or tone at each cumulative slice.
* At each image the user knows what regions have the same value or tone.
* You have the option to overlay a grid to all images and to choose the number of columns/rows.
* In all the process the program opens the images in windows and save them to files.

## Installation
Install Python Anaconda version 3.7 or greater. <br>
Install the Pillow library. <br>

## Configuration for each image processing.
Config the following variables:<br>

```
    # Configurations.
    path_in        = ".//images_in//"
    path_out       = ".//images_out//"
    file_image_in  = "lena-color.jpg"
    num_gray_tones = 8
    grid_on        = True  # True / False
    grid_number    = 4     # Grid num_col = num_row.          
```

## Example of images generated.
![Original input image](/images_in/lena-color.jpg)

![Expanded dynamic range image](/images_out/lena-color_01_expanded_range.png)

![All tones image, discrete value tones](/images_out/lena-color_02_all_tones.png)

![One tone image, discrete tone 0](/images_out/lena-color_03_one_tone_00_.png)

![One tone image, discrete tone 1](/images_out/lena-color_04_one_tone_01_.png)

![One tone image, discrete tone 2](/images_out/lena-color_05_one_tone_02_.png)

![One tone image, discrete tone 3](/images_out/lena-color_06_one_tone_03_.png)

![One tone image, discrete tone 4](/images_out/lena-color_07_one_tone_04_.png)

![One tone image, discrete tone 5](/images_out/lena-color_08_one_tone_05_.png)

![One tone image, discrete tone 6](/images_out/lena-color_09_one_tone_06_.png)

![Tone 0 overlay to the expanded dynamic image](/images_out/lena-color_10_overlay_00_.png)

![Tone 1 overlay to the expanded dynamic image](/images_out/lena-color_11_overlay_01_.png)

![Tone 2 overlay to the expanded dynamic image](/images_out/lena-color_12_overlay_02_.png)

![Tone 3 overlay to the expanded dynamic image](/images_out/lena-color_13_overlay_03_.png)

![Tone 4 overlay to the expanded dynamic image](/images_out/lena-color_14_overlay_04_.png)

![Tone 5 overlay to the expanded dynamic image](/images_out/lena-color_15_overlay_05_.png)

![Tone 6 overlay to the expanded dynamic image](/images_out/lena-color_16_overlay_06_.png)


<br>
Note: This program was tested on Windows but it should also work on Linux and MAC, but i didn't tested. <br>
<br>
Have fun! <br>


