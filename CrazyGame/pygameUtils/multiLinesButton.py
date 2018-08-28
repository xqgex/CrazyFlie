import pygame
import os
from pygameUtils import displaysConsts
from CrazyGame import logger
import logging
cf_logger = logger.get_logger(__name__, logging.INFO)

UNPRESSED_BUTTON_IMAGE = 'button_unpressed.png'
PRESSED_BUTTON_IMAGE = 'button_pressed.png'


class MultiLinesButton:
    BUTTON_TEXT_COLOR = displaysConsts.WHITE

    def __init__(self, position, size, lines, unpressed_image_name=UNPRESSED_BUTTON_IMAGE, pressed_image_name=PRESSED_BUTTON_IMAGE):
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.font = pygame.font.SysFont("arial", min(30, self.rect.height - 5))
        self.lines = lines
        self.text_surfaces = [self.font.render(self.lines[i], False, MultiLinesButton.BUTTON_TEXT_COLOR) for i in range(len(lines))]
        self.size = size
        self.current_image = ''
        self.pressed = False
        self.step = self.size[1]//(len(self.lines)+1)
        self.text_positions = [(self.rect.centerx - self.text_surfaces[i].get_width() / 2,
                              self.rect.top + self.step*(i+1) - self.text_surfaces[i].get_height() / 2) for i in range(len(self.text_surfaces))]

        self.has_image = unpressed_image_name is not None
        self.unpressed_image_name = unpressed_image_name
        self.pressed_image_name = pressed_image_name
        self._set_images()
        self.set_pressed(False)
        self.current_color = (0, 0, 0)

    def set_text(self, lines):
        self.text_surfaces = [self.font.render(self.lines[i], False, MultiLinesButton.BUTTON_TEXT_COLOR) for i in range(len(lines))]
        self.text_positions = [(self.rect.centerx - self.text_surfaces[i].get_width() / 2,
                              self.rect.top + self.text_surfaces[i].get_height() * i) for i in range(len(self.text_surfaces))]

        self.render()

    def render(self):
        if self.has_image:
            self.display_surf.blit(self.current_image, self.rect.topleft)
        else:
            pygame.draw.rect(self.display_surf, self.current_color, self.rect)

        for i in range(len(self.text_surfaces)):
            self.display_surf.blit(self.text_surfaces[i], self.text_positions[i])

    def set_pressed(self, state):
        self.pressed = state
        if self.pressed:
            self.current_color = displaysConsts.BLUE
            if self.has_image:
                self.current_image = self.pressed_image
        else:
            self.current_color = displaysConsts.GREEN
            if self.has_image:
                self.current_image = self.not_pressed_image

    def handle_mouse_event(self, event_type, mouse_location):
        if self.rect.collidepoint(*mouse_location):
            cf_logger.debug('mouse event %s occurred on button %s' % (event_type, self.lines))
            if event_type == pygame.MOUSEBUTTONDOWN:
                self.set_pressed(True)
            elif event_type == pygame.MOUSEBUTTONUP:
                if not self.pressed:
                    return False
                self.set_pressed(False)
            self.render()
            pygame.display.update()
            return True

        elif self.pressed:
            self.set_pressed(False)
            self.render()
            pygame.display.update()

        return False

    def _set_images(self):
        if self.has_image:
            button_unpressed_image = pygame.image.load(os.path.join(displaysConsts.PICTURE_DIRECTORY, self.unpressed_image_name))
            self.not_pressed_image = pygame.transform.scale(button_unpressed_image, self.size)
            button_pressed_image = pygame.image.load(os.path.join(displaysConsts.PICTURE_DIRECTORY, self.pressed_image_name))
            self.pressed_image = pygame.transform.scale(button_pressed_image, self.size)

    def is_pressed(self):
        return self.pressed

    def change_state(self):
        self.pressed = not self.pressed