from gui import GUI
from app import Application


def main():
    app = Application()
    gui = GUI(app)
    
    gui.start_window()

if __name__ == '__main__':
    main()