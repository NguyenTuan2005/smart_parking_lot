def getGlobalStyle():
    """
    Trả về CSS stylesheet đã điều chỉnh cho PyQt6.
    """
    return """
        /* === MAIN WINDOW === */
        QMainWindow {
            background-color: #2c3e50;
        }
        
        /* === DEFAULT TEXT === */
        QLabel {
            color: #ecf0f1;
            font-size: 12px; /* Giảm từ 14px */
        }
        
        /* === FRAMES === */
        QFrame#StatusFrame, QFrame#FeeFrame, QFrame#CardInfoFrame {
            border-radius: 6px; /* Giảm từ 8px */
            padding: 8px;      /* Giảm từ 10px */
            margin-bottom: 8px; /* Giảm từ 10px */
            border: 1px solid #34495e;
        }
        
        QFrame#VideoFrame {
            border: 2px solid #ffffff;
            border-radius: 4px; /* Giảm từ 5px */
            background-color: #000000;
        }
        
        /* === TITLE LABELS === */
        QLabel#TitleLabel {
            font-size: 16px; /* Giảm từ 18px */
            font-weight: bold;
            color: #ffffff;
            border-bottom: 1px solid #f1c40f; /* vàng nhạt */
            padding-bottom: 3px; /* Giảm từ 5px */
            margin-bottom: 8px; /* Giảm từ 10px */
        }
        
        /* === SPECIAL LABELS === */
        QLabel#ParkingLogo {
            font-size: 20px; /* Giảm từ 24px */
            font-weight: bold;
            color: #ffffff;
        }
        
        QLabel#BigNumber {
            font-size: 30px; /* Giảm từ 36px */
            font-weight: bold;
            color: #f1c40f;
        }
        
        /* === INPUT FIELDS === */
        QLineEdit {
            padding: 4px; /* Giảm từ 5px */
            border: 1px solid #f1c40f;
            border-radius: 3px; /* Giảm từ 4px */
            background-color: #34495e;
            color: #ecf0f1;
        }
        
        QLineEdit:focus {
            border: 2px solid #3498db;
            background-color: #2c3e50;
        }
        
        /* === BUTTONS === */
        QPushButton {
            background-color: #f1c40f;
            color: #000000;
            border-radius: 3px; /* Giảm từ 4px */
            padding: 4px 8px; /* Giảm từ 5px 10px */
            font-weight: bold;
            border: none;
        }

        QPushButton:hover {
            background-color: #d4b013;
        }

        QPushButton:pressed {
            background-color: #a8870f;
        }
        
        /* === TABLES === */
        QTableWidget {
            background-color: #34495e;
            color: #ecf0f1;
            border: 1px solid #2c3e50;
            gridline-color: #2c3e50;
            font-size: 12px; /* Đồng bộ với QLabel */
        }
        
        QTableWidget::item {
            padding: 3px; /* Giảm từ 4px */
            border: none;
        }
        
        QTableWidget::item:selected {
            background-color: #3498db;
        }
        
        QHeaderView::section {
            background-color: #2c3e50;
            color: #f1c40f;
            padding: 3px; /* Giảm từ 4px */
            border: 1px solid #34495e;
            font-weight: bold;
            font-size: 12px; /* Giảm nhẹ */
        }
        
        /* === MENUS === */
        QMenuBar {
            background-color: #34495e;
            color: #ecf0f1;
            border-bottom: 1px solid #2c3e50;
        }
        
        QMenuBar::item:selected {
            background-color: #3498db;
        }
        
        QMenu {
            background-color: #34495e;
            color: #ecf0f1;
            border: 1px solid #2c3e50;
            font-size: 12px;
        }
        
        QMenu::item:selected {
            background-color: #3498db;
        }
        
        /* === TAB WIDGET === */
        QTabWidget::pane {
            border: 1px solid #34495e;
        }
        
        QTabBar::tab {
            background-color: #34495e;
            color: #ecf0f1;
            padding: 4px 12px; /* Giảm từ 5px 15px */
            border: 1px solid #2c3e50;
            font-size: 12px;
        }
        
        QTabBar::tab:selected {
            background-color: #f1c40f;
            color: #000000;
        }

        QTabBar::tab:hover {
            background-color: #d4b013;
        }
    """