# -*- coding: utf-8 -*-
from __future__ import division

from pathomx.tools import BaseTool
from pathomx.ui import ConfigPanel
from pathomx.data import DataDefinition
from pathomx.plugins import AnalysisPlugin
from pathomx.qt import *

METHOD_TYPES = {
    'Nearest Point': 'single',
    'Farthest Point/Voor Hees': 'complete',
    'UPGMA': 'average',
    'WPGMA': 'weighted',
    'UPGMC': 'centroid',
    'WPGMC': 'median',
    'Incremental (Ward)': 'ward',
}


class HierarchicalClusterConfigPanel(ConfigPanel):

    def __init__(self, *args, **kwargs):
        super(HierarchicalClusterConfigPanel, self).__init__(*args, **kwargs)

        self.cb_method = QComboBox()
        self.cb_method.addItems(METHOD_TYPES.keys())
        self.config.add_handler('method', self.cb_method, METHOD_TYPES)

        self.layout.addWidget(self.cb_method)

        self.finalise()


class HierarchicalClusterTool(BaseTool):

    name = "Hierarchical Cluster"
    shortname = 'hierarchical'

    subcategory = "Clustering"

    def __init__(self, *args, **kwargs):
        super(HierarchicalClusterTool, self).__init__(*args, **kwargs)

        self.data.add_input('input_data')  # Add input slot

        # Setup data consumer options
        self.data.consumer_defs.append(
            DataDefinition('input_data', {
            })
        )

        self.config.set_defaults({
            'method': 'complete',
        })

        self.addConfigPanel(HierarchicalClusterConfigPanel, 'Settings')


class HierarchicalCluster(AnalysisPlugin):

    def __init__(self, *args, **kwargs):
        super(HierarchicalCluster, self).__init__(*args, **kwargs)
        self.register_app_launcher(HierarchicalClusterTool)
