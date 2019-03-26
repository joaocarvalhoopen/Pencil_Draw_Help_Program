###############################################################################
# Name:   Pencil Draw Help Program                                            #
# Author: Joao Nuno Carvalho                                                  #
# Email:  joaonunocarv@gmail.com                                              #
# Date:   2019.03.25                                                          #
# Description: This program takes a color or gray photo, transforms it into   #
#              gray. Then expands the dynamic range to occupy all the 0 to    #
#              255 value range. Then asks the user for the number of          #
#              independent values, or tones and subdivide the image into      #
#              different tones. It then shows them in a cumulative order, sow #
#              that the user builds value or tone at each cumulative slice.   #
# License: MIT Open source                                                    #
# Python version: Python 3.7                                                  #
# Libs used: Pillow a derivate from the lib PIL                               #
###############################################################################

from PIL import Image, ImageDraw

def show_and_save_image(image_in, grid_on, grid_number, path, filename):
    image_out = image_in
    if grid_on:
        # Draw grid.
        image = PencilImage(image_in)
        image.draw_grid(grid_number)
        image_out = image.get_img()
    image_out.show(title=filename)   # The title doesn't work on Windows 10.
    image_out.save(path + filename)

def apply_change_to_gray(pixel_in, param_1 = None, param_2 = None):
    # pixel_in is a tuple (R, G, B) each value is an int 0-255 .
    # It returns a pixel tuple.
    pixel_grey_val = ( pixel_in[0] + pixel_in[1] + pixel_in[2] ) / 3
    pixel_grey_val = int( pixel_grey_val )
                     #  R Red           G  Green       B Blue
    pixel_out = (pixel_grey_val, pixel_grey_val, pixel_grey_val)
    return pixel_out

def apply_change_expand_dynamic_range(pixel_in, param_1 = None, param_2 = None):
    # pixel_in is a tuple (R, G, B) each value is an int 0-255 .
    # It returns a pixel tuple.
    min = param_1
    max = param_2
    # Enforce that the image is gray.
    assert(pixel_in[0]==pixel_in[1] and pixel_in[1]==pixel_in[2])
    pixel_grey_val = pixel_in[0]
    pixel_grey_val = ((pixel_grey_val - min) / max) * 255
    pixel_grey_val = int( pixel_grey_val )
                     #  R Red           G  Green       B Blue
    pixel_out = (pixel_grey_val, pixel_grey_val, pixel_grey_val)
    return pixel_out


