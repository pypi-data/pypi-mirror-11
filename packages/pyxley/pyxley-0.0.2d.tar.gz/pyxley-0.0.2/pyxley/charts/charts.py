from ..ui import UIComponent
import pandas as pd
from flask import request, jsonify, make_response

class Chart(UIComponent):
    name = "Chart"

    @staticmethod
    def apply_filters(df, filters):
        idx = pd.Series([True]*df.shape[0])
        for k, v in filters.items():
            if k not in df.columns:
                continue
            idx &= (df[k] == v)

        return df.loc[idx]

class LinePlot(Chart):
    def __init__(self, chart_id, url, plot_object):
        opts = {
            "url": url,
            "chartid": chart_id
        }
        super(LinePlot, self).__init__("LinePlot", opts, plot_object.api_route)

