import math
import stdio


def main():
    """
    Takes 'distances' of the experiment and
    prints Boltzmann number and Avogadro number.
    """
    n_counter = 0  # number of 'distances'

    r2s = 0
    # We define the sum of squared 'r's as r2s.
    while True:
        # For every loop, we add one 'r' and recalculate the Variance
        n_counter += 1  # When we add one 'r', the n_counter adds 1

        r = stdio.readFloat()  # Reading the 'r's.

        r = r * 0.175 * (10 ** -6)  # 'r's are all in pixels, but all formulas are for meters;
        # so we convert distance in pixels to distance in meters by multiplying the 'r' by:
        # 0.175 x 10^-6
        var = (r ** 2 + r2s) / (2 * n_counter)
        # Using the variance formula (var = (sum of squared 'x's and 'y's)/(2 x n)) and
        # as (sum of squared 'x's and 'y's) = (sum of squared 'r's) we multiply the new 'r'
        # by itself and then add it to sum of the rest of squared 'r's (r2s).
        # finally we divide them by double the number of 'r's.
        r2s += r ** 2
        # As we want to use calculate Variance with the next 'r's,
        # we add the squared 'r' to 'r2s'.

        if stdio.isEmpty():  # The program will stay in this loop until
            # all of the 'r's are given and the final Variance is calculated
            # (Until there aren't any 'r's left)
            break

    D = var  # As 'Variance = 2 x D x delta(t)' ,and delta(t) = 0.5 s

    k = (D * 6 * math.pi * (9.135 * (10 ** -4)) * (0.5 * (10 ** -6))) / 297
    # Using 'Stokes-Einstein equation' and given values to calculate k (Boltzmann constant).

    avg = 8.31446 / k  # As 'k = R/Na' and R = 8.31466 to find Avogadro's number.

    print('Boltzmann = ' + '%4.4e' % k)  # Finally printing the Boltzmann Constant (k)
    # and Avogadro's number with 4 digit accuracy.
    print('Avogadro = ' + '%4.4e' % avg)


if __name__ == '__main__':
    main()
