
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import math
import imageIO.png


def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array


# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)


# This method packs together three individual pixel arrays for r, g and b values into a single array that is fit for
# use in matplotlib's imshow method
def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage
    

# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()


def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)

    # STUDENT CODE HERE

    for height in range(image_height):
        for width in range(image_width):
            g_val = 0.299 * pixel_array_r[height][width] + 0.587 * pixel_array_g[height][width] + 0.114 * pixel_array_b[height][width]
            greyscale_pixel_array[height][width] = round(g_val)

    return greyscale_pixel_array


def computeHorizontalEdgesSobel(pixel_array, image_width, image_height):
    edges = []
    for height in range(image_height):
        row = []
        for width in range(image_width):
            if height == 0 or width == 0 or height == image_height - 1 or width == image_width - 1:
                row.append(0.000)
            else:
                positive_part = pixel_array[height - 1][width - 1] / 8 + pixel_array[height - 1][width] / 4 + \
                                pixel_array[height - 1][width + 1] / 8
                negative_part = pixel_array[height + 1][width - 1] / 8 + pixel_array[height + 1][width] / 4 + \
                                pixel_array[height + 1][width + 1] / 8
                row.append(round(positive_part - negative_part, 3))
        edges.append(row)

    return edges


def computeVerticalEdgesSobel(pixel_array, image_width, image_height):
    edges = []
    for height in range(image_height):
        row = []
        for width in range(image_width):
            if height == 0 or width == 0 or height == image_height - 1 or width == image_width - 1:
                row.append(0.000)
            else:
                negative_part = pixel_array[height - 1][width - 1] / 8 + pixel_array[height][width - 1] / 4 + \
                                pixel_array[height + 1][width - 1] / 8
                positive_part = pixel_array[height - 1][width + 1] / 8 + pixel_array[height][width + 1] / 4 + \
                                pixel_array[height + 1][width + 1] / 8
                row.append(round(positive_part - negative_part, 3))
        edges.append(row)

    return edges


def get_edge_magnitude(horizontal_sobel_array, vertical_sobel_array, image_width, image_height):
    edge_magnitude = createInitializedGreyscalePixelArray(image_width, image_height)

    for height in range(image_height):
        for width in range(image_width):
            edge_magnitude[height][width] = math.sqrt(math.pow(horizontal_sobel_array[height][width], 2) + math.pow(vertical_sobel_array[height][width], 2))

    return edge_magnitude


def computeBoxAveraging3x3(pixel_array, image_width, image_height):
    edges = []
    for height in range(image_height):
        row = []
        for width in range(image_width):
            sum = 0
            if height == 0 or width == 0 or height == image_height - 1 or width == image_width - 1:
                row.append(0.000)
            else:
                sum += pixel_array[height - 1][width - 1]
                sum += pixel_array[height - 1][width]
                sum += pixel_array[height - 1][width + 1]
                sum += pixel_array[height][width - 1]
                sum += pixel_array[height][width]
                sum += pixel_array[height][width + 1]
                sum += pixel_array[height + 1][width - 1]
                sum += pixel_array[height + 1][width]
                sum += pixel_array[height + 1][width + 1]

                row.append(round(sum / 9, 3))
        edges.append(row)

    return edges


def contrast_stretch(pixel_array, image_width, image_height):
    g_max = 255
    g_low = 0

    contrast_stretched_array = createInitializedGreyscalePixelArray(image_width, image_height)

    low_list = []
    high_list = []

    for height in range(image_height):
        low_list.append(min(pixel_array[height]))
        high_list.append(max(pixel_array[height]))

    f_high = max(high_list)
    f_low = min(low_list)

    a = (g_max - g_low) / (f_high - f_low)
    b = g_low - f_low * ((g_max - g_low) / (f_high - f_low))

    for height in range(image_height):
        for width in range(image_width):
            pixel = pixel_array[height][width]

            if pixel < g_low:
                contrast_stretched_array[height][width] = 0
            elif pixel >= g_low and pixel <= g_max:
                contrast_stretched_array[height][width] = a * pixel + b
            elif pixel > g_max:
                contrast_stretched_array[height][width] = 255

    return contrast_stretched_array


def computeThresholdGE(pixel_array, threshold_value, image_width, image_height):
    edges = []

    for height in range(image_height):
        row = []
        for width in range(image_width):
            if pixel_array[height][width] < threshold_value:
                row.append(0)
            else:
                row.append(255)
        edges.append(row)

    return edges


def computeErosion8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    padded_array = createInitializedGreyscalePixelArray(image_width + 2, image_height + 2)
    edges = []

    for height in range(image_height):
        for width in range(image_width):
            padded_array[height + 1][width + 1] = pixel_array[height][width]

    for height in range(1, image_height + 1):
        row = []
        for width in range(1, image_width + 1):
            if padded_array[height - 1][width - 1] >= 1 and padded_array[height - 1][width] >= 1 and \
                    padded_array[height - 1][width + 1] >= 1 and padded_array[height][width - 1] >= 1 and \
                    padded_array[height][width] >= 1 and padded_array[height][width + 1] >= 1 and \
                    padded_array[height + 1][width - 1] >= 1 and padded_array[height + 1][width] >= 1 and \
                    padded_array[height + 1][width + 1] >= 1:
                row.append(1)
            else:
                row.append(0)
        edges.append(row)

    return edges


