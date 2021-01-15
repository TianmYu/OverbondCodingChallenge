# 
## Overview and Setup
Python 3 required. 

To run: open the file in your favorite IDE and run "yieldspreadcalculator.py". Alternatively, navigate to the file in the command prompt or terminal window and execute using "python yieldspreadcalculator.py"
	Ensure that the yieldspreadmodules.py file is in the same folder as yieldspreadcalculator.py

outputs: outputs will be printed in the terminal window. Alternatively, outputs will also be returned by the appropriate functions, which can easily be integrated with other software in the data pipeline. 

The program operates in two parts. The first to extract and ready the data for processing. The second employs the processed data and performs the final calculations required to provide the required outputs for challenges 1 and 2. 

In the first part, in the data_cleaning function, reads the CSV, cleans the data (converting the string yields and terms to floats), and separates the government and corporate bonds into two different NumPy arrays.
Next, the data is sent to the benchmark_candidates function, which employs NumPy searchsorted to quickly retrieve the indices of the immediately smaller and immediately larger government bond to each corporate bond.

In the second part, the spread_to_benchmark function takes the processed data, and finds the closer of the two benchmark candidates for each corporate bond, assigning it as the bond's benchmark. It then calculates the spread.
The spread_to_curve function does the same, but for the curve spread. It uses both candidates and linearly interpolates between them to produce a curve spread for each corporate bond. 
Both the prior functions end by formatting, printing, and returning the results

## Technical Decisions
A couple of assumptions were made beforehand:
	As stated in the problem, there would always be a government bond with a term shorter than all corporate bonds, and one with a term longer than all corporate bonds. This precluded us from considering some edge cases.
	The first line in the provided data is labels, and is therefore skipped
	The government and corporate bonds are given in the CSV file were not necessarily sorted in any order, nor where they guaranteed to be cleanly split (ex: we could have G, C, G, G, C for example)
	The term lengths and returns will all be strictly positive

Now, the following are specific technical decisions made for the problem:

### Modularity: 
	The entire program was written to be modular, with tasks being performed by specific functions. This improves the program's testability and allows for easily integrating it with a larger system, such as front end display, by importing the file and calling functions.
	Functions were written to be "general purpose" when possible, such as the CSV opening and linear interpolation, to reduce complexity and failure points when debugging, as well as allowing for potential reuse

### Scalability/Runtime:
	Numpy arrays were used when possible due to their faster runtime when working with larger sets of data. Although the practice set was only 7 elements, a true application of this system could require scaling to hundreds of thousands or even millions of data points.
		The initial data was still recorded with a python list to give flexibility in case we do not know the exact number of elements required
		However, once the data is loaded in, in data_cleaning, the data is transferred to fixed-size NumPy arrays when being split into corporate and government sets. This split would be required in any case to make later operations easier, so we do not lose much time here.
	The government bonds are also sorted by term length. This allows for quick searching in later operations. Specifically, it allows for the log time searchsorted function to be applied when determining candidates. 
		We note that determining benchmark candidates is one potential limiting step, and has nlog(m) time complexity, where we have n corporate bonds, and m government bonds. The other potential limiting step is sorting the government bonds, which would have mlog(m) complexity.

### Error Checking
	Basic checks were employed in functions to check that proper inputs are provided, and would terminate the function with an error message if some improper inputs were received

## Trade-Offs and Possible Future Developments
One possibility for future development is regarding the initial data storage after it is read from the CSV. Currently, the entire CSV is read and stored in memory. While it is perfectly possible to store millions of data points in the program memory, it could be more effective at larger scales to perform a line by line reading, or have a separate program that reads the CSV and provides a data stream.
	Switching to the use of a data stream could also allow the program to work in a real time pipeline with other software that records or preprocesses the data, rather than having to be rerun on each new CSV.

Another future development could be the integration with a visualization tool or front end. 
	For example, pyPlot could be used the visualize the data, and even potentially to debug the program
	Alternatively, this outlines a trade-off that was chosen, which is the development of the program in python. If JavaScript was used, the code could easily be integrated with CSS/HTML styling. While python integration is still possible, it would not be as straightforward

A final future development would be the investment into more extensive automated tests. The current submission's testing program only considers a small handfull of hand calculated cases to test for.
	This could include the creation of a test sample generator that could produce inputs and expected outputs, on which the program can be tested.

## Function Documentation
# open_CSV(string CSV_path)
	general purpose function to open and store data from CSV files
	returns a list of lists containing the CSV data

# in_interpolate (float x1, float y1, float x2, float y2, float target_x):
	general purpose linear interpolation funciton
	(x1, y1) and (x2, y2) are the poitns to interpolate between, (target_x, target_y) is the interpolatd point
	returns target_y

# data_cleaning (list raw_bonddata)
	input: (List with bond data strings in form [bond, type, term, yield])
	performs prelim data processing on inputs
	returns a list of corporate and government bond data [corporate bonds, government bonds]
		corporate and government bond data are stored in numpy lists with the form: [[bond# , term (years), yield (%)], ...]

# benchmark_candidates (np array corp_bonds, np array gov_bonds):
	input: corporate and government bond np arrays, formatted as specified above
	determines the closest pair of government bonds on either side of a corporate bond with respect to term lengths
	returns a numpy array of hte form [[corp_bond_index, left_govt_bond_index, right_govt_bond_index], ...]

# spread_to_benchmark (np array corp_bonds, np array gov_bonds, np array candidates, int spread_precision, bool print_result = False):
	input: first three are np arrays as specified above. Integer with precision if the spread requires rounding. Boolean to decide if the function should directly print data as well as returning it.
	determines which candidate is closer for each bond, and returns the spreads in the desired format
	returns a list of bond benchmark spreads in the form [[bond_name, benchmark_name, spread_to_benchmark], ...]

# spread_to_curve (np array corp_bonds, np array gov_bonds, np array candidates, int spread_precision, bool print_result = False):
	input: first three are np arrays as specified above. Integer with precision if the spread requires rounding. Boolean to decide if the function should directly print data as well as returning it.
	calculates linear interpolation between both candidates depending on the corporate bond term, returns the spreads in the desired format
	returns a list of bond benchmark spreads in the form [[bond_name, spread_to_curve], ...]