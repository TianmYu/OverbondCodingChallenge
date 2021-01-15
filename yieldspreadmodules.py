import csv
import numpy as np

def open_CSV (CSV_path):
    # input: (string, path from CSV file)
    # general purpose function to open and store data from CSV files

    CSV_data = []
    with open (CSV_path) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter='\n')
        for row in csv_reader:
            CSV_data += [row[0].split(",")]
    CSV_data = CSV_data[1:]
    return CSV_data

def lin_interpolate (x1, y1, x2, y2, target_x):
    # input: floats representing the x and y values of the points to interpolate between, float of the x value to interpolate
    # general purpose linear interpolation funciton

    if (target_x < x1 or target_x > x2):
        print ("error: target out of range")
        return (-1)
    else:
        x_ratio = (target_x - x1)/(x2 - x1)
        target_y = (x_ratio * (y2 - y1)) + y1
        return target_y


def data_cleaning (raw_bonddata):
    # input: (List with bond data strings in form [bond, type, term, yield])
    # performs prelim data processing on inputs

    # separating corporate and government bonds
    raw_corp = []
    raw_gov = []
    for i in raw_bonddata:
        if (i[1] == "corporate"):
            raw_corp += [i]
        elif (i[1] == "government"):
            raw_gov += [i]
        else:
            print ("error: improper formatting in bond: {}".format(i[0]))

    # cleaning the data them operatable numbers
    # we cast the bonds to numpy arrays so future operations will be faster
    # arrays are formatted [bond# , term (years), yield (%)]
    corp_bonds = np.zeros ((len(raw_corp),3))
    gov_bonds = np.zeros ((len(raw_gov),3))

    for i in range(0, len(raw_corp)):
        corp_bonds[i,0] = int(raw_corp[i][0][1:])
        corp_bonds[i,1] = float((raw_corp[i][2].split(" "))[0])
        corp_bonds[i,2] = float(raw_corp[i][3].split("%")[0])

    for i in range(0, len(raw_gov)):
        gov_bonds[i,0] = int(raw_gov[i][0][1:])
        gov_bonds[i,1] = float((raw_gov[i][2].split(" "))[0])
        gov_bonds[i,2] = float(raw_gov[i][3].split("%")[0])

    # sort the govt bonds in descending order to make search easier
    gov_bonds = gov_bonds[gov_bonds[:,1].argsort()] 
    return [corp_bonds, gov_bonds]

def benchmark_candidates (corp_bonds, gov_bonds):
    # input: (3xn np array, 3xm np array), for n corporate bonds and m government bonds.
    # expected np array formatting: [[bond# , term, yield], ...]
    # will return a 3xn array, where each pair represents the indices of the closest pair of government bonds on each side of a corporate bond. n is the number of corporate bonds

    # each candidate formatted: [corp_bond_index, left_govt_bond_index, right_govt_bond_index]
    candidates = np.zeros((len(corp_bonds),3), dtype=int)

    # use searchsorted to find govt bond indices
    for i, corp_bond in enumerate (corp_bonds):
        right_ind = np.searchsorted(gov_bonds[:,1], corp_bond[1])
        candidates[i,0] = i
        candidates[i,1] = right_ind - 1
        candidates[i,2] = right_ind
        # we dont have to consider the edge cases where the candidates are out of bounds, becase we are given 
        # that there will always be a govt bond smaller and larger in term than all corp bonds
    return candidates

def spread_to_benchmark(corp_bonds, gov_bonds, candidates, spread_precision, print_result = False):
    # input: (3xn np array, 3xm np array, 2xn np array, integer)
    # determines which candidate is closer for each bond, and returns the spreads in the desired format

    benchmark_spreads = [] # output list, formatted as presented in problem description
    if (len(corp_bonds) != len(candidates)): # checking if we have right #  of candidates
        print("error: candidate num != corp bond num")
        return(-1)
    else:
        if (print_result):
            print ("bond,benchmark,spread_to_benchmark")
        for i, corp_bond in enumerate (corp_bonds):
            bond_name = "C" + str(int(corp_bond[0]))
            benchmark_name = ""
            spread_to_benchmark = ""

            # determine the closer candidate
            if (abs(gov_bonds[candidates[i,1],1] - corp_bond[1]) < abs(gov_bonds[candidates[i,2],1] - corp_bond[1])):
                benchmark_ind = candidates[i,1]
            else:
                benchmark_ind = candidates[i,2]

            # finalize formatting, record, and print
            benchmark_name = "G" + str(int(gov_bonds[benchmark_ind,0]))
            spread_to_benchmark = str(np.around(corp_bond[2] - gov_bonds[benchmark_ind,2], spread_precision)) + "%"
            benchmark_spreads += [[bond_name, benchmark_name, spread_to_benchmark]]
            if (print_result):
                print("{},{},{}".format(bond_name, benchmark_name, spread_to_benchmark))
        return benchmark_spreads

def spread_to_curve (corp_bonds, gov_bonds, candidates, spread_precision, print_result = False):
    # input: (3xn np array, 3xm np array, 2xn np array, integer)
    # calculates linear interpolation between both candidates depending on the corporate bond term, returns the spreads in the desired format
    
    curve_spreads = [] # output list, formatted as presented in problem description
    if (len(corp_bonds) != len(candidates)): # checking if we have right #  of candidates
        print("error: candidate num != corp bond num")
        return(-1)
    else:
        if (print_result):
            print ("bond,spread_to_curve")
        for i, corp_bond in enumerate(corp_bonds):
            # set up left and right candidate govt bonds
            left_cand = gov_bonds[candidates[i][1]]
            right_cand = gov_bonds[candidates[i][2]]
 
            bond_name = "C" + str(int(corp_bond[0]))
            # use linear interpolation function to determine spread. Then format spread properly
            spread_to_curve = corp_bond[2] - lin_interpolate(left_cand[1], left_cand[2], right_cand[1], right_cand[2], corp_bond[1])
            spread_to_curve = str(np.around(spread_to_curve, spread_precision)) + "%"

            # record and print final outputs
            curve_spreads += [[bond_name, spread_to_curve]]
            if (print_result):
                print ("{},{}".format(bond_name, spread_to_curve))
        return curve_spreads