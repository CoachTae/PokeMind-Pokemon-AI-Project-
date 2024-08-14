import sys

class Vision:
    def __init__(self, pyboy, PokeMind):
        """
        Does anything that has to do with seeing the map or pulling images from the screen.
        May end up pulling sprite or tile images if needed.

        pyboy: Instance of PyBoy object
        PokeMind: Instance of PyBoy Pokemon Game Wrapper
        """
        
        self.pyboy = pyboy
        self.PokeMind = PokeMind
        
        self.screen_image = None    # Given value from get_screen function
        self.tilemap_window = None  # Given value from get_window function
        

    def get_screen(self):
        """
        Get the current image displaying on the screen

        return: Image of screen as PIL Image object
        """

        try:
            self.screen_image = self.pyboy.screen.image
            return self.screen_image

        except AttributeError as e:
            print("Message from Vision.py:")
            print("Screen image could not be pulled.")
            print(f"Error given: {e}")
            sys.exit()
        

    def get_window(self):
        """
        Gets current tilemap window from the wrapper.

        Only shows the tilemap window available on the screen.

        return: Tilemap window object
        """
        try:
            tilemap_window = self.PokeMind.tilemap_window()

            # Details about these objects and their methods can be found in the link below
            # https://docs.pyboy.dk/api/tilemap.html

            
            # Create a blank image for the combined tilemap
            screen_width = 8 * 20 # Each tile is 8x8 pixels. 20 tiles on screen
            screen_height = 8 * 17
            full_image = Image.new('RGB', (screen_width, screen_height))

            # Get player coordinates
            coords = get_player_position(pyboy)

            # Get the top-left corner of the visible area based on player position
            player_block_x, player_block_y = coords
            player_tile_x = player_block_x * 2 # Convert block coordinates to tile coordinates
            player_tile_y = player_block_y * 2

            # Center the player on the screen
            top_left_x = player_tile_x - 10
            top_left_y = player_tile_y - 10

            # Iterate over the visible screen area and paste each tile into the full image
            for row in range(17): # Visible rows
                for column in range(20): # Visible columns
                    try:
                        # Calculate the tile coordinates relative to player's position
                        tile_x = top_left_x + column
                        tile_y = top_left_y + row

                        # Get the tile image
                        tile = tilemap_window.tile(tile_x, tile_y).image()

                        # Ensure the tile is of the correct size
                        if tile.size != (8, 8):
                            tile=tile.resize((8,8))

                        # Calculate the position to paste the tile
                        position = (column * 8, row * 8)

                        # Paste the tile image into the full image
                        full_image.paste(tile, position)
                    except Exception as e:
                        pass
            
            
            
                
            return full_image


        except AttributeError as e:
            print("Message from Vision.py:")
            print("tilemap_window could not be pulled.")
            print(f"Error given: {e}")
            sys.exit()
        
