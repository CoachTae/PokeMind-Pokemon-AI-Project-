import sys

class Sprites:
    def __init__(self, pyboy):
        '''
        Pulls non-image information on sprites listed for the current map.
        Includes player sprite information (index 0 for the main loop).

        pyboy: Instance of PyBoy emulator object
        '''
        self.pyboy = pyboy

    def get_sprite_IDs(self):
        """
        Pulls sprite ID for each of up to 16 sprites on the map.
        Player is always sprite 0

        ID: Integer sprite ID

        return: List of 16 integer sprite IDs
        """

        IDs = []

        for i in range(16):
            try:
                IDs.append(self.pyboy.memory[0xC100 + i*16])

            except AttributeError as e:
                print("Message from Sprites.py:")
                print("Error pulling sprite IDs.")
                print(f"Error: {e}")
                sys.exit()

        return IDs


    def get_sprite_coordinates(self):
        """
        Pulls world coordinates of each sprite (in block coordinates).
        Player is always sprite 0

        coord = Tuple of sprite coordinates in shape (x, y)

        return: List of 16 tuples of shape (x, y)
        """

        coords = []

        for i in range(16):
            # Player position in global coordinates is found elsewhere
            # For some reason, C204 and C205 address always pull 0.
            # This appears to be screen coordinates but doesn't match convention for the rest of the sprites
            if i == 0:
                try:
                    x_pos = self.pyboy.memory[0xD362]
                    y_pos = self.pyboy.memory[0xD361]

                    coord = (x_pos, y_pos)

                    coords.append(coord)
                    
                except AttributeError as e:
                    print("Message from Sprites.py:")
                    print("Error in pulling Player Coordinates.")
                    print(f"Error: {e}")
                    sys.exit()

            else:
                try:
                    x_pos = self.pyboy.memory[0xC205 + i*16] - 4
                    y_pos = self.pyboy.memory[0xC204 + i*16] - 4

                    coord = (x_pos, y_pos)

                    coords.append(coord)

                except AttributeError as e:
                    print("Message from Sprite.py:")
                    print("Error in pulling nonplayer Sprite Coordinates.")
                    print(f"Error: {e}")
                    sys.exit()

        return coords

    def get_face_directions(self):
        """
        Pulls the directions that each sprite on the map is facing.
        Player is always sprite 0.

        0 = Down
        4 = Up
        8 = Left
        12 = Right

        face = Integer face direction
        
        return: List of 16 integers, each representing the facing direction of a sprite
        """

        faces = []

        for i in range(16):
            try:
                faces.append(self.pyboy.memory[0xC109 + i*16])

            except AttributeError as e:
                print("Message from Sprites.py.")
                print("Error pulling sprite face directions.")
                print(f"Error: {e}")
                sys.exit()

        return faces
                

    def get_sprite_data(self):
        """
        Pulls information for all of up to 16 sprites on the map.
        Player is always sprite 0

        Identifier: Integer of Picture ID for that sprite
        Coordinates: A tuple of shape (x, y) containing coordinates for that sprite
        Face Direction: Integer of sprite's Facing Direction

        returns list of dictionary objects with the above keys
        """

        self.sprite_data = []

        IDs = self.get_sprite_IDs()
        coords = self.get_sprite_coordinates()
        faces = self.get_face_directions()

        for i in range(16):
            sprite_dict = {}

            sprite_dict["Identifier"] = IDs[i]
            sprite_dict["Coordinates"] = coords[i]
            sprite_dict["Face Direction"] = faces[i]

            self.sprite_data.append(sprite_dict)

        return self.sprite_data

        
            

        
            
            
