import pygame
import time
from PIL import Image

class LoadingScreen:
    def __init__(self, screen, total_items,gif_path='images/loading.gif'):
        self.screen = screen
        self.total_items = total_items
        self.loaded_items = 0
        self.progress = 0

            # Load frames from GIF
        self.frames = []
        pil_img = Image.open(gif_path)
        try:
            while True:
                frame = pil_img.convert("RGBA")
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()
                py_image = pygame.image.fromstring(data, size, mode)
                self.frames.append(py_image)
                pil_img.seek(pil_img.tell() + 1)
        except EOFError:
            pass

        self.current_frame = 0
        self.last_update_time = time.time()
        self.frame_duration = 0.1  # seconds per frame
        
    def update(self, items_loaded=1):
        self.loaded_items += items_loaded
        self.progress = min(self.loaded_items / self.total_items, 1.0)  # Ensure progress doesn't exceed 100%
        
    def draw(self):
        # Dark overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Update GIF frame
        current_time = time.time()
        if current_time - self.last_update_time >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update_time = current_time

        gif_img = self.frames[self.current_frame]
        rect = gif_img.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(gif_img, rect)

        pygame.display.flip()
