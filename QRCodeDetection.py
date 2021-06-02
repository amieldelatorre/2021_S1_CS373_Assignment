
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


def contrast_stretch(pixel_array, image_width, image_height):
    pass


def mean_smoothing(pixel_array, image_width, image_height):
    pass


def main():
    filename = "./images/covid19QRCode/poster1small.png"

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)

    greyscale_pixel_array = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    horizontal_sobel_array = computeHorizontalEdgesSobel(greyscale_pixel_array, image_width, image_height)
    vertical_sobel_array = computeVerticalEdgesSobel(greyscale_pixel_array, image_width, image_height)
    edge_magnitude = get_edge_magnitude(horizontal_sobel_array, vertical_sobel_array, image_width, image_height)

    pyplot.imshow(edge_magnitude, cmap="gray")

    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    rect = Rectangle( (10, 30), 70, 50, linewidth=3, edgecolor='g', facecolor='none' )
    # paint the rectangle over the current plot
    axes.add_patch(rect)

    # plot the current figure
    pyplot.show()


if __name__ == "__main__":
    main()
