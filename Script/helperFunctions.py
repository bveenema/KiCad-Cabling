import collections
from componentList import getKiCadComponent

def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result
    

def anyPathIncomplete(paths):
    incomplete = False;
    for path in paths:
        if(path['complete'] == False):
            incomplete = True;
    return incomplete;

def addHeaders(ref, headersList, components):
    newHeaders = [];
    if(ref.startswith("HOUSING")):
        if(len(headersList) == 0):
            newHeaders = ['Label', 'Housing', 'Position'];
        else:
            newHeaders = ['Position', 'Housing', 'Label'];
    else:
        newHeaders = getKiCadComponent(ref, components).getFieldNames();
    # check to make sure the new headers are not the same as the last headers
    if( set(newHeaders) != set(headersList[-len(newHeaders):]) ):
        headersList.append(newHeaders);
    return flatten(headersList);