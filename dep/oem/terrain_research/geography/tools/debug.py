from array2d import array2d
from vmath import color32, vec2, vec2i
import math
import tileset_data

def tile_to_str(tileset_id: int, tile_id: int) -> tuple[str, str]:
    """打印单字符"""
    try:
        tileset = [tileset for tileset in tileset_data._data["tilesets"] if tileset["id"] == tileset_id][0]
    except IndexError:
        raise ValueError(f"Tileset {tileset_id} not found")
    
    try:
        tile = [tile for tile in tileset["tiles"] if tile["id"] == tile_id][0]
        char = tile["char"]
        bg = tile["bg"]
        fg = tile["fg"]
    except IndexError:
        raise ValueError(f"Tile {tile_id} not found in tileset {tileset_id}")
    
    if bg is not None:
        char = color32.from_hex(bg).ansi_bg(char)
    
    if fg is not None:
        char = color32.from_hex(fg).ansi_fg(char)
    
    return char, bg


def _get_tile_index_from_height(height_val: float, min_h_map: float, max_h_map: float, tileset_len: int) -> int:
    """Helper function to map a height value to a tile index.
    Assumes lower index corresponds to higher elevation.
    """
    if tileset_len == 0:
        # Should not happen if called after tileset_length checks, but as a safeguard
        raise ValueError("Cannot get tile index from an empty tileset.")
    if tileset_len == 1:
        return 0 # Only one tile, so always its index

    if max_h_map == min_h_map: # Single height value across the map
        return 0 # Default to the first tile (conventionally highest elevation)
    elif height_val >= max_h_map: # Highest value maps to index 0
        return 0
    elif height_val <= min_h_map: # Lowest value maps to last index
        return tileset_len - 1
    else:
        # (max_h_map - height_val) because high value -> low index
        inverted_relative_pos = (max_h_map - height_val) / (max_h_map - min_h_map)
        # -1e-9 for max_h_map boundary, ensure it maps to tileset_len -1 correctly
        target_tile_index = int(inverted_relative_pos * (tileset_len - 1e-9)) 
        return max(0, min(tileset_len - 1, target_tile_index)) # Clamp index

