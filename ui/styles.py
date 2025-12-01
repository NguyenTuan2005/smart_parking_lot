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
            border: 2px solid #3498db;
            border-radius: 4px; /* Giảm từ 5px */
            background-color: #000000;
        }
        
        /* === TITLE LABELS === */
        QLabel#TitleLabel {
            font-size: 16px; /* Giảm từ 18px */
            font-weight: bold;
            color: #f39c12;
            border-bottom: 1px solid #f39c12; /* Giảm từ 2px */
            padding-bottom: 3px; /* Giảm từ 5px */
            margin-bottom: 8px; /* Giảm từ 10px */
        }
        
        /* === SPECIAL LABELS === */
        QLabel#ParkingLogo {
            font-size: 20px; /* Giảm từ 24px */
            font-weight: bold;
            color: #3498db;
        }
        
        QLabel#BigNumber {
            font-size: 30px; /* Giảm từ 36px */
            font-weight: bold;
            color: #e74c3c;
        }
        
        /* === INPUT FIELDS === */
        QLineEdit {
            padding: 4px; /* Giảm từ 5px */
            border: 1px solid #3498db;
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
            background-color: #3498db;
            color: white;
            border-radius: 3px; /* Giảm từ 4px */
            padding: 4px 8px; /* Giảm từ 5px 10px */
            font-weight: bold;
            border: none;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton:pressed {
            background-color: #1b5a7a;
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
            color: #f39c12;
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
            background-color: #3498db;
            color: white;
        }
        
        QTabBar::tab:hover {
            background-color: #2980b9;
        }
    """