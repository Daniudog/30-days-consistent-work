import sys
import os
import json
import uuid
import webbrowser
import subprocess

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QLineEdit,
    QComboBox, QSizePolicy, QGraphicsDropShadowEffect, QSpacerItem,
    QMessageBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QCursor, QPalette


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspaces.json")

ACCENT_COLORS = {
    "blue":   {"btn": "#4f7cff", "btn_hover": "#6d93ff", "glow": "rgba(79,124,255,0.35)"},
    "purple": {"btn": "#7c3aff", "btn_hover": "#9a5fff", "glow": "rgba(124,58,255,0.35)"},
    "teal":   {"btn": "#22c5a0", "btn_hover": "#3dddba", "glow": "rgba(34,197,160,0.35)"},
    "coral":  {"btn": "#ff6b6b", "btn_hover": "#ff8f8f", "glow": "rgba(255,107,107,0.35)"},
    "amber":  {"btn": "#f59e0b", "btn_hover": "#fbbf24", "glow": "rgba(245,158,11,0.35)"},
}

ITEM_TYPES = ["url", "folder", "command"]

ITEM_ICONS = {
    "url":     "🔗",
    "folder":  "📁",
    "command": "⌨",
}


# ─────────────────────────────────────────────
# DATA LAYER
# ─────────────────────────────────────────────

def default_data():
    return {"workspaces": []}


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default_data()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def new_workspace():
    return {
        "id": str(uuid.uuid4()),
        "name": "New Workspace",
        "description": "",
        "color": "blue",
        "items": []
    }


def new_item(item_type="url", value=""):
    return {
        "id": str(uuid.uuid4()),
        "type": item_type,
        "value": value
    }


# ─────────────────────────────────────────────
# ACTION ENGINE
# ─────────────────────────────────────────────

def execute_item(item):
    t = item["type"]
    v = item["value"].strip()
    if not v:
        return
    if t == "url":
        webbrowser.open(v)
    elif t == "folder":
        if os.path.exists(v):
            os.startfile(v)
        else:
            QMessageBox.warning(None, "Folder not found", f"Path does not exist:\n{v}")
    elif t == "command":
        subprocess.Popen(v, shell=True)


def launch_workspace(workspace):
    for item in workspace.get("items", []):
        execute_item(item)


# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────

GLOBAL_STYLE = """
QWidget {
    background-color: #08090d;
    color: #f0f2ff;
    font-family: "Segoe UI", sans-serif;
}

QScrollArea, QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

QScrollBar:vertical {
    background: #0f1118;
    width: 6px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #2a2f45;
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QLineEdit {
    background-color: #0f1118;
    border: 1px solid #1e2236;
    border-radius: 8px;
    padding: 6px 10px;
    color: #c8ccec;
    font-size: 13px;
    selection-background-color: #4f7cff;
}
QLineEdit:focus {
    border-color: #4f7cff;
}

QComboBox {
    background-color: #0f1118;
    border: 1px solid #1e2236;
    border-radius: 8px;
    padding: 5px 10px;
    color: #c8ccec;
    font-size: 12px;
    min-width: 90px;
}
QComboBox:focus { border-color: #4f7cff; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox::down-arrow { image: none; }
QComboBox QAbstractItemView {
    background-color: #13151f;
    border: 1px solid #1e2236;
    color: #c8ccec;
    selection-background-color: #4f7cff;
    selection-color: white;
    padding: 4px;
}

QMessageBox {
    background-color: #13151f;
}
"""


def card_style(color_key):
    return f"""
    QFrame#workspaceCard {{
        background-color: #13151f;
        border: 1px solid #1a1d2e;
        border-radius: 16px;
    }}
    QFrame#workspaceCard:hover {{
        border-color: #252840;
    }}
    """


def launch_btn_style(color_key):
    c = ACCENT_COLORS.get(color_key, ACCENT_COLORS["blue"])
    return f"""
    QPushButton {{
        background-color: {c['btn']};
        color: white;
        border: none;
        border-radius: 10px;
        padding: 8px 18px;
        font-size: 13px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {c['btn_hover']};
    }}
    QPushButton:pressed {{
        background-color: {c['btn']};
    }}
    """


def ghost_btn_style():
    return """
    QPushButton {
        background-color: rgba(255,255,255,0.04);
        color: #6b7090;
        border: 1px solid #1a1d2e;
        border-radius: 8px;
        padding: 5px 12px;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: rgba(255,255,255,0.09);
        color: #f0f2ff;
        border-color: #2a2f45;
    }
    """


def danger_btn_style():
    return """
    QPushButton {
        background-color: rgba(255,60,60,0.08);
        color: #ff6b6b;
        border: 1px solid rgba(255,60,60,0.2);
        border-radius: 8px;
        padding: 5px 12px;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: rgba(255,60,60,0.15);
    }
    """


