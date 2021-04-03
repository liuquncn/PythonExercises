#Boa:Dialog:Dialog1

import wx
import wx.grid

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1GRID1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class Dialog1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(515, 238), size=wx.Size(400, 308),
              style=wx.DEFAULT_DIALOG_STYLE, title='Dialog1')
        self.SetClientSize(wx.Size(392, 264))

        self.grid1 = wx.grid.Grid(id=wxID_DIALOG1GRID1, name='grid1',
              parent=self, pos=wx.Point(72, 24), size=wx.Size(200, 100),
              style=0)
        self.grid1.SetCellHighlightPenWidth(2)

    def __init__(self, parent):
        self._init_ctrls(parent)
