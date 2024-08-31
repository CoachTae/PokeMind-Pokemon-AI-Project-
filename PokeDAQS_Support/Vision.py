import sys
import torch
import torch.nn as nn
import torch.nn.functional as F

class Vision(nn.Module):
    def __init__(self, pyboy, PokeMind, input_channels=3, feature_size=128,
                 layer2size=16, layer3size=32, kernel_size=3,
                 stride=1, padding=1, fcsize=64):
        """
        Does anything that has to do with seeing the map or pulling images from the screen.
        May end up pulling sprite or tile images if needed.

        pyboy: Instance of PyBoy object
        PokeMind: Instance of PyBoy Pokemon Game Wrapper

        input_channels = How many 2D matrices are in this image? (3 for RGB)
        feature_size = The size of the output vector produced by the full vision model
        layer2size = Number of neurons on the 2nd convolutional layer
        layer3size = Number of neurons on the 3rd convolutional layer
        kernel_size = Size of the kernel/filter scanning the image in each conv layer
        stride = How many rows/columns a kernel moves after it finishes scanning a given row
        padding = Adds this many pixels to the outside of the image to preserve image size
        fcsize = Number of neurons in the fully-connected layer after the conv layers

        The numbers 20 and 18 in the layers come from max pooling our image 3 times
            input image: 160x144 pixels
            1st Pool: 80x72
            2nd Pool: 40x36
            3rd Pool: 20x18
        """

        super(Vision, self).__init()
        
        self.pyboy = pyboy
        self.PokeMind = PokeMind
        
        self.screen_image = None    # Given value from get_screen function
        self.tilemap_window = None  # Given value from get_window function
        
        
        # Define CNN layers
        self.conv1 = nn.Conv2d(input_channels, layer2size,
                               kernel_size=kernel_size, stride=stride,
                               padding=padding)
        
        self.conv2 = nn.Conv2d(layer2size, layer3size,
                              kernel_size=kernel_size, stride=stride,
                              padding=padding)
        
        self.conv3 = nn.Conv2d(layer3size, fcsize, kernel_size=kernel_size,
                               stride=stride, padding=padding)

        self.fc = nn.Linear(fcsize * 20 * 18, feature_size)


    def forward(self, x):
        # Convolutional layers with ReLU activation and max pooling
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x,2)

        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x,2)

        x = F.relu(self.conv3(x))
        x = F.max_pool2d(x,2)

        # Flatten  the tensor for passage to the fully connected layer
        x = x.view(-1, fcsize * 20 * 18) #-1 infers the batch_size for this method based on given data

        # Fully connected layers
        x = F.relu(self.fc(x)) # Returns vector of size feature_size

        return x
        
        
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

    def get_processed_image(self):
        # Get image
        image = self.get_image()

        # Convert to tensor
        image = torch.tensor(image).float()

        # Ensure image has correct shape (batchsize, channels, height, width)
        if len(image.shape) == 3:
            image = image.unsqueeze(0)

        # Pass image through the CNN
        feature_vector = self.forward(image)
        
        return feature_vector
        
