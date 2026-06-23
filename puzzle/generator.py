import cv2
import os
import random


class PuzzleGenerator:

    def __init__(self, grid_size=3):
        self.grid_size = grid_size

    def generate_tiles(
        self,
        image_path="screenshots/captured_image.jpg",
        output_dir="assets/tiles"
    ):

        os.makedirs(output_dir, exist_ok=True)

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        height, width = image.shape[:2]

        tile_width = width // self.grid_size
        tile_height = height // self.grid_size

        tiles = []

        tile_id = 0

        for row in range(self.grid_size):

            for col in range(self.grid_size):

                x = col * tile_width
                y = row * tile_height

                tile = image[
                    y:y + tile_height,
                    x:x + tile_width
                ]

                tile_path = os.path.join(
                    output_dir,
                    f"tile_{tile_id}.jpg"
                )

                cv2.imwrite(tile_path, tile)

                tiles.append({
                    "id": tile_id,
                    "correct_position": tile_id,
                    "path": tile_path
                })

                tile_id += 1

        return tiles

    def shuffle_tiles(self, tiles):
        
        while True:
            shuffled_tiles = tiles.copy()
            random.shuffle(shuffled_tiles)
            solved = True

            for pos, tile in enumerate(shuffled_tiles):
                tile["current_position"] = pos
                if tile["id"] != pos:
                    solved = False

            if not solved:
                return shuffled_tiles