def generate_height_to_background_map(
    height_map: array2d[float], 
    tileset_id: int, 
    all_tilesets_data: dict, 
    zoom_out: int, 
    color_bar_range: tuple[float, float] | None = None,
    map_gwc_tl: vec2i | None = None,
    highlight_roi_gwc_tl: vec2i | None = None,
    highlight_roi_size: vec2i | None = None,
    highlight_color_hex: str = "#000000"
) -> tuple[array2d[tuple[float, str | None]], dict[int, tuple[float,float]], float, float]:
    """
    Generates a styled map (background colors) from a height map.
    Also calculates color ranges for each tile used in the color bar.
    Can now highlight a specific ROI.
    """
    
    current_tileset = None
    for ts_data in all_tilesets_data:
        if ts_data['id'] == tileset_id:
            current_tileset = ts_data
            break
    if not current_tileset:
        raise ValueError(f"Tileset with ID {tileset_id} not found.")

    tileset_tiles = current_tileset['tiles']
    tileset_len = len(tileset_tiles)
    if tileset_len == 0:
        raise ValueError(f"Tileset {tileset_id} is empty.")

    if height_map.n_cols == 0 or height_map.n_rows == 0:
        # Return empty or appropriately sized empty map and default ranges
        styled_width = 0
        styled_height = 0
        styled_map_data = array2d[tuple[float, str | None]](styled_width, styled_height)
        return styled_map_data, {}, 0.0, 1.0


    # 手动计算最小最大值
    min_h_actual = float('inf')
    max_h_actual = float('-inf')
    for y in range(height_map.n_rows):
        for x in range(height_map.n_cols):
            val = height_map[x, y]
            min_h_actual = min(min_h_actual, val)
            max_h_actual = max(max_h_actual, val)
    if min_h_actual == float('inf'):  # 空地图的情况
        min_h_actual, max_h_actual = 0.0, 1.0
    
    min_h_map_for_bar = color_bar_range[0] if color_bar_range is not None else min_h_actual
    max_h_map_for_bar = color_bar_range[1] if color_bar_range is not None else max_h_actual
    if min_h_map_for_bar == max_h_map_for_bar: # Avoid division by zero
        max_h_map_for_bar += 1e-6 

    styled_width = int(math.ceil(height_map.n_cols / zoom_out))
    styled_height = int(math.ceil(height_map.n_rows / zoom_out))
    
    styled_map_data = array2d[tuple[float, str | None]](styled_width, styled_height, (0.0, None))
    tile_color_ranges: dict[int, tuple[float,float]] = {}

    for sy in range(styled_height):
        for sx in range(styled_width):
            original_x_start = sx * zoom_out
            original_y_start = sy * zoom_out
            
            h_val_sum = 0.0
            count = 0
            for offsetY in range(zoom_out):
                for offsetX in range(zoom_out):
                    map_x = original_x_start + offsetX
                    map_y = original_y_start + offsetY
                    if 0 <= map_x < height_map.n_cols and 0 <= map_y < height_map.n_rows:
                        h_val_sum += height_map[map_x, map_y]
                        count += 1
            
            h_val = h_val_sum / count if count > 0 else 0.0

            tile_index = _get_tile_index_from_height(h_val, min_h_map_for_bar, max_h_map_for_bar, tileset_len)
            bg_color_hex = tileset_tiles[tile_index]['bg']
            styled_map_data[sx, sy] = (h_val, bg_color_hex)
            
            if tile_index not in tile_color_ranges:
                tile_color_ranges[tile_index] = [h_val, h_val]
            else:
                tile_color_ranges[tile_index][0] = min(tile_color_ranges[tile_index][0], h_val)
                tile_color_ranges[tile_index][1] = max(tile_color_ranges[tile_index][1], h_val)

    # ROI Highlighting logic
    if map_gwc_tl is not None and highlight_roi_gwc_tl is not None and highlight_roi_size is not None:
        if highlight_roi_size.x > 0 and highlight_roi_size.y > 0: # Ensure ROI is valid
            # Calculate GWC bottom-right for the highlight ROI
            highlight_roi_gwc_br_x = highlight_roi_gwc_tl.x + highlight_roi_size.x - 1
            highlight_roi_gwc_br_y = highlight_roi_gwc_tl.y + highlight_roi_size.y - 1

            # Calculate the outer border GWC coordinates
            outer_border_tl_x = highlight_roi_gwc_tl.x - 1
            outer_border_tl_y = highlight_roi_gwc_tl.y - 1
            outer_border_br_x = highlight_roi_gwc_br_x + 1
            outer_border_br_y = highlight_roi_gwc_br_y + 1

            # Calculate map boundaries in GWC
            map_gwc_br_x = map_gwc_tl.x + height_map.n_cols - 1
            map_gwc_br_y = map_gwc_tl.y + height_map.n_rows - 1

            for sy_styled in range(styled_height): # Iterate over styled_map_data dimensions
                for sx_styled in range(styled_width):
                    # Top-left GWC of the block of original cells corresponding to this styled cell
                    block_gwc_tl_x = map_gwc_tl.x + sx_styled * zoom_out
                    block_gwc_tl_y = map_gwc_tl.y + sy_styled * zoom_out
                    # Bottom-right GWC of the block
                    block_gwc_br_x = block_gwc_tl_x + zoom_out - 1
                    block_gwc_br_y = block_gwc_tl_y + zoom_out - 1

                    # Check if this cell is on the outer border of the ROI
                    is_on_border = False
                    
                    # Check if this cell overlaps with the outer border
                    overlap_starts_x = max(block_gwc_tl_x, outer_border_tl_x)
                    overlap_starts_y = max(block_gwc_tl_y, outer_border_tl_y)
                    overlap_ends_x = min(block_gwc_br_x, outer_border_br_x)
                    overlap_ends_y = min(block_gwc_br_y, outer_border_br_y)

                    if overlap_starts_x <= overlap_ends_x and overlap_starts_y <= overlap_ends_y:
                        # Check if this cell is on the outer border and within map boundaries
                        is_on_border = (
                            (block_gwc_tl_x == outer_border_tl_x and outer_border_tl_x >= map_gwc_tl.x) or\
                            (block_gwc_br_x == outer_border_br_x and outer_border_br_x <= map_gwc_br_x) or\
                            (block_gwc_tl_y == outer_border_tl_y and outer_border_tl_y >= map_gwc_tl.y) or\
                            (block_gwc_br_y == outer_border_br_y and outer_border_br_y <= map_gwc_br_y)\
                        )

                        if is_on_border:
                            original_value, _ = styled_map_data[sx_styled, sy_styled]
                            styled_map_data[sx_styled, sy_styled] = (original_value, highlight_color_hex)
    return styled_map_data, tile_color_ranges, min_h_map_for_bar, max_h_map_for_bar


