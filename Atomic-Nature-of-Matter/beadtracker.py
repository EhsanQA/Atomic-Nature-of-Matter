import sys
import glob
from beadfinder import BeadFinder
from blob import Blob
from picture import Picture

pics = glob.glob('run_1/*.jpg')  # Defining a directory for pictures in run_1 folder


def beadtracer(delta, current_beads, tau, min_pixels):
    """
    Takes delta, current_beads, tau, and min_pixels
    and prints the distance between two beads on each picture
    and the next picture.
    """
    for i in range(1, len(pics)):  # The other pictures start from i = 1 in run_1 folder.
        b2 = BeadFinder(Picture(pics[i]), tau)  # We now do the same things we did in the main()
        all_pixels2 = b2.Noise_Remover(Picture(pics[i]))  # for the next pictures for all the pictures.
        b2.BlobCollector(all_pixels2)
        next_beads = b2.GetBeads(min_pixels)  # Now that we have all the beads from both current_beads
        # and the next_beads, we just need to find the distance that
        # each bead moves in every frame.
        for x in next_beads:  # A bead, when it moves, can get out of the frame or go deeper in the picture,
            # if we just calculate the distance of current picture's bead coordinates
            # and the next one, then we won't be able to calculate it,
            # and the reason for this is that one bead can be removed in the next frame.
            # So the program would calculate the current bead's distance from a bead in
            # the next frame that it is NOT the same one traveling.
            # For example there are 5 beads in the first frame,
            # and 4 in the next one.
            # If we tell the computer to calculate the distance between 1st bead in the
            # first frame and 1st bead in the second frame,
            # and do this for all nth of
            # them (doing this for min(first_frame_beads,second_frame_beads))
            # then for example the 2nd bead in the first frame is disappeared in the
            # second frame then the 3rd bead in the first frame will actually be
            # the 2nd bead in the second frame!
            # The program will measure the distance between the
            # 2nd bead in the first frame AND the 2nd bead in the second frame
            # not knowing that the bead is actually not in the second frame.
            # So there will be 2 options in this,
            # either the distance between them will be more than delta
            # or the distance will be less than delta
            # which in first case, the program will NOT print the distance
            # (which is of course wrong)
            # but in the second case, the program will actually print the distance
            # but the distance is not correct! (as said before)

            minimum_distance = float('inf')  # So we need a better way.
            # Here, we use minimum distance method.
            # We set a variable called 'minimum_distance' to a very large number.
            # (the infinity)
            # Then we calculate every bead's distance in first frame from
            # every bead in the next frame.
            # And we set an 'if' statement checking if the distance in between
            # each bead is lower than the delta given or not.
            # But there can be a potential problem here.
            # A bead in the first frame could be closer than delta to 2 or more beads
            # in the second frame.
            # So to avoid that problem, we find the closest bead for
            # each bead in the first frame.
            # So that if there were more than 1 beads closer than delta to a bead in first frame,
            # the program will choose the closest one and print the distance.
            for y in current_beads:
                d = x.distanceTo(y) # Measuring the distance
                if d < delta and d < minimum_distance:
                    # This is the part where we find the closest bead.
                    # The program picks the first bead in the first frame and then
                    # measures the distance between it and the first bead in the next frame
                    # and then if 'd' is lower than delta then it enters the statement
                    # because 'd' is of course less than infinity;
                    # then the program will set the 'minimum_distance' as 'd'.
                    # Then the program checks the distance of the first bead in first frame
                    # and the second bead in the next frame.
                    # This time if 'd' is lower than the delta,
                    # the program will check if it is closer than the first bead or not.
                    # (d < minimum_distance)
                    # If it is, then it will choose the second bead (temporary) to be the closest bead.
                    # But if it isn't, then the first bead will still be chosen as the closest
                    # bead for the first bead in the first frame.
                    # The program will do it for all the beads in the first frame.
                    minimum_distance = d

            if not (minimum_distance == float('inf')):  # If there was at least one bead closer than delta,
                # the program will print the 'minimum_distance' which is the lowest distance in between beads.
                print('%.4f' % minimum_distance)
        print() # We leave an empty line in between distances of two frames.
        current_beads = next_beads  # Then the program does this operation for every two frames.
        # So we set the 'current_beads' as 'next_beads' so the next operation will be in between
        # second frame and the third frame. Then third and fourth and so on...


def main():
    """
    Takes min_pixels, tau, delta, and the first picture
    from commandline and finds the beads from the first picture using beadfinder,
    and then uses beadtracer function to get the beads from the next picture in commandline,
    then prints the distance of each bead in the first picture from the next picture,
    and does this for all of the pictures in the commandline.
    """
    min_pixels = int(sys.argv[1])
    tau = float(sys.argv[2])
    delta = float(sys.argv[3])
    the_first_pic = Picture(pics[0])
    b = BeadFinder(the_first_pic, tau)  # Defining b as BeadFinder.
    all_pixels = b.Noise_Remover(the_first_pic)  # Using Noise_Remover function in beadfinder
    # to cancel the noise and get the matrix of pixels.
    b.BlobCollector(all_pixels)  # Using BlobCollector function in beadfinder to
    # get all the blobs in an array.
    current_beads = b.GetBeads(min_pixels)  # Getting the beads from the array of blobs with
    # min_pixels.
    beadtracer(delta, current_beads, tau, min_pixels)  # Using the beadtracer function to print the
    # distance between each blob in every frame.


if __name__ == '__main__':
    main()
