import sys
from pathlib import Path

try:
    from PySide6.QtGui import QColor, QPalette
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QApplication,
        QComboBox,
        QDoubleSpinBox,
        QFileDialog,
        QFormLayout,
        QFrame,
        QGridLayout,
        QGroupBox,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QSizePolicy,
        QPushButton,
        QScrollArea,
        QSpinBox,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
        QWidget,
    )
except ImportError as exc:
    raise SystemExit('PySide6 nie jest zainstalowane. Zainstaluj je komendą: pip install PySide6') from exc

from Alghoritm import HarmonySearch
from DataConvertion import load_csv


STATS = ['pancerz', 'zdrowie', 'mana', 'obrazenia', 'charyzma']
ARMOR_SLOTS = ['Glowa', 'Korpus', 'Nogi', 'Buty', 'Rekawice']


def format_number(value) -> str:
    if isinstance(value, float):
        return f'{value:.2f}'
    return str(value)


def build_item_tooltip(item: dict | None, quantity: int = 1) -> str:
    if not item or item.get('id') is None:
        return 'Pusty slot.'

    lines = [
        f"<b>{item.get('nazwa', 'Bez nazwy')}</b>",
        f"Kategoria: {item.get('kategoria', '-')}",
        f"Slot: {item.get('slot', '-')}",
        f"Waga: {format_number(item.get('waga_kg', 0.0))} kg",
    ]

    if quantity > 1:
        lines.append(f'Ilość: {quantity}')

    lines.append('')
    for stat_name in STATS:
        lines.append(f'{stat_name.capitalize()}: {item.get(stat_name, 0)}')

    return '<br>'.join(lines)


