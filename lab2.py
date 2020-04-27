from spyre import server

import pandas as pd
import urllib.request as urllib2
import json
import datetime
import os
from download_files import getDf, week


class StockExample(server.App):
    title = "Historical Stock Prices"

    inputs = [{        "type":'dropdown',
                    "label": 'Company',
                    "options" : [ {"label": "VHI", "value":"VHI"},
                                  {"label": "TCI", "value":"TCI"},
                                  {"label": "VCI", "value":"VCI"}],
                    "key": 'ticker',
                    "action_id": "update_data"},
                {"type":'dropdown',
                    "label": 'province',
                    "options" : [ {"label": str(year), "value": str(year) } for year in range(1,25)],
                    "key": 'province',
                    "action_id": "update_data"},
                 {"type":'dropdown',
                    "label": 'From',
                    "options" : [ {"label": week+1, "value": week+1 } for week in range(52)],
                    "key": 'from',
                    "action_id": "update_data"},

                {"type":'dropdown',
                    "label": 'To',
                    "options" : [ {"label": week+1, "value": week+1 } for week in range(52)],
                    "key": 'to',
                    "action_id": "update_data"}   ]

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table", "KEK"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True },
                    { "type" : "html",
                    "id" : "kek",
                    "control_id" : "update_data",
                    "tab" : "KEK"}]

    def getData(self, params):
        province = params['province']
        df = getDf()
        df = df[df.province == province]
        df = week(df, params['from'], params['to'])
        #choseLine(params['ticker'], df)
        return df[[params['ticker']]]

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot()
        fig = plt_obj.get_figure()
        return fig

    def getHTML(self, params):
        return "HELLO WORLD"

app = StockExample()
app.launch(port=1337)

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#filelist = [ f for f in os.listdir(BASE_DIR) if f.endswith(".csv") ]
#df = readFile(os.path.join(BASE_DIR, filelist[1]))
#df = pd.concat([readFile(os.path.join(BASE_DIR, f)) for f in filelist], ignore_index=True)


#print(df)