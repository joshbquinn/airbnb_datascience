import os
this_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

os.chdir(this_dir)
print("\nRUN CSV CLEANER")
exec(open("./scripts/run_csv_cleaner.py").read())

os.chdir(this_dir)
print("\nRUN DATA CLEANER")
exec(open("./scripts/run_data_cleaner.py").read())

os.chdir(this_dir)
print("\nRUN ANALYSIS")
exec(open("./scripts/run_analysis.py").read())

os.chdir(this_dir)
print("\nRUN VISUALISATIONS")
exec(open("./scripts/run_visualisations.py").read())