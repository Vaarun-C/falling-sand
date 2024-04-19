import pygame

def init(dimensions: tuple[int, int], title: str) -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode(dimensions)
    pygame.display.set_caption(title)
    return screen

def init_grid(dimensions: tuple[int, int]) -> list[list[pygame.Color]]:
    grid = []
    for _ in range(dimensions[1]):
        pixel_row = []
        for _ in range(dimensions[0]):
            colour = pygame.Color((0,0,0,0))
            pixel_row.append(colour)
        grid.append(pixel_row)

    return grid

def main() -> None:
    screen_width, screen_height = 600,400
    screen = init((screen_width, screen_height), "Falling Sand Simulator")
    clock = pygame.time.Clock()

    pixel_width = 4
    width,height = screen_width//pixel_width, screen_height//pixel_width
    grid = init_grid((width, height))
    gradient = generate_gradient()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if (pygame.mouse.get_pressed()[0]):
                px, py  = pygame.mouse.get_pos()
                gx,gy = px//pixel_width, py//pixel_width
                colour = next(gradient)
                grid[gy][gx] = colour
                if(gx-1 > 0):
                    grid[gy][gx-1] = colour
                if(gx+1 < width):
                    grid[gy][gx+1] = colour
                if(gy-1 > 0):
                    grid[gy-1][gx] = colour
                if(gy+1 < height):
                    grid[gy+1][gx] = colour

        screen.fill((0, 0, 0))  # Clear the screen
        update_sand((width, height), grid, get_sand_pixels(grid))
        draw_pixels(screen, grid, pixel_width)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

def draw_pixels(screen: pygame.Surface, grid: list[list[pygame.Color]], pixel_width: int) -> None:
    for y,pixel_row in enumerate(grid):
        for x,pixel_colour in enumerate(pixel_row):
            pygame.draw.rect(screen, pixel_colour, (x*pixel_width, y*pixel_width, (x+1)*pixel_width, (y+1)*pixel_width))

def generate_gradient():    
    step = 1
    tic = 0
    while True:
        tic = (tic + step) % 256
        next_colour = pygame.Color((0,0,0,0))
        next_colour.hsva = (tic, 100, 100, 1)
        yield next_colour

def get_sand_pixels(grid: list[list[pygame.Color]]) -> list[tuple[int,int]]:
    sand_pixels = []
    for y,pixel_row in enumerate(grid):
        for x,pixel_colour in enumerate(pixel_row):
            if(pixel_colour.hsva[2] > 0):
                sand_pixels.append((x,y))

    return sand_pixels

def update_sand(dimensions: tuple[int, int], grid: list[list[pygame.Color]], pixels: list[tuple[int,int]]) -> None:
    max_x, max_y = dimensions
    for pixel in pixels:
        x, y = pixel

        if(x-1<0) or (x+1>=max_x) or (y+1>=max_y):
            continue
        
        if (grid[y+1][x].hsva[2] == 0):
            grid[y+1][x], grid[y][x] = grid[y][x], grid[y+1][x]
        elif (grid[y+1][x-1].hsva[2] == 0):
            grid[y+1][x-1], grid[y][x] = grid[y][x], grid[y+1][x-1]
        elif (grid[y+1][x+1].hsva[2] == 0):
            grid[y+1][x+1], grid[y][x] = grid[y][x], grid[y+1][x+1]

if __name__ == "__main__":
    main()