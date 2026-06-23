from puzzle.generator import PuzzleGenerator

generator = PuzzleGenerator(grid_size=3)

tiles = generator.generate_tiles()

shuffled_tiles = generator.shuffle_tiles(tiles)

print("\nOriginal Order")

for tile in tiles:
    print(tile["id"])

print("\nShuffled Order")

for tile in shuffled_tiles:
    print(tile["id"])