# Caméra Raspberry (B) Rev02

## Récupération du flux vidéo

Dans un premier temps, le flux vidéo était récupéré avec la commande :

 ```python
cap = cv2.VideoCapture(0)
```
Mais utilisant cette commande, la latense de la caméra est équivalent à une seconde.

On va donc utiliser la bibliothèque picamera pour récupérer le flux vidéo de la caméra, cela nous permet de passer à une latense d'environ 0,5 seconde soit deux fois moins qu'avec openCV.

 ```python
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24

rawCapture = PiRGBArray(camera, size=(640, 480))
camera.capture(rawCapture, format="bgr")
frame = rawCapture.array
```
Un objet PiCamera est créer pour contrôler la caméra, définit la résolution de l'image capturée à 640x480 pixels et la fréquence d'acquisition à 24 images par seconde.

rawCapture = PiRGBArray(camera, size=(640, 480)) : Cette ligne crée un objet PiRGBArray qui permet de stocker une image brute (non compressée) provenant de la caméra. L'objet est initialisé avec une résolution de 640x480 pixels (résolution de la caméra Raspberry), mais vous pouvez spécifier une autre résolution selon vos besoins.

camera.capture(rawCapture, format="bgr") : Cette ligne capture l'image à partir de la caméra et la stocke dans l'objet PiRGBArray créé précédemment. Le paramètre format="bgr" spécifie que l'image doit être stockée dans l'ordre des couleurs bleu, vert, rouge (BGR), qui est le format standard utilisé par OpenCV.

frame = rawCapture.array : Cette ligne extrait l'image brute stockée dans l'objet PiRGBArray et la stocke dans un objet frame. L'objet frame est un tableau NumPy qui contient les valeurs de pixel de l'image. 

On peut maintenant utiliser l'objet frame pour traiter l'image à l'aide des fonctions OpenCV.

## Traitement de l'image
### Isolation des pixels de la couleur jaune
Ensuite un traitement d'image est effectué sur les données pour extraire certaines couleurs. Dans le cas de la fonction *func_detect_ball*, c'est la couleur jaune. 

 ```python
# Convert the frame to HSV color space
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Define a range of yellow colors in HSV
lower_yellow = (15, 80, 80)
upper_yellow = (40, 255, 255)

# Create a mask that only allows black colors to pass through
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# Apply the mask to the frame
res = cv2.bitwise_and(frame, frame, mask=mask)
```

Cette partie du code convertit l'image capturée en espace de couleur HSV, définit une plage de valeurs HSV pour la couleur jaune, crée un masque pour filtrer les pixels correspondant à cette plage de valeurs, puis applique le masque à l'image d'origine pour ne garder que les pixels jaunes.

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) : Cette ligne convertit l'image capturée, qui est initialement en espace de couleur BGR, en espace de couleur HSV. Le format HSV est plus adapté à la détection de couleurs car il sépare la luminosité, la saturation et la teinte de chaque pixel.

lower_yellow = (15, 80, 80) et upper_yellow = (40, 255, 255) : Ces deux lignes définissent une plage de valeurs HSV pour la couleur jaune. Les valeurs sont choisies pour détecter une large gamme de jaunes

mask = cv2.inRange(hsv, lower_yellow, upper_yellow) : Cette ligne crée un masque qui ne laisse passer que les pixels dont les valeurs HSV sont comprises dans la plage de valeurs définie pour la couleur jaune. Tous les autres pixels sont mis à 0.

res = cv2.bitwise_and(frame, frame, mask=mask) : Cette ligne applique le masque créé précédemment à l'image d'origine. Seuls les pixels correspondant à la couleur jaune passent à travers le masque et les autres pixels sont masqués en noir. L'objet res contient maintenant l'image d'origine filtrée, où seuls les pixels jaunes sont présents.

### Calcul du centre de la balle
 ```python
 # Detect contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours that are too small
    contours = [c for c in contours if cv2.contourArea(c) > 200]

    # Loop over the contours
    for contour in contours:
        # Get the moments of the contour
        moments = cv2.moments(contour)

        # Calculate the coordinates of the center of the contour
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])

        # Draw the center of the contour on the original frame
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
 ```

Ce code détecte les contours des objets jaunes dans l'image filtrée, élimine les contours trop petits, calcule le centre de chaque contour à l'aide des moments et affiche le centre de chaque contour sous forme d'un cercle rouge sur l'image d'origine.

contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) : Cette ligne détecte les contours des objets jaunes dans l'image filtrée. La fonction cv2.findContours prend en entrée le masque créé précédemment et renvoie une liste de contours. Le deuxième argument (_) correspond à la hiérarchie des contours, qui n'est pas utilisée ici. Le troisième argument (cv2.CHAIN_APPROX_SIMPLE) spécifie une méthode de compression des contours qui permet de stocker uniquement les points d'extrémité des segments de contour.

contours = [c for c in contours if cv2.contourArea(c) > 200] : Cette ligne filtre les contours pour ne garder que ceux dont la surface est supérieure à 200 pixels. Cela permet d'éliminer les petits contours qui peuvent être des bruits ou des artefacts.

for contour in contours: : Cette boucle parcourt la liste des contours restants.

moments = cv2.moments(contour) : Cette ligne calcule les moments d'ordre 0, 1 et 2 du contour. Les moments sont des caractéristiques statistiques de la distribution de pixels dans le contour.

cx = int(moments["m10"] / moments["m00"]) et cy = int(moments["m01"] / moments["m00"]) : Ces deux lignes calculent les coordonnées du centre du contour en utilisant les moments d'ordre 0, 1 et 2. Le centre est déterminé par la moyenne des coordonnées x et y des pixels dans le contour.

cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1) : Cette ligne dessine un cercle rouge de rayon 5 pixels à l'emplacement du centre du contour sur l'image d'origine. La fonction cv2.circle prend en entrée l'image d'origine, les coordonnées du centre, le rayon du cercle, la couleur (ici, rouge) et l'épaisseur du contour (-1 signifie que le cercle est rempli).

Grâce à cette fonction, on peut maintenant récupérer les coordonnées du centre de la balle.

## Détection du centre du plateau

Dans le cas de la fonction *detect_center* c'est les coordonnées du centre de la planche sauf que dans ce cas là c'est les pixels de la couleur blanche qui sont extrait de du flux vidéo capturé.