class Normalizer:
    def __init__(self):
        pass

    def normalize(self, state):
        '''
        Normalizes numerical values from the flattened state.

        Does NOT make adjustments to categorical data.

        return: state object with normalized numerical values
        '''

        # Index 1 selects sprite coordinates, index 0 selects x pos
        for i in range(16):
            norm_x = state[f'Sprite {i}'][1][0] / state['Map Dimensions'][0]
            norm_y = state[f'Sprite {i}'][1][1] / state['Map Dimensions'][1]
            norm_coords = (norm_x, norm_y)
            state[f'Sprite {i}'][1] =  norm_coords
        
        
        
