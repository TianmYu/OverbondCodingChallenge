import yieldspreadmodules as ysm

CSV_path = "sample_input.csv"    # insert path to data here

raw_data = ysm.open_CSV(CSV_path)
bonds = ysm.data_cleaning(raw_data)
candidates = ysm.benchmark_candidates(bonds[0], bonds[1])
challenge1_data = ysm.spread_to_benchmark(bonds[0],bonds[1],candidates,4,True)
challenge2_data = ysm.spread_to_curve(bonds[0],bonds[1],candidates,4,True)
