import face_recognition
huge_image = face_recognition.load_image_file("huge1.jpeg")
huhuo_image = face_recognition.load_image_file("huhuo.jpeg")
# unknown_image = face_recognition.load_image_file("unknown.jpg");

huge_encoding = face_recognition.face_encodings(huge_image)[0]
hu_encoding = face_recognition.face_encodings(huhuo_image)[0]
huo_encoding = face_recognition.face_encodings(huhuo_image)[1]
# unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([hu_encoding, huo_encoding], huge_encoding )
labels = ['huge', 'huojianhua']

print('results:'+str(results))

for i in range(0, len(results)):
    if results[i] == True:
        print('The person is:'+labels[i])