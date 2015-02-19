# -*- coding: utf-8 -*-
from pathomx.tools import BaseTool, ExportDataTool
from pathomx.ui import ConfigPanel, QFolderLineEdit

from pathomx.plugins import ImportPlugin
from pathomx.qt import *


# Dialog box for Metabohunter search options
class BrukerImportConfigPanel(ConfigPanel):

    autophase_algorithms = {
        'None': False,
        'Peak minima': 'Peak_minima',
        'ACME': 'ACME',
    }

    def __init__(self, parent, *args, **kwargs):
        super(BrukerImportConfigPanel, self).__init__(parent, *args, **kwargs)

        self.v = parent
        self.config = parent.config
        gb = QGroupBox('Search path')
        grid = QGridLayout()
        self.filename = QFolderLineEdit(description='Select parent folder to import Bruker spectra')
        grid.addWidget(QLabel('Path'), 0, 0)
        grid.addWidget(self.filename, 0, 1)
        self.config.add_handler('filename', self.filename)
        gb.setLayout(grid)
        self.layout.addWidget(gb)

        gb = QGroupBox('Phase correction')
        grid = QGridLayout()

        cb_phasealg = QComboBox()
        cb_phasealg.addItems(self.autophase_algorithms.keys())
        grid.addWidget(QLabel('Algorithm'), 2, 0)
        grid.addWidget(cb_phasealg, 2, 1)
        self.config.add_handler('autophase_algorithm', cb_phasealg, self.autophase_algorithms)

        gb.setLayout(grid)
        self.layout.addWidget(gb)

        gb = QGroupBox('Sample filter')
        grid = QGridLayout()
        pathfreg_le = QLineEdit()
        grid.addWidget(QLabel('Path filter (regexp)'), 1, 0)
        grid.addWidget(pathfreg_le, 1, 1)
        self.config.add_handler('path_filter_regexp', pathfreg_le)

        cb_sampleidfrom = QComboBox()
        cb_sampleidfrom.addItems(['Scan number', 'Experiment (regexp)', 'Path (regexp)'])
        grid.addWidget(QLabel('Sample ID from'), 2, 0)
        grid.addWidget(cb_sampleidfrom, 2, 1)
        self.config.add_handler('sample_id_from', cb_sampleidfrom)

        sample_regexp_le = QLineEdit()
        grid.addWidget(QLabel('Sample ID regexp'), 3, 0)
        grid.addWidget(sample_regexp_le, 3, 1)
        self.config.add_handler('sample_id_regexp', sample_regexp_le)

        cb_classfrom = QComboBox()
        cb_classfrom.addItems(['None', 'Experiment (regexp)', 'Path (regexp)'])
        grid.addWidget(QLabel('Class from'), 4, 0)
        grid.addWidget(cb_classfrom, 4, 1)
        self.config.add_handler('class_from', cb_classfrom)

        class_regexp_le = QLineEdit()
        grid.addWidget(QLabel('Class regexp'), 5, 0)
        grid.addWidget(class_regexp_le, 5, 1)
        self.config.add_handler('class_regexp', class_regexp_le)

        gb.setLayout(grid)
        self.layout.addWidget(gb)

        gb = QGroupBox('Advanced')
        grid = QGridLayout()
        cb_delimag = QCheckBox()
        grid.addWidget(QLabel('Delete imaginaries'), 0, 0)
        grid.addWidget(cb_delimag, 0, 1)
        self.config.add_handler('delete_imaginaries', cb_delimag)

        cb_reverse = QCheckBox()
        grid.addWidget(QLabel('Reverse spectra'), 1, 0)
        grid.addWidget(cb_reverse, 1, 1)
        self.config.add_handler('reverse_spectra', cb_reverse)

        cb_remdf = QCheckBox()
        grid.addWidget(QLabel('Remove digital filter'), 2, 0)
        grid.addWidget(cb_remdf, 2, 1)
        self.config.add_handler('remove_digital_filter', cb_remdf)

        cb_zf = QCheckBox()
        grid.addWidget(QLabel('Zero fill'), 3, 0)
        grid.addWidget(cb_zf, 3, 1)
        self.config.add_handler('zero_fill', cb_zf)

        le_zf_to = QLineEdit()
        grid.addWidget(le_zf_to, 4, 1)
        self.config.add_handler('zero_fill_to', le_zf_to, mapper=(lambda x: int(x), lambda x: str(x)))

        gb.setLayout(grid)

        self.layout.addWidget(gb)

        self.finalise()


class BrukerImport(BaseTool):

    name = "Import Bruker"
    shortname = 'bruker_import'
    autoconfig_name = "{filename}"

    legacy_launchers = ['NMRGlue.NMRApp']
    legacy_outputs = {'output': 'output_data'}
    icon = 'bruker.png'

    category = "Import"
    subcategory = "NMR"

    def __init__(self, *args, **kwargs):
        super(BrukerImport, self).__init__(*args, **kwargs)

        self.config.set_defaults({
            'filename': None,
            'autophase_algorithm': 'Peak_minima',
            'remove_digital_filter': True,
            'delete_imaginaries': True,
            'reverse_spectra': True,
            'zero_fill': True,
            'zero_fill_to': 32768,

            'path_filter_regexp': '',
            'sample_id_from': 'Scan number',  # Experiment name, Path regexp,
            'sample_id_regexp': '',

            'class_from': 'None',  # Experiment name, Path regexp,
            'class_regexp': '',
        })

        self.addConfigPanel(BrukerImportConfigPanel, 'Settings')

        self.data.add_output('output_data')  # Add output slot
        self.data.add_output('output_dic')  # Add output slot        

    def onImportBruker(self):
        """ Open a data file"""
        Qd = QFileDialog()
        Qd.setFileMode(QFileDialog.Directory)
        Qd.setOption(QFileDialog.ShowDirsOnly)

        folder = Qd.getExistingDirectory(self.w, 'Open parent folder for your Bruker NMR experiments')
        if folder:
            self.config.set('filename', folder)
            self.autogenerate()


class BrukerExport(ExportDataTool):

    name = "Export Bruker"
    export_description = "Export Bruker fid format spectra"
    export_type = "data"

    shortname = 'bruker_export'

    icon = 'bruker.png'

    category = "Export"
    subcategory = "NMR"

    def __init__(self, *args, **kwargs):
        super(BrukerExport, self).__init__(*args, **kwargs)

        self.config.set_defaults({
            'filename': None,
        })

        self.data.add_input('input_data')
        self.data.add_input('dic_list')

    def addExportDataToolbar(self):
        t = self.getCreatedToolbar('External Data', 'external-data')

        export_dataAction = QAction(QIcon(os.path.join(self.plugin.path, 'bruker.png')), 'Export spectra in Bruker format\u2026', self.w)
        export_dataAction.setStatusTip('Export spectra in Bruker format')
        export_dataAction.triggered.connect(self.onExportBruker)
        t.addAction(export_dataAction)

    def onExportBruker(self):
        """ Open a data file"""
        Qd = QFileDialog()
        Qd.setFileMode(QFileDialog.Directory)
        Qd.setOption(QFileDialog.ShowDirsOnly)

        folder = Qd.getExistingDirectory(self.w, 'Open parent folder for your Bruker NMR experiments')
        if folder:
            self.config.set('filename', folder)
            self.autogenerate()


class NMRGlue(ImportPlugin):

    def __init__(self, *args, **kwargs):
        super(NMRGlue, self).__init__(*args, **kwargs)
        self.register_app_launcher(BrukerImport)
        self.register_app_launcher(BrukerExport)
