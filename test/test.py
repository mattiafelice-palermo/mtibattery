from galvanostatic import CellReadings


filename='20151126_graphite_foil_blank.txt'

first = CellReadings(filename)

#for cycle in first.cycles:
#    for step in cycle.steps.values():
#        print(step)

print(first.cycles[1].steps['CC_Chg'].records)

