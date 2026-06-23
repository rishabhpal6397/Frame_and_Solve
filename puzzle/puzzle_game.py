import pygame
import sys
import time
import os
from datetime import datetime


class PuzzleGame:

    def __init__(self, tiles, grid_size=3):

        pygame.init()

        self.grid_size = grid_size
        if grid_size == 3:
            self.difficulty = "Easy"
        elif grid_size == 4:
            self.difficulty = "Medium"
        else:
            self.difficulty = "Hard"
        self.tiles = tiles

        self.tile_size = 150

        self.width = self.tile_size * self.grid_size
        self.height = self.tile_size * self.grid_size + 60

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("Frame & Solve")

        self.selected_tile = None
        self.dragging_tile = None
        self.solved = False
        self.moves = 0

        self.start_time = time.time()
        self.end_time = None

        self.load_images()

    def load_images(self):

        for tile in self.tiles:

            image = pygame.image.load(tile["path"])

            image = pygame.transform.scale(
                image,
                (self.tile_size, self.tile_size)
            )

            tile["image"] = image
            print(tile["path"])

    def draw_board(self):

        self.screen.fill((30, 30, 30))

        for tile in self.tiles:

            position = tile["current_position"]

            row = position // self.grid_size
            col = position % self.grid_size

            x = col * self.tile_size
            y = row * self.tile_size

            self.screen.blit(
                tile["image"],
                (x, y)
            )

            border_color = (255, 255, 255)

            if tile == self.dragging_tile:
                border_color = (0, 255, 0)

            pygame.draw.rect(
                self.screen,
                border_color,
                (x, y, self.tile_size, self.tile_size),
                3
            )

        font = pygame.font.Font(None, 36)
        difficulty_text = font.render(
            f"Difficulty: {self.difficulty}",
            True,
            (255, 255, 255)
        )

        moves_text = font.render(
            f"Moves: {self.moves}",
            True,
            (255, 255, 255)
        )

        elapsed = int(
            (self.end_time or time.time())
            - self.start_time
        )

        timer_text = font.render(
            f"Time: {elapsed}s",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            difficulty_text,
            (10, self.height - 85)
        )

        if not self.solved:
            
            self.screen.blit(
                moves_text,
                (10, self.height - 50)
            )

            self.screen.blit(
                timer_text,
                (250, self.height - 50)
            )

        if self.solved:

            big_font = pygame.font.Font(
                None,
                60
            )

            small_font = pygame.font.Font(
                None,
                36
            )

            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 120))

            self.screen.blit(overlay, (0, 0))
            solved_text = big_font.render(
                "YOU DID IT!",
                True,
                (0, 255, 0)
            )

            elapsed = int(
                self.end_time - self.start_time
            )

            
            stats_text = small_font.render(
                f"Moves: {self.moves} | Time: {elapsed}s",
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                solved_text,
                (70, 30)
            )

            self.screen.blit(
                stats_text,
                (110, 90)
            )

        pygame.display.flip()

    def get_clicked_position(self, mouse_pos):

        x, y = mouse_pos

        if y >= self.tile_size * self.grid_size:
            return None

        col = x // self.tile_size
        row = y // self.tile_size

        return row * self.grid_size + col

    def get_tile_by_position(self, position):

        for tile in self.tiles:

            if tile["current_position"] == position:
                return tile

        return None

    def swap_tiles(self, tile1, tile2):

        pos1 = tile1["current_position"]
        pos2 = tile2["current_position"]

        tile1["current_position"] = pos2
        tile2["current_position"] = pos1

        self.moves += 1

    def check_solved(self):

        for tile in self.tiles:

            if tile["id"] != tile["current_position"]:
                return False

        return True
    
    def save_achievement(self):

        os.makedirs(
            "achievements",
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"achievements/victory_{timestamp}.png"
        )

        pygame.image.save(
            self.screen,
            filename
        )

        print(
            f"Achievement saved: {filename}"
        )

    def run(self):

        clock = pygame.time.Clock()

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Mouse Press
                if event.type == pygame.MOUSEBUTTONDOWN and not self.solved:

                    position = self.get_clicked_position(
                        pygame.mouse.get_pos()
                    )

                    if position is not None:
                        self.dragging_tile = self.get_tile_by_position(
                            position
                        )

                # Mouse Release
                elif event.type == pygame.MOUSEBUTTONUP and not self.solved:

                    if self.dragging_tile:

                        position = self.get_clicked_position(
                            pygame.mouse.get_pos()
                        )

                        if position is not None:

                            target_tile = self.get_tile_by_position(
                                position
                            )

                            if (
                                target_tile is not None
                                and
                                target_tile != self.dragging_tile
                            ):

                                self.swap_tiles(
                                    self.dragging_tile,
                                    target_tile
                                )

                                if self.check_solved():

                                    self.solved = True
                                    self.end_time = time.time()
                                    self.draw_board()
                                    self.save_achievement()

                        self.dragging_tile = None

            self.draw_board()

            clock.tick(60)