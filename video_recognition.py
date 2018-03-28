# coding: utf-8
import face_recognition
import cv2
import uuid
import json
import datetime

started = datetime.datetime.now()

video_capture = cv2.VideoCapture('三国.mp4')
fps = video_capture.get(cv2.CAP_PROP_FPS)
print 'fps: ', fps
# obama_img = face_recognition.load_image_file("ss.png")
# obama_face_encoding = face_recognition.face_encodings(obama_img)[0]

# face_locations = []
# face_encodings = []
# face_names = []
# process_this_frame = True

face_maps = {}

person_number = 0
person_appear_maps = {}

ignore_interval = datetime.timedelta(5)
step = int(fps) * 5


def get_or_register_face(face_encoding):
    """
    
    :param face_encoding: eigen value
    :type face_encoding: 
    :return: new, id
    """
    if face_maps:
        for k, v in face_maps.items():
            result = face_recognition.compare_faces([v, ], face_encoding, tolerance=0.6)
            # print 'result', result
            if result[0]:
                return False, k
    new_id = str(uuid.uuid4())
    face_maps[new_id] = face_encoding
    return True, new_id


def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated


def frame_to_time(frame):
    return str(datetime.timedelta(seconds=frame / fps)).split('.')[0]


def is_in_intervel(video_time):
    video_now = datetime.datetime.strptime(video_time, '%H:%M:%S')
    last_video_time = datetime.datetime.strptime(person_appear_maps[face_id][-1][-1],  '%H:%M:%S')
    return video_now - last_video_time < ignore_interval


frames = 0
face_names = []

while True:
    ret, frame = video_capture.read()
    if frame is None:
        print 'no frame'
        break
    # cv2.imshow('Video', frame)
    # time.sleep(3)
    # frame = rotate(frame, -90)
    # small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    if frames % step is not 0:
        frames += 1
        continue
    # face_locations = face_recognition.face_locations(small_frame)
    face_locations = face_recognition.face_locations(frame)
    # face_encodings = face_recognition.face_encodings(small_frame, face_locations)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    print face_locations

    for face_encoding in face_encodings:
        is_new, face_id = get_or_register_face(face_encoding)
        video_time = frame_to_time(frames)
        if is_new:
            person_appear_maps[face_id] = [[video_time, video_time]]
        elif is_in_intervel(video_time):
            person_appear_maps[face_id][-1][-1] = video_time
        else:
            person_appear_maps[face_id].append([video_time, video_time])
    frames += 1
    # match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
    #
    # if match[0]:
    #     name = "P1"
    # else:
    #     name = "unknown"
    # # print name
    face_names.append('xxx')
    # process_this_frame = not process_this_frame
    #
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # top *= 2
        # right *= 2
        # bottom *= 2
        # left *= 2

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255),  3)
        # print 'show'
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (55, 255, 155), 1)

    cv2.imshow('Video', frame)
    # cv2.waitKey(1000)
    # if cv2.waitKey(30) & 0xFF == ord('q'):
    #     break

print 'Person appearance meta: '
print json.dumps(person_appear_maps, indent=4)

video_capture.release()
cv2.destroyAllWindows()
end = datetime.datetime.now()
print end - started
