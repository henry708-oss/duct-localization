import math
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, ChainableUndefined

# This assumes that generate_x500.py is inside mrs_uav_gazebo_simulator
env = Environment(
    loader=FileSystemLoader(Path(__file__).resolve().parent / "models"),
    undefined=ChainableUndefined
)

env.globals["math"] = math
env.globals["spawner_args"] = {}

template = env.get_template(
    "mrs_robots_description/sdf/drones/x500.sdf.jinja"
)
output_path = Path(__file__).resolve().parent.parent / "x500.sdf"
with open(output_path, "w") as f:
    f.write(template.render())

print("Generated x500.sdf")