def add_btn_style():
    return """
    QPushButton {
        background-color: rgba(79,124,255,0.08);
        color: #7da3ff;
        border: 1px solid rgba(79,124,255,0.2);
        border-radius: 8px;
        padding: 6px 14px;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: rgba(79,124,255,0.16);
    }
    """


# ─────────────────────────────────────────────
# ITEM ROW WIDGET
# ─────────────────────────────────────────────

class ItemRowWidget(QWidget):
    removed = pyqtSignal(str)          # item id
    changed = pyqtSignal()

    def __init__(self, item: dict, parent=None):
        super().__init__(parent)
        self.item = item
        self._build()

    def _build(self):
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)

        # Type selector
        self.type_combo = QComboBox()
        for t in ITEM_TYPES:
            self.type_combo.addItem(f"{ITEM_ICONS[t]}  {t}", t)
        idx = ITEM_TYPES.index(self.item["type"]) if self.item["type"] in ITEM_TYPES else 0
        self.type_combo.setCurrentIndex(idx)
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)

        # Value input
        self.value_edit = QLineEdit(self.item["value"])
        self.value_edit.setPlaceholderText(self._placeholder())
        self.value_edit.textChanged.connect(self._on_value_changed)

        # Run button
        self.run_btn = QPushButton("▶")
        self.run_btn.setFixedSize(30, 30)
        self.run_btn.setStyleSheet(ghost_btn_style())
        self.run_btn.setToolTip("Run this item")
        self.run_btn.clicked.connect(lambda: execute_item(self.item))

        # Remove button
        self.rm_btn = QPushButton("✕")
        self.rm_btn.setFixedSize(30, 30)
        self.rm_btn.setStyleSheet(danger_btn_style())
        self.rm_btn.setToolTip("Remove")
        self.rm_btn.clicked.connect(lambda: self.removed.emit(self.item["id"]))

        row.addWidget(self.type_combo)
        row.addWidget(self.value_edit, 1)
        row.addWidget(self.run_btn)
        row.addWidget(self.rm_btn)

    def _placeholder(self):
        t = self.item["type"]
        if t == "url":     return "https://..."
        if t == "folder":  return r"C:\Projects\..."
        return "code C:\\..."

    def _on_type_changed(self, idx):
        self.item["type"] = ITEM_TYPES[idx]
        self.value_edit.setPlaceholderText(self._placeholder())
        self.changed.emit()

    def _on_value_changed(self, text):
        self.item["value"] = text
        self.changed.emit()


# ─────────────────────────────────────────────
# WORKSPACE CARD WIDGET
# ─────────────────────────────────────────────

