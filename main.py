# Written by Michael Langdon, 2022
# This program uses a genetic algorithm to find a solution to the Travelling Salesman Problem.
# To run it just set the parameters in start_the_process (in the main function) and wait for
# it to finish.  If you want to stop it early and get the result so far, just press Ctl-C or
# use the "stop" button in your IDE.  The parameters you can set are:
# population_size, crossover_rate=0.7, mutation_rate=0.0384, convergence_delta=0
# The default crossover_rate of 0.7 was taken from various papers suggesting it a good value.
# The default mutation_rate of 0.0384 was taken from a paper suggesting using 1/C as the ideal
#          mutation rate, where C=the size of the largest chromosome.
# The default value of convergence_delta of 0 is if you want absolute convergence.  It might take
#          a really, really long time to get that, so change this value to something around 500
#          or so.  It represents the difference between the best value and the average value.

import random

# Dictionary for the city codes.
cities = {
    0: "Barstow",
    1: "Carlsbad",
    2: "Eureka",
    3: "Fresno",
    4: "Lake Tahoe, So.",
    5: "Las Vegas",
    6: "Long Beach",
    7: "Los Angeles",
    8: "Merced",
    9: "Modesto",
    10: "Monterey",
    11: "Oakland",
    12: "Palm Springs",
    13: "Redding",
    14: "Sacramento",
    15: "San Bernardino",
    16: "San Diego",
    17: "San Francisco",
    18: "San Jose",
    19: "San Luis Obispo",
    20: "Santa Barbara",
    21: "San Cruz",
    22: "Santa Rosa",
    23: "Sequoia Park",
    24: "Stockton",
    25: "Yosemite"
}
# Dictionary containing distances between cities.
distances = {
    "-1_0": 129,  # Bakersfield to Barstow
    "-1_1": 206,  # Bakersfield to Carlsbad
    "-1_2": 569,  # Bakersfield to Eureka
    "-1_3": 107,  # Bakersfield to Fresno
    "-1_4": 360,  # Bakersfield to Lake Tahoe, So.
    "-1_5": 284,  # Bakersfield to Las Vegas
    "-1_6": 144,  # Bakersfield to Long Beach
    "-1_7": 115,  # Bakersfield to Los Angeles
    "-1_8": 162,  # Bakersfield to Merced
    "-1_9": 200,  # Bakersfield to Modesto
    "-1_10": 231,  # Bakersfield to Monterey
    "-1_11": 288,  # Bakersfield to Oakland
    "-1_12": 226,  # Bakersfield to Palm Springs
    "-1_13": 436,  # Bakersfield to Redding
    "-1_14": 272,  # Bakersfield to Sacramento
    "-1_15": 174,  # Bakersfield to San Bernardino
    "-1_16": 231,  # Bakersfield to San Diego
    "-1_17": 297,  # Bakersfield to San Francisco
    "-1_18": 252,  # Bakersfield to San Jose
    "-1_19": 118,  # Bakersfield to San Luis Obispo
    "-1_20": 146,  # Bakersfield to Santa Barbara
    "-1_21": 258,  # Bakersfield to San Cruz
    "-1_22": 347,  # Bakersfield to Santa Rosa
    "-1_23": 121,  # Bakersfield to Sequoia Park
    "-1_24": 227,  # Bakersfield to Stockton
    "-1_25": 200,  # Bakersfield to Yosemite
    #  --------------------------------------
    "0_1": 153,  # Barstow to Carlsbad
    "0_2": 696,  # Barstow to Eureka
    "0_3": 236,  # Barstow to Fresno
    "0_4": 395,  # Barstow to Lake Tahoe, So.
    "0_5": 155,  # Barstow to Las Vegas
    "0_6": 139,  # Barstow to Long Beach
    "0_7": 130,  # Barstow to Los Angeles
    "0_8": 291,  # Barstow to Merced
    "0_9": 329,  # Barstow to Modesto
    "0_10": 360,  # Barstow to Monterey
    "0_11": 417,  # Barstow to Oakland
    "0_12": 123,  # Barstow to Palm Springs
    "0_13": 565,  # Barstow to Redding
    "0_14": 401,  # Barstow to Sacramento
    "0_15": 71,  # Barstow to San Bernardino
    "0_16": 176,  # Barstow to San Diego
    "0_17": 426,  # Barstow to San Francisco
    "0_18": 381,  # Barstow to San Jose
    "0_19": 247,  # Barstow to San Luis Obispo
    "0_20": 225,  # Barstow to Santa Barbara
    "0_21": 387,  # Barstow to San Cruz
    "0_22": 476,  # Barstow to Santa Rosa
    "0_23": 250,  # Barstow to Sequoia Park
    "0_24": 356,  # Barstow to Stockton
    "0_25": 329,  # Barstow to Yosemite
    #  --------------------------------------
    "1_2": 777,  # Carlsbad to Eureka
    "1_3": 315,  # Carlsbad to Fresno
    "1_4": 780,  # Carlsbad to Lake Tahoe, So.
    "1_5": 312,  # Carlsbad to Las Vegas
    "1_6": 82,  # Carlsbad to Long Beach
    "1_7": 93,  # Carlsbad to Los Angeles
    "1_8": 370,  # Carlsbad to Merced
    "1_9": 406,  # Carlsbad to Modesto
    "1_10": 428,  # Carlsbad to Monterey
    "1_11": 496,  # Carlsbad to Oakland
    "1_12": 116,  # Carlsbad to Palm Springs
    "1_13": 644,  # Carlsbad to Redding
    "1_14": 480,  # Carlsbad to Sacramento
    "1_15": 827,  # Carlsbad to San Bernardino
    "1_16": 23,  # Carlsbad to San Diego
    "1_17": 505,  # Carlsbad to San Francisco
    "1_18": 460,  # Carlsbad to San Jose
    "1_19": 293,  # Carlsbad to San Luis Obispo
    "1_20": 188,  # Carlsbad to Santa Barbara
    "1_21": 466,  # Carlsbad to San Cruz
    "1_22": 565,  # Carlsbad to Santa Rosa
    "1_23": 329,  # Carlsbad to Sequoia Park
    "1_24": 435,  # Carlsbad to Stockton
    "1_25": 408,  # Carlsbad to Yosemite
    #  -----------------------------------------
    "2_3": 462,  # Eureka to Fresno
    "2_4": 398,  # Eureka to Lake Tahoe, So.
    "2_5": 797,  # Eureka to Las Vegas
    "2_6": 713,  # Eureka to Long Beach
    "2_7": 694,  # Eureka to Los Angeles
    "2_8": 407,  # Eureka to Merced
    "2_9": 369,  # Eureka to Modesto
    "2_10": 388,  # Eureka to Monterey
    "2_11": 291,  # Eureka to Oakland
    "2_12": 795,  # Eureka to Palm Springs
    "2_13": 150,  # Eureka to Redding
    "2_14": 314,  # Eureka to Sacramento
    "2_15": 43,  # Eureka to San Bernardino (that can't be right!)
    "2_16": 800,  # Eureka to San Diego
    "2_17": 272,  # Eureka to San Francisco
    "2_18": 317,  # Eureka to San Jose
    "2_19": 504,  # Eureka to San Luis Obispo
    "2_20": 609,  # Eureka to Santa Barbara
    "2_21": 349,  # Eureka to San Cruz
    "2_22": 222,  # Eureka to Santa Rosa
    "2_23": 544,  # Eureka to Sequoia Park
    "2_24": 356,  # Eureka to Stockton
    "2_25": 488,  # Eureka to Yosemite
    #  ---------------------------------------
    "3_4": 388,  # Fresno to Lake Tahoe, So.
    "3_5": 408,  # Fresno to Las Vegas
    "3_6": 251,  # Fresno to Long Beach
    "3_7": 222,  # Fresno to Los Angeles
    "3_8": 55,  # Fresno to Merced
    "3_9": 93,  # Fresno to Modesto
    "3_10": 152,  # Fresno to Monterey
    "3_11": 181,  # Fresno to Oakland
    "3_12": 333,  # Fresno to Palm Springs
    "3_13": 329,  # Fresno to Redding
    "3_14": 185,  # Fresno to Sacramento
    "3_15": 281,  # Fresno to San Bernardino
    "3_16": 338,  # Fresno to San Diego
    "3_17": 190,  # Fresno to San Francisco
    "3_18": 145,  # Fresno to San Jose
    "3_19": 137,  # Fresno to San Luis Obispo
    "3_20": 242,  # Fresno to Santa Barbara
    "3_21": 151,  # Fresno to San Cruz
    "3_22": 240,  # Fresno to Santa Rosa
    "3_23": 82,  # Fresno to Sequoia Park
    "3_24": 120,  # Fresno to Stockton
    "3_25": 93,  # Fresno to Yosemite
    #  -----------------------------------------
    "4_5": 466,  # Lake Tahoe, So. to Las Vegas
    "4_6": 479,  # Lake Tahoe, So. to Long Beach
    "4_7": 456,  # Lake Tahoe, So. to Los Angeles
    "4_8": 194,  # Lake Tahoe, So. to Merced
    "4_9": 156,  # Lake Tahoe, So. to Modesto
    "4_10": 266,  # Lake Tahoe, So. to Monterey
    "4_11": 195,  # Lake Tahoe, So. to Oakland
    "4_12": 435,  # Lake Tahoe, So. to Palm Springs
    "4_13": 249,  # Lake Tahoe, So. to Redding
    "4_14": 107,  # Lake Tahoe, So. to Sacramento
    "4_15": 436,  # Lake Tahoe, So. to San Bernardino
    "4_16": 542,  # Lake Tahoe, So. to San Diego
    "4_17": 192,  # Lake Tahoe, So. to San Francisco
    "4_18": 197,  # Lake Tahoe, So. to San Jose
    "4_19": 197,  # Lake Tahoe, So. to San Luis Obispo
    "4_20": 492,  # Lake Tahoe, So. to Santa Barbara
    "4_21": 229,  # Lake Tahoe, So. to San Cruz
    "4_22": 199,  # Lake Tahoe, So. to Santa Rosa
    "4_23": 335,  # Lake Tahoe, So. to Sequoia Park
    "4_24": 131,  # Lake Tahoe, So. to Stockton
    "4_25": 133,  # Lake Tahoe, So. to Yosemite
    #  -------------------------------------------
    "5_6": 314,  # Las Vegas to Long Beach
    "5_7": 302,  # Las Vegas to Los Angeles
    "5_8": 446,  # Las Vegas to Merced
    "5_9": 484,  # Las Vegas to Modesto
    "5_10": 504,  # Las Vegas to Monterey
    "5_11": 567,  # Las Vegas to Oakland
    "5_12": 276,  # Las Vegas to Palm Springs
    "5_13": 640,  # Las Vegas to Redding
    "5_14": 587,  # Las Vegas to Sacramento
    "5_15": 228,  # Las Vegas to San Bernardino
    "5_16": 332,  # Las Vegas to San Diego
    "5_17": 568,  # Las Vegas to San Francisco
    "5_18": 524,  # Las Vegas to San Jose
    "5_19": 414,  # Las Vegas to San Luis Obispo
    "5_20": 354,  # Las Vegas to Santa Barbara
    "5_21": 524,  # Las Vegas to San Cruz
    "5_22": 610,  # Las Vegas to Santa Rosa
    "5_23": 408,  # Las Vegas to Sequoia Park
    "5_24": 510,  # Las Vegas to Stockton
    "5_25": 435,  # Las Vegas to Yosemite
    #  ---------------------------------------------
    "6_7": 29,  # Long Beach to Los Angeles
    "6_8": 306,  # Long Beach to Merced
    "6_9": 344,  # Long Beach to Modesto
    "6_10": 364,  # Long Beach to Monterey
    "6_11": 432,  # Long Beach to Oakland
    "6_12": 112,  # Long Beach to Palm Springs
    "6_13": 580,  # Long Beach to Redding
    "6_14": 416,  # Long Beach to Sacramento
    "6_15": 68,  # Long Beach to San Bernardino
    "6_16": 105,  # Long Beach to San Diego
    "6_17": 441,  # Long Beach to San Francisco
    "6_18": 396,  # Long Beach to San Jose
    "6_19": 229,  # Long Beach to San Luis Obispo
    "6_20": 124,  # Long Beach to Santa Barbara
    "6_21": 402,  # Long Beach to San Cruz
    "6_22": 491,  # Long Beach to Santa Rosa
    "6_23": 265,  # Long Beach to Sequoia Park
    "6_24": 371,  # Long Beach to Stockton
    "6_25": 344,  # Long Beach to Yosemite
    #  -----------------------------------------------
    "7_8": 277,  # Los Angeles to Merced
    "7_9": 315,  # Los Angeles to Modesto
    "7_10": 335,  # Los Angeles to Monterey
    "7_11": 403,  # Los Angeles to Oakland
    "7_12": 111,  # Los Angeles to Palm Springs
    "7_13": 551,  # Los Angeles to Redding
    "7_14": 387,  # Los Angeles to Sacramento
    "7_15": 59,  # Los Angeles to San Bernardino
    "7_16": 116,  # Los Angeles to San Diego
    "7_17": 412,  # Los Angeles to San Francisco
    "7_18": 367,  # Los Angeles to San Jose
    "7_19": 200,  # Los Angeles to San Luis Obispo
    "7_20": 95,  # Los Angeles to Santa Barbara
    "7_21": 373,  # Los Angeles to San Cruz
    "7_22": 462,  # Los Angeles to Santa Rosa
    "7_23": 236,  # Los Angeles to Sequoia Park
    "7_24": 342,  # Los Angeles to Stockton
    "7_25": 315,  # Los Angeles to Yosemite
    #  ------------------------------------------------
    "8_9": 37,  # Merced to Modesto
    "8_10": 118,  # Merced to Monterey
    "8_11": 126,  # Merced to Oakland
    "8_12": 388,  # Merced to Palm Springs
    "8_13": 274,  # Merced to Redding
    "8_14": 110,  # Merced to Sacramento
    "8_15": 336,  # Merced to San Bernardino
    "8_16": 393,  # Merced to San Diego
    "8_17": 135,  # Merced to San Francisco
    "8_18": 114,  # Merced to San Jose
    "8_19": 192,  # Merced to San Luis Obispo
    "8_20": 297,  # Merced to Santa Barbara
    "8_21": 118,  # Merced to San Cruz
    "8_22": 185,  # Merced to Santa Rosa
    "8_23": 137,  # Merced to Sequoia Park
    "8_24": 65,  # Merced to Stockton
    "8_25": 81,  # Merced to Yosemite
    #  -------------------------------------------------
    "9_10": 153,  # Modesto to Monterey
    "9_11": 88,  # Modesto to Oakland
    "9_12": 426,  # Modesto to Palm Springs
    "9_13": 236,  # Modesto to Redding
    "9_14": 72,  # Modesto to Sacramento
    "9_15": 374,  # Modesto to San Bernardino
    "9_16": 431,  # Modesto to San Diego
    "9_17": 97,  # Modesto to San Francisco
    "9_18": 82,  # Modesto to San Jose
    "9_19": 230,  # Modesto to San Luis Obispo
    "9_20": 335,  # Modesto to Santa Barbara
    "9_21": 114,  # Modesto to San Cruz
    "9_22": 147,  # Modesto to Santa Rosa
    "9_23": 175,  # Modesto to Sequoia Park
    "9_24": 27,  # Modesto to Stockton
    "9_25": 119,  # Modesto to Yosemite
    #  ------------------------------------------------
    "10_11": 111,  # Monterey to Oakland
    "10_12": 446,  # Monterey to Palm Springs
    "10_13": 325,  # Monterey to Redding
    "10_14": 185,  # Monterey to Sacramento
    "10_15": 394,  # Monterey to San Bernardino
    "10_16": 451,  # Monterey to San Diego
    "10_17": 116,  # Monterey to San Francisco
    "10_18": 71,  # Monterey to San Jose
    "10_19": 135,  # Monterey to San Luis Obispo
    "10_20": 240,  # Monterey to Santa Barbara
    "10_21": 45,  # Monterey to San Cruz
    "10_22": 166,  # Monterey to Santa Rosa
    "10_23": 234,  # Monterey to Sequoia Park
    "10_24": 140,  # Monterey to Stockton
    "10_25": 199,  # Monterey to Yosemite
    #  ----------------------------------------------
    "11_12": 514,  # Oakland to Palm Springs
    "11_13": 214,  # Oakland to Redding
    "11_14": 87,  # Oakland to Sacramento
    "11_15": 462,  # Oakland to San Bernardino
    "11_16": 519,  # Oakland to San Diego
    "11_17": 9,  # Oakland to San Francisco
    "11_18": 40,  # Oakland to San Jose
    "11_19": 227,  # Oakland to San Luis Obispo
    "11_20": 332,  # Oakland to Santa Barbara
    "11_21": 72,  # Oakland to San Cruz
    "11_22": 59,  # Oakland to Santa Rosa
    "11_23": 263,  # Oakland to Sequoia Park
    "11_24": 75,  # Oakland to Stockton
    "11_25": 207,  # Oakland to Yosemite
    #  ---------------------------------------------
    "12_13": 682,  # Palm Springs to Redding
    "12_14": 498,  # Palm Springs to Sacramento
    "12_15": 52,  # Palm Springs to San Bernardino
    "12_16": 139,  # Palm Springs to San Diego
    "12_17": 523,  # Palm Springs to San Francisco
    "12_18": 478,  # Palm Springs to San Jose
    "12_19": 311,  # Palm Springs to San Luis Obispo
    "12_20": 206,  # Palm Springs to Santa Barbara
    "12_21": 484,  # Palm Springs to San Cruz
    "12_22": 573,  # Palm Springs to Santa Rosa
    "12_23": 347,  # Palm Springs to Sequoia Park
    "12_24": 453,  # Palm Springs to Stockton
    "12_25": 426,  # Palm Springs to Yosemite
    #  ------------------------------------------------
    "13_14": 164,  # Redding to Sacramento
    "13_15": 610,  # Redding to San Bernardino
    "13_16": 667,  # Redding to San Diego
    "13_17": 223,  # Redding to San Francisco
    "13_18": 254,  # Redding to San Jose
    "13_19": 411,  # Redding to San Luis Obispo
    "13_20": 546,  # Redding to Santa Barbara
    "13_21": 286,  # Redding to San Cruz
    "13_22": 251,  # Redding to Santa Rosa
    "13_23": 411,  # Redding to Sequoia Park
    "13_24": 209,  # Redding to Stockton
    "13_25": 355,  # Redding to Yosemite
    #  -----------------------------------------------
    "14_15": 446,  # Sacramento to San Bernardino
    "14_16": 503,  # Sacramento to San Diego
    "14_17": 87,  # Sacramento to San Francisco
    "14_18": 114,  # Sacramento to San Jose
    "14_19": 301,  # Sacramento to San Luis Obispo
    "14_20": 406,  # Sacramento to Santa Barbara
    "14_21": 146,  # Sacramento to San Cruz
    "14_22": 103,  # Sacramento to Santa Rosa
    "14_23": 247,  # Sacramento to Sequoia Park
    "14_24": 45,  # Sacramento to Stockton
    "14_25": 191,  # Sacramento to Yosemite
    #  -----------------------------------------------
    "15_16": 105,  # San Bernardino to San Diego
    "15_17": 471,  # San Bernardino to San Francisco
    "15_18": 426,  # San Bernardino to San Jose
    "15_19": 259,  # San Bernardino to San Luis Obispo
    "15_20": 254,  # San Bernardino to Santa Barbara
    "15_21": 432,  # San Bernardino to San Cruz
    "15_22": 521,  # San Bernardino to Santa Rosa
    "15_23": 295,  # San Bernardino to Sequoia Park
    "15_24": 401,  # San Bernardino to Stockton
    "15_25": 374,  # San Bernardino to Yosemite
    #  ----------------------------------------------
    "16_17": 528,  # San Diego to San Francisco
    "16_18": 483,  # San Diego to San Jose
    "16_19": 316,  # San Diego to San Luis Obispo
    "16_20": 211,  # San Diego to Santa Barbara
    "16_21": 489,  # San Diego to San Cruz
    "16_22": 578,  # San Diego to Santa Rosa
    "16_23": 352,  # San Diego to Sequoia Park
    "16_24": 458,  # San Diego to Stockton
    "16_25": 431,  # San Diego to Yosemite
    #  ----------------------------------------------
    "17_18": 45,  # San Francisco to San Jose
    "17_19": 232,  # San Francisco to San Luis Obispo
    "17_20": 337,  # San Francisco to Santa Barbara
    "17_21": 77,  # San Francisco to San Cruz
    "17_22": 50,  # San Francisco to Santa Rosa
    "17_23": 272,  # San Francisco to Sequoia Park
    "17_24": 84,  # San Francisco to Stockton
    "17_25": 216,  # San Francisco to Yosemite
    #  ----------------------------------------------
    "18_19": 187,  # San Jose to San Luis Obispo
    "18_20": 292,  # San Jose to Santa Barbara
    "18_21": 32,  # San Jose to San Cruz
    "18_22": 95,  # San Jose to Santa Rosa
    "18_23": 227,  # San Jose to Sequoia Park
    "18_24": 69,  # San Jose to Stockton
    "18_25": 195,  # San Jose to Yosemite
    #  ----------------------------------------------
    "19_20": 105,  # San Luis Obispo to Santa Barbara
    "19_21": 180,  # San Luis Obispo to San Cruz
    "19_22": 282,  # San Luis Obispo to Santa Rosa
    "19_23": 174,  # San Luis Obispo to Sequoia Park
    "19_24": 256,  # San Luis Obispo to Stockton
    "19_25": 230,  # San Luis Obispo to Yosemite
    #  -------------------------------------------------
    "20_21": 285,  # Santa Barbara to San Cruz
    "20_22": 387,  # Santa Barbara to Santa Rosa
    "20_23": 287,  # Santa Barbara to Sequoia Park
    "20_24": 361,  # Santa Barbara to Stockton
    "20_25": 335,  # Santa Barbara to Yosemite
    #  ------------------------------------------------
    "21_22": 127,  # San Cruz to Santa Rosa
    "21_23": 233,  # San Cruz to Sequoia Park
    "21_24": 101,  # San Cruz to Stockton
    "21_25": 199,  # San Cruz to Yosemite
    #  -----------------------------------------------
    "22_23": 322,  # Santa Rosa to Sequoia Park
    "22_24": 134,  # Santa Rosa to Stockton
    "22_25": 266,  # Santa Rosa to Yosemite
    #  ------------------------------------------------
    "23_24": 202,  # Sequoia Park to Stockton
    "23_25": 175,  # Sequoia Park to Yosemite
    #  --------------------------------------------------
    "24_25": 146  # Stockton to Yosemite
}


