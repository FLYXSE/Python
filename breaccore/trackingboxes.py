import cv2
import numpy as np
import moviepy.editor as mpe
import random

# tg winterchroma!
# настройки настроечки
MAX_TRACKERS = 15          # максимальное число отслеживаемых точек
REDETECTION_INTERVAL = 30  # как часто искать новые точки для отслеживания (fps)
#WORDS = ["CAN", "YOU", "SEE", "ME", "?"] # список подписей к боксам
WORDS = ["JOPA"]
BOX_LIFESPAN_MIN = 1.0  # минимальное время жизни рамки (сек)
BOX_LIFESPAN_MAX = 3.0  # максимальное время жизни рамки (сек)
BOX_SIZE = 50           # размер рамки
LINE_COLOR = (255, 255, 255) # цвет рамок в бгр (да именно бгр, не ргб) - сейчас стоит белый
LINE_THICKNESS = 1 # толщина полосочек :3

# дальше трогать не рекомендуется

feature_params = dict(
    maxCorners=MAX_TRACKERS,
    qualityLevel=0.3,
    minDistance=8,
    blockSize=7
)


lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
)

# дальше трогать ваще не стоит
tracked_objects = []
prev_gray = None
frame_count = 0
last_time = -1


class TrackedObject:
    def __init__(self, point, creation_time):
        self.id = random.randint(1000, 9999)
        self.point = point
        self.text = random.choice(WORDS)
        self.creation_time = creation_time
        self.lifespan = random.uniform(BOX_LIFESPAN_MIN, BOX_LIFESPAN_MAX)

    def is_alive(self, current_time):
        return (current_time - self.creation_time) < self.lifespan


def process_frame_with_tracking(frame, t):
    global prev_gray, tracked_objects, frame_count, last_time

    if t < last_time:
        prev_gray = None
        tracked_objects = []
        frame_count = 0
    last_time = t

    current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    output_frame = frame.copy() # t.me/winterchroma

    tracked_objects = [obj for obj in tracked_objects if obj.is_alive(t)]

    if len(tracked_objects) > 0:
        old_points = np.float32([obj.point for obj in tracked_objects]).reshape(-1, 1, 2)
        new_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, current_gray, old_points, None, **lk_params)
        good_new_points = new_points[status == 1]
        survived_objects = [obj for i, obj in enumerate(tracked_objects) if status[i] == 1]

        for i, obj in enumerate(survived_objects):
            obj.point = tuple(good_new_points[i].ravel())
        # t.me/winterchroma
        tracked_objects = survived_objects

    if len(tracked_objects) < MAX_TRACKERS // 2 or frame_count % REDETECTION_INTERVAL == 0:
        mask = np.ones_like(current_gray)
        for obj in tracked_objects:
            x, y = map(int, obj.point)
            cv2.circle(mask, (x, y), 15, 0, -1)

        new_features = cv2.goodFeaturesToTrack(current_gray, mask=mask, **feature_params)
        
        if new_features is not None:
            for point in new_features: # t.me/winterchroma
                if len(tracked_objects) < MAX_TRACKERS:
                    tracked_objects.append(TrackedObject(tuple(point.ravel()), t))


    if tracked_objects:
        for obj in tracked_objects:
            x, y = map(int, obj.point)
            half_size = BOX_SIZE // 2
            cv2.rectangle(output_frame, (x - half_size, y - half_size), (x + half_size, y + half_size), LINE_COLOR, LINE_THICKNESS)
            cv2.putText(output_frame, obj.text, (x - half_size, y - half_size - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, LINE_COLOR, 1)

        if len(tracked_objects) > 1:
            num_lines = len(tracked_objects) // 2
            temp_list = random.sample(tracked_objects, len(tracked_objects))
            for i in range(num_lines):
                obj1 = temp_list[i*2]
                obj2 = temp_list[i*2 + 1]
                pt1 = tuple(map(int, obj1.point))
                pt2 = tuple(map(int, obj2.point))
                cv2.line(output_frame, pt1, pt2, LINE_COLOR, LINE_THICKNESS)

    
    prev_gray = current_gray.copy()
    frame_count += 1 # t.me/winterchroma
    
    return output_frame


if __name__ == '__main__':
    input_video_path = "input.mp4" # название исходного видео
    output_video_path = "output_tracked.mp4" # название итогового видео

    print("загрузка видео ща")
    clip = mpe.VideoFileClip(input_video_path)

    print("рисую квадраты!")
    
    final_clip = clip.fl(lambda gf, t: process_frame_with_tracking(gf(t)[:,:,::-1], t)[:,:,::-1])

    print(f"результат сохранен в {output_video_path}...")
    final_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac', logger='bar')
