import pygame
import win32api, win32con, win32gui

class Overlay:
    def __init__(self,color_key=(0,1,1)):
        pygame.init()
        pygame.font.init()

        self.transparent_color = color_key
        self.width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        self.hwnd = pygame.display.get_wm_info()["window"]

        self._setup_overlay()
        self.clock = pygame.time.Clock()

    def _setup_overlay (self):
        ex_style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE,
                                ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(*self.transparent_color), 0, win32con.LWA_COLORKEY)

    def refresh(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
        self.screen.fill(self.transparent_color)
        return True

    def draw_extended_line(self, x1, y1, x2, y2, color=(255, 0, 0), thickness=3):
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0: return
        scale = 5000
        p1 = (int(x1 + scale * dx), int(y1 + scale * dy))
        p2 = (int(x1 - scale * dx), int(y1 - scale * dy))
        pygame.draw.line(self.screen, color, p1, p2, thickness)

    def display(self, fps=144):
        pygame.display.update()
        self.clock.tick(fps)