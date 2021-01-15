import yieldspreadmodules as ysm
import numpy as np

def check_result (expected_list, test_result, precision = 0):
    # input: (mxn iterable, 1xn iterable, integer)
    # this function will find the corresponding expected result in expected list based on matching its first element with the first element in test result. It will then check if they are sufficiently close.
    # note: set precision to 0 when comparing non rounded items in last element of test_result. Otherwise, considers number of decimal places to be equal as a pass. Accounts for and removes trailing percent sign.
    
    was_result_found = False
    for expected_result in expected_list:
        if expected_result[0] == test_result[0]:
            was_result_found = True
            for i in range (0, len(expected_result)):
                if precision == 0 or i < len(expected_result) - 1:
                    if expected_result[i] != test_result[i]:
                        return ("Test Failed. Expected Result: {}, Actual Result: {}".format(expected_result, test_result))
                else:
                    expected_rounded = np.around(float(expected_result[i][:len(expected_result[i]) - 1]), precision)
                    test_rounded = np.around(float(test_result[i][:len(test_result[i]) - 1]), precision)
                    if expected_rounded != test_rounded:
                        return ("Test Failed. Expected Result: {}, Actual Result: {}".format(expected_result, test_result))
    if (was_result_found):
        return ("Test Passed")
    else:
        return ("Test Failed. Expected Result Not Found for Test Result: {}".format(test_result))

# Test data setup
test_data = [["C1", "corporate", "1.3 years", "3.3%"],
            ["C2", "corporate", "2.0 years", "3.8%"],
            ["C3", "corporate", "5.2 years", "5.3%"],
            ["C4", "corporate", "7.0 years", "6.2%"],
            ["C5", "corporate", "7.2 years", "6.4%"],
            ["G1", "government", "0.9 years", "1.7%"],
            ["G2", "government", "2.3 years", "2.3%"],
            ["G3", "government", "7.8 years", "5.5%"],
            ["G4", "government", "8.2 years", "5.7%"]]
   
cleaned_expectations = [np.array([[1, 1.3, 3.3],
                                [2, 2.0, 3.8],
                                [3, 5.2, 5.3],
                                [4, 7.0, 6.2],
                                [5, 5.2, 5.7]]),
                        np.array([[1, 0.9, 1.7],
                                [2,  2.3, 2.3],
                                [3,  7.8, 5.5],
                                [4,  6.1, 9.1]])] 

candidate_expectations = np.array([[0, 0, 1],
                                  [1, 0, 1],
                                  [2, 1, 2],
                                  [3, 1, 2],
                                  [4, 2, 3]])

spread_to_benchmark_expectations = [["C1", "G1", "1.6%"],
                                    ["C2", "G2", "1.5%"],
                                    ["C3", "G3", "-0.2%"],
                                    ["C4", "G3", "0.7%"],
                                    ["C5", "G4", "0.7%"]] 

spread_to_curve_expectations = [["C1", "1.429%"],
                                ["C2", "1.629%"],
                                ["C3", "1.313%"],
                                ["C4", "1.166%"],
                                ["C5", "1.491%"]] 

# Running the function for each set of test data
print ("Note: The last test case for each situation is meant to fail, as a check for test functionality")

cleaned_test = ysm.data_cleaning(test_data)
print ("\nData Cleaning Corporate")
for i in cleaned_test[0]:
    print(check_result(cleaned_expectations[0], i))

print ("\nData Cleaning Government")
for i in cleaned_test[1]:
    print(check_result(cleaned_expectations[1], i))

candidate_test = ysm.benchmark_candidates(cleaned_expectations[0], cleaned_expectations[1])
print ("\nCandidates")
for i in candidate_test:
    print(check_result(candidate_expectations, i))

challenge1_data = ysm.spread_to_benchmark(cleaned_expectations[0],cleaned_expectations[1],candidate_expectations,4)
print ("\nSpread to Benchmark")
for i in challenge1_data:
    print(check_result(spread_to_benchmark_expectations, i))

challenge2_data = ysm.spread_to_curve(cleaned_expectations[0],cleaned_expectations[1],candidate_expectations,4)
print ("\nSpread to Curve")
for i in challenge2_data:
    print(check_result(spread_to_curve_expectations, i, 3))