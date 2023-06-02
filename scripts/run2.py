import argparse

import mesa
import mesa_geo as mg

from pyrosm import OSM

from src.model.model2 import AgentsAndNetworks
from src.visualization.server import (
    agent_draw,
    clock_element,
    status_chart,
)


def make_parser():
    parser = argparse.ArgumentParser("Agents and Networks in Python")
    parser.add_argument("--pbf", type=str, required=True)
    return parser


if __name__ == "__main__":
    args = make_parser().parse_args()

    try :
        print("Attempting to open PBF file...")
        osm = OSM(f"data/external/OSM/{args.pbf}.osm.pbf")

    except ValueError:
        print("File " + f"data/external/OSM/{args.pbf}.osm.pbf" + " not found.")

    osm = OSM(f"data/external/OSM/{args.pbf}.osm.pbf")
    print("PBF file opened successfully!")

    model_params = {
        "osm_object": osm,
        "data_crs": "epsg:5361",
        "show_walkway": True,
        "show_lakes_and_rivers": False,
        "show_driveway": False,
        "num_commuters": mesa.visualization.Slider(
            "Number of Commuters", value=50, min_value=10, max_value=150, step=10
        ),
        "commuter_speed": mesa.visualization.Slider(
            "Commuter Walking Speed (m/s)",
            value=0.5,
            min_value=0.1,
            max_value=1.5,
            step=0.1,
        ),
    }

    print("Creating Map Module...")
    map_element = mg.visualization.MapModule(agent_draw, map_height=600, map_width=600)
    server = mesa.visualization.ModularServer(
        AgentsAndNetworks,
        [map_element, clock_element, status_chart],
        "Agents and Networks",
        model_params,
    )

    print("Launching server...")
    server.launch()
