import sys
from PySide6.QtWidgets import QApplication, QSizePolicy, QSpacerItem, QMainWindow, QGridLayout, QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap

class MenuPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: lightgrey;")
        self.setCentralWidget(central_widget)
        
        
        # Use a QVBoxLayout for the main layout
        main_layout = QVBoxLayout()
        
        connect_four_label = QLabel('<font size="30" color="black"><b>Connect</b></font><font size ="30" color="red"><b>Four</b></font>', self)
        connect_four_label.setAlignment(Qt.AlignCenter)  # Center the label
        main_layout.addWidget(connect_four_label)
        # Create a horizontal layout for the image and buttons
        image_button_layout = QHBoxLayout()
    
        board_img = QLabel(self)
        image = QPixmap("images/board.png")
        board_img.setPixmap(image)
        board_img.setAlignment(Qt.AlignCenter)  # Center the image
        image_button_layout.addWidget(board_img)

        # Create a vertical layout for buttons
        button_layout = QVBoxLayout()

        start_game_button = QPushButton("Start Game", self)
        start_game_button.setStyleSheet("color: white; background-color: blue; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 3em; padding: 6px; min-height: 2em")
        start_game_button.clicked.connect(self.start_game)
        button_layout.addWidget(start_game_button)

        restart_game_button = QPushButton("Restart Game", self)
        restart_game_button.setStyleSheet("color: white; background-color: blue; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 3em; padding: 6px;min-height: 2em")
        restart_game_button.clicked.connect(self.reset_game)
        button_layout.addWidget(restart_game_button)

        reset_score_button = QPushButton("Reset Score", self)
        reset_score_button.setStyleSheet("color: white; background-color: grey; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 3em; padding: 6px;min-height: 2em")
        reset_score_button.clicked.connect(self.reset_score)
        button_layout.addWidget(reset_score_button)
        
        settings_buttons = QPushButton("Settings", self)
        settings_buttons.setStyleSheet("color: white; background-color: grey; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 3em; padding: 6px;min-height: 2em")
        settings_buttons.clicked.connect(self.settings)
        button_layout.addWidget(settings_buttons)

        # Add the button layout to the image and button layout
        image_button_layout.addLayout(button_layout)

        # Add the image and button layout to the main layout
        main_layout.addLayout(image_button_layout)


        central_widget.setLayout(main_layout)
        self.resize(600, 400)

    def start_game(self):
        self.connect_four_game = ConnectFourGUI(rows=6, columns=7, menu_page=self)
        self.connect_four_game.show()
        self.hide()
        
    def reset_game(self):
        pass
    def reset_score(self):
        pass
    def settings(self):
        pass

class ConnectFourGUI(QMainWindow):
    def __init__(self, rows, columns, menu_page):
        super().__init__()
        self.menu_page = menu_page
        self.player = 0
        self.rows = rows
        self.columns = columns
        self.board = [[-1] * self.columns for _ in range(self.rows)]

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        self.current_player_label = QLabel("Current Player: Red", self)
        main_layout.addWidget(self.current_player_label)

        layout = QGridLayout()

        self.buttons = []
        for row in range(self.rows):
            for col in range(self.columns):
                button = QPushButton()

                button.clicked.connect(lambda row=row, col=col: self.handle_button_click(row, col))
                self.buttons.append(button)
                layout.addWidget(button, row, col)
                self.style_button(button)
                #button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        main_layout.addLayout(layout)
        central_widget.setLayout(main_layout)
    
    def style_button(self, button):
        button.setFixedSize(50, 50)  # Set a fixed size for the button
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid black;
                border-radius: 25px; /* Half of the button size for a circular shape */
            }
            QPushButton:hover {
                background-color: green;
            }
        """)
    # ... (rest of your ConnectFourGUI class)
    def handle_button_click(self, row, col):
        # Add logic to handle button click
        # such as update the board and redraw the GUI
        
        if not self.check_winner():
            print(f"Button in row {row + 1}, column {col + 1} clicked")
            self.drop_piece(self.player, col)
            if self.check_winner():
                self.display_winner(self.player)
                QTimer.singleShot(1000, self.reset_game)
                #self.reset_game()
            else:
                #if you are checking wins, change 1 to 0. For functioning game, change to self.player + 1
                self.player = (self.player + 1) % 2
                if self.player == 1:
                    self.current_player_label = QLabel("Current Player: Red", self)
                else:
                    self.current_player_label = QLabel("Current Player: Yellow", self)
        
    
    def check_winner(self):
        for i in range(self.rows):
            for j in range(self.columns):
                # Check vertical
                if i + 3 < self.rows and self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j] != -1:
                    print(f"Player {self.board[i][j]} wins vertically!")
                    return True

                # Check horizontal
                if j + 3 < self.columns and self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3] != -1:
                    print(f"Player {self.board[i][j]} wins horizontally!")
                    return True

                # Check diagonal
                if i + 3 < self.rows and j + 3 < self.columns and self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3] != -1:
                    print(f"Player {self.board[i][j]} wins diagonally!")
                    return True
                
           
        
    
    def drop_piece(self, player, column):
        for row in range(self.rows -1, -1, -1):
            if self.board[row][column] == -1:
                self.board[row][column] = player
                self.update_button_visuals(row, column)
                break

    def update_button_visuals(self, row, col):
        player_color = "red" if self.player == 0 else "yellow"
        self.buttons[row * self.columns + col].setStyleSheet(f"""
            QPushButton {{
                background-color: {player_color};
                border: 2px solid black;
                border-radius: 25px; /* Half of the button size for a circular shape */
            }}
        """)
    
    def display_winner(self, player):
        # Disable all buttons
        for button in self.buttons:
            button.setEnabled(False)

        # Display a message indicating the winner
        print(f"Player {player} wins!")
        

    def reset_game(self):
        #self.menu_page.show()
        #self.hide()
        self.board = [[-1] * self.columns for _ in range(self.rows)]
        for button in self.buttons:
            button.setEnabled(True)
            self.style_button(button)
        
        #self.player = 0
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MenuPage()
    menu.show()
    sys.exit(app.exec())

