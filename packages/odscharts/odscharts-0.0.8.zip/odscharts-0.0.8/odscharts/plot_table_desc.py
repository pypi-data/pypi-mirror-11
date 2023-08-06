"""
A PlotTableDesc object holds the XML logic as well as all info about a 
scatter plot table
"""
import sys
if sys.version_info < (3,):
    import ElementTree_27OD as ET
else:
    import ElementTree_34OD as ET

from color_utils import EXCEL_COLOR_LIST


class PlotTableDesc(object):
    """Holds a description of a scatter plot sheet.
    """

    def get_next_color(self):
        """
        Return the next color in the list.
        Increment counter for next color.
        i_color and color_list are initialized in spreadsheet
        """
        i = self.i_color
        self.i_color += 1
        c = self.color_list[ i % len(self.color_list) ]
        
        #print( 'i_color = %i,  color = "%s"'%(i,c) )
        
        return c

    def __init__(self, plot_sheetname, num_chart, parent_obj):
        """Inits SpreadSheet with filename and blank content.
        
        NS: cleans up the namespace callouts of the xml Element
        
        Attributes::
        
            plot_sheetname: name of data sheet
        
        """
        self.i_color = 0 # index into color chart for next curve
        self.color_list = EXCEL_COLOR_LIST[:] # copy of default color list (reinitialized in spreadsheet)
        
        NS = parent_obj.NS
        
        # Start building new xml Element to be new Sheet in spreadsheet
        attribD = {NS('table:name'):plot_sheetname}
        newsheet = ET.Element(NS('table:table'), attrib=attribD)

        table_shapes  = ET.Element(NS('table:shapes'))
        #print( 'table_shapes.text =',table_shapes.text )
        
        def NS_attrib( attD ):
            D = {}
            for key,val in attD.items():
                D[ NS(key) ] = val
            return D
        
        attribD = NS_attrib({ 'draw:z-index':"1", 'draw:id':"id0", 'draw:style-name':"a0", 'draw:name':"Chart 1", 'svg:x':"0in",
                     'svg:y':"0in", 'svg:width':"9.47551in", 'svg:height':"6.88048in", 'style:rel-width':"scale",
                     'style:rel-height':"scale"})
        draw_frame = ET.Element(NS('draw:frame'), attrib=attribD)

        attribD = NS_attrib({'xlink:href':"Object %i/"%num_chart, 'xlink:type':"simple", 'xlink:show':"embed", 'xlink:actuate':"onLoad"})
        draw_obj = ET.Element(NS('draw:object'), attrib=attribD)
        
        svg_title  = ET.Element(NS('svg:title'))
        svg_desc  = ET.Element(NS('svg:desc'))
        
        draw_frame.append( draw_obj )
        draw_frame.append( svg_title )
        draw_frame.append( svg_desc )
        table_shapes.append( draw_frame )
        
        
        tab_col = ET.Element(NS('table:table-column'), attrib={NS('table:number-columns-repeated'):"16384"})
        tab_row = ET.Element(NS('table:table-row'), attrib={NS('table:number-rows-repeated'):"1048576"})
        tab_cell = ET.Element(NS('table:table-cell'), attrib={NS('table:number-columns-repeated'):"16384"})
        tab_row.append( tab_cell )
        
        
        newsheet.append( table_shapes )
        newsheet.append( tab_col )
        newsheet.append( tab_row )

        # make sure any added Element objects are in nsOD, rev_nsOD and qnameOD of parent_obj
        def add_tag( tag ):
            sL = tag.split('}')
            uri = sL[0][1:]
            name = sL[1]
            parent_obj.qnameOD[tag] = parent_obj.nsOD[uri] + ':' + name
            
        def add_tags( obj ):
            if hasattr(obj,'tag'):
                add_tag( obj.tag )
            if hasattr(obj, 'attrib'):
                for q,v in obj.attrib.items():
                    add_tag( q )
        
        for parent in newsheet.iter():
            add_tags( parent )
            for child in parent.getchildren():
                add_tags( child )
                
                
        self.xmlSheetObj = newsheet
        
        
        self.plot_sheetname = ''
        self.data_sheetname = ''
        self.title = ''
        self.xlabel = ''
        self.ylabel = ''
        self.y2label = ''
        self.ycolL = None
        self.ycol2L = None
        
        self.logx = False
        self.logy = False
        self.log2y = False
        
        self.xcolL = []
        self.ycolDataSheetNameL = []
                
        self.xcol2L = []
        self.ycol2_DataSheetNameL = []
        
        self.showMarkerL = None
        self.showMarker2L = None
        self.showUnits = True
        
        self.colorL = None
        self.color2L = None
        
        self.labelL = None
        self.label2L = None
        
    def add_to_primary_y(self, data_sheetname, xcol, ycolL, showMarkerL=None, colorL=None, labelL=None):
        """
        Add new curves to primary y axis
        """
        if ycolL is None:
            return
            
        if self.colorL is None:
            self.colorL = []
            self.labelL = []
            self.showMarkerL = []
            self.ycolL = []
            self.xcolL = []
            self.ycolDataSheetNameL = []
        
        for i,ycol in enumerate(ycolL):
            self.ycolL.append( ycol )
            self.xcolL.append( xcol )
            self.ycolDataSheetNameL.append( data_sheetname )
            
            self.colorL.append( get_ith_color_value( colorL, i, None ) )
            self.labelL.append( get_ith_value( labelL, i, None ) )
            
            if len(self.showMarkerL):
                self.showMarkerL.append( get_ith_value( showMarkerL, i, self.showMarkerL[-1] ) )
            else:
                self.showMarkerL.append( get_ith_value( showMarkerL, i, True ) )
            
        
    def add_to_secondary_y(self, data_sheetname, xcol, ycol2L, showMarker2L=None, color2L=None, label2L=None):
        """
        Add new curves to primary y axis
        """
        if ycol2L is None:
            return
        
        if self.color2L is None:
            self.color2L = []
            self.label2L = []
            self.showMarker2L = []
            self.ycol2L = []
            self.xcol2L = []
            self.ycol2_DataSheetNameL = []
        
        for i,ycol in enumerate(ycol2L):
            self.ycol2L.append( ycol )
            self.xcol2L.append( xcol )
            self.ycol2_DataSheetNameL.append( data_sheetname )
            
            self.color2L.append( get_ith_color_value( color2L, i, None ) )
            self.label2L.append( get_ith_value( label2L, i, None ) )
            
            if len(self.showMarker2L):
                self.showMarker2L.append( get_ith_value( showMarker2L, i, self.showMarker2L[-1] ) )
            else:
                self.showMarker2L.append( get_ith_value( showMarker2L, i, True ) )
            
            
def get_ith_value( valL, i, default_val ):
    """Return the ith value in valL if possible, otherwise default_val"""    
    
    try:
        val = valL[i]
    except:
        val = default_val
    return val
            

def get_ith_color_value( colorL, i, default_val ):
    """Return the ith value in valL if possible, otherwise default_val"""    
    
    try:
        val = colorL[i]
    except:
        val = default_val

    c = '%s'%val # make sure it's a string
    if c.startswith('#') and len(c)==7:
        return c
    else:
        return default_val

                
                
        