class PencilImage:

    def __init__(self, img_in, num_gray_tones = 6):
        self.__img = img_in.copy()
        self.__max_col = self.__img.size[0]
        self.__max_row = self.__img.size[1]
        self.__pixels = self.__img.load() # create the pixel map
        self.__min = -1
        self.__max = -1
        self.__num_gray_tones = num_gray_tones
        self.__delta = int(255 / self.__num_gray_tones) 
        self.__current_tone = 1

    def get_img(self):
        return self.__img

    def get_max_col(self):
        return self.__max_col

    def get_max_row(self):
        return self.__max_row

    def get_num_gray_tones(self):
        return self.__num_gray_tones

    def get_info_str(self):
        return     f" max_col = {self.__max_col}\n"  \
                 + f" max_row = {self.__max_row}\n"  \
                 + f" max_min = {self.__min}\n"      \
                 + f" max_max = {self.__max}\n"

    def set_num_gray_tones(self, num_gray_tones):
        self.__num_gray_tones = num_gray_tones
        self.__delta = int(255 / self.__num_gray_tones) 

    def apply_to_img_change(self, func_to_apply, param_1 = None, param_2 = None):
        for i in range(self.__max_col):    # for every col:
            for j in range(self.__max_row):    # For every row
                pixel_tmp_in = self.__pixels[i, j]
                pixel_tmp_out = func_to_apply(pixel_tmp_in, param_1, param_2)
                self.__pixels[i, j] = pixel_tmp_out

    def get_min_max(self):
        # Process only gray scale pictures.
        min = 255
        max = 0
        for i in range(self.__max_col):    # for every col:
            for j in range(self.__max_row):    # For every row
                pixel_tmp = self.__pixels[i, j]
                # Just to enforce that the image is a grey image.
                assert(pixel_tmp[0]==pixel_tmp[1] and pixel_tmp[1]==pixel_tmp[2])
                if pixel_tmp[0] > max:
                    max = pixel_tmp[0]
                if pixel_tmp[0] < min:
                    min = pixel_tmp[0]
        return (min, max)         

    def expand_dynamic_range(self):
        # Change the image to gray scale.
        self.apply_to_img_change(apply_change_to_gray)
        # Get min max value.
        self.__min, self.__max = self.get_min_max()
        # Expand dynamic range.
        self.apply_to_img_change(apply_change_expand_dynamic_range, self.__min, self.__max)

    def __generate_image_all_cases_tone(self, min_tone=None, unique_tone=None):
        tone_bins = self.__num_gray_tones

        img_out = self.__img.copy()
        pixels = img_out.load()
        for i in range(self.__max_col):    # for every col:
            for j in range(self.__max_row):    # For every row
                pixel_in = pixels[i, j]
                assert(pixel_in[0]==pixel_in[1] and pixel_in[1]==pixel_in[2])
                gray_value = pixel_in[0]
                # Inverts the list. ex:  7, 6, 5, 4, 3, 2, 1, 0 for num_tones = 8
                lst_tones = list(range(tone_bins - 1, -1, -1))                
                for tone_num in lst_tones:
                    tone_val = tone_num * self.__delta 

                    # Cumulative case upper then max_tone                    
                    if min_tone != None:
                        if tone_num < min_tone:
                            tone_out = (min_tone + 1) * self.__delta
                            pixel_val = (tone_out, tone_out, tone_out)
                            pixels[i, j] = pixel_val
                            break

                    # All tones case.
                    if gray_value > tone_val:
                        # tone_out = (tone_num - 1) * self.__delta
                        tone_out = tone_num * self.__delta
                                   # R         G         B
                        pixel = (tone_out, tone_out, tone_out)
                        
                        # Unique tone case.
                        if unique_tone != None:
                            if tone_num == unique_tone:
                                pixels[i, j] = pixel
                            else:
                                pixels[i, j] = (255, 255, 255)    # White    
                            break
                        # All tones case.    
                        pixels[i, j] = pixel
                        break

        return img_out

    def generate_image_only_one_tone(self, num_tone):
        return self.__generate_image_all_cases_tone(min_tone=None, unique_tone=num_tone)

    # The cumulative algorithm doesn't work, use the cumulative overlay. 
    def generate_image_cumulative_tone(self, min_tone):
        return self.__generate_image_all_cases_tone(min_tone=min_tone, unique_tone=None)

    def generate_image_final_tone_bins(self):
        return self.__generate_image_all_cases_tone(min_tone=None, unique_tone=None)

    def generate_image_cumulative_overlay(self, img_all_tones, min_tone):        
        # img_out_all_tones = pencil_img.generate_image_final_tone_bins()
        # img_out_all_tones.show()

        img_out = img_all_tones.copy()
        img_one_tone = self.generate_image_only_one_tone(num_tone=min_tone)  # 6 -> 0

        pixels_out = img_out.load()
        pixels_one_tone = img_one_tone.load()
        
        for i in range(self.__max_col):    # for every col:
            for j in range(self.__max_row):    # For every row
                pixel_one_tone = pixels_one_tone[i, j]
                if pixel_one_tone[0] < 255:  # if it isn't white.
                    pixel_output = (0, 255, 0)   # Green pixel.
                    pixels_out[i, j] = pixel_output

        return img_out

    def draw_grid(self, grid_number):
        # Calc grid lines position.
        delta_col = int(self.__max_col / grid_number)     # ex: 4
        lst_col = [delta_col * n for n in range(1, grid_number)]
        delta_row = int(self.__max_row / grid_number)     # ex: 4
        lst_row = [delta_row * n for n in range(1, grid_number)] 
        # Draw the grid lines.
        draw = ImageDraw.Draw(self.__img, mode="RGB")
        for point_col in lst_col:
            draw.line([point_col, 0, point_col, self.__max_row], fill=(0, 0, 255), width=1)   # fill RGB, blue
        for point_row in lst_row:
            draw.line([0, point_row, self.__max_col, point_row], fill=(0, 0, 255), width=1)   # fill RGB, blue


