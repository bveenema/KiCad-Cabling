# class to create and update tables. 
# 1 table instance represents 1 cable assembly
#   | ROW LABEL |   COL 1   |   COL 2   |  COL 3    |
#   ---------------------------------------------------------------------
#   |   HEADER  |   Label   |  Housing  | Position  |
#   ---------------------------------------------------------------------
#   |   PATHX   |    J2     |JST PH MALE|     1     |
#   ---------------------------------------------------------------------
#   |   PATHX   |           |           |     2     |  
#   ---------------------------------------------------------------------

class TableMaker():
    def __init__(self):
        self.table = [['HEADER']];

    def getNumRows(self):
        return len(self.table);

    def addPath(self, pathName):
        rowToAdd = [pathName];
        for i, _ in enumerate(self.table[0]):
            if(i != 0):
                rowToAdd.append('');
        self.table.append(rowToAdd);

    def getNumColumns(self):
        return len(self.table[0]);

    def addHeader(self, header):
        for i, row in enumerate(self.table):
            if(i==0):
                row.append(header);
            else:
                row.append('');

    def updateCell(self, newValue, header, path):
        # find column the "header" is in
        column = -1;
        for col, Header in enumerate(self.table[0]):
            if(header == Header):
                column = col;
        
        # find the row the representing the "path"
        row = -1;
        for r, ROWLABEL in enumerate(self.table):
            if(path == ROWLABEL[0]):
                row = r;
        # update the cell in the "row" and the "column"
        if(column >= 0 & row >= 0):
            self.table[row][column] = newValue;

    def addComponent(self, Component, Paths=None, NetList=None, path=None):
        # ADD HEADERS
        fields = [];
        import copy;
        currentHeaders = copy.copy(self.table[0]);
        if(Component.getRef().startswith("HOUSING")):
            fields = self.makeHousingHeaders(len(currentHeaders));
        elif(Component.getRef().startswith("TERMINAL")):
            fields = self.makeTerminalHeaders(Component, currentHeaders);
        else:
            fields = Component.getFieldNames();
        # check to make sure the new headers are not the same as the last headers
        if( set(fields) != set(currentHeaders[-len(fields):]) ):
            for header in fields:
                self.addHeader(header);
            
        # ADD CELL VALUES
        cellValues = [];
        if(Component.getRef().startswith("HOUSING") and Paths and NetList):
            self.populateHousingCells(Component, Paths, NetList);
        elif(Component.getRef().startswith('TERMINAL')):
            self.populateTerminalCells(Component, fields, path);
        else:
            for field in fields:
                cellValues.append({'fieldName': field, 'value': Component.getField(field)});
            for cell in cellValues:
                self.updateCell(cell['value'], cell['fieldName'], path['name']);

    def makeHousingHeaders(self, len):
        fields = [];
        if(len < 3):
            fields = ['Label', 'Housing', 'Position'];
        else:
            fields = ['Position', 'Housing', 'Label'];
        return fields;

    def makeTerminalHeaders(self, Component, currentHeaders):
        fields = [];
        if 'Terminal' not in currentHeaders:
            fields = ['Terminal'];
            for field in Component.getFieldNames():
                fields.append(field);
        else:
            for field in Component.getFieldNames():
                fields.append(field);
            fields.append('Terminal');
        return fields;

    def populateHousingCells(self, Component, Paths, NetList):
        cellValues = [];
        from componentList import getPosition;
        for i, path in enumerate(Paths):
            if(i==0):
                cellValues.append({ 'fieldName': 'Label', 'value': Component.getField('Label') });
                cellValues.append({ 'fieldName': 'Housing', 'value': Component.getValue() });
            cellValues.append({ 'fieldName': 'Position', 'value': getPosition(Component.getRef(), path['nets'][-1], NetList)});
            for cell in cellValues:
                self.updateCell(cell['value'], cell['fieldName'], path['name']);
            cellValues = [];

    def populateTerminalCells(self, Component, fields, path):
        cellValues = [];
        for field in fields:
            if(field == 'Terminal'):
                cellValues.append({'fieldName': field, 'value': Component.getValue()});
            else: 
                cellValues.append({'fieldName': field, 'value': Component.getField(field)});
        print(cellValues);
        for cell in cellValues:
            self.updateCell(cell['value'], cell['fieldName'], path['name']);

    def formatCSV(self):
        # strip ROW LABELS
        import copy
        formattedTable = copy.deepcopy(self.table);
        for row in formattedTable:
            row.pop(0);
        return formattedTable;
    
    def sortTable(self):
        # sort rows by path name, leave HEADER row at top
        self.table.sort();

    def printTable(self):
        for row in self.table:
            print(row);