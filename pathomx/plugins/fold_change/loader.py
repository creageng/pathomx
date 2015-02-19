# -*- coding: utf-8 -*-
from __future__ import division

from pathomx.tools import BaseTool
from pathomx.data import DataDefinition
from pathomx.plugins import AnalysisPlugin
from pathomx.qt import *


class FoldChangeApp(BaseTool):

    name = "Fold Change"
    notebook = 'fold_change.ipynb'
    shortname = 'fold_change'

    legacy_inputs = {'input': 'input_data'}
    legacy_outputs = {'output': 'output_data'}

    def __init__(self, *args, **kwargs):
        super(FoldChangeApp, self).__init__(*args, **kwargs)
        # Define automatic mapping (settings will determine the route; allow manual tweaks later)

        self.addExperimentConfigPanel()

        self.data.add_input('input_data')  # Add input slot
        self.data.add_output('output_data')

        # Setup data consumer options
        self.data.consumer_defs.append(
            DataDefinition('input_data', {
            'classes_n': (">1", None),  # At least one class
            })
        )

        self.config.set_defaults({
            'use_baseline_minima': True,
        })

        t = self.addToolBar('Fold change')
        t.cb_baseline_minima = QCheckBox('Auto minima')
        self.config.add_handler('use_baseline_minima', t.cb_baseline_minima)
        t.cb_baseline_minima.setStatusTip('Replace zero values with half of the smallest value')
        t.addWidget(t.cb_baseline_minima)
        self.toolbars['fold_change'] = t


class FoldChange(AnalysisPlugin):

    def __init__(self, *args, **kwargs):
        super(FoldChange, self).__init__(*args, **kwargs)
        self.register_app_launcher(FoldChangeApp)
