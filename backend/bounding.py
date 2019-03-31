# import sys
# sys.path.append("numpy_path")
import numpy as np
import matplotlib as mpl

# mpl.use('TkAgg')  # Mac
import matplotlib.pyplot as plt

# sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2


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
    x, y = v[0]
    h, w = abs(y - v[1][1]), abs(x - v[1][0])
    img = cv2.imread(img)
    crop_img = img[y:y + h, x:x + w].copy()
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)
    return crop_img
