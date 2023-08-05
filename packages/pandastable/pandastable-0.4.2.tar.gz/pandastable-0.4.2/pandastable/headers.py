#!/usr/bin/env python
"""
    Implements the pandastable headers classes.
    Created Jan 2014
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from tkinter import *
from tkinter.ttk import *
import math, time
import os, types, string
import numpy as np
import pandas as pd

def check_multiindex(index):
    """Check if multiindex"""
    if isinstance(index, pd.core.index.MultiIndex):
        return 1
    else:
        return 0

class ColumnHeader(Canvas):
    """Class that takes it's size and rendering from a parent table
        and column names from the table model."""

    def __init__(self, parent=None, table=None):
        Canvas.__init__(self, parent, bg='gray25', width=500, height=20)
        self.thefont='Arial 14'
        if table != None:
            self.table = table
            self.height = 20
            self.model = self.table.model
            self.config(width=self.table.width)
            #self.colnames = self.model.columnNames
            self.columnlabels = self.model.df.columns
            self.draggedcol = None
            self.bind('<Button-1>',self.handle_left_click)
            self.bind("<ButtonRelease-1>", self.handle_left_release)
            self.bind('<B1-Motion>', self.handle_mouse_drag)
            self.bind('<Motion>', self.handle_mouse_move)
            self.bind('<Shift-Button-1>', self.handle_left_shift_click)
            self.bind('<Control-Button-1>', self.handle_left_ctrl_click)
            self.bind("<Double-Button-1>",self.handle_double_click)
            if self.table.ostyp=='mac':
                #For mac we bind Shift, left-click to right click
                self.bind("<Button-2>", self.handle_right_click)
                self.bind('<Shift-Button-1>',self.handle_right_click)
            else:
                self.bind("<Button-3>", self.handle_right_click)
            self.thefont = self.table.thefont
        return

    def redraw(self):
        """Redraw column header"""

        df = self.model.df
        cols = self.model.getColumnCount()
        self.tablewidth=self.table.tablewidth
        self.configure(scrollregion=(0,0, self.table.tablewidth+self.table.x_start, self.height))
        self.delete('gridline','text')
        self.delete('rect')
        self.delete('dragrect')
        self.atdivider = None
        align = 'w'
        pad = 5
        h=self.height
        x_start = self.table.x_start
        if cols == 0:
            return

        #if check_multiindex(self.model.df.columns) == 1:
        #    cols = df.columns.get_level_values(1)
        for col in self.table.visiblecols:
            colname = df.columns[col]
            if colname in self.model.columnwidths:
                w = self.model.columnwidths[colname]
            else:
                w = self.table.cellwidth
            x = self.table.col_positions[col]
            if align == 'w':
                xt = x+pad
            elif align == 'e':
                xt = x+w-pad
            elif align == 'center':
                xt = x-w/2
            if type(colname) == 'tuple':
                colname = ','.join(colname)
            if len(str(colname)) > w/10:
                colname = str(colname)[0:int(w/10)]+'.'
            line = self.create_line(x, 0, x, h, tag=('gridline', 'vertline'),
                                 fill='white', width=1)
            self.create_text(xt,h/2,
                                text=colname,
                                fill='white',
                                font=self.thefont,
                                tag='text', anchor=align)

        x = self.table.col_positions[col+1]
        self.create_line(x,0, x,h, tag='gridline',
                        fill='white', width=2)
        return

    def handle_left_click(self,event):
        """Does cell selection when mouse is clicked"""

        self.delete('rect')
        self.table.delete('entry')
        self.table.delete('multicellrect')
        colclicked = self.table.get_col_clicked(event)
        if colclicked == None:
            return
        #set all rows selected
        self.table.allrows = True
        self.table.setSelectedCol(colclicked)

        if self.atdivider == 1:
            return
        self.drawRect(self.table.currentcol)
        #also draw a copy of the rect to be dragged
        self.draggedcol = None
        self.drawRect(self.table.currentcol, tag='dragrect',
                        color='lightblue', outline='white')
        if hasattr(self, 'rightmenu'):
            self.rightmenu.destroy()
        #finally, draw the selected col on the table
        self.table.drawSelectedCol()
        return

    def handle_left_release(self,event):
        """When mouse released implement resize or col move"""

        self.delete('dragrect')
        if self.atdivider == 1:
            #col = self.table.get_col_clicked(event)
            x=int(self.canvasx(event.x))
            col = self.table.currentcol
            x1,y1,x2,y2 = self.table.getCellCoords(0,col)
            newwidth=x - x1
            if newwidth < 5:
                newwidth=5
            self.table.resizeColumn(col, newwidth)
            self.table.delete('resizeline')
            self.delete('resizeline')
            self.delete('resizesymbol')
            self.atdivider = 0
            return
        self.delete('resizesymbol')
        #move column
        if self.draggedcol != None and self.table.currentcol != self.draggedcol:
            self.model.moveColumn(self.table.currentcol, self.draggedcol)
            self.table.setSelectedCol(self.draggedcol)
            self.table.redraw()
            self.table.drawSelectedCol(self.table.currentcol)
            self.drawRect(self.table.currentcol)
        return

    def handle_right_click(self, event):
        """respond to a right click"""

        colclicked = self.table.get_col_clicked(event)
        multicollist = self.table.multiplecollist
        if len(multicollist) > 1:
            pass
        else:
            self.handle_left_click(event)
        self.rightmenu = self.popupMenu(event)
        return

    def handle_mouse_drag(self, event):
        """Handle column drag, will be either to move cols or resize"""

        x=int(self.canvasx(event.x))
        if self.atdivider == 1:
            self.table.delete('resizeline')
            self.delete('resizeline')
            self.table.create_line(x, 0, x, self.table.rowheight*self.table.rows,
                                width=2, fill='gray', tag='resizeline')
            self.create_line(x, 0, x, self.height,
                                width=2, fill='gray', tag='resizeline')
            return
        else:
            w = self.table.cellwidth
            self.draggedcol = self.table.get_col_clicked(event)
            x1, y1, x2, y2 = self.coords('dragrect')
            x=int(self.canvasx(event.x))
            y = self.canvasy(event.y)
            self.move('dragrect', x-x1-w/2, 0)

        return

    def within(self, val, l, d):
        """Utility funtion to see if val is within d of any
            items in the list l"""

        for v in l:
            if abs(val-v) <= d:
                return 1
        return 0

    def handle_mouse_move(self, event):
        """Handle mouse moved in header, if near divider draw resize symbol"""

        if len(self.model.df.columns) == 0:
            return
        self.delete('resizesymbol')
        w=self.table.cellwidth
        h=self.height
        x_start=self.table.x_start
        #x = event.x
        x=int(self.canvasx(event.x))
        if x > self.tablewidth+w:
            return
        #if event x is within x pixels of divider, draw resize symbol
        if x!=x_start and self.within(x, self.table.col_positions, 4):
            col = self.table.get_col_clicked(event)
            if col == None:
                return
            self.draw_resize_symbol(col)
            self.atdivider = 1
        else:
            self.atdivider = 0
        return

    def handle_right_release(self, event):
        self.rightmenu.destroy()
        return

    def handle_left_shift_click(self, event):
        """Handle shift click, for selecting multiple cols"""

        self.table.delete('colrect')
        self.delete('rect')
        currcol = self.table.currentcol
        colclicked = self.table.get_col_clicked(event)
        if colclicked > currcol:
            self.table.multiplecollist = list(range(currcol, colclicked+1))
        elif colclicked < currcol:
            self.table.multiplecollist = list(range(colclicked, currcol+1))
        else:
            return
        for c in self.table.multiplecollist:
            self.drawRect(c, delete=0)
            self.table.drawSelectedCol(c, delete=0)
        return

    def handle_left_ctrl_click(self, event):
        """Handle ctrl clicks - for multiple column selections"""

        currcol = self.table.currentcol
        colclicked = self.table.get_col_clicked(event)
        multicollist = self.table.multiplecollist
        if 0 <= colclicked < self.table.cols:
            if colclicked not in multicollist:
                multicollist.append(colclicked)
            else:
                multicollist.remove(colclicked)
        self.table.delete('colrect')
        self.delete('rect')
        for c in self.table.multiplecollist:
            self.drawRect(c, delete=0)
            self.table.drawSelectedCol(c, delete=0)
        return

    def handle_double_click(self, event):
        """Double click sorts by this column. """

        colclicked = self.table.get_col_clicked(event)
        self.table.sortTable()
        return

    def popupMenu(self, event):
        """Add left and right click behaviour for column header"""

        colname = str(self.model.df.columns[self.table.currentcol])
        currcol = self.table.currentcol
        multicols = self.table.multiplecollist
        colnames = list(self.table.model.df.columns[multicols])
        colnames = ','.join(colnames)
        popupmenu = Menu(self, tearoff = 0)
        def popupFocusOut(event):
            popupmenu.unpost()
        popupmenu.add_command(label="Rename Column", command=self.renameColumn)
        popupmenu.add_command(label="Sort by " + colnames,
                    command=lambda : self.table.sortTable(ascending=[1 for i in multicols]))
        popupmenu.add_command(label="Sort by " + colnames + ' (descending)',
            command=lambda : self.table.sortTable(ascending=[0 for i in multicols]))
        popupmenu.add_command(label="Set %s as Index" %colnames, command=self.table.setindex)
        popupmenu.add_command(label="Delete Column(s)", command=self.table.deleteColumn)
        popupmenu.add_command(label="Set Column Type", command=self.table.setColumnType)
        popupmenu.bind("<FocusOut>", popupFocusOut)
        #self.bind("<Button-3>", popupFocusOut)
        popupmenu.focus_set()
        popupmenu.post(event.x_root, event.y_root)
        return popupmenu

    def renameColumn(self):
        col = self.table.currentcol
        new = simpledialog.askstring("New column name?", "Enter new name:")
        if new !=None:
            if new == '':
                messagebox.showwarning("Error", "Name should not be blank.")
                return
            else:
                #self.model.renameColumn(col, ans)
                df = self.model.df
                df.rename(columns={df.columns[col]: new}, inplace=True)
                self.redraw()
        return

    def draw_resize_symbol(self, col):
        """Draw a symbol to show that col can be resized when mouse here"""

        self.delete('resizesymbol')
        w=self.table.cellwidth
        h=self.height
        #if x_pos > self.tablewidth:
        #    return
        wdth=1
        hfac1=0.2
        hfac2=0.4
        x_start=self.table.x_start
        x1,y1,x2,y2 = self.table.getCellCoords(0,col)
        self.create_polygon(x2-3,h/4, x2-10,h/2, x2-3,h*3/4, tag='resizesymbol',
            fill='white', outline='gray', width=wdth)
        self.create_polygon(x2+2,h/4, x2+10,h/2, x2+2,h*3/4, tag='resizesymbol',
            fill='white', outline='gray', width=wdth)
        return

    def drawRect(self,col, tag=None, color=None, outline=None, delete=1):
        """User has clicked to select a col"""

        if tag==None:
            tag='rect'
        if color==None:
            color='#0099CC'
        if outline==None:
            outline='gray25'
        if delete == 1:
            self.delete(tag)
        w=1
        x1,y1,x2,y2 = self.table.getCellCoords(0,col)
        rect = self.create_rectangle(x1,y1-w,x2,self.height,
                                  fill=color,
                                  outline=outline,
                                  width=w,
                                  tag=tag)
        self.lower(tag)
        return

class RowHeader(Canvas):
    """Class that displays the row headings (or DataFrame index).
       Takes it's size and rendering from the parent table.
       This also handles row/record selection as opposed to cell
       selection"""

    def __init__(self, parent=None, table=None, width=40):
        Canvas.__init__(self, parent, bg='gray75', width=width, height=None)
        if table != None:
            self.table = table
            self.width = width
            self.inset = 1
            self.color = '#C8C8C8'
            self.showindex = False
            self.config(height = self.table.height)
            self.startrow = self.endrow = None
            self.model = self.table.model
            self.bind('<Button-1>',self.handle_left_click)
            self.bind("<ButtonRelease-1>", self.handle_left_release)
            self.bind("<Control-Button-1>", self.handle_left_ctrl_click)
            self.bind('<Button-3>',self.handle_right_click)
            self.bind('<B1-Motion>', self.handle_mouse_drag)
            #self.bind('<Shift-Button-1>', self.handle_left_shift_click)
        return

    def redraw(self, align='w', showkeys=False):
        """Redraw row header"""

        self.height = self.table.rowheight * self.table.rows+10
        self.configure(scrollregion=(0,0, self.width, self.height))
        self.delete('rowheader','text')
        self.delete('rect')

        xstart = 1
        pad = 3
        v = self.table.visiblerows
        scale = self.table.getScale()
        if self.showindex == True:
            if check_multiindex(self.model.df.index) == 1:
                ind = self.model.df.index.values[v]
                cols = [pd.Series(i) for i in list(zip(*ind))]
                l = [r.str.len().max() for r in cols]
                widths = [i * scale + 6 for i in l]
                #print (widths)
                xpos = [0]+list(np.cumsum(widths))[:-1]
            else:
                ind = self.model.df.index[v]
                dtype = ind.dtype
                r = ind.astype('object').astype('str')
                l = r.str.len().max()
                widths = [l * scale + 6]
                cols = [r]
                xpos = [xstart]
            w = np.sum(widths)
        else:
            rows = [i+1 for i in v]
            cols = [rows]
            w=45
            widths = [w]
            xpos = [xstart]

        if self.width != w:
            self.config(width=w)
            self.width = w
        h = self.table.rowheight

        i=0
        for col in cols:
            r=v[0]
            x = xpos[i]
            i+=1
            for row in col:
                text = row
                x1,y1,x2,y2 = self.table.getCellCoords(r,0)
                self.create_rectangle(x,y1,w-1,y2, fill=self.color,
                                        outline='white', width=1,
                                        tag='rowheader')
                self.create_text(x+pad,y1+h/2, text=text,
                                  fill='black', font=self.table.thefont,
                                  tag='text', anchor=align)
                r+=1
        return

    def setWidth(self, w):
        """Set width"""
        self.width = w
        self.redraw()
        return

    def clearSelected(self):
        """Clear selected rows"""
        self.delete('rect')
        return

    def handle_left_click(self, event):
        """Handle left click"""
        rowclicked = self.table.get_row_clicked(event)
        self.startrow = rowclicked
        if 0 <= rowclicked < self.table.rows:
            self.delete('rect')
            self.table.delete('entry')
            self.table.delete('multicellrect')
            #set row selected
            self.table.setSelectedRow(rowclicked)
            self.table.drawSelectedRow()
            self.drawSelectedRows(self.table.currentrow)
        return

    def handle_left_release(self,event):
        return

    def handle_left_ctrl_click(self, event):
        """Handle ctrl clicks - for multiple row selections"""

        rowclicked = self.table.get_row_clicked(event)
        multirowlist = self.table.multiplerowlist
        if 0 <= rowclicked < self.table.rows:
            if rowclicked not in multirowlist:
                multirowlist.append(rowclicked)
            else:
                multirowlist.remove(rowclicked)
            self.table.drawMultipleRows(multirowlist)
            self.drawSelectedRows(multirowlist)
        return

    def handle_right_click(self, event):
        """respond to a right click"""

        self.delete('tooltip')
        #self.tablerowheader.clearSelected()
        if hasattr(self, 'rightmenu'):
            self.rightmenu.destroy()
        #rowclicked = self.get_row_clicked(event)
        self.rightmenu = self.popupMenu(event, outside=1)
        return

    def handle_mouse_drag(self, event):
        """Handle mouse moved with button held down, multiple selections"""

        if hasattr(self, 'cellentry'):
            self.cellentry.destroy()
        rowover = self.table.get_row_clicked(event)
        colover = self.table.get_col_clicked(event)
        if rowover == None:
            return
        if rowover >= self.table.rows or self.startrow > self.table.rows:
            return
        else:
            self.endrow = rowover
        #draw the selected rows
        if self.endrow != self.startrow:
            if self.endrow < self.startrow:
                rowlist=list(range(self.endrow, self.startrow+1))
            else:
                rowlist=list(range(self.startrow, self.endrow+1))
            self.drawSelectedRows(rowlist)
            self.table.multiplerowlist = rowlist
            self.table.drawMultipleRows(rowlist)
        else:
            self.table.multiplerowlist = []
            self.table.multiplerowlist.append(rowover)
            self.drawSelectedRows(rowover)
            self.table.drawMultipleRows(self.table.multiplerowlist)
        return

    def toggleIndex(self):
        """Toggle index display"""

        if self.showindex == True:
            self.showindex = False
        else:
            self.showindex = True
        self.redraw()
        return

    def popupMenu(self, event, rows=None, cols=None, outside=None):
        """Add left and right click behaviour for canvas, should not have to override
            this function, it will take its values from defined dicts in constructor"""

        defaultactions = {"Sort by index" : lambda: self.table.sortTable(index=True),
                         "Reset index" : lambda: self.table.resetIndex(),
                         "Toggle index" : lambda: self.toggleIndex(),
                         "Copy index to column" : lambda: self.table.copyIndex(),
                         "Select All" : self.table.selectAll}
        main = ["Sort by index","Reset index","Toggle index","Copy index to column"]

        popupmenu = Menu(self, tearoff = 0)
        def popupFocusOut(event):
            popupmenu.unpost()
        for action in main:
            popupmenu.add_command(label=action, command=defaultactions[action])

        popupmenu.bind("<FocusOut>", popupFocusOut)
        popupmenu.focus_set()
        popupmenu.post(event.x_root, event.y_root)
        return popupmenu

    def drawSelectedRows(self, rows=None):
        """Draw selected rows, accepts a list or integer"""

        self.delete('rect')
        if type(rows) is not list:
            rowlist=[]
            rowlist.append(rows)
        else:
           rowlist = rows
        for r in rowlist:
            if r not in self.table.visiblerows:
                continue
            self.drawRect(r, delete=0)
        return

    def drawRect(self, row=None, tag=None, color=None, outline=None, delete=1):
        """Draw a rect representing row selection"""

        if tag==None:
            tag='rect'
        if color==None:
            color='#0099CC'
        if outline==None:
            outline='gray25'
        if delete == 1:
            self.delete(tag)
        w=0
        i = self.inset
        x1,y1,x2,y2 = self.table.getCellCoords(row, 0)
        rect = self.create_rectangle(0+i,y1+i,self.width-i,y2,
                                      fill=color,
                                      outline=outline,
                                      width=w,
                                      tag=tag)
        self.lift('text')
        return
