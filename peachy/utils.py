import pygame
import peachy


class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        if isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]


class Counter(object):
    def __init__(self, start, target, repeat=False, step=1):
        self.start = start
        self.target = target
        self.step = step
        self.current = start

        self.finished = False
        self.repeat = repeat

    def complete(self):
        self.current = self.target
        self.finished = True

    def reset(self):
        self.current = self.start
        self.finished = False

    def tick(self):
        if self.current >= self.target:
            return True
        else:
            self.current += self.step
            if self.current >= self.target:
                if self.repeat:
                    self.current = 0
                    return True
                else:
                    return True
            else:
                return False


class Camera(object):

    def __init__(self, view_width, view_height, speed=1):
        self.x = 0
        self.y = 0

        self.view_width = view_width
        self.view_height = view_height
        self.max_width = -1
        self.max_height = -1

        self.speed = speed
        self.target_x = 0
        self.target_y = 0

    def snap(self, target_x, target_y, center=False):
        self.snap_x(target_x, center)
        self.snap_y(target_y, center)

    def snap_x(self, target_x, center=False):
        if center:
            target_x -= self.view_width / 2
        self.x = target_x
        if self.x < 0:
            self.x = 0
        elif self.x + self.view_width > self.max_width:
            self.x = self.max_width - self.view_width

    def snap_y(self, target_y, center=False):
        if center:
            target_y -= self.view_height / 2
        self.y = target_y
        if self.y < 0:
            self.y = 0
        elif self.y + self.view_height > self.max_height:
            self.y = self.max_height - self.view_height

    def pan(self, target_x, target_y, center=False):
        self.pan_x(target_x, center)
        self.pan_y(target_y, center)

    def pan_x(self, target_x, center=False, speed=None):
        if speed is None:
            speed = self.speed
        if center:
            target_x -= self.view_width / 2

        if target_x < 0:
            target_x = 0
        elif target_x + self.view_width > self.max_width:
            target_x = self.max_width - self.view_width

        if self.x + speed < target_x:
            self.x += speed
        elif self.x - speed > target_x:
            self.x -= speed
        else:
            self.x = target_x

    def pan_y(self, target_y, center=False, speed=None):
        if speed is None:
            speed = self.speed
        if center:
            target_y -= self.view_height / 2

        if target_y < 0:
            target_y = 0
        elif target_y + self.view_height > self.max_height:
            target_y = self.max_height - self.view_height

        if self.y + speed < target_y:
            self.y += speed
        elif self.y - speed > target_y:
            self.y -= speed
        else:
            self.y = target_y

    def translate(self):
        peachy.graphics.translate(self.x, self.y)


class Mouse(object):
    """ Mouse input & tracking """
    current_state = (False, False, False)
    previous_state = (False, False, False)
    x = 0
    y = 0
    location = (0, 0)

    @staticmethod
    def init():
        Mouse.current_state = pygame.mouse.get_pressed()
        Mouse.previous_state = pygame.mouse.get_pressed()

    @staticmethod
    def down(button):
        code = Mouse._get_button_code(button)
        if code != -1:
            return Mouse.current_state[code]
        return False

    @staticmethod
    def pressed(button):
        code = Mouse._get_button_code(button)
        if code != -1:
            return Mouse.current_state[code] and not Mouse.previous_state[code]
        return False

    @staticmethod
    def released(button):
        code = Mouse._get_button_code(button)
        if code != -1:
            return not Mouse.current_state[code] and Mouse.previous_state[code]
        return False

    @staticmethod
    def _poll():
        Mouse.previous_state = Mouse.current_state
        Mouse.current_state = pygame.mouse.get_pressed()
        Mouse.x, Mouse.y = Mouse.location = pygame.mouse.get_pos()

    @staticmethod
    def _get_button_code(button):
        if button == 'left':
            return 0
        if button == 'right':
            return 2
        if button == 'middle' or button == 'center':
            return 1
        return -1