def show_height_map(
    height_map: array2d[float], 
    zoom_out: int = 1, 
    mode: str = "all", 
    color_bar_range: tuple[float, float] | None = None,
    map_gwc_tl: vec2i | None = None,
    highlight_roi_gwc_tl: vec2i | None = None,
    highlight_roi_size: vec2i | None = None,
    highlight_color_hex: str = "#000000"
):
    if height_map.n_cols == 0 or height_map.n_rows == 0:
        print("Height map is empty, nothing to show.")
        return

    if mode == "all":
        tileset_id = 3
    elif mode == "ground":
        tileset_id = 1
    elif mode == "sea":
        tileset_id = 2
    else:
        raise ValueError(f"Invalid mode: {mode}")

    # Fetch tileset info once for character/foreground color lookup
    try:
        selected_tileset_for_render = [ts for ts in tileset_data._data["tilesets"] if ts["id"] == tileset_id][0]
        tiles_in_set_for_render = selected_tileset_for_render["tiles"]
        tileset_length_for_render = len(tiles_in_set_for_render)
    except IndexError:
        raise ValueError(f"Tileset {tileset_id} not found for rendering.")

    if tileset_length_for_render == 0:
        raise ValueError(f"Tileset {tileset_id} for rendering is empty.")

    styled_map_data, tile_color_ranges_output, min_h_map_val, max_h_map_val = generate_height_to_background_map(
        height_map, tileset_id, tileset_data._data['tilesets'], zoom_out, color_bar_range,
        map_gwc_tl=map_gwc_tl,
        highlight_roi_gwc_tl=highlight_roi_gwc_tl,
        highlight_roi_size=highlight_roi_size,
        highlight_color_hex=highlight_color_hex
    )
    
    for y in range(styled_map_data.shape.y - 1, -1, -1):
        for x in range(styled_map_data.shape.x):
            height_val_at_point, bg_color_hex = styled_map_data[x, y]

            target_tile_index_render = _get_tile_index_from_height(
                height_val_at_point, min_h_map_val, max_h_map_val, tileset_length_for_render
            )
            
            tile_spec_for_char = tiles_in_set_for_render[target_tile_index_render]
            char_to_print = tile_spec_for_char["char"]
            fg_color_hex = tile_spec_for_char["fg"]

            # Apply coloring using retrieved bg_color_hex and newly determined fg_color_hex
            if bg_color_hex is not None:
                char_to_print = color32.from_hex(bg_color_hex).ansi_bg(char_to_print)
            if fg_color_hex is not None:
                char_to_print = color32.from_hex(fg_color_hex).ansi_fg(char_to_print)
            
            print(char_to_print, end="")
        print()
        
    # 打印颜色条
    print("\n颜色条:")

    if tileset_length_for_render == 0:
        print(" (No tiles in tileset to display in color bar)")
    elif color_bar_range is not None:
        # User specified a color_bar_range, so print idealized, evenly divided ranges.
        display_min_h = min_h_map_val  # This is color_bar_range[0]
        display_max_h = max_h_map_val  # This is color_bar_range[1]
        
        if display_min_h == display_max_h: # Avoid division by zero if range is zero
            display_max_h += 1e-6 

        total_span_for_bar = display_max_h - display_min_h
        segment_size = total_span_for_bar / tileset_length_for_render if tileset_length_for_render > 0 else 0

        # Iterate tiles by their natural index order (0 for highest value mapping, N-1 for lowest)
        for tile_idx_for_legend in range(tileset_length_for_render):
            tile_spec = tiles_in_set_for_render[tile_idx_for_legend]
            bg_bar = tile_spec["bg"]

            # Calculate the ideal range for this tile index (higher index = lower value)
            current_range_max = display_max_h - tile_idx_for_legend * segment_size
            current_range_min = display_max_h - (tile_idx_for_legend + 1) * segment_size
            
            # Clamp the lowest range's min to display_min_h for precision
            if tile_idx_for_legend == tileset_length_for_render - 1:
                current_range_min = display_min_h
            
            bar_text = f" {current_range_min:.2f} ~ {current_range_max:.2f} "
            if bg_bar is not None:
                bar_text = color32.from_hex(bg_bar).ansi_bg(bar_text)
            bar_text = color32.from_hex("#000000").ansi_fg(bar_text) # Black text
            print(bar_text)
    else:
        # color_bar_range is None. Print ranges based on actual observed data values for each tile.
        # tile_color_ranges_output is a dict: {tile_index: [min_observed, max_observed]}
        if not tile_color_ranges_output:
            print(" (No data to display in color bar based on actual ranges)")
        else:
            # Sort by tile_index to maintain a consistent visual order (0=high, N-1=low values)
            sorted_observed_ranges = sorted(tile_color_ranges_output.items(), key=lambda item: item[0])

            for tile_idx, observed_range in sorted_observed_ranges:
                observed_min, observed_max = observed_range
                if 0 <= tile_idx < tileset_length_for_render:
                    tile_spec = tiles_in_set_for_render[tile_idx] # Get tile properties from the list
                    bg_bar = tile_spec["bg"]
                    
                    bar_text = f" {observed_min:.2f} ~ {observed_max:.2f} " # Display observed range
                    if bg_bar is not None:
                        bar_text = color32.from_hex(bg_bar).ansi_bg(bar_text)
                    bar_text = color32.from_hex("#000000").ansi_fg(bar_text) # Black text
                    print(bar_text)
                # else: # Optional: print warning for unexpected tile_idx if it occurs

    print("\n参数:")
    print(f"min_h (for color mapping): {min_h_map_val:.2f}") # Use .2f for consistency
    print(f"max_h (for color mapping): {max_h_map_val:.2f}") # Use .2f for consistency
    print(f"shape: {height_map.shape}")
    print(f"zoom_out: {zoom_out}")


