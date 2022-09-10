import random

class Helper:
    """
    Helper class providing additional utilities
    """

    def randomize():
        """
        Method to generate random RGB intensities

        Returns:
            list: list of random RGB floats
        """

        rand_clrs = []
        for i in range(0,3):
            n = round(random.uniform(0, 1), 5)
            rand_clrs.append(n)
            print(rand_clrs)
        return rand_clrs