def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    padded_array = createInitializedGreyscalePixelArray(image_width + 2, image_height + 2)
    edges = []

    for height in range(image_height):
        for width in range(image_width):
            padded_array[height + 1][width + 1] = pixel_array[height][width]

    for height in range(1, image_height + 1):
        row = []
        for width in range(1, image_width + 1):
            if padded_array[height - 1][width - 1] >= 1 or padded_array[height - 1][width] >= 1 or \
                    padded_array[height - 1][width + 1] >= 1 or padded_array[height][width - 1] >= 1 or \
                    padded_array[height][width] >= 1 or padded_array[height][width + 1] >= 1 or \
                    padded_array[height + 1][width - 1] >= 1 or padded_array[height + 1][width] >= 1 or \
                    padded_array[height + 1][width + 1] >= 1:
                row.append(1)
            else:
                row.append(0)
        edges.append(row)

    return edges


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def computeConnectedComponentLabeling(pixel_array, image_width, image_height):
    current_label = 1
    a_dict = {}
    image_array = createInitializedGreyscalePixelArray(image_width, image_height)
    padded_array = createInitializedGreyscalePixelArray(image_width + 1, image_height + 1)
    q = Queue()
    visited = createInitializedGreyscalePixelArray(image_width, image_height)

    for height in range(image_height):
        for width in range(image_width):
            padded_array[height + 1][width + 1] = pixel_array[height][width]

    for height in range(1, image_height + 1):
        for width in range(1, image_width + 1):
            if padded_array[height][width] >= 1 and visited[height][width] == 0:
                q.enqueue((height, width))

                object_num_pixels = 0

                while not q.isEmpty():
                    (h, w) = q.dequeue()
                    object_num_pixels += 1

                    image_array[h - 1][w - 1] = current_label
                    
                    visited[h][w] = 1

                    if padded_array[h][w - 1] >= 1 and visited[h][w - 1] == 0:
                        visited[h][w - 1] = 1
                        q.enqueue((h, w - 1))

                    if padded_array[h][w + 1] >= 1 and visited[h][w + 1] == 0:
                        visited[h][w + 1] = 1
                        q.enqueue((h, w + 1))

                    if padded_array[h - 1][w] >= 1 and visited[h - 1][w] == 0:
                        visited[h - 1][w] = 1
                        q.enqueue((h - 1, w))

                    if padded_array[h + 1][w] >= 1 and visited[h + 1][w] == 0:
                        visited[h + 1][w] = 1
                        q.enqueue((h + 1, w))

                a_dict[current_label] = object_num_pixels
                current_label += 1

    return (image_array, a_dict)


def find_largest_component(pixel_array, component_sizes, image_width, image_height):
    largest_label = 0
    largest_number = 0

    for key in component_sizes.keys():
        if component_sizes[key] > largest_number:
            largest_number = component_sizes[key]
            largest_label = key

    for height in range(image_height):
        for width in range(image_width):
            if pixel_array[height][width] != largest_label:
                pixel_array[height][width] = 0

    return pixel_array


def bounding_box(pixel_array, image_width, image_height):
    min_x = None
    min_y = None
    max_x = 0
    max_y = 0

    for height in range(image_height):
        if min_y is None:
            if max(pixel_array[height]) != 0:
                min_y = height

        if max(pixel_array[height]) != 0 and height > max_y:
            max_y = height

    for width in range(image_width):
        for height in range(image_height):
            if min_x is None and pixel_array[height][width] != 0:
                min_x = width
            elif min_x is not None and width < min_x and pixel_array[height][width] != 0:
                min_x = width

            if pixel_array[height][width] != 0 and width > max_x:
                max_x = width

    return (min_x, min_y, max_x, max_y)


def main():
    filename = "./images/covid19QRCode/poster1small.png"

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)

    greyscale_pixel_array = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    horizontal_sobel_array = computeHorizontalEdgesSobel(greyscale_pixel_array, image_width, image_height)
    vertical_sobel_array = computeVerticalEdgesSobel(greyscale_pixel_array, image_width, image_height)
    edge_magnitude = get_edge_magnitude(horizontal_sobel_array, vertical_sobel_array, image_width, image_height)

    smoothing_repeat = 9
    smoothed_image = edge_magnitude
    while smoothing_repeat != 0:
        smoothed_image = computeBoxAveraging3x3(smoothed_image, image_width, image_height)
        smoothing_repeat -= 1

    contrast_stretched_image = contrast_stretch(smoothed_image, image_width, image_height)

    threshold_value = 70

    binary_image = computeThresholdGE(contrast_stretched_image, threshold_value, image_width, image_height)

    dilation_number = 1
    erosion_number = 1
    dilation_array = binary_image

    while dilation_number != 0:
        dilation_array = computeDilation8Nbh3x3FlatSE(dilation_array, image_width, image_height)
        dilation_number -= 1

    erosion_array = dilation_array

    while erosion_number != 0:
        erosion_array = computeErosion8Nbh3x3FlatSE(erosion_array, image_width, image_height)
        erosion_number -= 1

    (ccimg, ccsizes) = computeConnectedComponentLabeling(erosion_array, image_width, image_height)

    largest_component_array = find_largest_component(ccimg, ccsizes, image_width, image_height)

    (min_x, min_y, max_x, max_y) = bounding_box(largest_component_array, image_width, image_height)

    pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height))

    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    rect = Rectangle((min_x, min_y), max_x - min_x, max_y - min_y, linewidth=3, edgecolor='g', facecolor='none')
    # paint the rectangle over the current plot
    axes.add_patch(rect)

    # plot the current figure
    pyplot.show()


if __name__ == "__main__":
    main()
