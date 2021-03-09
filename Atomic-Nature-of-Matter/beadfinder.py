from blob import Blob
import sys
import stdarray
from picture import Picture


class BeadFinder:

    def __init__(self, picture, tau):
        """
        Defining BeadFinder's attributes.
        """
        self.blobs = []  # We will use this empty array to find blobs from pixels.
        self.tau = float(tau)  # tau is the minimum amount that the red,
        # the blue, and the green component of the pixel should have in order to
        # consider that pixel as a pixel of a Blob
        # (because the pictures that are given to us are noisy and we need to differentiate the
        # noise from the actual blobs).
        self.w = picture.width()  # the width of the given picture.
        self.h = picture.height()  # the height of the given picture.

    def Noise_Remover(self, pic):
        """
        Takes the noisy picture
        and returns a 2 dimensional matrix (array) with
        number of cols: the width of the picture and
        number of rows: the height of the picture
        that every element of the matrix is a pixel,
        and that element is 1 if the the color components
        of the pixel is larger than the tau.
        And that element is 0 if color components of the pixel is lower than the tau.
        """
        all_pixels = stdarray.create2D(self.w, self.h, 0)  # This is the matrix that its elements are the pixels.

        for col in range(self.w):  # Here we are checking to see for every pixel in the picture,
            for row in range(self.h):  # if its color component is larger or lower than tau
                the_pixel_color = pic.get(col, row)  # And here we use the p.get() function in
                # the Picture module, and we set 'the_pixel_color_'
                # as the color of the pixel.

                if the_pixel_color.getRed() > self.tau:  # As in a Black & White picture, the red component,
                    # the green component, and the blue component of a pixel
                    # are equal (because if they aren't, then the pixel
                    # will have more red, green, or blue color more and
                    # won't be black & white).
                    # But in our case the picture is not completely black & white
                    # but we can ignore that difference, because the red, green,
                    # or the blue components are really close to each other in this.
                    # So we only need to check the red component of the pixel
                    # and that is enough for this comparison (we could use green
                    # or blue component of the pixel too, because they are really
                    # close to each other).
                    all_pixels[col][row] = 1  # Now we set the same element in that matrix:1 .
                    # We converted the noisy picture with pixels larger than
                    # tau into a matrix which the pixels that their color component
                    # is larger than tau are marked as '1' .
        return all_pixels

    def BlobCollector(self, all_pixels):  # Now that we have the picture converted into a matrix
        # we just need to identify the elements in the matrix that are 1
        # and connected to each other (are neighbours) and
        # differentiate them from other pixels.
        # Then we call those pixels: Blob
        """
        Takes the BLOBS matrix and uses
        the 'thePixelCounter' function and
        adds all the blobs to an array.
        """
        for i in range(self.w):  # Here we look for all the elements in the matrix that
            for j in range(self.h):  # are 1.
                pixel = Blob()  # We define every element as a Blob.
                if all_pixels[i][j] == 1:  # And if that element is 1, then
                    self.thePixelCounter(i, j, all_pixels, pixel)  # we look for its neighbour elements
                    # using the 'thePixelCounter' which
                    # counts the pixels of the Blob.
                    if pixel.mass() > 0:  # if the Blob's mass (pixels) are not 0
                        self.blobs += [pixel]  # Then we add that Blob into the array that
                        # we created before (the Blob's array).
                        # And the elements of the array are Objects.
                        # We cannot print them, because we cannot
                        # print Objects. But we can print one of their
                        # attributes. Such as its mass or coordinate.

    def thePixelCounter(self, i, j, all_pixels, pixel):
        """
        Takes the matrix, the element of the matrix,and the column and row of the matrix and
        checks for its neighbours and if they are 0 or
        have been counted as a Blob's pixel (they are 2) then it adds the elements that have been
        marked as 2 to the blob array.
        (it checks if the neighbour element exists or not too)

        """
        if (all_pixels[i][j] == 2) or i < 0 or j < 0 or i >= self.w - 1 or j >= self.h - 1 or (all_pixels[i][j] == 0):
            return
        # This function is a 'Returning Function' and it marks the elements that are 1: 2.
        # And it does this for all the neighbour elements of the matrix.
        # So our matrix now has 3 numbers in it: 0, 1, and 2
        # 0 means that this element (pixel) is not a Blob's pixel and WILL NOT BE
        # (because it's color component was not higher than tau and the element is considered
        # as a noise).
        # 1 means that this element is not a Blob's pixel but it will be.
        # The neighbours of the 1-element that are 1 and the element itself will be counted,
        # marked as 2 ,and be added to an element in the blobs array we created earlier.
        # 2 means that this element is blob's pixel, is counted ,and is added to the blob.
        all_pixels[i][j] += 1

        pixel.add(i, j)  # It adds the pixel to the same element as its neighbours in the blob array.

        self.thePixelCounter(i - 1, j, all_pixels, pixel)  # Does this operation for its neighbours.
        self.thePixelCounter(i + 1, j, all_pixels, pixel)  # The upper element, the bottom element,
        self.thePixelCounter(i, j + 1, all_pixels, pixel)  # the right element, and the left element.
        self.thePixelCounter(i, j - 1, all_pixels, pixel)

    def GetBeads(self, min_pixels):
        """
        Takes the minimum pixels that is needed a blob to
        be a bead and returns the beads.

        """
        beads = []  # Creates an empty array that the elements of this array
        # will be blobs that their mass is larger than 'min_pixels' (The elements will be beads).

        for blob in self.blobs:  # Here, it looks for the Blobs in the array
            # we created and put the blobs in it.
            if blob.mass() >= min_pixels:
                beads += [blob]  # And adds the blob that its mass is larger than 'min_pixels'
                # to the 'beads' array we created in this function earlier.

        return beads


def main():
    """
    Takes minimum pixels that are needed for a blob to be
    a bead, the tau, and the picture as commandline arguments
    and prints the list of beads.

    """
    min_pixels = int(sys.argv[1])
    tau = float(sys.argv[2])
    pic = Picture(sys.argv[3])
    b = BeadFinder(pic, tau)  # First we define b as BeadFinder.
    all_pixels = b.Noise_Remover(pic)  # Find the BLOBS matrix.
    b.BlobCollector(all_pixels)  # Use the BlobCollector function to find blobs.
    beads = b.GetBeads(min_pixels)  # And find beads using GetBeads function.
    for bead in beads:
        print(bead.str())  # At the end, we print the mass and the coordinate of the
        # elements in the beads array using the str function in blob.py


if __name__ == '__main__':
    main()
