from geography.schema import DEFAULT_GEO_CONFIG
from geography import request_area
from vmath import vec2, vec2i
from geography.tools.debug import show_height_map
from dev_tools.progress_tracker import ProgressTracker, step
from rooms import generate_room
from rooms.schema import WASTELAND_ROOM_REQUEST_CONFIG
from rooms.tools.debug import show_terrain

with ProgressTracker("test_math"):
    # geo_area = request_area(vec2i(10000, 1000), 200, 200, geo_config)
    # show_height_map(geo_area.map(lambda cell: cell.humidity), 1)
    # show_height_map(geo_area.map(lambda cell: float(cell.slope<80.0)), 1)
    
    result = generate_room(WASTELAND_ROOM_REQUEST_CONFIG)
    show_terrain(result, True)
    print(result[10,10], flush=True)