def initialize_population(city_list, size):
    """
    Initializes the population by creating a list of permutations.

    :param city_list: (list) list of cities, represented by integers
    :param size: (int) the number of chromosomes to create
    :return chromosomes: (list) a list of shuffled lists representing permutations of cities
    """
    chromosomes = []
    for x in range(size):
        # random.sample creates a new list of the specified length.
        chromosomes.append(random.sample(city_list, len(city_list)))
    return chromosomes


def swap_mutate(city_list, city1, city2):
    """
    Mutates a chromosome (a list) by swapping 2 genes (entries).

    :param city_list: (list) list of cities, represented by integers
    :param city1: (int) index into city_list, representing a city
    :param city2: (int) index into city_list, representing a city
    :return city_list:  (list) A new list representing a permutation of cities
    """
    city_list[city1], city_list[city2] = city_list[city2], city_list[city1]
    return city_list


def crossover(city_list1, city_list2):
    """
    Using "Davis' Order 1 crossover" algorithm to recombine/exchange genes, i.e. "mate".
    Keeping it simple by just returning a single child.  Run it again with lists swapped for a 2nd child.

    :param city_list1: (list) list of cities, represented by integers
    :param city_list2: (list) list of cities, represented by integers
    :return child: (list) a new list of cities generated by the parent lists
    """
    # Step 1:  Create two random crossover points in the parent and copy
    #          the segment between them from the first parent (city_list1)
    #          to the child.
    child = city_list1[:]
    # keeping point1 just shy of end of list to have at least one gene in the segment
    point1 = random.randint(0, len(child) - 3)
    # want point2 to be to the right of point1
    point2 = random.randint(point1 + 1, len(child) - 1)

    # Step 2:  Starting from the second crossover point in the second parent,
    #          copy the remaining unused entries from the second parent to the
    #          child, wrapping around the list.
    child_index = parent2_index = (point2 + 1) % len(child)

    while child_index != point1:    # when child_index==point1 we have returned to the parent1 segment
        if city_list2[parent2_index] not in city_list1[point1:point2 + 1]:
            child[child_index] = city_list2[parent2_index]
            child_index = (child_index + 1) % len(child)
        parent2_index = (parent2_index + 1) % len(city_list2)  # it doesn't matter which list to use for len()
    return child


