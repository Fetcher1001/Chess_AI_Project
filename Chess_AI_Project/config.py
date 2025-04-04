import pygame
import os
from sound import Sound
from theme import Theme

class Config:

    def __init__(self):

        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold= True)
        self.move_sound = Sound(os.path.join('C:\\Users\johan\john_programms\Chess_AI_Project\\assets\sounds\move.wav'))
        self.capture_sound = Sound(os.path.join('C:\\Users\johan\john_programms\Chess_AI_Project\\assets\sounds\capture.wav'))


    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes) #
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (127, 195, 51), '#C86464', '#C84646')
        brown = Theme((240, 217, 181), (181, 136, 99), (246, 246, 105), (186, 202, 43), '#C86464', '#C84646')
        blue = Theme((200, 230, 245), (50, 100, 160), (100, 150, 210), (20, 60, 120),'#C86464', '#C84646')
        gray = Theme((220, 220, 220), (169, 169, 169), (198, 198, 198), (130, 130, 130),'#C86464', '#C84646')

        self.themes = [green, brown, blue, gray]