class WorkspaceCard(QFrame):
    deleted = pyqtSignal(str)
    data_changed = pyqtSignal()

    def __init__(self, workspace: dict, parent=None):
        super().__init__(parent)
        self.workspace = workspace
        self.expanded = False
        self.setObjectName("workspaceCard")
        self.setStyleSheet(card_style(workspace.get("color", "blue")))
        self._build()

    def _build(self):
        self._outer = QVBoxLayout(self)
        self._outer.setContentsMargins(0, 0, 0, 0)
        self._outer.setSpacing(0)

        # ── Header ──
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 16, 18, 16)
        header_layout.setSpacing(14)

        # Color dot
        color = self.workspace.get("color", "blue")
        dot_color = ACCENT_COLORS.get(color, ACCENT_COLORS["blue"])["btn"]
        dot = QLabel("●")
        dot.setStyleSheet(f"color: {dot_color}; font-size: 14px; background: transparent;")
        dot.setFixedWidth(16)

        # Name + description block
        meta = QVBoxLayout()
        meta.setSpacing(2)

        self.name_edit = QLineEdit(self.workspace["name"])
        self.name_edit.setStyleSheet("""
            QLineEdit {
                background: transparent; border: none; border-radius: 0;
                color: #f0f2ff; font-size: 16px; font-weight: 700; padding: 0;
            }
            QLineEdit:focus {
                background: rgba(255,255,255,0.04);
                border-bottom: 1px solid #4f7cff;
                border-radius: 4px;
                padding: 2px 4px;
            }
        """)
        self.name_edit.textChanged.connect(self._on_name_changed)

        self.desc_edit = QLineEdit(self.workspace.get("description", ""))
        self.desc_edit.setPlaceholderText("Add a description…")
        self.desc_edit.setStyleSheet("""
            QLineEdit {
                background: transparent; border: none; border-radius: 0;
                color: #6b7090; font-size: 12px; padding: 0;
                font-family: 'Consolas', monospace;
            }
            QLineEdit:focus {
                background: rgba(255,255,255,0.04);
                border-bottom: 1px solid #4f7cff;
                border-radius: 4px;
                padding: 2px 4px;
            }
        """)
        self.desc_edit.textChanged.connect(self._on_desc_changed)

        meta.addWidget(self.name_edit)
        meta.addWidget(self.desc_edit)

        # Color picker
        self.color_combo = QComboBox()
        for ck in ACCENT_COLORS:
            self.color_combo.addItem(ck.capitalize(), ck)
        keys = list(ACCENT_COLORS.keys())
        cur = self.workspace.get("color", "blue")
        if cur in keys:
            self.color_combo.setCurrentIndex(keys.index(cur))
        self.color_combo.currentIndexChanged.connect(self._on_color_changed)
        self.color_combo.setFixedWidth(95)

        # Item count badge
        count = len(self.workspace.get("items", []))
        self.count_label = QLabel(f"{count} item{'s' if count != 1 else ''}")
        self.count_label.setStyleSheet("color: #383d54; font-size: 12px; background: transparent;")

        # Launch button
        self.launch_btn = QPushButton("  Launch All")
        self.launch_btn.setStyleSheet(launch_btn_style(self.workspace.get("color", "blue")))
        self.launch_btn.setFixedHeight(34)
        self.launch_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.launch_btn.clicked.connect(self._launch_all)

        # Expand toggle
        self.toggle_btn = QPushButton("▾")
        self.toggle_btn.setFixedSize(32, 32)
        self.toggle_btn.setStyleSheet(ghost_btn_style())
        self.toggle_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggle_btn.clicked.connect(self._toggle_expand)

        # Delete
        del_btn = QPushButton("✕")
        del_btn.setFixedSize(32, 32)
        del_btn.setStyleSheet(danger_btn_style())
        del_btn.setToolTip("Delete workspace")
        del_btn.clicked.connect(self._delete_self)

        header_layout.addWidget(dot)
        header_layout.addLayout(meta, 1)
        header_layout.addWidget(self.count_label)
        header_layout.addWidget(self.color_combo)
        header_layout.addWidget(self.launch_btn)
        header_layout.addWidget(self.toggle_btn)
        header_layout.addWidget(del_btn)

        self._outer.addWidget(header)

        # ── Expandable body ──
        self._body = QWidget()
        self._body.setStyleSheet("background: transparent;")
        self._body.setVisible(False)
        body_layout = QVBoxLayout(self._body)
        body_layout.setContentsMargins(18, 0, 18, 16)
        body_layout.setSpacing(6)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #1a1d2e; background-color: #1a1d2e; border: none; max-height: 1px;")
        body_layout.addWidget(divider)
        body_layout.addSpacing(8)

        # Items container
        self._items_layout = QVBoxLayout()
        self._items_layout.setSpacing(6)
        body_layout.addLayout(self._items_layout)

        # Add item row
        add_row = QHBoxLayout()
        add_row.setSpacing(8)

        self.new_type_combo = QComboBox()
        for t in ITEM_TYPES:
            self.new_type_combo.addItem(f"{ITEM_ICONS[t]}  {t}", t)
        self.new_type_combo.setFixedWidth(110)

        self.new_value_edit = QLineEdit()
        self.new_value_edit.setPlaceholderText("Enter URL, folder path, or command…")
        self.new_value_edit.returnPressed.connect(self._add_item)

        add_btn = QPushButton("+ Add")
        add_btn.setStyleSheet(add_btn_style())
        add_btn.setFixedHeight(32)
        add_btn.clicked.connect(self._add_item)

        add_row.addWidget(self.new_type_combo)
        add_row.addWidget(self.new_value_edit, 1)
        add_row.addWidget(add_btn)

        body_layout.addSpacing(4)
        body_layout.addLayout(add_row)

        self._outer.addWidget(self._body)

        # Populate existing items
        for item in self.workspace.get("items", []):
            self._append_item_row(item)

    # ── Item management ──

    def _append_item_row(self, item):
        row = ItemRowWidget(item)
        row.removed.connect(self._remove_item)
        row.changed.connect(self._on_items_changed)
        self._items_layout.addWidget(row)

    def _add_item(self):
        t = self.new_type_combo.currentData()
        v = self.new_value_edit.text().strip()
        if not v:
            return
        item = new_item(t, v)
        self.workspace.setdefault("items", []).append(item)
        self._append_item_row(item)
        self.new_value_edit.clear()
        self._on_items_changed()

    def _remove_item(self, item_id):
        self.workspace["items"] = [i for i in self.workspace["items"] if i["id"] != item_id]
        for i in range(self._items_layout.count()):
            w = self._items_layout.itemAt(i).widget()
            if isinstance(w, ItemRowWidget) and w.item["id"] == item_id:
                w.setParent(None)
                break
        self._on_items_changed()

    # ── Change handlers ──

    def _on_name_changed(self, text):
        self.workspace["name"] = text
        self.data_changed.emit()

    def _on_desc_changed(self, text):
        self.workspace["description"] = text
        self.data_changed.emit()

    def _on_color_changed(self, idx):
        color = list(ACCENT_COLORS.keys())[idx]
        self.workspace["color"] = color
        self.launch_btn.setStyleSheet(launch_btn_style(color))
        dot_color = ACCENT_COLORS[color]["btn"]
        # update dot
        header = self._outer.itemAt(0).widget()
        header.layout().itemAt(0).widget().setStyleSheet(
            f"color: {dot_color}; font-size: 14px; background: transparent;"
        )
        self.data_changed.emit()

    def _on_items_changed(self):
        count = len(self.workspace.get("items", []))
        self.count_label.setText(f"{count} item{'s' if count != 1 else ''}")
        self.data_changed.emit()

    # ── Actions ──

    def _toggle_expand(self):
        self.expanded = not self.expanded
        self._body.setVisible(self.expanded)
        self.toggle_btn.setText("▴" if self.expanded else "▾")

    def _launch_all(self):
        launch_workspace(self.workspace)

    def _delete_self(self):
        reply = QMessageBox.question(
            self, "Delete workspace",
            f'Delete "{self.workspace["name"]}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.deleted.emit(self.workspace["id"])


# ─────────────────────────────────────────────
# MAIN WINDOW
# ─────────────────────────────────────────────

class LauncherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workspace Launcher")
        self.resize(860, 640)
        self.setStyleSheet(GLOBAL_STYLE)
        self.data = load_data()
        self._build_ui()

    def _build_ui(self):
        root = QWidget()
        root.setStyleSheet("background: #08090d;")
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(0)

        # ── Top bar ──
        topbar = QHBoxLayout()
        topbar.setSpacing(12)

        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        title = QLabel("Workspace Launcher")
        title.setStyleSheet("font-size: 22px; font-weight: 800; color: #f0f2ff; letter-spacing: -0.5px;")

        subtitle = QLabel("// instant environment switching")
        subtitle.setStyleSheet("font-size: 12px; color: #383d54; font-family: 'Consolas', monospace;")

        title_col.addWidget(title)
        title_col.addWidget(subtitle)

        add_ws_btn = QPushButton("+ New Workspace")
        add_ws_btn.setStyleSheet(add_btn_style() + "QPushButton { font-size: 13px; padding: 10px 20px; }")
        add_ws_btn.setFixedHeight(40)
        add_ws_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        add_ws_btn.clicked.connect(self._add_workspace)

        topbar.addLayout(title_col)
        topbar.addStretch()
        topbar.addWidget(add_ws_btn)

        layout.addLayout(topbar)
        layout.addSpacing(24)

        # ── Scroll area ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._cards_container = QWidget()
        self._cards_container.setStyleSheet("background: transparent;")
        self._cards_layout = QVBoxLayout(self._cards_container)
        self._cards_layout.setContentsMargins(0, 0, 0, 0)
        self._cards_layout.setSpacing(12)
        self._cards_layout.addStretch()

        scroll.setWidget(self._cards_container)
        layout.addWidget(scroll)

        # Populate cards
        for ws in self.data["workspaces"]:
            self._insert_card(ws)

    def _insert_card(self, workspace):
        card = WorkspaceCard(workspace)
        card.deleted.connect(self._delete_workspace)
        card.data_changed.connect(self._save)
        # Insert before the stretch
        idx = self._cards_layout.count() - 1
        self._cards_layout.insertWidget(idx, card)

    def _add_workspace(self):
        ws = new_workspace()
        self.data["workspaces"].append(ws)
        self._insert_card(ws)
        self._save()

    def _delete_workspace(self, ws_id):
        self.data["workspaces"] = [w for w in self.data["workspaces"] if w["id"] != ws_id]
        # Remove card widget
        for i in range(self._cards_layout.count()):
            item = self._cards_layout.itemAt(i)
            if item and isinstance(item.widget(), WorkspaceCard):
                if item.widget().workspace["id"] == ws_id:
                    item.widget().setParent(None)
                    break
        self._save()

    def _save(self):
        save_data(self.data)


# ─────────────────────────────────────────────
# ENTRY
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#08090d"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#f0f2ff"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#0f1118"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#c8ccec"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#13151f"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#f0f2ff"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#4f7cff"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = LauncherApp()
    window.show()
    sys.exit(app.exec())