# This selects for LONGEST paths.  Not used, wrote it for fun.
def selection_roulette(list_of_city_lists):
    """
    Selection of next generation via the Roulette Wheel method, in which the
    probability of selection is proportional to the fitness of the individual
    relative to the fitness of the entire population.  p(i) = f(i)/(f(1) +...+ f(n))

    :param list_of_city_lists: (list) the current generation of chromosomes
    :return next_generation: (list) a new list of lists of cities, representing different paths.
    """
    number_of_chromosomes = len(list_of_city_lists)
    # stores the total distance of each path
    path_distances = []
    for path in list_of_city_lists:
        path_distances.append(calculate_fitness(path))
    sum_of_distances = sum(path_distances)

    # calculate selection probabilities for each path
    selection_probs = []
    for path_distance in path_distances:
        selection_probs.append(path_distance / sum_of_distances)

    # generate the next generation by "spinning" the roulette wheel one time for each chromosome.
    # To clarify for my future self, I'm selecting from list_of_city_lists, using the list of selection_probs
    # as weights for each list, and returning a list of number_of_chromosomes lists.
    next_generation = random.choices(list_of_city_lists, weights=selection_probs, k=number_of_chromosomes)
    return next_generation


def selection_rank_order(list_of_city_lists):
    """
    Selection of next generation via the Rank Order method, in which the best
    individual is ranked n, the worst individual is ranked 1, and the probability
    of selection is f(i) = rank(i)/n(n-1)

    :param list_of_city_lists: (list) the current generation of chromosomes
    :return next_generation: (list) a new list of lists of cities, representing different paths.
    """
    number_of_chromosomes = len(list_of_city_lists)
    # stores the total distance of each path
    path_distances = []
    for path in list_of_city_lists:
        path_distances.append(calculate_fitness(path))
    path_distances.sort(reverse=True)  # descending order, to make rank assignments easier

    # calculate selection probabilities for each path
    denom = number_of_chromosomes * (number_of_chromosomes - 1)
    selection_probs = []
    for rank in range(1, len(path_distances) + 1):
        selection_probs.append(rank / denom)

    # To clarify for my future self, I'm selecting from list_of_city_lists, using the list of selection_probs
    # as weights for each list, and returning a list of number_of_chromosomes lists.
    next_generation = random.choices(list_of_city_lists, weights=selection_probs, k=number_of_chromosomes)

    return next_generation


