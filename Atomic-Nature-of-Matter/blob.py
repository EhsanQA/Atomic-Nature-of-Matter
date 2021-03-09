import sys


class Blob:

    # First, we define an object. The Blob.

    def __init__(self):
        """
        We defines Blob's attributes.

        """
        # Blob has 2 attributes: 1.Its coordinates 2.Its mass(which is
        # equal to the number of pixels it has.)
        # the frames are in 2 dimensions so the coordinate of the Blob
        # has X-coordinate and the Y-coordinate.
        # And the coordinates of the Blob is the mean value of the
        # X-coordinate and Y-coordinate of the pixels that are in the Blob.

        self.x_coor = 0.0
        self.y_coor = 0.0
        self.pixel_counter = 0

    def add(self, i, j):
        """
        Takes the pixel coordinate that will be added to the blob (i,j)
        and adds it to Blob.
        Then adds one to the mass of the Blob.
        """

        # To recalculate the coordinate of the Blob after adding a new pixel to it,
        # we use the mean value formula. We imagine that before adding the new pixel,
        # All the other pixels had the same coordinate,So to recalculate the new coordinate,
        # We use the 'Weighted Mean' formula.
        # We simply multiply the X-coordinate and the Y-coordinate of the Blob by the number of
        # pixels it had before, and add the X-coordinate of the new pixel and the Y-coordinate of it.
        # And at the end, we divide them by the 'NEW' number of pixels (the number of pixels it had + 1).

        self.x_coor = ((self.x_coor * self.pixel_counter) + i) / (1 + self.pixel_counter)
        self.y_coor = ((self.y_coor * self.pixel_counter) + j) / (1 + self.pixel_counter)
        self.pixel_counter += 1

    def mass(self):
        """
        Takes the number of pixels the Blob has and,
        returns it as the mass of the Blob.

        """

        return self.pixel_counter

    def distanceTo(self, another_blob):
        """
        Takes the coordinates of another Blob and,
        returns the distance between the current Blob,
        and the other one.
        """
        # Using the Pythagoras's theorem to calculate the distance between Blobs.
        dx = self.x_coor - another_blob.x_coor
        dy = self.y_coor - another_blob.y_coor

        d = (dx ** 2 + dy ** 2) ** 0.5

        return d

    def str(self):
        """
        Returns the mass of the Blob
        and the coordinate of it.

        """

        return '%d (%.4f, %.4f)' % (self.pixel_counter, self.x_coor, self.y_coor)


def main():
    """
    Prints the mass of the Blob, the coordinate of the Blob
    (After adding the coordinate of a pixel that will be added to the Blob)
    using the str function,
    and the distance between two Blobs
    (by giving it the coordinate of another Blob).

    """
    blob = Blob()  # Defining the object 'blob' as a Blob
    # So now, it's an empty Blob with no mass
    x_new = float(sys.argv[1])  # Taking the coordinate of the new pixel
    y_new = float(sys.argv[2])  # from the command line.

    blob.add(x_new, y_new)  # Adding the new pixel to the Blob.

    blob2 = Blob()  # Defining another Blob, 'blob2' which we will calculate the
    # distance between 'blob' and 'blob2', using the 'distanceTo' function.

    blob2.x_coor = float(sys.argv[3])  # taking the coordinate of 'blob2' from
    blob2.y_coor = float(sys.argv[4])  # commandline.

    str_of_the_blob = blob.str()  # Using the 'str' function to print the mass
    # and the coordinate of 'blob'.

    distance = blob.distanceTo(blob2)  # Calculating the distance of the two Blobs
    # ('blob' and 'blob2').

    print(str_of_the_blob)
    print('%.4f' % distance)    # Printing the 'distance' with 4-digit accuracy.


if __name__ == '__main__':
    main()
