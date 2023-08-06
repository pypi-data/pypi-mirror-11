from io import BytesIO
from collections import defaultdict
from os import path

from PyQt4 import QtCore, QtGui, QtWebKit

from Orange.widgets import widget, gui, settings
from skfusion import fusion
from orangecontrib.datafusion.models import Relation, FusionGraph, FittedFusionGraph


JS_GRAPH = open(path.join(path.dirname(__file__), 'graph_script.js'), encoding='utf-8').read()

DECOMPOSITION_ALGO = [
    ('Matrix tri-factorization', fusion.Dfmf),
    ('Matrix tri-completion', fusion.Dfmc),
]
INITIALIZATION_ALGO = [
    'Random',
    'Random C',
    'Random Vcol'
]


class Output:
    RELATION = 'Relation'
    FUSION_GRAPH = 'Fusion Graph'
    FUSER = 'Fitted Fusion Graph'


def rel_shape(relation):
    return '{}×{}'.format(*relation.shape)


def rel_cols(relation):
    return [relation.row_type.name,
            relation.name or '→',
            relation.col_type.name]


def relation_str(relation):
    return '[{}] {}'.format(rel_shape(relation.data), ' '.join(rel_cols(relation)))


def bold_item(item):
    font = item.font()
    font.setBold(True)
    item.setFont(font)


def redraw_graph(webview, graph):
    stream = BytesIO()
    if graph:
        graph.draw_graphviz(stream, 'svg')
    stream.seek(0)
    stream = QtCore.QByteArray(stream.read())
    webview.setContent(stream, 'image/svg+xml')
    webview.evalJS(JS_GRAPH)


class OWFusionGraph(widget.OWWidget):
    name = "Fusion Graph"
    description = "Construct data fusion graph and run " \
                  "collective matrix factorization."
    priority = 10000
    icon = "icons/FusionGraph.svg"
    inputs = [("Relation", Relation, "on_relation_change", widget.Multiple)]
    outputs = [
        (Output.RELATION, Relation),
        (Output.FUSER, FittedFusionGraph, widget.Default),
        (Output.FUSION_GRAPH, FusionGraph),
    ]

    # Signal emitted when a node in the SVG is selected, carrying its name
    graph_element_selected = QtCore.pyqtSignal(str)

    pref_algo_name = settings.Setting('')
    pref_algorithm = settings.Setting(0)
    pref_initialization = settings.Setting(0)
    pref_n_iterations = settings.Setting(10)
    pref_rank = settings.Setting(10)
    autorun = settings.Setting(False)

    def __init__(self):
        super().__init__()
        self.n_object_types = 0
        self.n_relations = 0
        self.relations = {}  # id-->relation map
        self.graph_element_selected.connect(self.on_graph_element_selected)
        self.graph = FusionGraph(fusion.FusionGraph())
        self.webview = gui.WebviewWidget(self.mainArea, self)
        self._create_layout()

    @QtCore.pyqtSlot(str)
    def on_graph_element_selected(self, element_id):
        """Handle self.graph_element_selected signal, and highlight also:
           * if edge was selected, the two related nodes,
           * if node was selected, all its edges.
           Additionally, update the info box.
        """
        if not element_id:
            return self._populate_table()
        selected_is_edge = element_id.startswith('edge ')
        nodes = self.graph.get_selected_nodes(element_id)
        # CSS selector query for selection-relevant nodes
        selector = ','.join('[id^="node "][id*="`%s`"]' % n.name for n in nodes)
        # If a node was selected, include the edges that connect to it
        if not selected_is_edge:
            selector += ',[id^="edge "][id*="`%s`"]' % nodes[0].name
        # Highlight these additional elements
        self.webview.evalJS("highlight('%s');" % selector)
        # Update the control table table
        if selected_is_edge:
            relations = self.graph.get_relations(*nodes)
        else:
            relations = (set(i for i in self.graph.in_relations(nodes[0])) |
                         set(i for i in self.graph.out_relations(nodes[0])))
        self._populate_table(relations)

    def _create_layout(self):
        info = gui.widgetBox(self.controlArea, 'Info')
        gui.label(info, self, '%(n_object_types)d object types')
        gui.label(info, self, '%(n_relations)d relations')
        # Table view of relation details
        info = gui.widgetBox(self.controlArea, 'Relations')

        def send_relation(selected, deselected):
            if not selected:
                assert len(deselected) > 0
                relation = None
            else:
                assert len(selected) == 1
                data = self.table.rowData(selected[0].top())
                relation = Relation(data)
            self.send(Output.RELATION, relation)

        self.table = gui.TableWidget(info, select_rows=True)
        self.table.selectionChanged = send_relation
        self.table.setColumnFilter(bold_item, (1, 3))

        self.controlArea.layout().addStretch(1)
        gui.lineEdit(self.controlArea,
                     self, 'pref_algo_name', 'Fuser name',
                     callback=self.checkcommit, enterPlaceholder=True)
        gui.radioButtons(self.controlArea,
                         self, 'pref_algorithm', [i[0] for i in DECOMPOSITION_ALGO],
                         box='Decomposition algorithm',
                         callback=self.checkcommit)
        gui.radioButtons(self.controlArea,
                         self, 'pref_initialization', INITIALIZATION_ALGO,
                         box='Initialization algorithm',
                         callback=self.checkcommit)
        gui.hSlider(self.controlArea, self, 'pref_n_iterations',
                    'Maximum number of iterations',
                    minValue=10, maxValue=500, createLabel=True,
                    callback=self.checkcommit)
        self.slider_rank = gui.hSlider(self.controlArea, self, 'pref_rank',
                                       'Factorization rank',
                                       minValue=1, maxValue=100, createLabel=True,
                                       labelFormat=" %d%%",
                                       callback=self.checkcommit)
        gui.auto_commit(self.controlArea, self, "autorun", "Run",
                        checkbox_label="Run after any change  ")

    def checkcommit(self):
        return self.commit()

    def commit(self):
        self.progressbar = gui.ProgressBar(self, self.pref_n_iterations)
        Algo = DECOMPOSITION_ALGO[self.pref_algorithm][1]
        init_type = INITIALIZATION_ALGO[self.pref_initialization].lower().replace(' ', '_')
        # Update rank on object-types
        maxrank = defaultdict(int)
        for rel in self.graph.relations:
            rows, cols = rel.data.shape
            row_type, col_type = rel.row_type, rel.col_type
            if rows > maxrank[row_type]:
                maxrank[row_type] = row_type.rank = max(5, int(rows * (self.pref_rank / 100)))
            if cols > maxrank[col_type]:
                maxrank[col_type] = col_type.rank = max(5, int(cols * (self.pref_rank / 100)))
        # Run the algo ...
        self.fuser = Algo(init_type=init_type,
                          max_iter=self.pref_n_iterations,
                          random_state=0,
                          callback=lambda *args: self.progressbar.advance()).fuse(self.graph)
        self.progressbar.finish()
        self.fuser.name = self.pref_algo_name
        self.send(Output.FUSER, FittedFusionGraph(self.fuser))

    def _populate_table(self, relations=None):
        self.table.clear()
        for rel in relations or self.graph.relations:
            self.table.addRow([rel_shape(rel.data)] + rel_cols(rel), data=rel)
        self.table.selectFirstRow()

    def on_relation_change(self, relation, id):
        def _on_remove_relation(id):
            try: relation = self.relations.pop(id)
            except KeyError: return
            self.graph.remove_relation(relation)

        def _on_add_relation(relation, id):
            _on_remove_relation(id)
            self.relations[id] = relation
            self.graph.add_relation(relation)

        if relation:
            _on_add_relation(relation.relation, id)
        else:
            _on_remove_relation(id)
        self._populate_table()
        LIMIT_RANK_THRESHOLD = 1000  # If so many objects or more, limit maximum rank
        self.slider_rank.setMaximum(30
                                    if any(max(rel.data.shape) > LIMIT_RANK_THRESHOLD
                                           for rel in self.graph.relations)
                                    else
                                    100)
        redraw_graph(self.webview, self.graph)
        self.send(Output.FUSION_GRAPH, FusionGraph(self.graph))
        # this ensures gui.label-s get updated
        self.n_object_types = self.graph.n_object_types
        self.n_relations = self.graph.n_relations

    # called when all signals are received, so the graph is updated only once
    def handleNewSignals(self):
        self.commit()