def apply_background_to_styled_foreground(
    styled_foreground_chars: array2d[str], 
    background_colors_hex: array2d[str | None]
) -> array2d[str]:
    """Applies background colors to an array of pre-styled foreground characters."""
    if styled_foreground_chars.shape != background_colors_hex.shape:
        raise ValueError(f"Shape mismatch: styled_foreground_chars {styled_foreground_chars.shape} !="+f" background_colors_hex {background_colors_hex.shape}")
    
    output_map = array2d(styled_foreground_chars.shape.x, styled_foreground_chars.shape.y, "")
    for y in range(styled_foreground_chars.shape.y):
        for x in range(styled_foreground_chars.shape.x):
            styled_fg_char = styled_foreground_chars[x, y]
            bg_hex = background_colors_hex[x, y]
            
            if bg_hex is not None:
                # It's assumed that color32.from_hex(bg_hex).ansi_bg() can correctly wrap
                # a string that already contains ANSI foreground codes.
                output_map[x, y] = color32.from_hex(bg_hex).ansi_bg(styled_fg_char)
            else:
                output_map[x, y] = styled_fg_char # No background to apply
    return output_map


def show_vector_field(
    vector_field: array2d[vec2],
    zoom_out: int = 1,
    background_tileset_id: int = 3, # For magnitude, default to "debug-height-all"
    vector_magnitude_range: tuple[float, float] | None = None, # Analogous to color_bar_range for height
    map_gwc_tl: vec2i | None = None,
    highlight_roi_gwc_tl: vec2i | None = None,
    highlight_roi_size: vec2i | None = None,
    highlight_color_hex: str = "#000000"
):
    """Displays a vector field using arrows for direction and background color for magnitude."""
    if not isinstance(vector_field, array2d) or (vector_field.shape.x > 0 and vector_field.shape.y > 0 and not isinstance(vector_field[0,0], vec2)):
        raise TypeError("vector_field must be an array2d of vec2 objects.")

    # 1. Create magnitude_map from vector_field
    magnitude_map = array2d(vector_field.shape.x, vector_field.shape.y, 0.0)
    for y_idx in range(vector_field.shape.y):
        for x_idx in range(vector_field.shape.x):
            v = vector_field[x_idx, y_idx]
            magnitude_map[x_idx, y_idx] = math.sqrt(v.x**2 + v.y**2)

    # 2. Use generate_height_to_background_map for background colors based on magnitudes
    # The 'height_map' here is actually our 'magnitude_map'
    # 'color_bar_range' for generate_height_to_background_map is our 'vector_magnitude_range'
    magnitude_color_map_zoomed, ranges_for_magnitudes, min_magnitude, max_magnitude = generate_height_to_background_map(
        magnitude_map, 
        background_tileset_id, 
        tileset_data._data["tilesets"], # global tileset data
        zoom_out, 
        vector_magnitude_range,
        map_gwc_tl,
        highlight_roi_gwc_tl,
        highlight_roi_size,
        highlight_color_hex
    )

    # 3. Get direction tileset (id=4)
    direction_tileset_id = 4
    try:
        # Ensure the direction tileset exists, though tile_to_str would also catch issues.
        _ = [ts for ts in tileset_data._data["tilesets"] if ts["id"] == direction_tileset_id][0]
    except IndexError:
        raise ValueError(f"Direction tileset (id={direction_tileset_id}) not found.")

    # 4. Prepare styled foreground arrows and background hex colors
    zoomed_width = magnitude_color_map_zoomed.shape.x
    zoomed_height = magnitude_color_map_zoomed.shape.y

    styled_arrow_map = array2d(zoomed_width, zoomed_height, "")
    # Create an array2d for background hex strings, initialized with None
    background_hex_map = array2d[str|None](zoomed_width, zoomed_height, None)

    for y_out in range(zoomed_height):
        for x_out in range(zoomed_width):
            # a. Get original vector for direction calculation
            original_x = x_out * zoom_out
            original_y = y_out * zoom_out
            current_vector = vector_field[original_x, original_y] if (original_x < vector_field.shape.x and original_y < vector_field.shape.y) else vec2(0,0)

            # b. Calculate angle and map to direction_tile_id for the arrow character
            vx, vy = current_vector.x, current_vector.y
            angle_rad = math.atan2(-vy, vx)
            angle_deg = math.degrees(angle_rad)
            if angle_deg < 0: angle_deg += 360
            direction_arrow_tile_id = int(math.floor((angle_deg + 22.5) / 45.0)) % 8
            
            # c. Get direction arrow character with its predefined foreground color
            arrow_char_with_fg, _ = tile_to_str(direction_tileset_id, direction_arrow_tile_id)
            styled_arrow_map[x_out, y_out] = arrow_char_with_fg
            
            # d. Get background_color_hex from the magnitude map
            _original_magnitude_at_point, bg_color_hex = magnitude_color_map_zoomed[x_out, y_out]
            background_hex_map[x_out, y_out] = bg_color_hex

    # 5. Combine foreground arrows with magnitude-based background colors using the new function
    final_display_map = apply_background_to_styled_foreground(styled_arrow_map, background_hex_map)

    # 6. Print the final combined map
    for y_out in range(final_display_map.shape.y - 1, -1, -1):
        for x_out in range(final_display_map.shape.x):
            print(final_display_map[x_out, y_out], end="")
        print() # Newline after each row

    # 7. Print color bar for magnitudes
    print("\nMagnitude Color Bar:")
    # Sort ranges by the min value of the magnitude interval they represent
    ranges_sorted_magnitudes = sorted(ranges_for_magnitudes.items(), key=lambda item: item[1][0])

    for tile_id_for_bar, range_m_val in ranges_sorted_magnitudes:
        range_min, range_max = range_m_val
        # Get the character and background for the color bar swatch from the background_tileset_id
        _char_bar_swatch, bg_bar_swatch = tile_to_str(background_tileset_id, tile_id_for_bar)
        
        bar_text = f" {range_min:.2f} ~ {range_max:.2f} " # Text showing magnitude range
        if bg_bar_swatch is not None:
            bar_text = color32.from_hex(bg_bar_swatch).ansi_bg(bar_text)
        # Ensure text is visible (e.g., black text)
        bar_text = color32.from_hex("#000000").ansi_fg(bar_text) 
        print(bar_text)

    # 8. Print parameters
    print("\nParameters:")
    print(f"min_magnitude: {min_magnitude:.2f}")
    print(f"max_magnitude: {max_magnitude:.2f}")
    print(f"vector_field_shape: {vector_field.shape}")
    print(f"zoom_out: {zoom_out}")
    print(f"background_tileset_id (for magnitude): {background_tileset_id}")