class Key(object):
    """ Keyboard & Mouse input helper """

    current_state = []
    previous_state = []

    @staticmethod
    def init():
        Key.current_state = pygame.key.get_pressed()
        Key.previous_state = pygame.key.get_pressed()

    @staticmethod
    def down(key):
        code = Key._get_key_code(key)
        if code is not None:
            return Key.current_state[code]
        return False

    @staticmethod
    def pressed(key):
        if key == 'any':
            for code in range(len(Key.current_state)):
                if Key.current_state[code] and not Key.previous_state[code]:
                    return True
            return False
        else:
            code = Key._get_key_code(key)
            if code is not None:
                return Key.current_state[code] and not \
                    Key.previous_state[code]
            return False

    @staticmethod
    def released(key):
        code = Key._get_key_code(key)
        if code is not None:
            return not Key.current_state[code] and Key.previous_state[code]
        return False

    @staticmethod
    def _poll():
        Key.previous_state = Key.current_state
        Key.current_state = pygame.key.get_pressed()

    @staticmethod
    def _get_key_code(key):
        if key == 'enter':
            return pygame.locals.K_RETURN
        elif key == 'escape':
            return pygame.locals.K_ESCAPE
        elif key == 'lshift':
            return pygame.locals.K_LSHIFT
        elif key == 'rshift':
            return pygame.locals.K_RSHIFT
        elif key == 'space' or key == ' ':
            return pygame.locals.K_SPACE
        elif key == 'left':
            return pygame.locals.K_LEFT
        elif key == 'right':
            return pygame.locals.K_RIGHT
        elif key == 'up':
            return pygame.locals.K_UP
        elif key == 'down':
            return pygame.locals.K_DOWN
        elif key == 'backspace':
            return pygame.locals.K_BACKSPACE
        elif key == 'delete':
            return pygame.locals.K_DELETE
        elif key == 'tab':
            return pygame.locals.K_TAB

        elif key == '1':
            return pygame.locals.K_1
        elif key == '2':
            return pygame.locals.K_2
        elif key == '3':
            return pygame.locals.K_3
        elif key == '4':
            return pygame.locals.K_4
        elif key == '5':
            return pygame.locals.K_5
        elif key == '6':
            return pygame.locals.K_6
        elif key == '7':
            return pygame.locals.K_7
        elif key == '8':
            return pygame.locals.K_8
        elif key == '9':
            return pygame.locals.K_9
        elif key == '0':
            return pygame.locals.K_0

        elif key == 'F1':
            return pygame.locals.K_F1
        elif key == 'F2':
            return pygame.locals.K_F2
        elif key == 'F3':
            return pygame.locals.K_F3
        elif key == 'F4':
            return pygame.locals.K_F4
        elif key == 'F5':
            return pygame.locals.K_F5
        elif key == 'F6':
            return pygame.locals.K_F6
        elif key == 'F7':
            return pygame.locals.K_F7
        elif key == 'F8':
            return pygame.locals.K_F8
        elif key == 'F9':
            return pygame.locals.K_F9
        elif key == 'F10':
            return pygame.locals.K_F10
        elif key == 'F11':
            return pygame.locals.K_F11
        elif key == 'F12':
            return pygame.locals.K_F12

        elif key == '+':
            return pygame.locals.K_KP_PLUS
        elif key == '-':
            return pygame.locals.K_KP_MINUS
        elif key == '_':
            return pygame.locals.K_UNDERSCORE
        elif key == '.':
            return pygame.locals.K_PERIOD

        elif key == 'a':
            return pygame.locals.K_a
        elif key == 'b':
            return pygame.locals.K_b
        elif key == 'c':
            return pygame.locals.K_c
        elif key == 'd':
            return pygame.locals.K_d
        elif key == 'e':
            return pygame.locals.K_e
        elif key == 'f':
            return pygame.locals.K_f
        elif key == 'g':
            return pygame.locals.K_g
        elif key == 'h':
            return pygame.locals.K_h
        elif key == 'i':
            return pygame.locals.K_i
        elif key == 'j':
            return pygame.locals.K_j
        elif key == 'k':
            return pygame.locals.K_k
        elif key == 'l':
            return pygame.locals.K_l
        elif key == 'm':
            return pygame.locals.K_m
        elif key == 'n':
            return pygame.locals.K_n
        elif key == 'o':
            return pygame.locals.K_o
        elif key == 'p':
            return pygame.locals.K_p
        elif key == 'q':
            return pygame.locals.K_q
        elif key == 'r':
            return pygame.locals.K_r
        elif key == 's':
            return pygame.locals.K_s
        elif key == 't':
            return pygame.locals.K_t
        elif key == 'u':
            return pygame.locals.K_u
        elif key == 'v':
            return pygame.locals.K_v
        elif key == 'w':
            return pygame.locals.K_w
        elif key == 'x':
            return pygame.locals.K_x
        elif key == 'y':
            return pygame.locals.K_y
        elif key == 'z':
            return pygame.locals.K_z
        else:
            return None


class TextCapture(object):
    """
    The TextCapture takes all alphanumeric input recorded by Key and stores it
    inside of self.value. This is useful for text input like naming things.
    """

    def __init__(self, value=''):
        self.value = value

    def update(self):
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '_', '-',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            ' '
        ]

        shift = Key.down('lshift') or Key.down('rshift')

        if Key.pressed('backspace') or Key.pressed('delete'):
            self.value = self.value[:-1]

        for key in keys:
            if Key.pressed(key):
                if shift:
                    self.value += key.upper()
                else:
                    self.value += key