def main():
    # example from https://github.com/marinkaz/scikit-fusion
    import numpy as np
    R12 = np.random.rand(50, 100)
    R22 = np.random.rand(100, 100)
    R13 = np.random.rand(50, 40)
    R31 = np.random.rand(40, 50)
    R23 = np.random.rand(100, 40)
    R23 = np.random.rand(100, 40)
    R24 = np.random.rand(100, 400)
    R34 = np.random.rand(40, 400)
    t1 = fusion.ObjectType('Users', 10)
    t2 = fusion.ObjectType('Actors', 20)
    t3 = fusion.ObjectType('Movies', 30)
    t4 = fusion.ObjectType('Genres', 40)
    relations = [fusion.Relation(R12, t1, t2, name='like'),
                 fusion.Relation(R13, t1, t3, name='rated'),
                 fusion.Relation(R23, t2, t3, name='play in'),
                 fusion.Relation(R31, t3, t1),
                 fusion.Relation(R24, t2, t4, name='prefer'),
                 fusion.Relation(R34, t3, t4, name='belong to'),
                 fusion.Relation(R22, t2, t2, name='married to')]

    app = QtGui.QApplication(['asdf'])
    w = OWFusionGraph()
    w.show()

    def _add_next_relation(event,
                           id=iter(range(len(relations))),
                           relation=iter(map(Relation, relations))):
        try: w.on_relation_change(next(relation), next(id))
        except StopIteration:
            w.killTimer(w.timer_id)
            w.on_relation_change(None, 4)  # Remove relation #4
    w.timerEvent = _add_next_relation
    w.timer_id = w.startTimer(500)
    app.exec()


if __name__ == "__main__":
    main()
