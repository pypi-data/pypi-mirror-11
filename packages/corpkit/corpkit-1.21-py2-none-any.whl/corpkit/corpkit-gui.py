#!usr/bin/python

# corpkit GUI
# Daniel McDonald
# Template created by: Patrick T. Cossette <cold_soul79078@yahoo.com>

import Tkinter
from Tkinter import *
import sys,string
import threading
import ScrolledText
import time
from time import strftime, localtime

########################################################################

# stdout to app
class RedirectText(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, text_ctrl):
        """Constructor"""
        self.output = text_ctrl
 
    #----------------------------------------------------------------------
    def write(self, string):
        """"""
        import re
        reg = re.compile(r'^\s*$')
        if not re.match(reg, string):
            self.output.insert(Tkinter.END, '\n' + string.replace('\r', ''))
 
class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self,str):
        self.text_area.write(str,False)

class Notebook(Frame):

    """Notebook Widget"""
    def __init__(self, parent, activerelief = RAISED, inactiverelief = RIDGE, xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw):
        """Construct a Notebook Widget

        Notebook(self, parent, activerelief = RAISED, inactiverelief = RIDGE, xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw)        
    
        Valid resource names: background, bd, bg, borderwidth, class,
        colormap, container, cursor, height, highlightbackground,
        highlightcolor, highlightthickness, relief, takefocus, visual, width, activerelief,
        inactiverelief, xpad, ypad.

        xpad and ypad are values to be used as ipady and ipadx
        with the Label widgets that make up the tabs. activefg and inactivefg define what
        color the text on the tabs when they are selected, and when they are not

        """
                                                                                           #Make various argument available to the rest of the class
        self.activefg = activefg                                                           
        self.inactivefg = inactivefg
        self.deletedTabs = []        
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief                                               
        self.kwargs = kw                                                                   
        self.tabVars = {}                                                                  #This dictionary holds the label and frame instances of each tab
        self.tabs = 0                                                                      #Keep track of the number of tabs                                                                             
        self.noteBookFrame = Frame(parent)                                                 #Create a frame to hold everything together
        self.BFrame = Frame(self.noteBookFrame)
        self.statusbar = Frame(self.noteBookFrame, bd = 2, height = 25, width = kw['width'])                                            #Create a frame to put the "tabs" in
        self.noteBook = Frame(self.noteBookFrame, relief = RAISED, bd = 2, **kw)           #Create the frame that will parent the frames for each tab
        self.noteBook.grid_propagate(0)
        self.text = Text(self.statusbar, height = 0.5, font = ("Courier New", 15), width = 135)
        self.text.grid()
        # alternative ...
        #self.text = Text(self.statusbar, height = 1, undo = True)
        self.text.update_idletasks()

        def xcallback(*args):
            self.text.see(END)
            self.text.edit_modified(0)
        self.text.bind('<<Modified>>', xcallback)

        self.redir = RedirectText(self.text)
        sys.stdout = self.redir
        sys.stderr = self.redir

        #self.statusbar.grid_propagate(0)                                                    #self.noteBook has a bad habit of resizing itself, this line prevents that
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row = 0, column = 0, columnspan = 27, sticky = N) # ", column = 13)" puts the tabs in the middle!
        self.noteBook.grid(row = 1, column = 0, columnspan = 27)
        self.statusbar.grid(row = 2)

    def change_tab(self, IDNum):
        """Internal Function"""
        
        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if not i in self.deletedTabs:                                                  #Make sure tab hasen't been deleted
                if i <> IDNum:                                                             #Check to see if the tab is the one that is currently selected
                    self.tabVars[i][1].grid_remove()                                       #Remove the Frame corresponding to each tab that is not selected
                    self.tabVars[i][0]['relief'] = self.inactiverelief                     #Change the relief of all tabs that are not selected to "Groove"
                    self.tabVars[i][0]['fg'] = self.inactivefg                             #Set the fg of the tab, showing it is selected, default is black
                else:                                                                      #When on the tab that is currently selected...
                    self.tabVars[i][1].grid()                                              #Re-grid the frame that corresponds to the tab                      
                    self.tabVars[IDNum][0]['relief'] = self.activerelief                   #Change the relief to "Raised" to show the tab is selected
                    self.tabVars[i][0]['fg'] = self.activefg                               #Set the fg of the tab, showing it is not selected, default is black

    def add_tab(self, width = 2, **kw):
        import Tkinter
        """Creates a new tab, and returns its corresponding frame

        """
        
        temp = self.tabs
        self.tabVars[self.tabs] = [Label(self.BFrame, relief = RIDGE, **kw)]               #Create the tab
        self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event:self.change_tab(temp))  #Makes the tab "clickable"
        self.tabVars[self.tabs][0].pack(side = LEFT, ipady = self.ypad, ipadx = self.xpad) #Packs the tab as far to the left as possible
        self.tabVars[self.tabs].append(Frame(self.noteBook, **self.kwargs))                #Create Frame, and append it to the dictionary of tabs
        self.tabVars[self.tabs][1].grid(row = 0, column = 0)                               #Grid the frame ontop of any other already existing frames
        self.change_tab(0)                                                                 #Set focus to the first tab
        self.tabs += 1                                                                     #Update the tab count
        return self.tabVars[temp][1]                                                       #Return a frame to be used as a parent to other widgets

    def destroy_tab(self, tab):
        """Delete a tab from the notebook, as well as it's corresponding frame

        """
        
        self.iteratedTabs = 0                                                              #Keep track of the number of loops made
        for b in self.tabVars.values():                                                    #Iterate through the dictionary of tabs
            if b[1] == tab:                                                                #Find the NumID of the given tab
                b[0].destroy()                                                             #Destroy the tab's frame, along with all child widgets
                self.tabs -= 1                                                             #Subtract one from the tab count
                self.deletedTabs.append(self.iteratedTabs)                                 #Apend the NumID of the given tab to the list of deleted tabs
                break                                                                      #Job is done, exit the loop
            self.iteratedTabs += 1                                                         #Add one to the loop count
    
    def focus_on(self, tab):
        """Locate the IDNum of the given tab and use
        change_tab to give it focus

        """
        
        self.iteratedTabs = 0                                                              #Keep track of the number of loops made
        for b in self.tabVars.values():                                                    #Iterate through the dictionary of tabs
            if b[1] == tab:                                                                #Find the NumID of the given tab
                self.change_tab(self.iteratedTabs)                                         #send the tab's NumID to change_tab to set focus, mimicking that of each tab's event bindings
                break                                                                      #Job is done, exit the loop
            self.iteratedTabs += 1                                                         #Add one to the loop count

def corpkit_gui():
    import Tkinter, Tkconstants, tkFileDialog, tkMessageBox, tkSimpleDialog
    from Tkinter import StringVar, Listbox, Text
    import sys
    from tkintertable import TableCanvas, TableModel
    import os
    import corpkit

    # add tregex to path
    corpath = os.path.dirname(corpkit.__file__)
    baspat = os.path.dirname(os.path.dirname(corpkit.__file__))
    dicpath = os.path.join(baspat, 'dictionaries')
    os.environ["PATH"] += os.pathsep + corpath + os.pathsep + dicpath
    sys.path.append(corpath)
    sys.path.append(dicpath)
    sys.path.append(baspat)

