import streamlit as st
from PIL import Image
import numpy as np
import noise
from rich.progress import track

from height_maps.army import army_height_map_1
from height_maps.navy import navy_height_map_1
from height_maps.airforce import airforce_height_map_1

"# Camoflouge pattern"

selection = st.sidebar.selectbox("Pattern", ("Army", "Navy", "Airforce"))
if selection == "Army":
  height_map = army_height_map_1
elif selection == "Navy":
  height_map = navy_height_map_1
elif selection == "Airforce":
  height_map = airforce_height_map_1

shape = (512, 512)
scale = st.sidebar.slider("Scale", 0.0, 30.0, 15.0)
octaves = st.sidebar.slider("Octaves", 0, 15, 6)
persistence = st.sidebar.slider("Persistence", 0.0, 1.0, 0.5)
lacunarity = st.sidebar.slider("Lacunarity", 0.0, 10.0, 2.0)

pattern_array = np.zeros(
    (shape[0], shape[1], 3),
    dtype=np.uint8
)

for i in track(range(shape[0]), description="Generating image ..."):
  for j in range(shape[1]):
    n1 = noise.pnoise2(
        i / scale,
        j / scale,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        repeatx=shape[0],
        repeaty=shape[1],
        base=0
    )

    for key in height_map.keys():
      min_height = height_map[key]['height']
      if n1 <= min_height:
        color = height_map[key]['color']
        break

    pattern_array[i][j] = color

image = Image.fromarray(pattern_array, 'RGB')
# image.save('pattern.png')
st.image(image)