class Index:

    def __init__(self):
        self.__index = -1

    def next(self):
        self.__index += 1
        return self.__index


if __name__ == "__main__":
    
    # Configurations.
    path_in        = ".//images_in//"
    path_out       = ".//images_out//"
    file_image_in  = "lena-color.jpg"
    # This number is the number of different tones you can make
    # with graphite, inclusing the white.
    num_gray_tones = 8
    grid_on        = True  # True / False
    grid_number    = 4     # Grid num_col = num_row.                 
    

    # Execution.
    file_main = file_image_in[ : -4]  # ex: "lena-color"
    ext = ".png"
    index_a = Index()

    img_in = Image.open(path_in + file_image_in)
    filename_out = file_main + f"_{index_a.next():02d}_original" + ext
    show_and_save_image(img_in, grid_on, grid_number, path_out, filename=filename_out)
    
    pencil_img = PencilImage(img_in, num_gray_tones=num_gray_tones)
    pencil_img.expand_dynamic_range()

    info_str = pencil_img.get_info_str()
    print(info_str)

    img_out = pencil_img.get_img()
    filename_out = file_main + f"_{index_a.next():02d}_expanded_range" + ext
    show_and_save_image(img_out, grid_on, grid_number, path_out, filename=filename_out)
    
    img_out_all_tones = pencil_img.generate_image_final_tone_bins()
    filename_out = file_main + f"_{index_a.next():02d}_all_tones" + ext 
    show_and_save_image(img_out_all_tones, grid_on, grid_number, path_out, filename=filename_out)
    
    # For tone number = 8, and it draws the tones 6, 5, 4, 3, 2, 1, 0   (From lighter to darker)
    index_b = Index()
    for tone_i in range(pencil_img.get_num_gray_tones() - 2, -1, -1):
        img_out_one_tone = pencil_img.generate_image_only_one_tone(num_tone = tone_i)
        filename_out = file_main + f"_{index_a.next():02d}_one_tone_{index_b.next():02d}_" + ext 
        show_and_save_image(img_out_one_tone, grid_on, grid_number, path_out, filename=filename_out)
        
    # img_overlay = pencil_img.generate_image_cumulative_overlay(img_out_all_tones, min_tone = 6)
    # img_overlay.show()    

    # Shows all overlays.
    # For tone number = 8, and it draws the tones 6, 5, 4, 3, 2, 1, 0   (From lighter to darker)
    index_b = Index()
    for tone_i in range(pencil_img.get_num_gray_tones() - 2, -1, -1):
        img_overlay = pencil_img.generate_image_cumulative_overlay(img_out_all_tones, min_tone = tone_i)
        filename_out = file_main + f"_{index_a.next():02d}_overlay_{index_b.next():02d}_" + ext 
        show_and_save_image(img_overlay, grid_on, grid_number, path_out, filename=filename_out)
        

    # Tests...

    # img_out.save("lena_processada.png")

    # img_out_one_tone = pencil_img.generate_image_only_one_tone(num_tone = 6)
    # img_out_one_tone.show("tone: " + str(6))

    # img_out_one_tone = pencil_img.generate_image_only_one_tone(num_tone = 5)
    # img_out_one_tone.show("tone: " + str(5))

    # img_out_one_tone = pencil_img.generate_image_only_one_tone(num_tone = 4)
    # img_out_one_tone.show("tone: " + str(4))

    # img_out_one_tone = pencil_img.generate_image_only_one_tone(num_tone = 3)
    # img_out_one_tone.show("tone: " + str(3))

    # img_out_one_tone = pencil_img.generate_image_only_one_tone(num_tone = 2)
    # img_out_one_tone.show("tone: " + str(2))

    # img_out_one_tone = pencil_img.generate_image_only_one_tone(num_tone = 1)
    # img_out_one_tone.show("tone: " + str(1))

    # img_out_one_tone = pencil_img.generate_image_only_one_tone(num_tone = 0)
    # img_out_one_tone.show("tone: " + str(0))




