import sys

class Menu:
    def __init__(self, pyboy):
        '''
        Pull information about the pause menu and PC menu.

        pyboy: Instance of PyBoy emulator object
        '''

        self.pyboy = pyboy

    def get_cursor_coord(self):
        '''
        Finds the (x, y) coordinate of the cursor on the screen.
        If no menu is active, it retains the last known position value.
        Menus include (but might not be limited to?) Pause menu, Naming menus, Battle menus

        return: Tuple of shape (x, y) in (???) units.
        '''

        try:
            x_pos = self.pyboy.memory[0xCC25]
            y_pos = self.pyboy.memory[0xCC24]

            coord = (x_pos, y_pos)

            return coord

        except AttributeError as e:
            print("Message from Menu.py:")
            print("Error finding cursor coordinates.")
            print(f"Error: {e}")
            sys.exit()

    def get_current_selection(self):
        '''
        Gets the identifier (integer) of the item current selected by the cursor.

        returns: Integer ID number
        '''

        try:
            item_number = self.pyboy.memory[0xCC26]
            item_ID = self.pyboy.memory[0xD31E + item_number*2]
            return item_ID

        except AttributeError as e:
            print("Message from Menu.py")
            print("Error trying to get ID of currently selected item.")
            print(f"Error: {e}")
            sys.exit()

    def get_select_item(self):
        '''
        Gets the item's list number that is currently set for "Select" button.
        00 = no item, 01 = first item, etc.

        return: Integer list number
        '''

        try:
            return self.pyboy.memory[0xCC35]

        except AttributeError as e:
            print("Message from Menu.py:")
            print("Error retrieving the item on the menu set for the Select button.")
            print(f"Error: {e}")
            sys.exit()

    def get_menu_data(self):
        '''
        Retrieve all menu data and combine them in a dictionary.

        Cursor Coordinate: (x, y) tuple of the cursor's coordinates
        Current Selection: ID of currently selected menu item (topmost is 0)
        Select Item: Item highlighted with Select (01 = first item, 00 = no item, etc)

        return: Dictionary of the above items
        '''
        self.menu_data = {}

        # Get cursor coordinates
        cursor_coord = self.get_cursor_coord()
        self.menu_data["Cursor Coordinate"] = cursor_coord

        # Get current selected item ID
        self.menu_data["Current Selection"] = self.get_current_selection()

        # Get currently selected "Select Item" ID
        self.menu_data["Select Item"] = self.get_select_item()

        return self.menu_data
