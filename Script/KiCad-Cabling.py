from __future__ import print_function
import kicad_netlist_reader
import sys
import csv

from netList import *
from componentList import *
from helperFunctions import *
from TableMaker import *

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])
Components = net.getInterestingComponents();

# Create the netList and componentList lists
netList = getNetList(net);
componentList = getComponentList(net);

# Get an Anchor component and start Paths
Paths = [];
Tables = []
Tables.append(TableMaker());
table = Tables[0];
for component in componentList:
    if(component['isAnchor'] == True):
        # start Paths
        for i, net in enumerate(component['nets']):
            path = {};
            position = getPosition(component['ref'], net, netList);
            path['name'] = "Path"+str(position);
            path['refs'] = [component['ref']];
            path['nets'] = [net];
            path['complete'] = False;
            Paths.append(path);
            table.addPath(path['name']);
        table.sortTable();
        # Add Headers
        table.addComponent(getKiCadComponent(component['ref'], Components,), Paths, netList);
        # Remove Component
        componentList = removeComponent(component['ref'], componentList);


# For each path that is incomplete:  
# Get next component, by looking up last net in path.nets in netList, 
# then lookup the next net for that component by looking in componentList, 
# then remove component from componentList
while anyPathIncomplete(Paths):
    for path in Paths:
        if(path['complete'] == False):
            lastNet = path['nets'][-1];
            lastRef = path['refs'][-1];
            refs = getNetRefs(lastNet, lastRef, netList);
            if(len(refs) == 1):
                ref = refs[0];
                nextNets = [];
                component = getComponent(ref, componentList);
                if(component):
                    path['refs'].append(ref);
                    for net in component['nets']:
                        if(net != lastNet):
                            nextNets.append(net);
                    if(len(nextNets) == 1):
                        path['nets'].append(nextNets[0]);
                    table.addComponent(getKiCadComponent(component['ref'], Components,), Paths, netList, path);
                    componentList = removeComponent(ref, componentList);
                else:
                    path['complete'] = True;
            else:
                path['complete'] = True;

# Write Tables to CSV
# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open(sys.argv[2], 'wb')
    writer = csv.writer(f, quotechar="\"", quoting=csv.QUOTE_ALL);
    for table in Tables:
        writer.writerows(table.formatCSV());
        writer.writerows([[]]);
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print( __file__, ":", e, sys.stderr )
    f = sys.stdout

    
print("**********************************************");
print('Tables');
table.printTable();
print("**********************************************");
printPaths(Paths);
print("**********************************************");
printComponentList(componentList);
print("**********************************************");
print("ALL DONE");