class ItemCard(QFrame):
    def __init__(self, title: str, compact: bool = False) -> None:
        super().__init__()
        self.compact = compact
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if compact:
            self.title_label.hide()
        else:
            self.title_label.setFixedHeight(20)
            self.title_label.setStyleSheet('font-size: 11px;')

        self.name_label = QLabel('Pusty')
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setWordWrap(True)
        if compact:
            self.name_label.setStyleSheet('font-size: 10px;')
        else:
            self.name_label.setStyleSheet('font-size: 11px;')

        layout = QVBoxLayout(self)
        if compact:
            layout.setContentsMargins(8, 6, 8, 6)
            layout.setSpacing(4)
        else:
            layout.setContentsMargins(8, 8, 8, 8)
            layout.setSpacing(5)
        layout.addWidget(self.title_label)
        layout.addWidget(self.name_label, 1)

        if compact:
            self.setMinimumSize(112, 76)
        else:
            self.setMinimumSize(126, 92)
        self.show_empty(title)

    def show_empty(self, title: str) -> None:
        if not self.compact:
            self.title_label.setText(title)
        self.name_label.setText('Pusty' if not self.compact else '—')
        self.setToolTip('Pusty slot.')
        self.setStyleSheet(
            'QFrame {'
            ' background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f2ebe2, stop:1 #e2d6c6);'
            ' border: 1px solid #c9b9a1;'
            ' border-radius: 14px;'
            '}'
            'QLabel { color: #6a5c4d; }'
        )

    def show_item(self, title: str, item: dict, quantity: int = 1) -> None:
        item_name = item.get('nazwa', 'Bez nazwy')
        if quantity > 1:
            item_name = f'{item_name} x{quantity}'

        if not self.compact:
            self.title_label.setText(title)
        self.name_label.setText(item_name)
        self.setToolTip(build_item_tooltip(item, quantity))
        self.setStyleSheet(
            'QFrame {'
            ' background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fffaf0, stop:1 #f3dfc2);'
            ' border: 1px solid #b88754;'
            ' border-radius: 14px;'
            '}'
            'QLabel { color: #2d261d; }'
        )


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Optymalizacja ekwipunku')
        self.resize(1450, 860)
        self.setStyleSheet(self._build_styles())

        root = QWidget()
        self.setCentralWidget(root)

        self.armor_cards = {}
        self.backpack_cards = []

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        self.left_panel = self._build_left_panel()
        self.armor_panel = self._build_center_panel()
        self.right_panel = self._build_right_panel()
        self.backpack_panel = self._build_backpack_panel()

        left_center_panel = QWidget()
        left_center_layout = QVBoxLayout(left_center_panel)
        left_center_layout.setContentsMargins(0, 0, 0, 0)
        left_center_layout.setSpacing(8)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(16)
        top_row.addWidget(self.left_panel, 2)
        top_row.addWidget(self.armor_panel, 4)

        left_center_layout.addLayout(top_row, 3)
        left_center_layout.addWidget(self.backpack_panel, 2)

        main_layout.addWidget(left_center_panel, 6)
        main_layout.addWidget(self.right_panel, 2)

        default_file = Path.cwd() / 'przedmioty.csv'
        self.file_input.setText(str(default_file))
        self._rebuild_backpack_grid()
        self._show_empty_state()

        if default_file.exists():
            self._refresh_file_info(str(default_file))

    def _apply_line_edit_palette(self, line_edit: QLineEdit) -> None:
        palette = line_edit.palette()
        palette.setColor(QPalette.ColorRole.Text, QColor('#2f261c'))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor('#7d6d5b'))
        palette.setColor(QPalette.ColorRole.Base, QColor('#fffdf8'))
        line_edit.setPalette(palette)

    def _build_styles(self) -> str:
        return """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f6f0e8, stop:0.55 #efe4d6, stop:1 #e7d8c4);
        }
        QGroupBox {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fffdf9, stop:1 #f8efe3);
            border: 1px solid #cfbfa8;
            border-radius: 12px;
            margin-top: 12px;
            padding-top: 18px;
            font-size: 14px;
            font-weight: bold;
            color: #3a2e22;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 14px;
            padding: 0 6px;
            color: #6d4625;
            background: #fff7ec;
            border-radius: 6px;
        }
        QLabel {
            color: #2f261c;
        }
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTableWidget {
            background: #fffdf8;
            border: 1px solid #cfbfa8;
            border-radius: 8px;
            padding: 6px;
            color: #2f261c;
            selection-background-color: #d6b48d;
            selection-color: #2f261c;
        }
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border: 1px solid #b6804c;
            background: #fffaf2;
        }
        QComboBox::drop-down, QSpinBox::up-button, QSpinBox::down-button,
        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
            background: #eadbc8;
            border: none;
            border-left: 1px solid #cfbfa8;
            width: 22px;
        }
        QComboBox::drop-down:hover, QSpinBox::up-button:hover, QSpinBox::down-button:hover,
        QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
            background: #dcc3a5;
        }
        QScrollArea {
            background: #fffaf3;
            border: none;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8d5a30, stop:1 #714523);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 9px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #9c673a, stop:1 #7d4d28);
        }
        QPushButton:pressed {
            background: #6a3f20;
        }
        QTableWidget {
            gridline-color: #dbc8b1;
            alternate-background-color: #fcf6ef;
        }
        QToolTip {
            background: #fff8ee;
            color: #2d261d;
            border: 1px solid #c9a57c;
            padding: 6px;
        }
        QScrollBar:vertical {
            background: #efe1cf;
            width: 12px;
            border-radius: 6px;
            margin: 4px;
        }
        QScrollBar::handle:vertical {
            background: #c69a6e;
            min-height: 24px;
            border-radius: 6px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QHeaderView::section {
            background: #eadbc8;
            border: none;
            padding: 6px;
            font-weight: bold;
        }
        """

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(14)

        file_box = QGroupBox('Dane wejściowe')
        file_layout = QVBoxLayout(file_box)

        file_row = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText('Ścieżka do pliku CSV')
        self._apply_line_edit_palette(self.file_input)

        browse_button = QPushButton('Przeglądaj')
        browse_button.clicked.connect(self.choose_file)

        file_row.addWidget(self.file_input, 1)
        file_row.addWidget(browse_button)
        file_layout.addLayout(file_row)

        self.file_info_label = QLabel('Wczytaj plik z listą przedmiotów.')
        self.file_info_label.setWordWrap(True)
        file_layout.addWidget(self.file_info_label)

        params_box = QGroupBox('Parametry algorytmu')
        params_layout = QFormLayout(params_box)

        self.focus_input = QComboBox()
        self.focus_input.addItems(STATS)

        self.max_weight_input = QDoubleSpinBox()
        self.max_weight_input.setRange(0.0, 100000.0)
        self.max_weight_input.setDecimals(2)
        self.max_weight_input.setValue(100.0)

        self.max_slots_input = QSpinBox()
        self.max_slots_input.setRange(1, 100)
        self.max_slots_input.setValue(20)
        self.max_slots_input.valueChanged.connect(self._rebuild_backpack_grid)

        params_layout.addRow('Statystyka priorytetowa', self.focus_input)
        params_layout.addRow('Maks. waga [kg]', self.max_weight_input)
        params_layout.addRow('Maks. sloty plecaka', self.max_slots_input)

        run_button = QPushButton('Uruchom algorytm')
        run_button.clicked.connect(self.run_algorithm)

        self.status_label = QLabel('Gotowe.')
        self.status_label.setWordWrap(True)

        layout.addWidget(file_box)
        layout.addWidget(params_box)
        layout.addWidget(run_button)
        layout.addWidget(self.status_label)
        layout.addStretch()
        return panel

    def _build_center_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        armor_box = QGroupBox('Ekwipunek')
        armor_layout = QGridLayout(armor_box)
        armor_layout.setContentsMargins(10, 8, 10, 10)
        armor_layout.setHorizontalSpacing(10)
        armor_layout.setVerticalSpacing(8)

        positions = {
            'Glowa': (0, 0),
            'Korpus': (1, 0),
            'Rekawice': (1, 1),
            'Nogi': (2, 0),
            'Buty': (2, 1),
        }

        for slot_name in ARMOR_SLOTS:
            card = ItemCard(slot_name)
            self.armor_cards[slot_name] = card
            row, column = positions[slot_name]
            armor_layout.addWidget(card, row, column)

        layout.addWidget(armor_box, 1)
        return panel

    def _build_backpack_panel(self) -> QWidget:
        backpack_box = QGroupBox('Plecak')
        backpack_layout = QVBoxLayout(backpack_box)
        backpack_layout.setContentsMargins(6, 0, 6, 4)

        self.backpack_scroll = QScrollArea()
        self.backpack_scroll.setWidgetResizable(True)
        self.backpack_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.backpack_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.backpack_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.backpack_scroll.viewport().setStyleSheet('background: #fffaf3;')

        self.backpack_wrapper = QWidget()
        self.backpack_wrapper.setStyleSheet('background: #fffaf3;')
        self.backpack_layout = QGridLayout(self.backpack_wrapper)
        self.backpack_layout.setHorizontalSpacing(10)
        self.backpack_layout.setVerticalSpacing(12)
        self.backpack_layout.setContentsMargins(6, 0, 6, 4)

        self.backpack_wrapper.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.backpack_scroll.setWidget(self.backpack_wrapper)
        backpack_layout.addWidget(self.backpack_scroll)
        return backpack_box

    def _update_backpack_scroll_height(self, slot_count: int) -> None:
        columns = 5
        visible_rows = min(4, max(1, (slot_count + columns - 1) // columns))
        card_height = self.backpack_cards[0].minimumHeight() if self.backpack_cards else 76
        spacing = self.backpack_layout.verticalSpacing()
        margins = self.backpack_layout.contentsMargins()
        frame_extra = 4

        total_height = (
            margins.top()
            + margins.bottom()
            + visible_rows * card_height
            + max(0, visible_rows - 1) * spacing
            + frame_extra
        )
        self.backpack_scroll.setFixedHeight(total_height)

    def _build_right_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(14)

        summary_box = QGroupBox('Wynik')
        summary_layout = QFormLayout(summary_box)

        self.fitness_label = QLabel('-')
        self.weight_label = QLabel('-')
        self.slots_label = QLabel('-')
        self.focus_label = QLabel('-')

        summary_layout.addRow('Fitness', self.fitness_label)
        summary_layout.addRow('Łączna waga', self.weight_label)
        summary_layout.addRow('Zajęte sloty', self.slots_label)
        summary_layout.addRow('Priorytet', self.focus_label)

        stats_box = QGroupBox('Statystyki gracza')
        stats_layout = QVBoxLayout(stats_box)

        self.stats_table = QTableWidget(0, 2)
        self.stats_table.setHorizontalHeaderLabels(['Statystyka', 'Wartość'])
        self.stats_table.setAlternatingRowColors(True)
        self.stats_table.verticalHeader().setVisible(False)
        self.stats_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.stats_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.stats_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.stats_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        stats_layout.addWidget(self.stats_table)

        info_box = QGroupBox('Opis')
        info_layout = QVBoxLayout(info_box)
        self.info_label = QLabel(
            'Po najechaniu na element ekwipunku zobaczysz tooltip z nazwą, wagą i statystykami.'
        )
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)

        layout.addWidget(summary_box)
        layout.addWidget(stats_box, 1)
        layout.addWidget(info_box)
        return panel

    def choose_file(self) -> None:
        selected_file, _ = QFileDialog.getOpenFileName(
            self,
            'Wybierz plik CSV',
            self.file_input.text() or str(Path.cwd()),
            'Pliki CSV (*.csv);;Wszystkie pliki (*)'
        )

        if selected_file:
            self.file_input.setText(selected_file)
            self._refresh_file_info(selected_file)

    def _refresh_file_info(self, path: str) -> None:
        try:
            items = load_csv(path)
            self.file_info_label.setText(f'Wczytano {len(items)} przedmiotów z pliku.')
        except Exception:
            self.file_info_label.setText('Nie udało się odczytać pliku.')

    def _rebuild_backpack_grid(self) -> None:
        while self.backpack_layout.count():
            child = self.backpack_layout.takeAt(0)
            widget = child.widget()
            if widget is not None:
                widget.deleteLater()

        self.backpack_cards = []
        slots = self.max_slots_input.value() if hasattr(self, 'max_slots_input') else 20
        columns = 5

        for index in range(slots):
            card = ItemCard(f'Slot {index + 1}', compact=True)
            self.backpack_cards.append(card)
            self.backpack_layout.addWidget(card, index // columns, index % columns)

        self._update_backpack_scroll_height(slots)

    def _show_empty_state(self) -> None:
        for slot_name, card in self.armor_cards.items():
            card.show_empty(slot_name)

        for index, card in enumerate(self.backpack_cards):
            card.show_empty(f'Slot {index + 1}')

        self.fitness_label.setText('-')
        self.weight_label.setText('-')
        self.slots_label.setText('-')
        self.focus_label.setText('-')
        self.stats_table.setRowCount(0)

    def run_algorithm(self) -> None:
        items_file = self.file_input.text().strip()
        if not items_file:
            QMessageBox.warning(self, 'Brak pliku', 'Wskaż plik CSV z przedmiotami.')
            return

        try:
            items = load_csv(items_file)
            self.file_info_label.setText(f'Wczytano {len(items)} przedmiotów z pliku.')
        except Exception as error:
            QMessageBox.critical(self, 'Błąd wczytywania', str(error))
            self.status_label.setText('Nie udało się wczytać pliku.')
            return

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.status_label.setText('Algorytm pracuje...')

        try:
            result = HarmonySearch(
                focus_stat=self.focus_input.currentText(),
                max_weight=self.max_weight_input.value(),
                max_slots=self.max_slots_input.value(),
                items_file=items_file,
            )
        except Exception as error:
            QMessageBox.critical(self, 'Błąd obliczeń', str(error))
            self.status_label.setText('Uruchomienie algorytmu nie powiodło się.')
            return
        finally:
            QApplication.restoreOverrideCursor()

        self._show_result(result)
        self.status_label.setText('Optymalizacja zakończona.')

    def _show_result(self, result: dict) -> None:
        for slot_name in ARMOR_SLOTS:
            item = result.get('zbroja', {}).get(slot_name)
            if item and item.get('id') is not None:
                self.armor_cards[slot_name].show_item(slot_name, item)
            else:
                self.armor_cards[slot_name].show_empty(slot_name)

        backpack = result.get('plecak', [])
        visible_slots = max(self.max_slots_input.value(), len(backpack))

        if visible_slots != len(self.backpack_cards):
            while self.backpack_layout.count():
                child = self.backpack_layout.takeAt(0)
                widget = child.widget()
                if widget is not None:
                    widget.deleteLater()

            self.backpack_cards = []
            columns = 5
            for index in range(visible_slots):
                card = ItemCard(f'Slot {index + 1}', compact=True)
                self.backpack_cards.append(card)
                self.backpack_layout.addWidget(card, index // columns, index % columns)

            self._update_backpack_scroll_height(visible_slots)

        for index, card in enumerate(self.backpack_cards):
            if index < len(backpack):
                item = backpack[index]
                card.show_item(f'Slot {index + 1}', item, item.get('wylosowana_ilosc', 1))
            else:
                card.show_empty(f'Slot {index + 1}')

        self.fitness_label.setText(format_number(result.get('fitness_score', 0)))
        self.weight_label.setText(format_number(result.get('calkowita_waga', 0.0)))
        self.slots_label.setText(str(result.get('zajete_sloty', 0)))
        self.focus_label.setText(result.get('focus_stat', '-'))

        player_stats = result.get('player_stats', {})
        self.stats_table.setRowCount(len(STATS))
        for row, stat_name in enumerate(STATS):
            self.stats_table.setItem(row, 0, QTableWidgetItem(stat_name.capitalize()))
            self.stats_table.setItem(row, 1, QTableWidgetItem(str(player_stats.get(stat_name, 0))))


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
