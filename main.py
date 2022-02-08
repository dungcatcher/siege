from enemies import *
from towers import *
import config

window = pyglet.window.Window(config.width, config.height, resizable=True)
window.set_caption('Siege')
icon = pyglet.image.load('./Assets/icon.png')
window.set_icon(icon, icon)

towers = []
enemies = []

camera_pos = [config.width // 2, config.height // 2]
map_img = pyglet.image.load('./Assets/map.png')
map_sprite = pyglet.sprite.Sprite(map_img)
map_original_width = map_img.width
map_original_height = map_img.height


def cartesian_to_isometric(cart_x, cart_y):
    iso_x = (cart_x - cart_y)
    iso_y = (cart_x + cart_y) * 0.75
    return [iso_x, iso_y]


def isometric_to_cartesian(iso_x, iso_y):
    cart_x = ((4 / 3) * iso_y + iso_x) * 0.75
    cart_y = ((4 / 3) * iso_y - iso_x) * 0.75
    return [cart_x, cart_y]


batch = pyglet.graphics.Batch()


def generate_grid():
    for x in range(config.COLS):
        for y in range(config.ROWS):
            origin = [x * (config.tile_width / 2), y * (config.tile_width / 2)]
            points = [
                cartesian_to_isometric(origin[0], origin[1]),
                cartesian_to_isometric(origin[0], origin[1] + (config.tile_width / 2)),
                cartesian_to_isometric(origin[0] + (config.tile_width / 2), origin[1] + (config.tile_width / 2)),
                cartesian_to_isometric(origin[0] + (config.tile_width / 2), origin[1])
            ]

            for point in points:  # Adjust position
                point[0] += camera_pos[0]
                point[1] += (camera_pos[1] - (config.ROWS / 2) * config.tile_height) + config.tile_width / 2
            # circle = pyglet.shapes.Circle(x=points[0][0], y=points[0][1], radius=2, batch=batch)
            label = pyglet.text.Label(text=str(origin), x=points[0][0], y=points[0][1], font_name='Arial', font_size=7)
            label.draw()
            # polygons.append(circle)


@window.event
def on_draw():
    window.clear()

    map_img.anchor_x = map_img.width // 2
    map_img.anchor_y = map_img.height // 2
    map_img.x = camera_pos[0]
    map_img.y = camera_pos[1]
    map_sprite.x = map_img.x - map_img.anchor_x
    map_sprite.y = map_img.y - map_img.anchor_y
    map_sprite.draw()
    # generate_grid()

    batch.draw()
    for tower in towers:
        tower.sprite.draw()


@window.event
def on_resize(new_width, new_height):
    global camera_pos

    window.set_size(new_width, new_height)
    config.width, config.height = new_width, new_height
    camera_pos = [config.width // 2, config.height // 2]


@window.event
def on_mouse_release(x, y, button, modifiers):
    x -= camera_pos[0] - config.tile_width / 2
    y -= (camera_pos[1] - (config.ROWS / 2) * config.tile_height)

    print(cartesian_to_isometric(x // (config.tile_width / 2), y // (config.tile_height / 2)))

    cursor = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
    window.set_mouse_cursor(cursor)


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    original_tile_scale_factor = config.tile_scale_factor
    config.tile_scale_factor += scroll_y * 0.5
    tile_width = 4 * config.tile_scale_factor
    tile_height = 3 * config.tile_scale_factor

    image_scale = (config.COLS * tile_width) / map_original_width
    if image_scale * map_original_width > config.width and image_scale * map_original_height > config.height:
        map_sprite.scale = image_scale
        map_img.width = image_scale * map_original_width
        map_img.height = image_scale * map_original_height
    else:
        tile_scale_factor = original_tile_scale_factor
        tile_width = 4 * original_tile_scale_factor
        tile_height = 3 * original_tile_scale_factor


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global camera_pos

    if 0 <= camera_pos[0] + dx <= config.width and 0 <= camera_pos[1] + dy <= config.height:
        camera_pos[0] += dx
        camera_pos[1] += dy
        cursor = window.get_system_mouse_cursor(window.CURSOR_HAND)
        window.set_mouse_cursor(cursor)


pyglet.app.run()