# these add to pythonpath, mostly so we can find dictionaries
# doesn't seem to be working at the moment, though.

    #from dictionaries.process_types import process_types
    #from dictionaries.roles import roles
    #from dictionaries.wordlists import wordlists
    #from corpkit import interrogator, editor, plotter

    def adjustCanvas(someVariable = None):
        fontLabel["font"] = ("arial", var.get())

    # key binding
    if sys.platform == 'darwin':
        key = 'Mod1'
    else:
        key = 'Control'
    
    root = Tk()
    root.title("corpkit")
    root.resizable(FALSE,FALSE)

    #HWHW h 550
    note = Notebook(root, width= 1250, height = 600, activefg = 'red', inactivefg = 'blue')  #Create a Note book Instance
    note.grid()
    tab0 = note.add_tab(text = "Build")
    tab1 = note.add_tab(text = "Interrogate")                                                  #Create a tab with the text "Tab One"
    tab2 = note.add_tab(text = "Edit")                                                  #Create a tab with the text "Tab Two"
    tab3 = note.add_tab(text = "Visualise")                                                    #Create a tab with the text "Tab Three"
    tab4 = note.add_tab(text = "Concordance")                                                 #Create a tab with the text "Tab Four"
    tab5 = note.add_tab(text = "Manage")                                                 #Create a tab with the text "Tab Five"
    #Label(tab1, text = 'Tab one').grid(row = 0, column = 0)                                #Use each created tab as a parent, etc etc...
    
    note.text.see(Tkinter.END)
    note.text.yview_pickplace("end")
    note.text.update_idletasks()

    ###################     ###################     ###################     ###################
    # INTERROGATE TAB #     # INTERROGATE TAB #     # INTERROGATE TAB #     # INTERROGATE TAB #
    ###################     ###################     ###################     ###################

    # a dict of the editor frame names and models
    editor_tables = {}
    currently_in_each_frame = {}
    sort_direction = True

    def convert_pandas_dict_to_ints(dict_obj):
        vals = []
        for a, b in dict_obj.items():
            # c = year, d = count
            for c, d in b.items():
                vals.append(d)
        if all([float(x).is_integer() for x in vals if is_number(x)]):
            for a, b in dict_obj.items():
                for c, d in b.items():
                    if is_number(d):
                        b[c] = int(d)
        return dict_obj

    def update_spreadsheet(frame_to_update, df_to_show = None, model = False, height = 140, width = False, indexwidth = 70, just_default_sort = False):
        """refresh a spreadsheet in the editor window"""
        from collections import OrderedDict
        import pandas
        kwarg = {}
        if width:
            kwarg['width'] = width
        if model and not df_to_show:
            df_to_show = make_df_from_model(model)
            if need_make_totals:
                df_to_show = make_df_totals(df_to_show)
        if df_to_show is not None:
            if just_default_sort is False:    
                # for abs freq, make total
                model = TableModel()
                df_to_show = pandas.DataFrame(df_to_show, dtype = object)
                if need_make_totals(df_to_show):
                    df_to_show = make_df_totals(df_to_show)
                
                # turn pandas into dict
                raw_data = df_to_show.to_dict()
                
                # convert to int if possible
                raw_data = convert_pandas_dict_to_ints(raw_data)
                        
                table = TableCanvas(frame_to_update, model=model, 
                                    showkeynamesinheader=True, 
                                    height = height,
                                    rowheaderwidth=indexwidth,
                                    **kwarg)
                table.createTableFrame()
                model = table.model
                model.importDict(raw_data) #can import from a dictionary to populate model            
                for index, name in enumerate(list(df_to_show.index)):
                    model.moveColumn(model.getColumnIndex(name), index)
                table.createTableFrame()
                if 'tkintertable-order' in list(df_to_show.index):
                    table.sortTable(columnName = 'tkintertable-order')
                    ind = model.columnNames.index('tkintertable-order')
                    try:
                        model.deleteColumn(ind)
                    except:
                        pass
                else:
                    table.sortTable(reverse = 1)
            else:
                table = TableCanvas(frame_to_update, model=model, 
                                    showkeynamesinheader=True, 
                                    height = height,
                                    rowheaderwidth=indexwidth,
                                    **kwarg)
                table.createTableFrame()
                table.sortTable(columnName = 'Total', reverse = direct())

            table.redrawTable()
            editor_tables[frame_to_update] = model
            currently_in_each_frame[frame_to_update] = df_to_show
            return
        if model:
            table = TableCanvas(frame_to_update, model=model, 
                                showkeynamesinheader=True, 
                                height = height,
                                rowheaderwidth=indexwidth,
                                **kwarg)
            table.createTableFrame()
            try:
                table.sortTable(columnName = 'Total', reverse = direct())
            except:
                direct()           
                table.sortTable(reverse = direct())
            table.createTableFrame()            # sorts by total freq, ok for now
            table.redrawTable()
        else:
            table = TableCanvas(frame_to_update, height = height, width = width)
            table.createTableFrame()            # sorts by total freq, ok for now
            table.redrawTable()

    def remake_special_query(query):
        lst_of_specials = ['PROCESSES:', 'ROLES:', 'WORDLISTS:']
        if any([special in query for special in lst_of_specials]):
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: Special query detected. Loading wordlists ... ' % thetime
            from dictionaries.process_types import processes
            from dictionaries.roles import roles
            from dictionaries.wordlists import wordlists
            dict_of_specials = {'PROCESSES:': processes, 'ROLES:': roles, 'WORDLISTS:': wordlists}
            for special in lst_of_specials:
                # temporary, to show off process type searching.
                if special == 'PROCESSES:':
                    lemmatag = 'v'
                from corpkit import as_regex
                if special in query:
                    types = [k for k in dict_of_specials[special]._asdict().keys()]
                    reg = re.compile('(^.*)(%s)(:)([A-Z]+)(.*$)' % special[:-1])
                    divided = re.search(reg, query)
                    if special == 'PROCESSES:':
                        the_bound = 'w'
                    if special == 'ROLES:':
                        the_bound = False
                    if special == 'WORDLISTS:':
                        the_bound = 'w'
                    try:
                        lst_of_matches = dict_of_specials[special]._asdict()[divided.group(4).lower()]
                        asr = as_regex(lst_of_matches, 
                                       boundaries = the_bound, 
                                       case_sensitive = case_sensitive.get(), 
                                       inverse = False)
                        query = divided.group(1) + asr + divided.group(5)
                    except:
                        thetime = strftime("%H:%M:%S", localtime())
                        print '%s: "%s" must be: %s' % (thetime, divided.group(4), ', '.join(dict_of_specials[special]._asdict().keys()))
                        return False
        return query


    def need_make_totals(df):
        try:
            x = df.iloc[0,0]
        except:
            return False
        vals = [i for i in list(df.iloc[0,].values) if is_number(i)]
        if len(vals) == 0:
            return False
        if all([float(x).is_integer() for x in vals]):
            return True
        else:
            return False

    def make_df_totals(df):   
        df = df.drop('Total', errors = 'ignore')
        # add new totals
        df.ix['Total'] = df.drop('tkintertable-order', errors = 'ignore').sum().astype(object)
        return df

    def make_df_from_model(model):
        import pandas
        from StringIO import StringIO
        recs = model.getAllCells()
        colnames = model.columnNames
        collabels = model.columnlabels
        row=[]
        csv_data = []
        for c in colnames:
            row.append(collabels[c])
        csv_data.append(','.join([unicode(s, errors = 'ignore') for s in row]))
        #csv_data.append('\n')
        for row in recs.keys():
            rowname = model.getRecName(row)
            csv_data.append(','.join([unicode(rowname, errors = 'ignore')] + [unicode(s, errors = 'ignore') for s in recs[row]]))
            #csv_data.append('\n')
            #writer.writerow(recs[row])
        csv = '\n'.join(csv_data)
        newdata = pandas.read_csv(StringIO(csv), index_col=0, header=0)
        newdata = pandas.DataFrame(newdata, dtype = object)
        newdata = newdata.T
        newdata = newdata.drop('Total', errors = 'ignore')
        newdata = add_tkt_index(newdata)
        if need_make_totals(newdata):
            newdata = make_df_totals(newdata)
        return newdata

    def refresh():
        """refreshes the list of dataframes in the editor and plotter panes"""
        # Reset name_of_o_ed_spread and delete all old options
        # get the latest only after first interrogation
        if len(all_interrogations.keys()) == 1:
            selected_to_edit.set(all_interrogations.keys()[-1])
        dataframe1s['menu'].delete(0, 'end')
        dataframe2s['menu'].delete(0, 'end')
        if len(all_interrogations.keys()) > 0:
            data_to_plot.set(all_interrogations.keys()[-1])
        every_interrogation['menu'].delete(0, 'end')
        every_interro_listbox.delete(0, 'end')
        new_choices = []
        for interro in all_interrogations.keys():
            new_choices.append(interro)
        new_choices = tuple(new_choices)
        dataframe2s['menu'].add_command(label='Self', command=Tkinter._setit(data2_pick, 'Self'))
        for choice in new_choices:
            dataframe1s['menu'].add_command(label=choice, command=Tkinter._setit(selected_to_edit, choice))
            dataframe2s['menu'].add_command(label=choice, command=Tkinter._setit(data2_pick, choice))
            every_interrogation['menu'].add_command(label=choice, command=Tkinter._setit(data_to_plot, choice))
            #every_interro_listbox.delete(0, END)
            if choice != 'None':
                every_interro_listbox.insert(END, choice)

    def add_tkt_index(df):
        import pandas
        """add order to df for tkintertable"""
        df = df.T
        df = df.drop('tkintertable-order', errors = 'ignore', axis = 1)
        df['tkintertable-order'] = pandas.Series([index for index, data in enumerate(list(df.index))], index = list(df.index))
        df = df.T
        return df

    def namer(name_box_text, type_of_data = 'interrogation'):
        """returns a name to store interrogation/editor result as"""
        
        if name_box_text.lower() == 'untitled' or name_box_text == '':
            c = 0
            the_name = '%s-%s' % (type_of_data, str(c).zfill(2))
            while the_name in all_interrogations.keys():
                c += 1
                the_name = '%s-%s' % (type_of_data, str(c).zfill(2))
        else:
            the_name = name_box_text
        return the_name

    transdict = {
            'Get distance from root for regex match': 'a',
            'Get tag and word of match': 'b',
            'Count matches': 'c',
            'Get "role:dependent", matching governor': 'd',
            'Get semantic role of match': 'f',
            'Get "role:governor", matching dependent': 'g',
            'Get lemmata via dependencies': 'l',
            'Get tokens by dependency role': 'm',
            'Get dependency index of regular expression match': 'n',
            'Get part-of-speech tag': 'p',
            'Regular expression search': 'r',
            'Simple search string search': 's',
            'Match tokens via dependencies': 't',
            'Get words': 'w'}

    option_dict = {'Trees': ['Get words', 
                             'Get tag and word of match', 
                             #'Count matches', 
                             'Get part-of-speech tag'],
                   'Dependencies':
                            ['Get "role:dependent", matching governor',
                             'Get semantic role of match',
                             'Get "role:governor", matching dependent',
                             'Get lemmata via dependencies',
                             'Get tokens by dependency role',
                             'Match tokens via dependencies',
                             'Get distance from root for regex match'],
                   'Plaintext': 
                            ['Regular expression search', 
                             'Simple search string search']}

    sort_trans = {'None': False,
                  'Total': 'total',
                  'Inverse total': 'infreq',
                  'Name': 'name',
                  'Increase': 'increase',
                  'Decrease': 'decrease',
                  'Static': 'static',
                  'Turbulent': 'turbulent'}

    spec_quer_translate = {'Participants': 'participants',
                           'Any': 'any',
                           'Processes': 'processes',
                           'Subjects': 'subjects',
                           'Entities': 'entities'}

    # not currently using this sort feature---should use in conc though
    import itertools
    direct = itertools.cycle([0,1]).next

    def data_sort(pane = 'interrogate', sort_direction = False):
        """sort spreadsheets ... not currently used"""
        import pandas
        if pane == 'interrogate':
            df = make_df_from_model(editor_tables[interro_results])
            if need_make_totals(df):
                df = make_df_totals(df)
            df_tot = pandas.DataFrame(df.sum(), dtype = object)
            update_spreadsheet(interro_results, df_to_show = df, height = 340, just_default_sort = True, width = 650)
            update_spreadsheet(interro_totals, df_to_show = df_tot, height = 10, just_default_sort = True, width = 650)
        elif pane == 'edit':
            df = make_df_from_model(editor_tables[o_editor_results])
            if need_make_totals(df):
                df = make_df_totals(df)
            df_tot = pandas.DataFrame(df.sum(), dtype = object)
            update_spreadsheet(o_editor_results, df_to_show = df, height = 340, model = editor_tables[o_editor_results], just_default_sort = True, width = 720)
            update_spreadsheet(o_editor_totals, df_to_show = df_tot, height = 10, model = editor_tables[o_editor_totals], just_default_sort = True, width = 720)
            df = make_df_from_model(editor_tables[n_editor_results])
            if need_make_totals(df):
                df = make_df_totals(df)
            df_tot = pandas.DataFrame(df.sum(), dtype = object)
            update_spreadsheet(n_editor_results, df_to_show = None, height = 340, model = editor_tables[n_editor_results], just_default_sort = True, width = 720)
            update_spreadsheet(n_editor_totals, df_to_show = None, height = 10, model = editor_tables[n_editor_totals], just_default_sort = True, width = 720)
        elif pane == 'plot':
            pass

    def do_interrogation():
        """performs an interrogation"""
        import pandas
        from corpkit import interrogator
        
        # spelling conversion?
        conv = (spl.var).get()
        if conv == 'Convert spelling' or conv == 'Off':
            conv = False
        
        # lemmatag: do i need to add as button if trees?
        lemmatag = False

        # special query: add to this list!
        if special_queries.get() != 'Off':
            query = spec_quer_translate[special_queries.get()]
        
        else:
            query = entrytext.get()
            # allow list queries
            if query.startswith('[') and query.endswith(']'):
                query = query.lstrip('[').rstrip(']').replace("'", '').replace('"', '').replace(' ', '').split(',')
            else:
                # convert special stuff
                query = remake_special_query(query)

        if funfil.get() is not False and funfil.get() != '':
            ff = remake_special_query(funfil.get())
        else:
            ff = False

        # dep type
        depdict = {'Basic': 'basic-dependencies', 
                   'Collapsed': 'collapsed-dependencies', 
                   'CC-processed': 'collapsed-ccprocessed-dependencies'}

        # make name
        the_name = namer(nametext.get(), type_of_data = 'interrogation')
        
        selected_option = transdict[datatype_chosen_option.get()]
        interrogator_args = {'query': query,
                             'lemmatise': lem.get(),
                             'phrases': phras.get(),
                             'titlefilter': tit_fil.get(),
                             'case_sensitive': case_sensitive.get(),
                             'convert_spelling': conv,
                             'root': root,
                             'function_filter': ff,
                             'dep_type': depdict[kind_of_dep.get()]}

        if lemmatag:
            interrogator_args['lemmatag'] = lemmatag

        pf = posfil.get()
        if pf is not False and pf != '':
            interrogator_args['pos_filter'] = pf

        if corpus_fullpath.get() == '':
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: You need to select a corpus.' % thetime
            return
    
        r = interrogator(corpus_fullpath.get(), selected_option, **interrogator_args)
        if not r or r == 'Bad query':
            return

        # drop over 1000?
        large = [n for i, n in enumerate(list(r.results.columns)) if i > 9999]
        r.results.drop(large, axis = 1, inplace = True)

        # remove dummy entry from master
        try:
            del all_interrogations['None']
        except KeyError:
            pass

        # add interrogation to master
        all_interrogations[the_name] = r
        name_of_interro_spreadsheet.set(the_name)
        i_resultname.set('Interrogation results: %s' % str(name_of_interro_spreadsheet.get()))

        # total in a way that tkintertable likes
        totals_as_df = pandas.DataFrame(r.totals, dtype = object)

        # update spreadsheets
        if selected_option != 'c':
            update_spreadsheet(interro_results, r.results, height = 340, indexwidth = 70, width = 650)
        update_spreadsheet(interro_totals, totals_as_df, height = 10, indexwidth = 70, width = 650)
        
        refresh()

        Button(tab1, text = 'Update interrogation', command = lambda: update_all_interrogations(pane = 'interrogate')).grid(row = 14, column = 2, sticky = E)

    class MyOptionMenu(OptionMenu):
        """Simple OptionMenu for things that don't change"""
        def __init__(self, tab1, status, *options):
            self.var = StringVar(tab1)
            self.var.set(status)
            OptionMenu.__init__(self, tab1, self.var, *options)
            self.config(font=('calibri',(12)),width=20)
            self['menu'].config(font=('calibri',(10)))
    
    # corpus path setter
    corpus_fullpath = StringVar()
    corpus_fullpath.set('')
    basepath = StringVar()
    basepath.set('Select corpus path')
    subcorpora = {corpus_fullpath.get(): ['None']}

    def getdir():
        import os
        fp = tkFileDialog.askdirectory()
        if not fp:
            return
        corpus_fullpath.set(fp)
        basepath.set('Corpus: "%s"' % os.path.basename(fp))
        subs = sorted([d for d in os.listdir(fp) if os.path.isdir(os.path.join(fp, d))])
        for k in subcorpora.keys():
            del subcorpora[k]
        subcorpora[fp] = subs
        pick_subcorpora['menu'].delete(0, 'end')
        for choice in subs:
            pick_subcorpora['menu'].add_command(label=choice, command=Tkinter._setit(subc_pick, choice))
        time = strftime("%H:%M:%S", localtime())
        print '%s: Set corpus directory: "%s"' % (time, os.path.basename(fp))
    
    Label(tab1, text = 'Corpus directory: ').grid(row = 0, column = 0)
    Button(tab1, textvariable = basepath, command = getdir).grid(row = 0, column = 1, sticky=E)

    # function filter
    funfil = StringVar()
    Label(tab1, text = 'Function filter:').grid(row = 9, column = 0, sticky = W)
    funfil.set(r'(nsubj|nsubjpass)')
    q = Entry(tab1, textvariable = funfil, width = 20, state = DISABLED)
    q.grid(row = 9, column = 0, columnspan = 2, sticky = E)

    # pos filter
    posfil = StringVar()
    Label(tab1, text = 'POS filter:').grid(row = 10, column = 0, sticky = W)
    posfil.set(r'^n')
    qr = Entry(tab1, textvariable = posfil, width = 20, state = DISABLED)
    qr.grid(row = 10, column = 0, columnspan = 2, sticky = E)

    # lemma tags
    lemtags = tuple(('Noun', 'Verb', 'Adjective', 'Adverb'))
    lemtag = StringVar(root)
    lemtag.set('Noun')
    Label(tab1, text = 'Result word class (for lemmatisation):').grid(row = 11, column = 0, sticky = W)
    lmt = OptionMenu(tab1, lemtag, *lemtags)
    lmt.config(state = NORMAL)
    lmt.grid(row = 11, column = 1, sticky=E)
    #lemtag.trace("w", d_callback)

    # dep type
    dep_types = tuple(('Basic', 'Collapsed', 'CC-processed'))
    kind_of_dep = StringVar(root)
    kind_of_dep.set('Basic')
    Label(tab1, text = 'Dependency type:').grid(row = 12, column = 0, sticky = W)
    pick_dep_type = OptionMenu(tab1, kind_of_dep, *dep_types)
    pick_dep_type.config(state = DISABLED)
    pick_dep_type.grid(row = 12, column = 1, sticky=E)
    #kind_of_dep.trace("w", d_callback)

    # query
    entrytext = StringVar()
    Label(tab1, text = 'Query:').grid(row = 4, column = 0, sticky = W)
    entrytext.set(r'JJ > (NP <<# /\brisk/)')
    qa = Entry(tab1, textvariable = entrytext, width = 30)
    qa.grid(row = 4, column = 0, columnspan = 2, sticky = E)

    def onselect(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        callback()
        datatype_chosen_option.set(value)

    def callback(*args):
        """if the drop down list for data type changes, fill options"""
        datatype_listbox.delete(0, 'end')
        chosen = datatype_picked.get()
        lst = option_dict[chosen]
        for e in lst:
            datatype_listbox.insert(END, e)
        if chosen == 'Dependencies':
            pick_dep_type.configure(state = NORMAL)
            q.configure(state = NORMAL)
            qr.configure(state = NORMAL)
            lmt.configure(state = DISABLED)
            entrytext.set(r'\b(m.n|wom.n|child(ren)?)\b')
            if datatype_chosen_option.get() == 'Get tokens by dependency role':
                entrytext.set(r'\b(amod|nn|advm|vmod|tmod)\b')
        else:
            pick_dep_type.configure(state = DISABLED)
            q.configure(state = DISABLED)
            qr.configure(state = DISABLED)
            lmt.configure(state = NORMAL)
        if chosen == 'Trees':
            entrytext.set(r'JJ > (NP <<# /\brisk/)')
        if chosen == 'Plaintext':
            entrytext.set(r'\b(m.n|wom.n|child(ren)?)\b')
            if datatype_chosen_option.get() == 'Simple search string search':
                entrytext.set(r'[cat,cats,mouse,mice,cheese]')
            elif datatype_chosen_option.get() == 'Regular expression search':
                entrytext.set(r'(m.n|wom.n|child(ren)?)')

    datatype_picked = StringVar(root)
    datatype_picked.set('Dependencies')
    Label(tab1, text = 'Kind of data:').grid(row = 1, column = 0)
    pick_a_datatype = OptionMenu(tab1, datatype_picked, *tuple(('Trees', 'Dependencies', 'Plaintext')))
    pick_a_datatype.grid(row = 1, column = 1, sticky=E)
    datatype_picked.trace("w", callback)

    datatype_listbox = Listbox(tab1, selectmode = BROWSE, width = 40)
    datatype_listbox.grid(row = 3, column = 0, columnspan = 2)
    datatype_chosen_option = StringVar()
    datatype_chosen_option.set('Get words')
    #datatype_chosen_option.set('w')
    x = datatype_listbox.bind('<<ListboxSelect>>', onselect)
    # hack: change it now to populate below 
    datatype_picked.set('Trees')
    datatype_listbox.select_set(0)

    def q_callback(*args):
        if special_queries.get() == 'Off':
            q.configure(state=NORMAL)
            qa.configure(state=NORMAL)
            qr.configure(state=NORMAL)
        else:
            q.configure(state=DISABLED)
            qa.configure(state=DISABLED)
            qr.configure(state=DISABLED)

    queries = tuple(('Off', 'Any', 'Participants', 'Processes', 'Subjects'))
    special_queries = StringVar(root)
    special_queries.set('Off')
    Label(tab1, text = 'Preset query:').grid(row = 5, column = 0, sticky = W)
    pick_a_query = OptionMenu(tab1, special_queries, *queries)
    pick_a_query.grid(row = 5, column = 1, sticky=E)
    special_queries.trace("w", q_callback)

    # boolean interrogation arguments
    lem = IntVar()
    Checkbutton(tab1, text="Lemmatise", variable=lem, onvalue = True, offvalue = False).grid(column = 0, row = 6, sticky=W)
    phras = IntVar()
    Checkbutton(tab1, text="Multiword results", variable=phras, onvalue = True, offvalue = False).grid(column = 1, columnspan = 2, row = 6, sticky=W)
    tit_fil = IntVar()
    Checkbutton(tab1, text="Filter titles", variable=tit_fil, onvalue = True, offvalue = False).grid(row = 7, column = 0, sticky=W)
    case_sensitive = IntVar()
    Checkbutton(tab1, text="Case sensitive", variable=case_sensitive, onvalue = True, offvalue = False).grid(row = 7, column = 1, sticky=W)

    Label(tab1, text = 'Normalise spelling:').grid(row = 8, column = 0, sticky = W)
    spl = MyOptionMenu(tab1, 'Off','UK','US')
    spl.grid(row = 8, column = 1, sticky = E)

    # Interrogation name
    nametext = StringVar()
    nametext.set('untitled')
    Label(tab1, text = 'Interrogation name:').grid(row = 13, column = 0, sticky = W)
    Entry(tab1, textvariable = nametext).grid(row = 13, column = 1)

    def query_help():
        tkMessageBox.showwarning('Not yet implemented', 'Coming soon ...')

    # query help, interrogate button
    Button(tab1, text = 'Query help', command = query_help).grid(row = 14, column = 0, sticky = W)
    Button(tab1, text = 'Interrogate!', command = lambda: do_interrogation()).grid(row = 14, column = 1, sticky = E)

    # name to show above spreadsheet 0
    i_resultname = StringVar()
    name_of_interro_spreadsheet = StringVar()
    name_of_interro_spreadsheet.set('')
    i_resultname.set('Interrogation results: %s' % str(name_of_interro_spreadsheet.get()))
    Label(tab1, textvariable = i_resultname, 
          font = ("Helvetica", 12, "bold")).grid(row = 0, 
           column = 2, sticky = W, padx=20, pady=0)    
    
    # make spreadsheet frames for interrogate pane
    interro_results = Frame(tab1, height = 28, width = 20, borderwidth = 2)
    interro_results.grid(column = 2, row = 1, rowspan=10, padx=20, pady=5)

    interro_totals = Frame(tab1, height = 1, width = 20, borderwidth = 2)
    interro_totals.grid(column = 2, row = 11, rowspan=2, padx=20, pady=5)

    # show nothing in them yet
    update_spreadsheet(interro_results, df_to_show = None, height = 340, width = 650)
    update_spreadsheet(interro_totals, df_to_show = None, height = 10, width = 650)

    ##############    ##############     ##############     ##############     ############## 
    # EDITOR TAB #    # EDITOR TAB #     # EDITOR TAB #     # EDITOR TAB #     # EDITOR TAB # 
    ##############    ##############     ##############     ##############     ############## 

    def exchange_interro_branch(namedtupname, newdata, branch = 'results'):
        """replaces a namedtuple results/totals with newdata
           --- such a hack, should upgrade to recordtype"""
        namedtup = all_interrogations[namedtupname]
        if branch == 'results':
            the_branch = namedtup.results
            the_branch.drop(the_branch.index, inplace = True)
            the_branch.drop(the_branch.columns, axis = 1, inplace = True)
            for i in list(newdata.columns):
                the_branch[i] = i
            for index, i in enumerate(list(newdata.index)):
                the_branch.loc[i] = newdata.ix[index]
        elif branch == 'totals':
            the_branch = namedtup.totals
            the_branch.drop(the_branch.index, inplace = True)
            for index, datum in zip(newdata.index, newdata.iloc[:,0].values):
                the_branch.set_value(index, datum)
        all_interrogations[namedtupname] = namedtup

    def update_interrogation(table_id, id, is_total = False):
        """takes any changes made to spreadsheet and saves to the interrogation
        id: 0 = interrogator
            1 = old editor window
            2 = new editor window"""

        model=editor_tables[table_id]
        newdata = make_df_from_model(model)
        if need_make_totals(newdata):
            newdata = make_df_totals(newdata)

        if id == 0:
            name_of_interrogation = name_of_interro_spreadsheet.get()
        if id == 1:
            name_of_interrogation = name_of_o_ed_spread.get()
        if id == 2:
            name_of_interrogation = name_of_n_ed_spread.get()
        if not is_total:
            exchange_interro_branch(name_of_interrogation, newdata, branch = 'results')
        else:
            exchange_interro_branch(name_of_interrogation, newdata, branch = 'totals')

    def update_all_interrogations(pane = 'interrogate'):
        import pandas
        """update all_interrogations within spreadsheet data
        need a very serious cleanup!"""
        # to do: only if they are there
        if pane == 'interrogate':
            update_interrogation(interro_results, id = 0)
            update_interrogation(interro_totals, id = 0, is_total = True)
        if pane == 'edit':
            update_interrogation(o_editor_results, id = 1)
            update_interrogation(o_editor_totals, id = 1, is_total = True)
            # update new editor sheet if it's there
            if name_of_n_ed_spread.get() != '':
                update_interrogation(n_editor_results, id = 2)
                update_interrogation(n_editor_totals, id = 2, is_total = True)
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Updated interrogations with manual data.' % thetime
        if pane == 'interrogate':
            the_data = all_interrogations[name_of_interro_spreadsheet.get()]
            tot = pandas.DataFrame(the_data.totals, dtype = object)
            update_spreadsheet(interro_results, the_data.results, height = 340, indexwidth = 70, width = 650)
            update_spreadsheet(interro_totals, tot, height = 10, indexwidth = 70, width = 650)
        if pane == 'edit':
            the_data = all_interrogations[name_of_o_ed_spread.get()]
            there_is_new_data = False
            try:
                newdata = all_interrogations[name_of_n_ed_spread.get()]
                there_is_new_data = True
            except:
                pass
            update_spreadsheet(o_editor_results, the_data.results, height = 140, indexwidth = 70, width = 720)
            update_spreadsheet(o_editor_totals, pandas.DataFrame(the_data.totals, dtype = object), height = 10, indexwidth = 70, width = 720)
            if there_is_new_data:
                if newdata != 'None' and newdata != '':
                    update_spreadsheet(n_editor_results, newdata.results, indexwidth = 70, height = 140, width = 720)
                    update_spreadsheet(n_editor_totals, pandas.DataFrame(newdata.totals, dtype = object), height = 10, indexwidth = 70, width = 720)
            if name_of_o_ed_spread.get() == name_of_interro_spreadsheet.get():
                the_data = all_interrogations[name_of_interro_spreadsheet.get()]
                tot = pandas.DataFrame(the_data.totals, dtype = object)
                update_spreadsheet(interro_results, the_data.results, height = 340, indexwidth = 70, width = 650)
                update_spreadsheet(interro_totals, tot, height = 10, indexwidth = 70, width = 650)
        
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Updated spreadsheet display in edit window.' % thetime

    def is_number(s):
        """check if str can be added for the below"""
        try:
            float(s) # for int, long and float
        except ValueError:
            try:
                complex(s) # for complex
            except ValueError:
                return False
        return True

    def do_editing():
        """what happens when you press edit"""
        import pandas
        from corpkit import editor

        # translate operation into interrogator input
        operation_text = opp.get()
        if operation_text == 'None' or operation_text == 'Select an operation':
            operation_text = None
        else:
            operation_text = opp.get()[0]
        # translate dataframe2 into interrogator input
        data2 = data2_pick.get()
        if data2 == 'None' or data2 == '' or data2 == 'Self':
            data2 = False

        if data2:
            if df2branch.get() == 'results':
                data2 = all_interrogations[data2].results
            elif df2branch.get() == 'totals':
                data2 = all_interrogations[data2].totals
            if transpose.get():
                data2 = data2.T

        the_data = all_interrogations[name_of_o_ed_spread.get()]
        if df1branch.get() == 'results':
            data1 = the_data.results
        elif df1branch.get() == 'totals':
            data1 = the_data.totals

        if (spl_editor.var).get() == 'Off' or (spl_editor.var).get() == 'Convert spelling':
            spel = False
        else:
            spel = (spl_editor.var).get()

        # editor kwargs
        editor_args = {'operation': operation_text,
                       'dataframe2': data2,
                       'spelling': spel,
                       'sort_by': sort_trans[sort_val.get()],
                       'print_info': False}

        if do_sub.get() == 'Merge':
            editor_args['merge_subcorpora'] = subc_sel_vals
        elif do_sub.get() == 'Keep':
            editor_args['just_subcorpora'] = subc_sel_vals
        elif do_sub.get() == 'Span':
            editor_args['span_subcorpora'] = subc_sel_vals
        elif do_sub.get() == 'Skip':
            editor_args['skip_subcorpora'] = subc_sel_vals

        # special query: add to this list!
        #if special_queries.get() != 'Off':
            #query = spec_quer_translate[special_queries.get()]
        
        entry_do_with = entry_regex.get()
        # allow list queries
        if entry_do_with.startswith('[') and entry_do_with.endswith(']'):
            entry_do_with = entry_do_with.lower().lstrip('[').rstrip(']').replace("'", '').replace('"', '').replace(' ', '').split(',')
        else:
            # convert special stuff
            entry_do_with = remake_special_query(entry_do_with)

        if do_with_entries.get() == 'Merge':
            editor_args['merge_entries'] = entry_do_with
            nn = newname_var.get()
            if nn == '':
                editor_args['newname'] = False
            elif is_number(nn):
                editor_args['newname'] = int(nn)
            else:
                editor_args['newname'] = nn
        elif do_with_entries.get() == 'Keep':
            editor_args['just_entries'] = entry_do_with
        elif do_with_entries.get() == 'Skip':
            editor_args['skip_entries'] = entry_do_with
        
        if new_subc_name.get() != '':
            editor_args['new_subcorpus_name'] = new_subc_name.get()
        if newname_var.get() != '':
            editor_args['new_subcorpus_name'] = newname_var.get()
            
        if keep_stats_setting.get() == 1:
            editor_args['keep_stats'] = True

        if rem_abv_p_set.get() == 1:
            editor_args['remove_above_p'] = True

        if just_tot_setting.get() == 1:
            editor_args['just_totals'] = True

        if transpose.get():
            data1 = data1.T
        
        # do editing
        r = editor(data1, **editor_args)
        
        if not r:
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: Editing caused an error.' % thetime
            return

        if len(list(r.results.columns)) == 0:
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: Editing removed all results.' % thetime
            return

        # drop over 1000?
        large = [n for i, n in enumerate(list(r.results.columns)) if i > 9999]
        r.results.drop(large, axis = 1, inplace = True)

        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Result editing completed successfully.' % thetime
        
        # name the edit
        the_name = namer(edit_nametext.get(), type_of_data = 'edited')

        # add edit to master dict
        all_interrogations[the_name] = r

        # update edited results speadsheet name
        name_of_n_ed_spread.set(all_interrogations.keys()[-1])
        editoname.set('Edited results: %s' % str(name_of_n_ed_spread.get()))
        
        # add current subcorpora to editor menu
        for subcl in [subc_listbox, subc_listbox_build]:
            subcl.configure(state = NORMAL)
            subcl.delete(0, 'end')
            for e in list(r.results.index):
                if 'tkintertable-order' not in e:
                    subcl.insert(END, e)
            subcl.configure(state = DISABLED)

        # update edited spreadsheets
        most_recent = all_interrogations[all_interrogations.keys()[-1]]
        update_spreadsheet(n_editor_results, most_recent.results, height = 140, width = 720)
        update_spreadsheet(n_editor_totals, pandas.DataFrame(most_recent.totals, dtype = object), height = 10, width = 720)
        
        # add button to update
        Button(tab2, text = 'Update interrogation(s)', command = lambda: update_all_interrogations(pane = 'edit')).grid(row = 18, column = 2, sticky = E)
        
        # finish up
        refresh()

    def df_callback(*args):
        """show names and spreadsheets for what is selected as result to edit
           also, hide the edited results section"""
        if selected_to_edit.get() != 'None':
            name_of_o_ed_spread.set(selected_to_edit.get())
            update_spreadsheet(o_editor_results, all_interrogations[name_of_o_ed_spread.get()].results, height = 140, width = 720)
            update_spreadsheet(o_editor_totals, all_interrogations[name_of_o_ed_spread.get()].totals, height = 10, width = 720)
            resultname.set('Results to edit: %s' % str(name_of_o_ed_spread.get()))
        name_of_n_ed_spread.set('')
        editoname.set('Edited results: %s' % str(name_of_n_ed_spread.get()))
        update_spreadsheet(n_editor_results, df_to_show = None, height = 140, width = 720)
        update_spreadsheet(n_editor_totals, df_to_show = None, height = 10, width = 720)
        for subcl in [subc_listbox, subc_listbox_build]:
            subcl.configure(state = NORMAL)
            subcl.delete(0, 'end')
            subcl.configure(state = NORMAL)
            for e in list(all_interrogations[name_of_o_ed_spread.get()].results.index):
                if 'tkintertable-order' not in e:
                    subcl.insert(END, e) 
            subcl.configure(state = DISABLED)       

    # all interrogations here
    from collections import OrderedDict
    all_interrogations = OrderedDict()
    all_interrogations['None'] = 'None'

    # result to edit
    tup = tuple([i for i in all_interrogations.keys()])    
    selected_to_edit = StringVar(root)
    selected_to_edit.set('None')
    x = Label(tab2, text = 'To edit:', font = ("Helvetica", 12, "bold"))
    x.grid(row = 0, column = 0, sticky = W)
    dataframe1s = OptionMenu(tab2, selected_to_edit, *tup)
    dataframe1s.grid(row = 1, column = 0, sticky=W)
    selected_to_edit.trace("w", df_callback)

    # DF1 branch selection
    df1branch = StringVar()
    df1branch.set('results')
    df1box = OptionMenu(tab2, df1branch, 'results', 'totals')
    df1box.grid(row = 1, column = 1, sticky = E)

    def op_callback(*args):
        if opp.get() != 'None':
            dataframe2s.config(state = NORMAL)
            df2box.config(state = NORMAL)
        elif opp.get() == 'None':
            dataframe2s.config(state = DISABLED)
            df2box.config(state = DISABLED)

    # operation for editor
    opp = StringVar(root)
    opp.set('None')
    operations = ('None', '%', '*', '/', '-', '+', 'a', 'd', 'keywords')
    Label(tab2, text='Operation and demonominator:', font = ("Helvetica", 12, "bold")).grid(row = 2, column = 0, sticky = W)
    ops = OptionMenu(tab2, opp, *operations)
    ops.grid(row = 3, column = 0, sticky = W)
    opp.trace("w", op_callback)

    # DF2 option for editor
    tups = tuple(['Self'] + [i for i in all_interrogations.keys()])
    data2_pick = StringVar(root)
    data2_pick.set('Self')
    #Label(tab2, text = 'Denominator:').grid(row = 3, column = 0, sticky = W)
    dataframe2s = OptionMenu(tab2, data2_pick, *tups)
    dataframe2s.config(state = DISABLED)
    dataframe2s.grid(row = 3, column = 0, columnspan = 2, sticky = N)

    # DF2 branch selection
    df2branch = StringVar(root)
    df2branch.set('totals')
    df2box = OptionMenu(tab2, df2branch, 'results', 'totals')
    df2box.config(state = DISABLED)
    df2box.grid(row = 3, column = 1, sticky = E)

    # sort by
    Label(tab2, text = 'Sort results by:', font = ("Helvetica", 12, "bold")).grid(row = 4, column = 0, sticky = W)
    sort_val = StringVar(root)
    sort_val.set('None')
    sorts = OptionMenu(tab2, sort_val, 'None', 'Total', 'Inverse total', 'Name','Increase', 'Decrease', 'Static', 'Turbulent')
    sorts.grid(row = 4, column = 1, sticky = E)

    # spelling again
    Label(tab2, text = 'Spelling:', font = ("Helvetica", 12, "bold")).grid(row = 5, column = 0, sticky = W)
    spl_editor = MyOptionMenu(tab2, 'Off','UK','US')
    spl_editor.grid(row = 5, column = 1, sticky = E)

    # currently broken: just totals button
    just_tot_setting = IntVar()
    just_tot_but = Checkbutton(tab2, text="Just totals", variable=just_tot_setting, state = DISABLED)
    #just_tot_but.select()
    just_tot_but.grid(column = 0, row = 6, sticky = W)

    keep_stats_setting = IntVar()
    keep_stat_but = Checkbutton(tab2, text="Keep stats", variable=keep_stats_setting)
    #keep_stat_but.select()
    keep_stat_but.grid(column = 1, row = 6, sticky = E)

    rem_abv_p_set = IntVar()
    rem_abv_p_but = Checkbutton(tab2, text="Remove above p", variable=rem_abv_p_set)
    #rem_abv_p_but.select()
    rem_abv_p_but.grid(column = 0, row = 7, sticky = W)

    # transpose
    transpose = IntVar()
    trans_but = Checkbutton(tab2, text="Transpose", variable=transpose, onvalue = True, offvalue = False)
    trans_but.grid(column = 1, row = 7, sticky = E)

    subc_sel_vals = []
    # entries + entry field for regex, off, skip, keep, merge
    Label(tab2, text = 'Edit entries:', font = ("Helvetica", 12, "bold")).grid(row = 8, column = 0, sticky = W)
    
    # edit entries regex box
    entry_regex = StringVar()
    entry_regex.set(r'.*ing$')
    edit_box = Entry(tab2, textvariable = entry_regex, state = DISABLED)
    edit_box.grid(row = 9, column = 1, sticky = E)

    # merge entries newname
    Label(tab2, text = 'Merge name:').grid(row = 10, column = 0, sticky = W)
    newname_var = StringVar()
    newname_var.set('')
    mergen = Entry(tab2, textvariable = newname_var, state = DISABLED)
    mergen.grid(row = 11, column = 0)
    
    def do_w_callback(*args):
        """if not merging entries, diable input fields"""
        if do_with_entries.get() != 'Off':
            edit_box.configure(state = NORMAL)
        else:
            edit_box.configure(state = DISABLED)
        if do_with_entries.get() == 'Merge':
            mergen.configure(state = NORMAL)
        else:
            mergen.configure(state = DISABLED)

    # options for editing entries
    do_with_entries = StringVar(root)
    do_with_entries.set('Off')
    edit_ent_op = ('Off', 'Skip', 'Keep', 'Merge')
    ed_op = OptionMenu(tab2, do_with_entries, *edit_ent_op)
    ed_op.grid(row = 9, column = 0, sticky = W)
    do_with_entries.trace("w", do_w_callback)

    def onselect_subc(evt):
        """get selected subcorpora"""
        for i in subc_sel_vals:
            subc_sel_vals.pop()
        wx = evt.widget
        indices = wx.curselection()
        for index in indices:
            value = wx.get(index)
            if value not in subc_sel_vals:
                subc_sel_vals.append(value)

    def do_s_callback(*args):
        """hide subcorpora edit options if off"""
        if do_sub.get() != 'Off':
            subc_listbox.configure(state = NORMAL)
        else:
            subc_listbox.configure(state = DISABLED)
        if do_sub.get() == 'Merge':
            merge.configure(state = NORMAL)
        else:
            merge.configure(state = DISABLED)

    # subcorpora + optionmenu off, skip, keep
    Label(tab2, text = 'Edit subcorpora:', font = ("Helvetica", 12, "bold")).grid(row = 12, column = 0, sticky = W)
    
    subc_listbox = Listbox(tab2, selectmode = EXTENDED, height = 5, state = DISABLED)
    subc_listbox.grid(row = 12, column = 1, rowspan = 5, sticky = E)
    xx = subc_listbox.bind('<<ListboxSelect>>', onselect_subc)
    subc_listbox.select_set(0)

    # subcorpora edit options
    do_sub = StringVar(root)
    do_sub.set('Off')
    do_with_subc = OptionMenu(tab2, do_sub, *('Off', 'Skip', 'Keep', 'Merge', 'Span'))
    do_with_subc.grid(row = 13, column = 0, sticky = W)
    do_sub.trace("w", do_s_callback)

    # subcorpora merge name    
    Label(tab2, text = 'Merge name:').grid(row = 14, column = 0, sticky = 'NW')
    new_subc_name = StringVar()
    new_subc_name.set('')
    merge = Entry(tab2, textvariable = new_subc_name, state = DISABLED)
    merge.grid(row = 15, column = 0, sticky = 'SW')
    
    # name the edit
    edit_nametext = StringVar()
    edit_nametext.set('untitled')
    Label(tab2, text = 'Edit name:', font = ("Helvetica", 12, "bold")).grid(row = 16, column = 0, sticky = W)
    msn = Entry(tab2, textvariable = edit_nametext)
    msn.grid(row = 17, column = 0)

    # edit button
    Button(tab2, text = 'Edit', command = lambda: do_editing()).grid(row = 17, column = 1, sticky = E)

    # show spreadsheets
    resultname = StringVar()
    name_of_o_ed_spread = StringVar()
    name_of_o_ed_spread.set('')
    resultname.set('Results to edit: %s' % str(name_of_o_ed_spread.get()))
    Label(tab2, textvariable = resultname, 
          font = ("Helvetica", 12, "bold")).grid(row = 0, 
           column = 2, sticky = W, padx = 20)    
    o_editor_results = Frame(tab2, height = 20, width = 20)
    o_editor_results.grid(column = 2, row = 1, rowspan=7, padx = 20)
    #Label(tab2, text = 'Totals to edit:', 
          #font = ("Helvetica", 12, "bold")).grid(row = 4, 
           #column = 2, sticky = W, pady=0)
    o_editor_totals = Frame(tab2, height = 1, width = 20)
    o_editor_totals.grid(column = 2, row = 8, rowspan=1, padx = 20)
    update_spreadsheet(o_editor_results, df_to_show = None, height = 140, width = 720)
    update_spreadsheet(o_editor_totals, df_to_show = None, height = 10, width = 720)
    editoname = StringVar()
    name_of_n_ed_spread = StringVar()
    name_of_n_ed_spread.set('')
    editoname.set('Edited results: %s' % str(name_of_n_ed_spread.get()))
    Label(tab2, textvariable = editoname, 
          font = ("Helvetica", 12, "bold")).grid(row = 9, 
           column = 2, sticky = W, padx = 20)        
    n_editor_results = Frame(tab2, height = 30, width = 20)
    n_editor_results.grid(column = 2, row = 10, rowspan=7, padx = 20)
    #Label(tab2, text = 'Edited totals:', 
          #font = ("Helvetica", 12, "bold")).grid(row = 15, 
           #column = 2, sticky = W, padx=20, pady=0)
    n_editor_totals = Frame(tab2, height = 1, width = 20)
    n_editor_totals.grid(column = 2, row =17, rowspan=1, padx = 20)
    update_spreadsheet(n_editor_results, df_to_show = None, height = 140, width = 720)
    update_spreadsheet(n_editor_totals, df_to_show = None, height = 10, width = 720)

    # ????
    #interrogation_name = StringVar()
    #interrogation_name.set('waiting')
    #Label(tab1, textvariable = interrogation_name.get()).grid()
    #root.TEXT_INFO = Label(tab1, height=20, width=80, text="", justify = LEFT, font=("Courier New", 12))

    #################       #################      #################      #################  
    # VISUALISE TAB #       # VISUALISE TAB #      # VISUALISE TAB #      # VISUALISE TAB #  
    #################       #################      #################      #################  

    # where to put the current figure
    thefig = []

    def do_plotting():
        """when you press plot"""
        # junk for showing the plot in tkinter
        import matplotlib
        matplotlib.use('TkAgg')
        from numpy import arange, sin, pi
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
        # implement the default mpl key bindings
        from matplotlib.backend_bases import key_press_handler
        from matplotlib.figure import Figure
        from corpkit import plotter

        if data_to_plot.get() == 'None':
            time = strftime("%H:%M:%S", localtime())
            print '%s: No data selected to plot.' % (time)
            return

        if plotbranch.get() == 'results':
            what_to_plot = all_interrogations[data_to_plot.get()].results
        elif plotbranch.get() == 'totals':
            what_to_plot = all_interrogations[data_to_plot.get()].totals
        
        if transpose_vis.get():
            if plotbranch.get() != 'totals':
                what_to_plot = what_to_plot.T
        # determine num to plot
        def determine_num_to_plot(num):
            """translate num to num_to_plot"""
            try:
                num = int(num)
            except:
                if num.lower() == 'all':
                    num = 'all'
                else:
                    num = 7
            return num

        num = determine_num_to_plot(number_to_plot.get())

        the_kind = charttype.get()
        if the_kind == 'Type of chart':
            the_kind = 'line'
        # plotter options
        d = {'num_to_plot': num,
             'kind': the_kind}

        d['style'] = plot_style.get()
        d['tex'] = texuse.get()
        d['black_and_white'] = bw.get()

        if log_x.get() == 1 and log_y.get() == 1:
            d['log'] = 'x,y'
        if log_x.get() == 1 and not log_y.get() == 1:
            d['log'] = 'x'
        if log_y.get() == 1 and not log_x.get() == 1:
            d['log'] = 'y'

        if x_axis_l.get() != '':
            d['x_label'] = x_axis_l.get()
        if x_axis_l.get() == 'None':
            d['x_label'] = False
        if y_axis_l.get() != '':
            d['y_label'] = y_axis_l.get()
        if y_axis_l.get() == 'None':
            d['y_label'] = False

        if chart_cols.get() != 'Default':
            d['colours'] = chart_cols.get()

        legend_loc = legloc.get()
        if legend_loc == 'None':
            d['legend'] = False
        else:
            d['legend_pos'] = legend_loc

        show_totals_in_plot = showtot.get()
        if show_totals_in_plot == 'plot':
            d['show_totals'] = 'plot'
        if show_totals_in_plot == 'legend':
            d['show_totals'] = 'legend'
        if show_totals_in_plot == 'legend + plot':
            d['show_totals'] = 'both'

        d['figsize'] = (11.4, 5.7)

        f = plotter(plotnametext.get(), what_to_plot, **d)
        time = strftime("%H:%M:%S", localtime())
        print '%s: %s plotted.' % (time, plotnametext.get())
        # a Tkinter.DrawingArea
        toolbar_frame = Tkinter.Frame(tab3)
        toolbar_frame.grid(row=17, column=2, columnspan = 3, sticky = N)
        canvas = FigureCanvasTkAgg(f.gcf(), tab3)
        canvas.show()
        canvas.get_tk_widget().grid(column = 2, row = 0, rowspan = 16, padx = 20, columnspan = 3)
        toolbar = NavigationToolbar2TkAgg(canvas,toolbar_frame)
        toolbar.update()
        for i in thefig:
            thefig.pop()
        thefig.append(f.gcf())

    def save_current_image():
        import os
        # figre out filename
        filename = namer(plotnametext.get(), type_of_data = 'image') + '.png'
        import sys
        defaultextension = '.png' if sys.platform == 'darwin' else ''
        kwarg = {'defaultextension': defaultextension,
                 #'filetypes': [('all files', '.*'), 
                               #('png file', '.png')],
                 'initialfile': filename}
        imagedir = image_fullpath.get()
        if imagedir:
            kwarg['initialdir'] = imagedir

        fo = tkFileDialog.asksaveasfilename(**kwarg)

        #fo = tkFileDialog.asksaveasfile(mode='w', defaultextension=".png")
        if fo is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        #fo.write(f.gcf())
        #fo.close() # `()` was missing.
        thefig[0].savefig(os.path.join(image_fullpath.get(), fo))
        time = strftime("%H:%M:%S", localtime())
        print '%s: %s saved to %s.' % (time, fo, image_fullpath.get())

    # not working
    def image_clear():
        thefig[0].get_tk_widget().grid_forget()

    def reset_plotter_pane():
        return

    # title tab
    Label(tab3, text = 'Image title:').grid(row = 0, column = 0, sticky = 'W')
    plotnametext = StringVar()
    plotnametext.set('Untitled')
    Entry(tab3, textvariable = plotnametext).grid(row = 0, column = 1)

    Label(tab3, text = 'Data to plot:').grid(row = 1, column = 0, sticky = W)
    # select result to plot
    data_to_plot = StringVar(root)
    most_recent = all_interrogations[all_interrogations.keys()[-1]]
    data_to_plot.set(most_recent)
    every_interrogation = OptionMenu(tab3, data_to_plot, *tuple([i for i in all_interrogations.keys()]))
    every_interrogation.grid(column = 0, row = 2, sticky = W, columnspan = 2)

    # branch selection
    plotbranch = StringVar(root)
    plotbranch.set('results')
    plotbox = OptionMenu(tab3, plotbranch, 'results', 'totals')
    #plotbox.config(state = DISABLED)
    plotbox.grid(row = 2, column = 0, sticky = E, columnspan = 2)

    # transpose
    transpose_vis = IntVar()
    trans_but_vis = Checkbutton(tab3, text="Transpose", variable=transpose_vis, onvalue = True, offvalue = False)
    trans_but_vis.grid(column = 1, row = 3, sticky = E)

    # num_to_plot
    Label(tab3, text = 'Results to show:').grid(row = 5, column = 0, sticky = W)
    number_to_plot = StringVar()
    number_to_plot.set('7')
    Entry(tab3, textvariable = number_to_plot, width = 3).grid(row = 5, column = 1, sticky = E)

    # chart type
    Label(tab3, text='Kind of chart').grid(row = 6, column = 0, sticky = W)
    charttype = StringVar(root)
    charttype.set('line')
    kinds_of_chart = ('line', 'bar', 'barh', 'pie', 'area')
    chart_kind = OptionMenu(tab3, charttype, *kinds_of_chart)
    chart_kind.grid(row = 6, column = 1, sticky = E)

    # axes
    Label(tab3, text = 'x axis label:').grid(row = 7, column = 0, sticky = W)
    x_axis_l = StringVar()
    x_axis_l.set('')
    Entry(tab3, textvariable = x_axis_l).grid(row = 7, column = 1, sticky = W)

    Label(tab3, text = 'y axis label:').grid(row = 8, column = 0, sticky = W)
    y_axis_l = StringVar()
    y_axis_l.set('')
    Entry(tab3, textvariable = y_axis_l).grid(row = 8, column = 1)

    # log options
    log_x = IntVar()
    Checkbutton(tab3, text="Log x axis", variable=log_x).grid(column = 0, row = 9, sticky = W)
    log_y = IntVar()
    Checkbutton(tab3, text="Log y axis", variable=log_y).grid(column = 1, row = 9, sticky = E)

    bw = IntVar()
    Checkbutton(tab3, text="Black and white", variable=bw, onvalue = True, offvalue = False).grid(column = 0, row = 10, sticky = W)
    texuse = IntVar()
    Checkbutton(tab3, text="Use TeX", variable=texuse, onvalue = True, offvalue = False).grid(column = 1, row = 10, sticky = E)

    # chart type
    Label(tab3, text='Colour scheme:').grid(row = 11, column = 0, sticky = W)
    chart_cols = StringVar(root)
    chart_cols.set('Default')
    schemes = tuple(('Default', 'Spectral', 'summer', 'coolwarm', 'pink_r', 'Set1', 'Set2', 
        'Set3', 'brg_r', 'Dark2', 'prism', 'PuOr_r', 'afmhot_r', 'terrain_r', 'PuBuGn_r', 
        'RdPu', 'gist_ncar_r', 'gist_yarg_r', 'Dark2_r', 'YlGnBu', 'RdYlBu', 'hot_r', 'Wistia_r',
        'gist_rainbow_r', 'gist_stern', 'PuBu_r', 'cool_r', 'cool', 'gray', 'copper_r', 
        'Greens_r', 'GnBu', 'gist_ncar', 'spring_r', 'gist_rainbow', 'gist_heat_r', 'Wistia', 
        'OrRd_r', 'CMRmap', 'bone', 'gist_stern_r', 'RdYlGn', 'Pastel2_r', 'spring', 'terrain', 
        'YlOrRd_r', 'Set2_r', 'winter_r', 'PuBu', 'RdGy_r', 'spectral', 'rainbow', 'flag_r', 
        'jet_r', 'RdPu_r', 'gist_yarg', 'BuGn', 'Paired_r', 'hsv_r', 'bwr', 'cubehelix', 
        'Greens', 'PRGn', 'gist_heat', 'spectral_r', 'Paired', 'hsv', 'Oranges_r', 'prism_r', 
        'Pastel2', 'Pastel1_r', 'Pastel1', 'gray_r', 'jet', 'Spectral_r', 'gnuplot2_r', 
        'gist_earth', 'YlGnBu_r', 'copper', 'gist_earth_r', 'Set3_r', 'OrRd', 'gnuplot_r', 
        'ocean_r', 'brg', 'gnuplot2', 'PuRd_r', 'bone_r', 'BuPu', 'Oranges', 'RdYlGn_r', 'PiYG', 
        'CMRmap_r', 'YlGn', 'binary_r', 'gist_gray_r', 'Accent', 'BuPu_r', 'gist_gray', 'flag', 
        'bwr_r', 'RdBu_r', 'BrBG', 'Reds', 'Set1_r', 'summer_r', 'GnBu_r', 'BrBG_r', 'Reds_r', 
        'RdGy', 'PuRd', 'Accent_r', 'Blues', 'autumn_r', 'autumn', 'cubehelix_r', 
        'nipy_spectral_r', 'ocean', 'PRGn_r', 'Greys_r', 'pink', 'binary', 'winter', 'gnuplot', 
        'RdYlBu_r', 'hot', 'YlOrBr', 'coolwarm_r', 'rainbow_r', 'Purples_r', 'PiYG_r', 'YlGn_r', 
        'Blues_r', 'YlOrBr_r', 'seismic', 'Purples', 'seismic_r', 'RdBu', 'Greys', 'BuGn_r', 
        'YlOrRd', 'PuOr', 'PuBuGn', 'nipy_spectral', 'afmhot'))
    ch_col = OptionMenu(tab3, chart_cols, *schemes)
    ch_col.grid(row = 11, column = 1, sticky = E)

    # style
    stys = tuple(('ggplot', 'fivethirtyeight', 'bmh'))
    plot_style = StringVar(root)
    plot_style.set('ggplot')
    Label(tab3, text = 'Plot style:').grid(row = 12, column = 0, sticky = W)
    pick_a_datatype = OptionMenu(tab3, plot_style, *stys)
    pick_a_datatype.grid(row = 12, column = 1, sticky=E)

    # legend pos
    Label(tab3, text='Legend position:').grid(row = 13, column = 0, sticky = W)
    legloc = StringVar(root)
    legloc.set('best')
    locs = tuple(('best', 'outside right', 'upper right', 'right', 'lower right', 'lower left', 'upper left', 'middle', 'none'))
    loc_options = OptionMenu(tab3, legloc, *locs)
    loc_options.grid(row = 13, column = 1, sticky = E)

    # show_totals option
    Label(tab3, text='Show totals: ').grid(row = 14, column = 0, sticky = W)
    showtot = StringVar(root)
    showtot.set('Off')
    showtot_options = tuple(('Off', 'legend', 'plot', 'legend + plot'))
    show_tot_menu = OptionMenu(tab3, showtot, *showtot_options)
    show_tot_menu.grid(row = 14, column = 1, sticky = E)

    # plot button
    Button(tab3, text = 'Plot', command = lambda: do_plotting()).grid(row = 15, column = 1, sticky = E)

    # save image button
    #Button(tab3, text = 'Save image', command = lambda: save_current_image()).grid(column = 2, row = 13)

    # clear image
    #Button(tab3, text = 'Clear image', command = lambda: do_plotting()).grid(column = 3, row = 13)

    # reset pane
    #Button(tab3, text = 'Reset plotter pane', command = lambda: reset_plotter_pane()).grid(column = 4, row = 13)


    ###################     ###################     ###################     ###################
    # CONCORDANCE TAB #     # CONCORDANCE TAB #     # CONCORDANCE TAB #     # CONCORDANCE TAB #
    ###################     ###################     ###################     ###################

    current_conc = ['None']

    def add_conc_lines_to_window(data):
        current_conc[0] = data
        lines = data.to_string(header = False, formatters={'r':'{{:<{}s}}'.format(data['r'].str.len().max()).format}).splitlines()
        conclistbox.delete(0, END)
        for line in lines:
            conclistbox.insert(END, str(line))
        time = strftime("%H:%M:%S", localtime())
        print '%s: Concordancing done: %d results.' % (time, len(lines))

    def do_concordancing():
        import os
        """when you press 'run'"""
        time = strftime("%H:%M:%S", localtime())
        print '%s: Concordancing in progress ... ' % (time)       
        from corpkit import conc
        if subc_pick.get() == "Select subcorpus":
            corpus = corpus_fullpath.get()
        else:
            corpus = os.path.join(corpus_fullpath.get(), subc_pick.get())
        query = query_text.get()
        tree = show_trees.get()
        if (wind_size.var).get() == "Window size":
            w_size = 75
            if tree:
                w_size = w_size / 2
        else:
            w_size = (wind_size.var).get()
        d = {'window': int(w_size), 
             'random': random_conc_option.get(),
             'trees': tree,
             'n': 9999,
             'print_status': False,
             'print_output': False,
             'root': root}
        
        # special kinds of query
        if query.startswith('[') and query.endswith(']'):
                query = query.lstrip('[').rstrip(']').replace("'", '').replace('"', '').replace(' ', '').split(',')
        else:
            query = remake_special_query(query)

        r = conc(corpus, query, **d)  
        if r is False:
            return
        add_conc_lines_to_window(r)
        
    def delete_conc_lines(*args):
        items = conclistbox.curselection()
        #current_conc[0].results.drop(current_conc[0].results.iloc[1,].name)
        r = current_conc[0].drop([current_conc[0].iloc[int(n),].name for n in items])
        add_conc_lines_to_window(r)
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: %d lines removed.' % (thetime, len(items))

    def delete_reverse_conc_lines(*args):
        items = [int(i) for i in conclistbox.curselection()]
        r = current_conc[0].iloc[items,]
        add_conc_lines_to_window(r)
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: %d lines removed.' % (thetime, (len(conclistbox.get(0, END)) - len(items)))

    def conc_export():
        """export conc lines to csv"""
        import os
        import pandas
        if project_fullpath.get() ==  '':
            home = os.path.expanduser("~")
            docpath = os.path.join(home, 'Documents')
        else:
            docpath = project_fullpath.get()
        csv = current_conc[0].to_csv(header = False, sep = '\t')
        savepath = tkFileDialog.asksaveasfilename(title = 'Save file',
                                       initialdir = docpath,
                                       message = 'Choose a name and place for your exported data.',
                                       defaultextension = '.csv',
                                       initialfile = 'data.csv')
        if savepath == '':
            return
        with open(savepath, "w") as fo:
            fo.write(csv)
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Concordance lines exported.' % (thetime)

    import itertools
    toggle = itertools.cycle([True, False]).next

    def conc_sort(*args):
        """various sorting for conc. basically, get columns by regex,
        tokenise the l or r if needed, sort by tokens, turn back to df,
        back to string, show.

        current fail when match is first word in sent.

        the new idea is to simply edit and reshow the dataframe!"""

        lines = conclistbox.get(0, END)
        seplines = []
        import re
        import pandas
        import itertools
        sort_way = True
        if prev_sortval[0] == sortval.get():
            # if subcorpus is the same, etc, as well
            sort_way = toggle()
        df = current_conc[0]
        prev_sortval[0] = sortval.get()

        # sorting by first column is easy, so we don't need pandas
        if sortval.get() == 'M':
            low = [l.lower() for l in df['m']]
            df['tosorton'] = low
        # if sorting by other columns, however, it gets tough.
        else:
            from nltk import word_tokenize as tokenise
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: Tokenising concordance lines ... ' % (thetime)
            # tokenise the right part of each line
            # get l or r column
            col = sortval.get()[0].lower()
            tokenised = [tokenise(s) for s in list(df[col].values)]
            for line in tokenised:
                for i in range(6 - len(line)):
                    if col == 'l':
                        line.insert(0, '')
                    if col == 'r':
                        line.append('')

            # get 1-5 and convert it
            num = int(sortval.get()[-1])
            if col == 'l':
                num = -num
            if col == 'r':
                num = num - 1

            just_sortword = []
            for l in tokenised:
                just_sortword.append(l[num].lower())

            # append list to df
            df['tosorton'] = just_sortword

        df = df.sort(['tosorton'], ascending = sort_way).drop(['tosorton'], axis = 1)
        add_conc_lines_to_window(df)
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: %d concordance lines sorted.' % (thetime, len(conclistbox.get(0, END)))
        
    # conc box
    scrollbar = Scrollbar(tab4)
    scrollbar.grid(row = 0, column = 0)
    conclistbox = Listbox(tab4, yscrollcommand=scrollbar.set, height = 30, width = 177, font = ('Courier New', 12), selectmode = EXTENDED)
    conclistbox.grid(column = 0, columnspan = 60, row = 0)
    conclistbox.bind("<BackSpace>", delete_conc_lines)
    conclistbox.bind("<Shift-KeyPress-BackSpace>", delete_reverse_conc_lines)
    conclistbox.bind("<Shift-KeyPress-Tab>", conc_sort)
    
    scrollbar.config(command=conclistbox.yview)

    # select subcorpus
    subc_pick = StringVar()
    subc_pick.set("Select subcorpus")
    pick_subcorpora = OptionMenu(tab4, subc_pick, *tuple([s for s in subcorpora[corpus_fullpath.get()]]))
    pick_subcorpora.grid(row = 1, column = 0)

    # to do: query type
    # tregex
    # deps
    # plaintext...
    #
    #

    # query: should be drop down, with custom option ...
    query_text = StringVar()
    query_text.set('/NN.?/ >># NP')
    Entry(tab4, textvariable = query_text).grid(row = 1, column = 1)
    
    # window size
    window_sizes = ('20', '30', '40', '50', '60', '70', '80', '90', '100')
    l =  ['Window size'] + [i for i in window_sizes]
    wind_size = MyOptionMenu(tab4, 'Window size', *window_sizes)
    wind_size.grid(row = 1, column = 4)

    # random
    random_conc_option = IntVar()
    Checkbutton(tab4, text="Random", variable=random_conc_option, onvalue = True, offvalue = False).grid(row = 1, column = 2)

    # trees
    show_trees = IntVar()
    Checkbutton(tab4, text="Show trees", variable=show_trees, onvalue = True, offvalue = False).grid(row = 1, column = 3)

    # run button
    Button(tab4, text = 'Run', command = lambda: do_concordancing()).grid(row = 1, column = 5)

    # edit conc lines
    Button(tab4, text = 'Delete selected', command = lambda: delete_conc_lines(), ).grid(row = 1, column = 6)
    Button(tab4, text = 'Just selected', command = lambda: delete_reverse_conc_lines(), ).grid(row = 1, column = 7)
    Button(tab4, text = 'Sort', command = lambda: conc_sort()).grid(row = 1, column = 8)

    # possible sort
    sort_vals = ('L5', 'L4', 'L3', 'L2', 'L1', 'M', 'R1', 'R2', 'R3', 'R4', 'R5')
    sortval = StringVar()
    sortval.set('M')
    prev_sortval = ['None']
    srtkind = OptionMenu(tab4, sortval, *sort_vals)
    srtkind.grid(row = 1, column = 9)

    # export to csv
    Button(tab4, text = 'Export', command = lambda: conc_export()).grid(row = 1, column = 10)

    ##############     ##############     ##############     ##############     ############## 
    # MANAGE TAB #     # MANAGE TAB #     # MANAGE TAB #     # MANAGE TAB #     # MANAGE TAB # 
    ##############     ##############     ##############     ##############     ############## 

    def make_new_project():
        import os
        from corpkit import new_project
        name = tkSimpleDialog.askstring('New project', 'Choose a name for your project:')
        if not name:
            return
        home = os.path.expanduser("~")
        docpath = os.path.join(home, 'Documents')
        fp = tkFileDialog.askdirectory(title = 'New project location',
                                       initialdir = docpath,
                                       message = 'Choose a directory in which to create your new project')
        if not fp:
            return
        new_proj_basepath.set('New project: "%s"' % name)
        new_project(name = name, loc = fp, root = root)
        load_project(path = os.path.join(fp, name))
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Project "%s" created.' % (thetime, name)

    def get_saved_results():
        from corpkit import load_all_results
        r = load_all_results(data_dir = data_fullpath.get(), root = root)

        for name, loaded in r.items():
            all_interrogations[name] = loaded
        refresh()
    
    # corpus path setter
    data_fullpath = StringVar()
    data_fullpath.set('')
    data_basepath = StringVar()
    data_basepath.set('Select data directory')
    project_fullpath = StringVar()
    project_fullpath.set('')

    def data_getdir():
        import os
        fp = tkFileDialog.askdirectory()
        if not fp:
            return
        data_fullpath.set(fp)
        data_basepath.set('Saved data: "%s"' % os.path.basename(fp))
        #fs = sorted([d for d in os.listdir(fp) if os.path.isfile(os.path.join(fp, d))])
        time = strftime("%H:%M:%S", localtime())
        print '%s: Set data directory: %s' % (time, os.path.basename(fp))
    
    # corpus path setter
    image_fullpath = StringVar()
    image_fullpath.set('')
    image_basepath = StringVar()
    image_basepath.set('Select image directory')

    def image_getdir(nodialog = False):
        import os
        fp = tkFileDialog.askdirectory()
        if not fp:
            return
        image_fullpath.set(fp)
        image_basepath.set('Images: "%s"' % os.path.basename(fp))
        time = strftime("%H:%M:%S", localtime())
        print '%s: Set image directory: %s' % (time, os.path.basename(fp))

    def save_one_or_more():
        if len(sel_vals) == 0:
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: No interrogations selected.' % thetime
            return
        from corpkit import save_result
        import os
        saved = 0
        existing = 0
        for i in sel_vals:
            if urlify(i) + '.p' not in os.listdir(data_fullpath.get()):
                save_result(all_interrogations[i], urlify(i) + '.p', savedir = data_fullpath.get(), root = root)
                saved += 1
            else:
                existing += 1
                thetime = strftime("%H:%M:%S", localtime())
                print '%s: %s already exists in %s.' % (thetime, urlify(i), os.path.basename(data_fullpath.get()))   
        thetime = strftime("%H:%M:%S", localtime())
        if saved == 1 and existing == 0:
            print '%s: %s saved.' % (thetime, sel_vals[0])
        else:
            if existing == 0:
                print '%s: %d interrogations saved.' % (thetime, len(sel_vals))
            else:
                print '%s: %d interrogations saved, %d already existed' % (thetime, saved, existing)
        refresh()

    def remove_one_or_more():
        if len(sel_vals) == 0:
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: No interrogations selected.' % thetime
            return
        for i in sel_vals:
            try:
                del all_interrogations[i]
            except:
                pass
        thetime = strftime("%H:%M:%S", localtime())
        if len(sel_vals) == 1:
            print '%s: %s removed.' % (thetime, sel_vals[0])
        else:
            print '%s: %d interrogations removed.' % (thetime, len(sel_vals))
        refresh()

    def del_one_or_more():
        if len(sel_vals) == 0:
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: No interrogations selected.' % thetime
            return
        import os
        result = tkMessageBox.askquestion("Are You Sure?", "Permanently delete the following files:\n\n    %s" % '\n    '.join(sel_vals), icon='warning')
        if result == 'yes':
            for i in sel_vals:
                try:
                    del all_interrogations[i]
                    os.remove(os.path.join(data_fullpath.get(), i + '.p'))
                except:
                    pass
        thetime = strftime("%H:%M:%S", localtime())
        if len(sel_vals) == 1:
            print '%s: %s deleted.' % (thetime, sel_vals[0])
        else:
            print '%s: %d interrogations deleted.' % (thetime, len(sel_vals))
        refresh()

    def urlify(s):
        "Turn title into filename"
        import re
        s = s.lower()
        s = re.sub(r"[^\w\s-]", '', s)
        s = re.sub(r"\s+", '-', s)
        s = re.sub(r"-(textbf|emph|textsc|textit)", '-', s)
        return s

    def rename_one_or_more():
        if len(sel_vals) == 0:
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: No interrogations selected.' % thetime
            return
        import os
        if perm.get():
            perm_text = 'permanently '
        else:
            perm_text = ''
        for i in sel_vals:
            answer = tkSimpleDialog.askstring('Rename', 'Choose a new name for "%s":' % i)
            if answer is None or answer == '':
                continue
            else:
                all_interrogations[answer] = all_interrogations.pop(i)
            if perm.get():
                p = data_fullpath.get()
                oldf = os.path.join(p, i + '.p')
                if os.path.isfile(oldf):
                    newf = os.path.join(p, urlify(answer) + '.p')
                    os.rename(oldf, newf)
            if name_of_interro_spreadsheet.get() == i:
                name_of_interro_spreadsheet.set(answer)
                i_resultname.set('Interrogation results: %s' % str(answer))
                #update_spreadsheet(interro_results, all_interrogations[answer].results)
            if name_of_o_ed_spread.get() == i:
                name_of_o_ed_spread.set(answer)
                #update_spreadsheet(o_editor_results, all_interrogations[answer].results)
            if name_of_n_ed_spread.get() == i:
                name_of_n_ed_spread.set(answer)
                #update_spreadsheet(n_editor_results, all_interrogations[answer].results)

        thetime = strftime("%H:%M:%S", localtime())
        if len(sel_vals) == 1:
            print '%s: %s %srenamed as %s.' % (thetime, sel_vals[0], perm_text, answer)
        print '%s: %d interrogations %srenamed.' % (thetime, len(sel_vals), perm_text)
        refresh()

    sel_vals = []

    def export_interrogation():
        """save dataframes and options to file"""
        import os
        import pandas
        for i in sel_vals:
            answer = tkSimpleDialog.askstring('Rename', 'Choose a save name for "%s":' % i)
            if answer is None or answer == '':
                continue
            data = all_interrogations[i]
            keys = data._asdict().keys()
            if project_fullpath.get() == '' or project_fullpath.get() is None:
                fp = tkFileDialog.askdirectory(title = 'Choose save directory',
                    message = 'Choose save directory for exported interrogation')
                if fp == '':
                    return
            else:
                fp = project_fullpath.get()
            os.makedirs(os.path.join(fp, answer))
            for k in keys:
                if k == 'results':
                    data.results.to_csv(os.path.join(fp, answer, 'results.csv'), sep ='\t')
                if k == 'totals':
                    pandas.DataFrame(data.totals).to_csv(os.path.join(fp, answer, 'totals.csv'), sep ='\t')
                if k == 'query':
                    pandas.DataFrame(data.query.values(), index = data.query.keys()).to_csv(os.path.join(fp, answer, 'query.csv'), sep ='\t')
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Results exported to %s' % (thetime, os.path.join(fp, answer))        

    def reset_everything():
        # result names
        i_resultname.set('Interrogation results:')
        resultname.set('Results to edit:')
        editoname.set('Edited results:')
        # spreadsheets
        update_spreadsheet(interro_results, df_to_show = None, height = 340, width = 650)
        update_spreadsheet(interro_totals, df_to_show = None, height = 10, width = 650)
        update_spreadsheet(o_editor_results, df_to_show = None, height = 140, width = 720)
        update_spreadsheet(o_editor_totals, df_to_show = None, height = 10, width = 720)
        update_spreadsheet(o_editor_results, df_to_show = None, height = 140, width = 720)
        update_spreadsheet(o_editor_totals, df_to_show = None, height = 10, width = 720)
        # interrogations
        for e in all_interrogations.keys():
            del all_interrogations[e]
        # subcorpora listbox
        subc_listbox.delete(0, END)
        subc_listbox_build.delete(0, END)
        conclistbox.delete(0, END)
        every_interro_listbox.delete(0, END)
        every_interrogation['menu'].delete(0, 'end')
        pick_subcorpora['menu'].delete(0, 'end')
        for k in subcorpora.keys():
            del subcorpora[k]
        refresh()

    def load_project(path = False):
        import os
        if path is False:
            fp = tkFileDialog.askdirectory(title = 'Open project',
                                       message = 'Choose project directory')
        else:
            fp = path
        if not fp or fp == '':
            return
        project_fullpath.set(fp)
        image_fullpath.set(os.path.join(fp, 'images'))
        data_fullpath.set(os.path.join(fp, 'saved_interrogations'))
        #corpus_fullpath.set(os.path.join(fp, 'corpus'))
        open_proj_basepath.set('Loaded project: "%s"' % os.path.basename(fp))
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Project "%s" opened.' % (thetime, os.path.basename(fp))
        os.chdir(fp)
        # reset tool:
        root.title("corpkit: %s" % os.path.basename(fp))
        reset_everything()
        all_corpora = [d for d in os.listdir(os.path.join(fp, 'data')) if os.path.isdir(os.path.join(fp, 'data', d))]
        parsed_corp = [d for d in all_corpora if d.endswith('-parsed')]
        first = False
        if len(parsed_corp) > 0:
            first = parsed_corp[0]
        else:
            if len(all_corpora) > 0:
                first = all_corpora[0]
        if first:
            corpus_fullpath.set(os.path.join(fp, 'data', first))
            basepath.set('Corpus: "%s"' % first)
            subcorpora = {corpus_fullpath.get(): sorted([d for d in os.listdir(corpus_fullpath.get()) if os.path.isdir(os.path.join(corpus_fullpath.get(), d))])}

        # settings
        def load_config():
            import os
            import ConfigParser
            Config = ConfigParser.ConfigParser()
            f = os.path.join(project_fullpath.get(), 'settings.ini')
            Config.read(f)

            def conmap(section):
                dict1 = {}
                options = Config.options(section)
                for option in options:
                    try:
                        dict1[option] = Config.get(section, option)
                        if dict1[option] == -1:
                            DebugPrint("skip: %s" % option)
                    except:
                        print("exception on %s!" % option)
                        dict1[option] = None
                return dict1

            plot_style.set(conmap("Visualise")['plot style'])
            texuse.set(conmap("Visualise")['use tex'])
            x_axis_l.set(conmap("Visualise")['x axis title'])
            chart_cols.set(conmap("Visualise")['colour scheme'])
            corpus_fullpath.set(conmap("Interrogate")['corpus path'])
        
        f = os.path.join(project_fullpath.get(), 'settings.ini')
        if os.path.isfile(f):
            load_config()


    def view_query():
        Label(tab5, text = 'Query option', font = ("Helvetica", 12, "bold")).grid(sticky = W, row = 0, column = 4, padx = 40)
        show_query_keys = Listbox(tab5, selectmode = EXTENDED, height = 20)
        show_query_keys.grid(sticky = W, column = 4, row = 2, rowspan = 20, padx = 40)
        
        Label(tab5, text = 'Query value', font = ("Helvetica", 12, "bold")).grid(sticky = W, row = 0, column = 5, padx = 5)
        show_query_vals = Listbox(tab5, selectmode = EXTENDED, height = 20)
        show_query_vals.grid(sticky = E, column = 5, row = 2, rowspan = 20, padx = 5)

        #Label(tab5, text = 'Queries', font = ("Helvetica", 12, "bold")).grid(sticky = W, row = 0, column = 2, padx = 40)

        if len(sel_vals) > 1:
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: Can only view one interrogation at a time.' % (thetime)
            return
        q_dict = dict(all_interrogations[sel_vals[0]].query)
        show_query_keys.delete(0, 'end')
        show_query_vals.delete(0, 'end')
        flipped_trans = {v: k for k, v in transdict.items()}
        
        # flip options dict, make 'kind of search'
        if 'option' in q_dict.keys():
            flipped_opt = {}
            for nm, lst in option_dict.items():
                for i in lst:
                    flipped_opt[i] = nm
            the_opt = flipped_opt[flipped_trans[q_dict['option']]]
            q_dict['kind_of_search'] = the_opt

        try:
            del k['dataframe1']
        except:
            pass
        try:
            del k['dataframe2']
        except:
            pass
        for i, k in enumerate(sorted(q_dict.keys())):
            v = q_dict[k]
            if v is False:
                v = 'False'
            if v is True:
                v = 'True'
            if k == 'option':
                v = flipped_trans[v]
            show_query_keys.insert(END, '%d. %s' % (i, str(k)))
            show_query_vals.insert(END, '%d. %s' % (i, str(v)))

    # a list of every interrogation
    def onselect_interro(evt):
        # remove old vals
        for i in sel_vals:
            sel_vals.pop()
        wx = evt.widget
        indices = wx.curselection()
        for index in indices:
            value = wx.get(index)
            if value not in sel_vals:
                sel_vals.append(value)

    every_interro_listbox = Listbox(tab5, selectmode = EXTENDED, height = 20)
    every_interro_listbox.grid(sticky = E, column = 1, row = 2, rowspan = 20)
    # Set interrogation option
    ei_chosen_option = StringVar()
    #ei_chosen_option.set('w')
    xx = every_interro_listbox.bind('<<ListboxSelect>>', onselect_interro)
    # default: w option
    every_interro_listbox.select_set(0)

    new_proj_basepath = StringVar()
    new_proj_basepath.set('New project')
    open_proj_basepath = StringVar()
    open_proj_basepath.set('Open project')

    Label(tab5, text = 'Project', font = ("Helvetica", 12, "bold")).grid(sticky = W, row = 0, column = 0)
    Button(tab5, textvariable = new_proj_basepath, command = make_new_project).grid(row = 1, column = 0, sticky=W)
    Button(tab5, textvariable = open_proj_basepath, command = load_project).grid(row = 2, column = 0, sticky=W)
    Button(tab5, textvariable = data_basepath, command = data_getdir).grid(row = 3, column = 0, sticky=W)
    #Label(tab5, text = 'Image directory: ').grid(sticky = W, row = 1, column = 0)
    Button(tab5, textvariable = image_basepath, command = image_getdir).grid(row = 4, column = 0, sticky=W)

    Label(tab5, text = 'Interrogations', font = ("Helvetica", 12, "bold")).grid(sticky = W, row = 0, column = 1)
    Button(tab5, text = 'Get saved interrogations', command = get_saved_results).grid(row = 1, column = 1, sticky=E)

    #Label(tab5, text = 'Save selected: ').grid(sticky = E, row = 6, column = 1)
    Button(tab5, text = 'Save', command = save_one_or_more).grid(sticky = E, column = 1, row = 22)
    Button(tab5, text = 'View query', command = view_query).grid(sticky = E, column = 1, row = 23)
    Button(tab5, text = 'Rename', command = rename_one_or_more).grid(sticky = E, column = 1, row = 24)
    perm = IntVar()
    #Checkbutton(tab5, text="Permanently", variable=perm, onvalue = True, offvalue = False).grid(column = 1, row = 16, sticky=W)
    Button(tab5, text = 'Export', command = export_interrogation).grid(sticky = E, column = 1, row = 25)
    #Label(tab5, text = 'Remove selected: ').grid(sticky = W, row = 4, column = 0)
    Button(tab5, text="Remove", command=remove_one_or_more).grid(sticky = E, column = 1, row = 26)
    #Label(tab5, text = 'Delete selected: ').grid(sticky = E, row = 5, column = 1)
    Button(tab5, text = 'Delete', command = del_one_or_more).grid(sticky = E, column = 1, row = 27)

    ##############     ##############     ##############     ##############     ############## 
    # BUILD TAB  #     # BUILD TAB  #     # BUILD TAB  #     # BUILD TAB  #     # BUILD TAB  # 
    ##############     ##############     ##############     ##############     ############## 
    

    from corpkit import download_cnlp, extract_cnlp, rename_duplicates, get_corpus_filepaths, check_jdk, parse_corpus, move_parsed_files, corenlp_exists

    def create_parsed_corpus():
        """make sure things are installed, then parse, then structure"""
        unparsed_corpus_path = sel_corpus.get()
        import os
        if not corenlp_exists():
            downstall_nlp = tkMessageBox.askyesno("CoreNLP not found.", 
                          "CoreNLP parser not found. Download/install it?")
            if downstall_nlp:
                stanpath, cnlp_zipfile = download_cnlp(project_fullpath.get(), root = root)
                extract_cnlp(cnlp_zipfile, root = root)
            else:
                time = strftime("%H:%M:%S", localtime())
                print '%s: Cannot parse data without Stanford CoreNLP.' % (time)
                return
        jdk = check_jdk()
        if jdk is False:
            downstall_jdk = tkMessageBox.askyesno("You need Java JDK 1.8 to use CoreNLP.", "Hit 'yes' to open web browser at download link. Once installed, corpkit should resume automatically")
            if downstall_jdk:
                import webbrowser
                webbrowser.open_new('http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html')
                import time
                time = strftime("%H:%M:%S", localtime())
                print '%s: Waiting for Java JDK 1.8 installation to complete.' % (time)
                while jdk is False:
                    jdk = check_jdk()
                    time = strftime("%H:%M:%S", localtime())
                    print '%s: Waiting for Java JDK 1.8 installation to complete.' % (time)
                    time.sleep(5)
            else:
                time = strftime("%H:%M:%S", localtime())
                print '%s: Cannot parse data without Java JDK 1.8.' % (time)
                return
        filelist = get_corpus_filepaths(project_fullpath.get(), unparsed_corpus_path)
        parsed_dir = parse_corpus(project_fullpath.get(), unparsed_corpus_path, filelist, root = root, stdout = sys.stdout)
        sys.stdout = note.redir
        new_corpus_path = move_parsed_files(project_fullpath.get(), unparsed_corpus_path, parsed_dir)
        corpus_fullpath.set(new_corpus_path)
        basepath.set('Corpus: "%s"' % os.path.basename(new_corpus_path))
        time = strftime("%H:%M:%S", localtime())
        print '%s: Corpus parsed and ready to interrogate: "%s"' % (time, os.path.basename(new_corpus_path))

    get_text_corpus = StringVar()

    parse_button_text = StringVar()
    parse_button_text.set('Parse corpus')

    sel_corpus = StringVar()
    sel_corpus.set('')
    sel_corpus_button = StringVar()
    sel_corpus_button.set('Select corpus in project')

    path_to_new_unparsed_corpus = StringVar()
    path_to_new_unparsed_corpus.set('')

    add_corpus = StringVar()
    add_corpus.set('')
    add_corpus_button = StringVar()
    add_corpus_button.set('Add corpus%s' % add_corpus.get())

    def select_corpus_to_parse():
        """clean this up!"""
        import os
        if project_fullpath.get() == '':
            home = os.path.expanduser("~")
            docpath = os.path.join(home, 'Documents')
        else:
            init = os.path.join(project_fullpath.get(), 'data')
        unparsed_corpus_path = tkFileDialog.askdirectory(title = 'Path to unparsed corpus',
                initialdir = init,
                message = 'Select your corpus of unparsed text files for parsing.')
        if unparsed_corpus_path is False or unparsed_corpus_path == '':    
            return
        #sel_corpus.set(unparsed_corpus_path)
        #sel_corpus_button.set('Corpus selected: "%s"' % os.path.basename(unparsed_corpus_path))
        parse_button_text.set('Parse corpus: "%s"' % os.path.basename(unparsed_corpus_path))
        path_to_new_unparsed_corpus.set(unparsed_corpus_path)
        #add_corpus_button.set('Added: %s' % os.path.basename(unparsed_corpus_path))
        where_to_put_corpus = os.path.join(project_fullpath.get(), 'data')
        newc = os.path.join(where_to_put_corpus, os.path.basename(unparsed_corpus_path))        
        sel_corpus.set(newc)
        sel_corpus_button.set('Corpus selected: "%s"' % os.path.basename(newc))
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Corpus copied to project folder.' % (thetime)
        parse_button_text.set('Parse corpus: "%s"' % os.path.basename(newc))
        subc_listbox_build.configure(state = NORMAL)
        subc_listbox_build.delete(0, 'end')
        for e in list([d for d in os.listdir(unparsed_corpus_path) if os.path.isdir(os.path.join(unparsed_corpus_path, d))]):
            subc_listbox_build.insert(END, e)

        time = strftime("%H:%M:%S", localtime())
        print '%s: Selected corpus: "%s"' % (time, os.path.basename(unparsed_corpus_path))

    def getcorpus():
        import shutil
        import os
        home = os.path.expanduser("~")
        docpath = os.path.join(home, 'Documents')
        fp = tkFileDialog.askdirectory(title = 'Path to unparsed corpus',
                                       initialdir = docpath,
                                       message = 'Select your corpus of unparsed text files.')
        where_to_put_corpus = os.path.join(project_fullpath.get(), 'data')
        newc = os.path.join(where_to_put_corpus, os.path.basename(fp))
        try:
            shutil.copytree(fp, newc)
        except OSError:
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: "%s" already exists in project.' % (thetime, os.path.basename(fp)) 
            return 

        get_text_corpus.set(fp)
        path_to_new_unparsed_corpus.set(fp)
        add_corpus_button.set('Added: "%s"' % os.path.basename(fp))
        sel_corpus.set(newc)
        sel_corpus_button.set('Corpus to parse: "%s"' % os.path.basename(newc))
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Corpus copied to project folder.' % (thetime)
        
        parse_button_text.set('Parse corpus: %s' % os.path.basename(newc))
        
        subc_listbox_build.configure(state = NORMAL)
        subc_listbox_build.delete(0, 'end')
        for e in list([d for d in os.listdir(fp) if os.path.isdir(os.path.join(fp, d))]):
            subc_listbox_build.insert(END, e)
        time = strftime("%H:%M:%S", localtime())
        print '%s: Selected corpus for parsing: "%s"' % (time, os.path.basename(newc))
        # unlock editing  

    # duplicate of one in 'manage
    Label(tab0, text = 'Create project', font = ("Helvetica", 12, "bold")).grid(sticky = W, row = 0, column = 0)
    #Label(tab0, text = 'New project', font = ("Helvetica", 12, "bold")).grid(sticky = W, row = 0, column = 0)
    Button(tab0, textvariable = new_proj_basepath, command = make_new_project).grid(row = 1, column = 0, sticky=W)
    #Label(tab0, text = 'Open project: ').grid(row = 2, column = 0, sticky=W)
    Button(tab0, textvariable = open_proj_basepath, command = load_project).grid(row = 2, column = 0, sticky=W)
    #Label(tab0, text = 'Add corpus to project: ').grid(row = 4, column = 0, sticky=W)
    Button(tab0, textvariable = add_corpus_button, command=getcorpus).grid(row = 3, column = 0, sticky=W)
    #Label(tab0, text = 'Corpus to parse: ').grid(row = 6, column = 0, sticky=W)
    Button(tab0, textvariable = sel_corpus_button, command=select_corpus_to_parse).grid(row = 4, column = 0, sticky=W)
    #Label(tab0, text = 'Parse corpus: ').grid(row = 8, column = 0, sticky=W)
    Button(tab0, textvariable = parse_button_text, command=create_parsed_corpus).grid(row = 5, column = 0, sticky=W)

    subc_sel_vals_build = []

    # a list of every interrogation
    def onselect_subc_build(evt):
        import os
        """get selected subcorpora"""
        # should only be one
        for i in subc_sel_vals_build:
            subc_sel_vals_build.pop()
        wx = evt.widget
        indices = wx.curselection()
        for index in indices:
            value = wx.get(index)
            if value not in subc_sel_vals_build:
                subc_sel_vals_build.append(value)

        f_view.configure(state = NORMAL)
        f_view.delete(0, 'end')
        newp = path_to_new_unparsed_corpus.get()
        newsub = os.path.join(newp, subc_sel_vals_build[0])

        fs = [f for f in os.listdir(newsub) if f.endswith('.txt')]
        for e in fs:
            f_view.insert(END, e)
        f_in_s.set('Files in subcorpus: %s' % subc_sel_vals_build[0])

    # a listbox of subcorpora
    Label(tab0, text = 'Subcorpora', font = ("Helvetica", 12, "bold")).grid(row = 10, column = 0, sticky=W, pady = 10)
    subc_listbox_build = Listbox(tab0, selectmode = SINGLE, height = 17, state = DISABLED)
    subc_listbox_build.grid(row = 11, column = 0, rowspan = 5, pady = 25)
    xxy = subc_listbox_build.bind('<<ListboxSelect>>', onselect_subc_build)
    subc_listbox_build.select_set(0)

    chosen_f = []

    # a list of every interrogation
    def onselect_f(evt):
        import os
        """get selected subcorpora"""
        # should only be one
        for i in chosen_f:
            chosen_f.pop()
        wx = evt.widget
        indices = wx.curselection()
        for index in indices:
            value = wx.get(index)
            if value not in chosen_f:
                chosen_f.append(value)
        editor.configure(state = NORMAL)
        newp = path_to_new_unparsed_corpus.get()
        fp = os.path.join(newp, subc_sel_vals_build[0], chosen_f[0])
        text = open(fp).read()
        editor.delete(1.0, END)
        editor.insert(END, text)
        editor.mark_set(INSERT, 1.0)
        editf.set('Edit file: %s' % chosen_f[0])
        filename.set(chosen_f[0])
        fullpath_to_file.set(fp)
        
        # f_in_s.set('Files in corpus: %s' subc_selected)

    f_in_s = StringVar()
    f_in_s.set('Files in subcorpus: ')

    # a listbox of files
    Label(tab0, textvariable = f_in_s, font = ("Helvetica", 12, "bold")).grid(row = 0, column = 1, sticky=W, padx = 30)
    f_view = Listbox(tab0, selectmode = EXTENDED, height = 28, state = DISABLED)
    f_view.grid(row = 1, column = 1, rowspan = 15, columnspan = 3, padx = 30)
    xxyy = f_view.bind('<<ListboxSelect>>', onselect_f)
    f_view.select_set(0)

    editf = StringVar()
    editf.set('Edit file: ')

    def savebuttonaction(*args):
        f = open(fullpath_to_file.get(), "w")
        text = editor.get(1.0, END)
        try:
            # normalize trailing whitespace
            f.write(text.rstrip())
            f.write("\n")
        finally:
            f.close()
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: %s saved.' % (thetime, filename.get())

    Label(tab0, textvariable = editf, font = ("Helvetica", 12, "bold")).grid(row = 0, column = 4, sticky=W, padx = 30)
    editor = Text(tab0, height = 30, state = DISABLED)
    editor.grid(row = 1, column = 4, columnspan = 12, rowspan = 20, padx = 30)
    editor.bind("<%s-s>" % key, savebuttonaction)

    editor.config(borderwidth=0,
                  font="{Lucida Sans Typewriter} 12",
                  #foreground="green",
                  #background="black",
                  #insertbackground="white", # cursor
                  #selectforeground="green", # selection
                  #selectbackground="#008000",
                  wrap=WORD, # use word wrapping
                  width=64,
                  undo=True, # Tk 8.4
                  )
    filename = StringVar()
    filename.set('')
    fullpath_to_file = StringVar()
    fullpath_to_file.set('')

    #Label(tab0, text = 'Corpus directory: ').grid(row = 22, column = 3, columnspan = 8)
    Button(tab0, text = 'Save changes', command = savebuttonaction).grid(row = 22, column = 3, columnspan = 8, sticky = 'N')


    ############ ############ ############ ############ ############ 
    # MENU BAR # # MENU BAR # # MENU BAR # # MENU BAR # # MENU BAR # 
    ############ ############ ############ ############ ############ 

    realquit = IntVar()
    realquit.set(0)

    def clear_all():
        import os
        import sys
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def save_config():
        #settings = [corpus_fullpath, basepath, funfil, posfil, lemtag, kind_of_dep, 
        #       entrytext, datatype_picked, datatype_chosen_option, special_queries, 
        #       lem, phras, tit_fil, case_sensitive, nametext, i_resultname, 
        #       name_of_interro_spreadsheet, selected_to_edit, df1branch, opp, 
        #       data2_pick, df2branch, sort_val, just_tot_setting, keep_stats_setting, 
        #       rem_abv_p_set, entry_regex, newname_var, do_with_entries, do_sub, 
        #       new_subc_name, edit_nametext, resultname, name_of_o_ed_spread, 
        #       editoname, name_of_n_ed_spread, plotnametext, data_to_plot, plotbranch, 
        #       number_to_plot, charttype, x_axis_l, y_axis_l, log_x, log_y, bw, texuse, 
        #       chart_cols, plot_style, legloc, showtot, subc_pick, query_text, 
        #       random_conc_option, show_trees, sortval, data_fullpath, data_basepath, 
        #       project_fullpath, image_fullpath, image_basepath, ei_chosen_option, 
        #       new_proj_basepath, open_proj_basepath, perm, get_text_corpus, 
        #       parse_button_text, sel_corpus, sel_corpus_button, 
        #       path_to_new_unparsed_corpus, add_corpus, add_corpus_button, f_in_s, editf, 
        #       filename, fullpath_to_file, realquit]
        import ConfigParser
        import os
        Config = ConfigParser.ConfigParser()
        cfgfile = open(os.path.join(project_fullpath.get(), 'settings.ini') ,'w')
        Config.add_section('Build')
        Config.add_section('Interrogate')
        Config.set('Interrogate','Corpus path', corpus_fullpath.get())
        Config.add_section('Edit')
        Config.add_section('Visualise')
        Config.set('Visualise','Plot style', plot_style.get())
        Config.set('Visualise','Use TeX', texuse.get())
        Config.set('Visualise','x axis title', x_axis_l.get())
        Config.set('Visualise','Colour scheme', chart_cols.get())
        Config.add_section('Concordance')
        Config.add_section('Manage')
        Config.set('Manage','Project path',project_fullpath.get())
        Config.write(cfgfile)
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Project settings saved to settings.ini ... ' % thetime

    def quitfunc():
        if project_fullpath.get() != '':
            save_ask = tkMessageBox.askyesno("Save project settings.", 
                          "Save settings before quitting?")
            if save_ask:
                save_config()
        realquit.set(1)
        root.quit()

    def check_updates(showfalse = True):
        """check for updates, showing a window if there is one, and if showfalse, 
           even if not. This works by simply downloading the html of the GitHub main
           page, and searching for the .tar.gz file. This avoids extra dependencies
           on (e.g.) PythonGit. Not sure if this should unzip and overwrite the
           existing file or not."""
        import corpkit
        ver = corpkit.__version__
        ver = float(ver)
        import re
        import urllib2
        from time import strftime, localtime
        thetime = strftime("%H:%M:%S", localtime())
        print '%s: Checking for updates ... ' % thetime
        try:
            response = urllib2.urlopen('https://www.github.com/interrogator/corpkit')
            html = response.read()
        except:
            if showfalse:
                tkMessageBox.showinfo(
                "No connection to remote server",
                "Could not connect to remote server.")
            return

        reg = re.compile('title=.corpkit-([0-9\.]+)\.tar\.gz')
        vnum = float(re.search(reg, str(html)).group(1))
        if vnum > ver:
            download_update = tkMessageBox.askyesno("Update available: corpkit %s." % str(vnum), 
                          "Download corpkit %s now?" % str(vnum))
            if download_update:
                import webbrowser
                webbrowser.open_new('https://raw.githubusercontent.com/interrogator/corpkit/master/corpkit-%s.tar.gz' % str(vnum))
                thetime = strftime("%H:%M:%S", localtime())
                print '%s: Update found: corpkit %s' % (thetime, str(vnum))
            else:
                thetime = strftime("%H:%M:%S", localtime())
                print '%s: Update found: corpkit %s. Not downloaded.' % (thetime, str(vnum))
                return
        else:
            if showfalse:
                tkMessageBox.showinfo(
                "Up to date!",
                "corpkit (version %s) up to date!" % ver)
                thetime = strftime("%H:%M:%S", localtime())
                print '%s: corpkit (version %s) up to date.' % (thetime, str(vnum))
                return
            #else:
                #thetime = strftime("%H:%M:%S", localtime())
                #print '%s: No updates available.' % thetime

    # check for updates on launch
    check_updates(showfalse = False)

    menubar = Menu(root)
    if sys.platform == 'darwin':
        filemenu = Menu(menubar, tearoff=0, name='apple')
    else:
        filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New project", command=make_new_project)
    filemenu.add_command(label="Open project", command=load_project)
    filemenu.add_command(label="Save project settings", command=save_config)
    filemenu.add_separator()
    filemenu.add_command(label="Check for updates", command=check_updates)
    # broken on deployed version ... path to self stuff
    #filemenu.add_separator()
    #filemenu.add_command(label="Restart tool", command=clear_all)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=quitfunc)
    menubar.add_cascade(label="File", menu=filemenu)
    if sys.platform == 'darwin':
        windowmenu = Menu(menubar, name='window')
        menubar.add_cascade(menu=windowmenu, label='Window')
    else:
        sysmenu = Menu(menubar, name='system')
        menubar.add_cascade(menu=sysmenu)

    # prefrences section
    if sys.platform == 'darwin':
        def showMyPreferencesDialog():
            tkMessageBox.showinfo("Preferences",
                    "Preferences here.")
        root.createcommand('tk::mac::ShowPreferences', showMyPreferencesDialog)

    def about_box():
        import corpkit
        ver = corpkit.__version__
        tkMessageBox.showinfo('About', 'corpkit %s\n\ngithub.com/interrogator/corpkit\npypi.python.org/pypi/corpkit\n\n' \
                              'Creator: Daniel McDonald\nmcdonaldd@unimelb.edu.au' % ver)

    def show_log():
        import os
        from time import strftime, localtime
        if project_fullpath.get() == '':
            home = os.path.expanduser("~")
            docpath = os.path.join(home, 'Documents')
        else:
            docpath = project_fullpath.get()
        input = note.text.get("1.0",END)
        c = 0
        logpath = os.path.join(docpath, 'log-%s.txt' % str(c).zfill(2))
        while os.path.isfile(logpath):
            logpath = os.path.join(docpath, 'log-%s.txt' % str(c).zfill(2))
            c += 1
        with open(logpath, "w") as fo:
            fo.write(input)
            thetime = strftime("%H:%M:%S", localtime())
            print '%s: Log saved to "%s".' % (thetime, logpath)
        import sys
        if sys.platform == 'darwin':
            import subprocess
            subprocess.call(['open', logpath])
        else:
            os.startfile(logpath)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Query help", command=query_help)
    helpmenu.add_command(label="Save log", command=show_log)
    helpmenu.add_command(label="About", command=about_box)
    menubar.add_cascade(label="Help", menu=helpmenu)

    if sys.platform == 'darwin':
        import corpkit
        import subprocess
        ver = corpkit.__version__
        corpath = os.path.dirname(corpkit.__file__)
        if not corpath.startswith('/Library/Python') and not 'corpkit/corpkit/corpkit' in corpath:
            subprocess.call('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "corpkit-%s" to true' ''' % ver, shell = True)
    root.config(menu=menubar)
    print '\n\n\n'
    note.focus_on(tab1)

    root.mainloop()

if __name__ == "__main__":
    corpkit_gui()

