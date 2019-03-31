import io
import os
import cv2
import numpy as np

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

#route =  bananaIMG.jpg
#route = '/home/rchikka/gcloud/visionex/a-Ripening-Stages-of-Banana-Fruit-1-7-Completely-unripe-to-completely-ripen.png'
#route = '/home/rchikka/gcloud/visionex/190683-131-E796F1EE.jpg'

def buffer(x, y):
    if (x + 50 > y) or (x - 50 < y):
        return True

def colorAnalyze(arc):
    # arc = np.load(route)
    valid_count = []
    blu_conch = 0
    red_conch = 0
    gre_conch = 0
    whitespace = 0
    black = 0
    yellow_conch = 0
    reference = int(arc.shape[1] / 2)

    for n in range(0, arc.shape[0]):
        for m in range(0, arc.shape[1]):
            for q in range(0, 3):
                if (arc[n][m][q] != arc[0][reference][q]):
                    valid_count.append(arc[n][m])
    #print("valid pixels: " + str(len(valid_count)))
    for n in valid_count:
        if n[0] > 230 and n[1] > 230 and n[2] > 220:
            whitespace = whitespace + 1
        if n[0] < 120 and n[1] < 120 and n[2] < 120:
            black = black + 1
        elif n[1] > n[2] and n[1] > n[0]:
            gre_conch = gre_conch + 1
        elif buffer(n[0], n[1]) == True:
            yellow_conch = yellow_conch + 1
        elif n[2] > n[1] and n[2] > n[0]:
            blu_conch = blu_conch + 1
        if n[0] > n[1] + 50 and n[0] > n[2]:
            red_conch = red_conch + 1

    comp = len(valid_count) - whitespace

    if (gre_conch / comp) > yellow_conch / comp:
        return 0  # print("unripe")
    elif (black / comp) > (0.5 * yellow_conch / comp):
        return 2  # print("overripe")
    elif (red_conch / comp) + 0.1 > (0.5 * yellow_conch / comp):
        return 1  # print("soon to expire: eat soon")
    else:
        return 1  # print("store ready")

def markBackground(filename):
    # == Parameters =======================================================================
    # BLUR = 21
    CANNY_THRESH_1 = 0
    CANNY_THRESH_2 = 170
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (0.0, 0.0, 1.0)  # In BGR format

    # == Processing =======================================================================

    # -- Read image -----------------------------------------------------------------------
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    orig = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # np.save("bananaORIG", orig)

    # -- Edge detection -------------------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    # -- Find contours in edges, sort by area ---------------------------------------------
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    # -- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    # -- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    # mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)  # we're not blurring
    mask_stack = np.dstack([mask] * 3)  # Create 3-channel alpha mask

    # -- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack = mask_stack.astype('float32') / 255.0  # Use float matrices,
    img = img.astype('float32') / 255.0  # for easy blending

    masked = (mask_stack * img) + ((1 - mask_stack) * MASK_COLOR)  # Blend
    masked = (masked * 255).astype('uint8')  # Convert back to 8-bit

    masked = cv2.cvtColor(masked, cv2.COLOR_BGR2RGB)
    np.save("bananaMASKED14", masked)
    mpl.image.imsave('bananaMASKED14.jpg', masked)
    plt.imshow(masked)
    plt.show()

    # cv2.imwrite('C:/Temp/person-masked.jpg', masked)           # Save

    return masked


# markBackground('banana1.jpg')
# markBackground('banana2.jpg')
# markBackground('banana4.jpg')
# markBackground('banana5.jpg')
# markBackground('banana6.jpg')
# markBackground('banana7.jpg')
# markBackground('banana8.jpg')
# markBackground('banana9.jpg')
# markBackground('banana10.jpg')
# markBackground('banana11.jpg')
# markBackground('banana12.jpg')
# markBackground('banana13.png')
# markBackground('banana14.png')


def cropBox(img, v):
    # img is the full image
    # v is a list of vertices, [[x,y], [x,y]]
    x, y = v[0][0]+2, v[0][1]+2
    h, w = abs(y - v[1][1] - 2), abs(x - v[1][0] - 2)
    
    #x, y = v[0]
    #h, w = abs(y-v[1][1]), abs(x - v[1][0])
    img = cv2.imread(img)
    crop_img = img[y:y + h, x:x + w].copy()
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)
    return crop_img


def label_check(path):
	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	# The name of the image file to annotate
	file_name = os.path.join(
    		os.path.dirname(__file__),
    		'resources/wakeupcat.jpg')

	# Loads the image into memory
	with open(path, 'rb') as image_file:
    		content = image_file.read()

	image = vision.types.Image(content=content)

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations

	for label in labels:
		if(label.description == "Banana"):
			return True
	return False

def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    coords = []
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    #print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        if(object_.name == "Banana" or object_.name == "Food" or object_.name == "Fruit"):
        	for vertex in object_.bounding_poly.normalized_vertices:
            		coords.append([int(vertex.x * img.shape[1]), int(vertex.y * img.shape[0])])
    return coords

def main(route):
	if(not label_check(route)): 
		return 3
		# no  banana was found
		#print("oh no")
		#error message

	imagelist = []
	vertices = localize_objects(route)
	#for i in range(len(vertices)):
	#	print("x-vertex: " + str(vertices[i][0]))
	#	print("y-vertex: " + str(vertices[i][1]))
	for i in range(len(vertices)-2):
		imagelist.append(cropBox(route, [vertices[i], vertices[i+2]]))

	tally = [0, 0, 0]

	for img in imagelist:
		tally[colorAnalyze(img)] += 1

	spot = tally.index(max(tally))
	#print(tally)
	#print(spot)
	#return spot

# main(route) # make sure route is established!
