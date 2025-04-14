import os
from openslide import OpenSlide
import warnings
import cv2
import joblib
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import shutil
import csv
from tqdm import tqdm
from tiatoolbox import logger
from tiatoolbox.models.engine.nucleus_instance_segmentor import NucleusInstanceSegmentor
from tiatoolbox.utils.misc import download_data, imread
warnings.filterwarnings('ignore', category=DeprecationWarning)

# We need this function to visualize the nuclear predictions
from tiatoolbox.utils.visualization import (
    overlay_prediction_contours,
)
from tiatoolbox.wsicore.wsireader import WSIReader

# warnings.filterwarnings("ignore")
mpl.rcParams["figure.dpi"] = 300  # for high resolution figure in notebook
mpl.rcParams["figure.facecolor"] = "white"  # To make sure text is visible in dark mode
plt.rcParams.update({"font.size": 5})
# Should be changed to False if no cuda-enabled GPU is available.
ON_GPU = True  # Default is True.

# Tile prediction
inst_segmentor = NucleusInstanceSegmentor(
    pretrained_model="hovernet_fast-pannuke",
    num_loader_workers=2,
    num_postproc_workers=2,
    batch_size=4,
)

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Assuming inst_segmentor and ON_GPU are already initialized
ON_GPU = True


def process_tile(tile_info):
    """
    Process a single tile by performing prediction.

    Parameters:
    - tile_info: A tuple containing the tile path and output directory.

    Returns:
    - The result of the prediction.
    """
    tile_path, output_dir = tile_info
    # Perform the prediction
    return inst_segmentor.predict(
        [tile_path],
        save_dir=output_dir,
        mode="tile",
        on_gpu=ON_GPU,
        crash_on_exception=True,
    )


def fun_qupath_tile(input_dir, output_dir, num_threads=1):
    """
    Process tiles from an input directory and save the results to an output directory using multithreading.

    Parameters:
    - input_dir: Path to the input directory containing tiles.
    - output_dir: Path to the output directory where results will be saved.
    - num_threads: Number of threads to use for concurrent processing.
    """
    print("Input directory:", input_dir)
    print("Output directory:", output_dir)

    # Iterate over patient directories
    for patient in sorted(os.listdir(input_dir), reverse=True):
        patient_tile_path = os.path.join(input_dir, patient)

        # Create the patient's output directory if it does not exist
        output_patient_dir = os.path.join(output_dir, patient)
        if not os.path.exists(output_patient_dir):
            os.makedirs(output_patient_dir)

        # Collect information for each tile
        tiles = sorted(os.listdir(patient_tile_path))
        tile_info_list = []
        for tile in tiles:
            tile_path = os.path.join(patient_tile_path, tile)
            output_tile_dir = os.path.join(output_patient_dir, tile[:-4])
            tile_info_list.append((tile_path, output_tile_dir))

        # Use ThreadPoolExecutor to process tiles concurrently
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit all tasks to the thread pool
            future_to_tile = {executor.submit(process_tile, tile_info): tile_info for tile_info in tile_info_list}

            # Display progress bar
            for future in tqdm(as_completed(future_to_tile), total=len(future_to_tile),
                               desc=f"Processing tiles for {patient}", unit="tile"):
                try:
                    future.result()  # Retrieve the result of the future, may raise an exception
                except Exception as exc:
                    print(f"Tile processing generated an exception: {exc}")
