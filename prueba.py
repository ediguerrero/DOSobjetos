import cv2
import time
anchocam, altocam = 1280, 720
cuadro = 200

mitad = int(anchocam / 2)

cap = cv2.VideoCapture(0)
cap.set(3, anchocam)
cap.set(4, altocam)


def algoritmo():
    cant = 0
    test = 0
    timeout = 5000000000000
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        ret, frame = cap.read()
        cv2.putText(frame, "ubique el obj 1", (cuadro - 20, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 0, 0), 2)
        cv2.rectangle(frame, (cuadro, cuadro), (mitad - cuadro, altocam - cuadro), (0, 0, 0), 2)
        ox1, oy1 = cuadro, cuadro
        ancho1, alto1 = (mitad - cuadro) - ox1, (altocam - cuadro) - oy1
        ox2, oy2 = ox1 + ancho1, oy1 + alto1
        obj_gris = cv2.cvtColor(frame[oy1:oy2, ox1:ox2], cv2.COLOR_BGR2GRAY)

        cv2.putText(frame, "ubique el obj 2", ((mitad + 180), 180), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 0, 0), 2)
        cv2.rectangle(frame, ((mitad + cuadro), cuadro), (anchocam - cuadro, altocam - cuadro), (0, 0, 0), 2)
        ox3, oy3 = (mitad + cuadro), cuadro
        ancho2, alto2 = (anchocam - cuadro) - ox3, (altocam - cuadro) - oy3
        ox4, oy4 = ox3 + ancho2, oy3 + alto2
        objeto2 = frame[oy3:oy4, ox3:ox4]
        obj_gris2 = cv2.cvtColor(objeto2, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create()

        pc1, des1 = orb.detectAndCompute(obj_gris, None)
        pc2, des2 = orb.detectAndCompute(obj_gris2, None)
        # print(pc1, des2)
        fb = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        if des1 is not None and des2 is not None:
            coincidencias = fb.match(des2, des1)
            coincidencias = sorted(coincidencias, key=lambda x: x.distance)
        else:
            continue

        puntos = []
        for c in coincidencias:
            if int(c.distance) <= 57:
                puntos.append(c)
                # print(len(puntos))
        if len(puntos) > 35:
            cant += 1
            print(cant)
            cv2.putText(frame, "objetos similares", ((mitad - 150), 580), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
#            roi = img[oy3:oy4, ox3:ox4]
        elif len(puntos) <= 34 and len(puntos) > 1:
            cv2.putText(frame, "objetos distintos", ((mitad - 150), 580), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        elif len(puntos) == 0:
            cv2.putText(frame, "ubicar los objetos", ((mitad - 150), 580), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

        cv2.imshow("comparador", frame)
        k = cv2.waitKey(1)
        if k == 27:
            break


# cap.release()
cv2.destroyAllWindows()
