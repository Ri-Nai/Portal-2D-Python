import pygame

class SoundManager:
    def __init__(self, path):
        pygame.mixer.init()
        self.sounds: dict[str, dict[str, pygame.mixer.Sound]] = {}
        from . import data_manager
        self.soundsURL = data_manager.DataManager().loadJSON(path)
        self.sound_status = {}
        self.channels = [pygame.mixer.Channel(0)]
        self.channel_status = {0: ""}

        for kind in self.soundsURL:
            self.sounds[ kind ] = {}
            self.sound_status[ kind ] = {}
            for id in self.soundsURL[ kind ]:
                audio = pygame.mixer.Sound(self.soundsURL[ kind ][ id ])
                self.sounds[ kind ][ id ] = audio
                self.sound_status[ kind ][ id ] = False

    def play_sound(self, kind, id = '0'):
        soundExists = kind in self.sounds and str(id) in self.sounds[ kind ]
        if not soundExists:
            print(f"Sound kind {kind} id {id} not found in AudioManager.")
            return
        
        if not self.sound_status[ kind ][ id ]:
            if (kind == "walk"):
                return
        self.__play(kind, id)


    def __play(self, kind, id = 0):
        sound = self.sounds[ kind ][ id ]
        for num in range(len(self.channels)):
            channel = self.channels[ num ]
            if not channel.get_busy():
                channel.play(sound)
                self.sound_status[ kind ][ id ] = True
                self.channel_status[num] = f'{kind}@{id}'
                return
        
        channel_id = len(self.channels)
        channel = pygame.mixer.Channel(channel_id)
        self.channel_status[channel_id] = f'{kind}@{id}'
        channel.play(sound)
        self.channels.append(channel)

    def update(self):
        for num in range(len(self.channels)):
            channel: pygame.mixer.Channel = self.channels[ num ]
            if not channel.get_busy():
                if self.channel_status[num] != "":
                    prev = self.channel_status[num]
                    if prev != "":
                        kind, id = prev.split("@")
                        self.sound_status[ kind ][ id ] = False
                        print(f"Channel {num} stopped playing {prev}")
                    self.channel_status[num] = ""
