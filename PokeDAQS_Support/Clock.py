class Clock:
    def __init__(self, pyboy):
        self.pyboy = pyboy


    def get_game_time(self):
        '''
        Gets the time and frames elapsed.

        These likely reset upon reaching a max value.

        Frames = 1 byte
        Seconds = 1 byte
        Minutes = 2 bytes
        Hours = 2 bytes

        return: (frames, seconds, minutes, hours)
        '''

        frames = self.pyboy.memory[0xDA45]
        seconds = self.pyboy.memory[0xDA44]
        minutes = sum(self.pyboy.memory[0xDA42:0xDA44])
        hours = sum(self.pyboy.memory[0xDA40:0xDA42])

        time_tuple = (frames, seconds, minutes, hours)

        return time_tuple
