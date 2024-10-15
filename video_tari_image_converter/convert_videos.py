import os
import cv2
import logging
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

def extract_frames(video_path, output_dir, video_id, classname, fps=1, frame_size=(224,224)):
	"""Extract frames from a video file"""
	cap = cv2.VideoCapture(video_path)
	original_fps = cap.get(cv2.CAP_PROP_FPS)
	frame_interval = int(original_fps / fps)
	count = 0
	frame_id = 0

	logging.info(f"Starting frame extraction for video {video_id} ({classname})")

	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			break

		if count % frame_interval == 0:
			frame = cv2.resize(frame, frame_size)
			frame_filename = f"{video_id}_{classname}_frame_{frame_id:05d}.jpg"
			frame_path = os.path.join(output_dir, frame_filename)
			if not os.path.exists(frame_path):
				cv2.imwrite(frame_path, frame)

			frame_id += 1

		count += 1

	cap.release()

# def process_dataset(dataset_dir, csv_file, output_csv_file):
# 	df = pd.read_csv(csv_file)
# 	new_rows = []

# 	for index, row in tqdm(df.iterrows(), total=len(df), desc=f"Processing {csv_file}"):
# 		video_id = row["id"]
# 		filename = row["filename"]
# 		classname = row["classname"]
# 		video_rel_path = row["path"]
# 		video_abs_path = os.path.join(dataset_dir, video_rel_path)
# 		video_class_path = os.path.join(dataset_dir, classname)

# 		# Define output directory for frames
# 		frames_dir = os.path.join(dataset_dir, f"{classname}_frames")
# 		os.makedirs(frames_dir, exist_ok=True)

# 		# Extract frames from video
# 		extract_frames(
# 			video_path=video_abs_path, 
# 			output_dir=frames_dir,
# 			video_id=video_id,
# 			classname=classname)

# 		# Record new paths in the new CSV file
# 		frame_files = sorted(os.listdir(frames_dir))
# 		for frame_file in frame_files:
# 			frame_rel_path = os.path.join(frames_dir, frame_file)
# 			new_rows.append({
# 				"video_id": video_id,
# 				"frame_filename": frame_file,
# 				"classname": classname,
# 				"path": frame_rel_path
# 			})

# 	# Save new CSV file
# 	new_df = pd.DataFrame(new_rows)
# 	new_df.to_csv(output_csv_file, index=False)
def process_video(row, dataset_dir):
	video_id = row["id"]
	filename = row["filename"]
	classname = row["classname"]
	video_rel_path = row["path"]
	video_abs_path = os.path.join(dataset_dir, video_rel_path)
	video_class_path = os.path.join(dataset_dir, classname)

	# Define output directory for frames
	frames_dir = os.path.join(dataset_dir, f"{classname}_frames")
	os.makedirs(frames_dir, exist_ok=True)

	# Extract frames from video
	extract_frames(
		video_path=video_abs_path, 
		output_dir=frames_dir,
		video_id=video_id,
		classname=classname)

	# Record new paths in the new CSV file
	frame_files = sorted(os.listdir(frames_dir))
	new_rows = []
	for frame_file in frame_files:
		frame_rel_path = os.path.join(frames_dir, frame_file)
		new_rows.append({
			"video_id": video_id,
			"frame_filename": frame_file,
			"classname": classname,
			"path": frame_rel_path
		})
	return new_rows

def process_dataset(dataset_dir, csv_file, output_csv_file):
	df = pd.read_csv(csv_file)
	new_rows = []

	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(process_video, row, dataset_dir) for index, row in df.iterrows()]
		for future in tqdm(futures, total=len(futures), desc=f"Processing {csv_file}"):
			new_rows.extend(future.result())

	# Save new CSV file
	new_df = pd.DataFrame(new_rows)
	new_df.to_csv(output_csv_file, index=False)

def main():
	base_dir = "E:\Machine Learning Datasets\Gerakan Dasar Tari Bali\small-Dasar-Gerakan-Tari-Bali-All-Women"
	subsets = ["train", "val", "test"]

	for subset in subsets:
		dataset_dir = os.path.join(base_dir, subset)
		csv_file = os.path.join(base_dir, f"{subset}.csv")
		output_csv_file = os.path.join(base_dir, f"{subset}_frames.csv")

		process_dataset(dataset_dir, csv_file, output_csv_file)

if __name__ == "__main__":
	main()