def calculate_fitness(city_list):
    """
    Takes city_list and calculates the total distance.

    :param city_list: (list) permutation of cities, representing a particular path.
    :return total_distance: (int) represents the total distance for this city_list
    """
    # Initialize starting city to -1, which is Bakersfield (see key at top of file for city codes).
    from_city = -1
    total_distance = 0
    for city in city_list:
        to_city = city
        total_distance += get_distance_from_dict(from_city, to_city)
        from_city = to_city
    # Add distance from final city in list back to starting point, which is Bakersfield (-1).
    total_distance += get_distance_from_dict(city_list[-1], -1)
    return total_distance


def get_distance_from_dict(from_city, to_city):
    """
    Helper function to create keys from parameters, in order to retrieve values from dictionary distances{}.

    :param from_city: (int) number signifying a city (see key at top of file for city codes).
    :param to_city: (int) number signifying a city (see key at top of file for city codes).
    :return distance: (int) distance between from_city and to_city, from dictionary distances{}.
    """
    if from_city < to_city:
        # the dictionary distances{} needs the form "smallerNum_biggerNum"
        dict_key = str(from_city) + "_" + str(to_city)
    else:
        dict_key = str(to_city) + "_" + str(from_city)
    return distances[dict_key]


def start_the_process(population_size, crossover_rate=0.7, mutation_rate=0.0384, convergence_delta=0):
    """
    Runs the genetic algorithm according to the parameters specified.

    :param convergence_delta: (float) hyperparameter to adjust how close to absolute convergence to get.
                                    higher values with speed it up.  Values are miles.
    :param population_size: (int) number of chromosomes (paths between cities) in a generation
    :param crossover_rate: (float) frequency of genetic exchange.  Should be around 0.7
    :param mutation_rate: (float) frequency of mutation.  Should be miniscule: 1/(size of chromosome)=1/26=0.0384
    :return shortest_path: (list) the path with the shortest total distance.
    """
    # generate a seed list to permute
    seed = [*range(26)]
    # population is a list of lists, each list representing a path
    population = initialize_population(city_list=seed, size=population_size)
    generations = 1

    # Check fitness of initial population
    path_distances = []
    for path in population:
        path_distances.append(calculate_fitness(path))
    avg_distance = sum(path_distances) / len(path_distances)

    # convergence is when the difference between the best value and the average is 0 or very small.
    convergence = abs(min(path_distances) - avg_distance)
    # children[] is a list of lists, representing the next generation
    children = []
    shortest_path = []
    shortest_distance = avg_distance  # just to initialize it

    try:
        #  select, crossover, mutate, check fitness until convergence...
        while convergence > convergence_delta:
            # selection
            next_gen = selection_rank_order(population)

            # crossover
            for i in range(0, len(next_gen) - 1, 2):  # need parent pairs, so skip every other
                rand_num = random.random()
                if rand_num < crossover_rate:
                    child1 = (crossover(next_gen[i], next_gen[i + 1]))
                    child2 = (crossover(next_gen[i + 1], next_gen[i]))  # reverse parents for 2nd child

                else:
                    child1 = next_gen[i]
                    child2 = next_gen[i + 1]
                children.append(child1)
                children.append(child2)

            # mutation
            for child in children:
                rand_num = random.random()
                if rand_num < mutation_rate:
                    # randomly pick a city/child to swap with
                    random_city1 = random.randint(0, len(child) - 1)
                    # it's ok if same number is chosen.  want mutation low anyway.
                    random_city2 = random.randint(0, len(child) - 1)
                    child = swap_mutate(child, random_city1, random_city2)

            # copy new population and null out children[]
            population = children[:]
            children = []

            # check fitness of new population
            path_distances = []
            for path in population:
                path_distances.append(calculate_fitness(path))

            shortest_distance = min(path_distances)
            # need the index of min value to get the path from population[]
            shortest_distance_index = path_distances.index(shortest_distance)
            shortest_path = population[shortest_distance_index]

            generations += 1

    except KeyboardInterrupt:  # Press Ctrl-C to terminate while loop
        # check fitness of new population
        path_distances = []
        for path in population:
            path_distances.append(calculate_fitness(path))

        shortest_distance = min(path_distances)
        # need the index of min value to get the path from population[]
        shortest_distance_index = path_distances.index(shortest_distance)
        shortest_path = population[shortest_distance_index]

    print("Number of generations: " + str(generations))
    print("Total distance: " + str(shortest_distance))

    return shortest_path


def print_the_result(city_list):
    print("The shortest path is: ")
    print("Bakersfield")
    for city in city_list:
        # get city name from dictionary cities{}
        city_name = cities[city]
        print(city_name)
    print("Bakersfield")


if __name__ == '__main__':
    # if you don't feel like waiting forever, kill it with Ctl-C or your IDE's stop button,
    # or set the convergence_delta to a higher value.
    print_the_result(start_the_process(population_size=600, convergence_delta=500))

    # Running with population_size=500, convergence_delta=500 and the default mutation and
    # crossover rates, I got a distance of 5730 in 12634 generations.  I stopped it manually
    # after about 5 minutes.  Running on a 2016 MacBook Pro.
