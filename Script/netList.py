def getNetList(net):
    nets = net.nets;

    netList = [];
    # [
    #     {
    #         netName: "Net-(PIN3-Pad1)",
    #         nodes: 	[
    #                     {ref: "W4", pin: "2"},
    #                     {ref: "PIN3", pin: "1"}
    #                 ]
    #     },
    #     ...
    # ]

    # add nets to components
    for thisNet in nets:
        newNet = {};
        newNet['netName'] = thisNet.attributes['name'];

        nodes = thisNet.getChildren();

        newNet['nodes'] = [];
        for node in nodes:
            nodeDict = {};
            nodeDict['ref'] = node.attributes['ref'];
            nodeDict['pin'] = node.attributes['pin'];
            
            newNet['nodes'].append(nodeDict);

        netList.append(newNet);
    return netList;

def printNetList(netList):
    for net in netList:
        print("Net Name: ", net['netName']);
        print("Nodes: ", net['nodes']);
        print("----------");

def getNetRefs(lastNet, lastRef, netList):
    refs = [];
    for net in netList:
        if(lastNet == net['netName']):
            for node in net['nodes']:
                if(node['ref'] != lastRef):
                    refs.append(node['ref']);
    return refs;