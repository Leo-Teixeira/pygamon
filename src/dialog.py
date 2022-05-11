import pygame


class dialogBox:
    X_position = 60
    Y_position = 650

    def __init__(self):
        self.box = pygame.image.load('../dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.text = ["Bonjour test", "clara la moche", "leo bobo"]
        self.text_index = 0
        self.letter_index = 0
        self.reading = False
        self.font = pygame.font.Font("../dialogs/dialog_font.ttf", 18)

    def execute(self):
        if self.reading:
            self.next_text()
        else:
            self.reading: True
            self.text_index = 0

    def render(self, screen):
        if self.reading:
            self.letter_index += 1
            if self.letter_index >= len(self.text[self.text_index]):
                self.letter_index = self.letter_index
            screen.blit(self.box, (self.X_position, self.Y_position))
            text = self.font.render(self.text[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (self.X_position + 60, self.Y_position + 30))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.text):
            self.reading = False
