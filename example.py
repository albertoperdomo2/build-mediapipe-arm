import mediapipe as mp
import numpy as np
import PIL.Image as Image
mp_holistic = mp.solutions.holistic

holistic = mp_holistic.Holistic(static_image_mode=True)
for idx, file in enumerate(['/path/to/pic.jpg', '/path/to/pic2.jpg']):
  pic = Image.open(file)
  image_data = np.frombuffer(pic.tobytes(), dtype=np.uint8)
  image = np.copy(image_data.reshape((image_height, image_width, 3))[:,:,::-1])
  image_height, image_width, _ = image.shape
  results = holistic.process(image)
  if results.pose_landmarks:
    print(
        f'Nose coordinates: ('
        f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE]\
 .x * image_width}, '
        f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE]\
 .y * image_height})'
    )
holistic.close()
