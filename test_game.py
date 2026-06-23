from puzzle.generator import PuzzleGenerator
from puzzle.puzzle_game import PuzzleGame

generator = PuzzleGenerator(grid_size=3)

tiles = generator.generate_tiles()

shuffled_tiles = generator.shuffle_tiles(tiles)

game = PuzzleGame(
    shuffled_tiles,
    grid_size=3
)

game.run()
