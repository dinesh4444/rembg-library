import cv2
import numpy as np
import rembg

def draw_outline(image, points):
    for i in range(len(points)-1):
        if len(points[i][0]) == 2 and len(points[i+1][0]) == 2:
            pt1 = tuple(points[i][0])
            pt2 = tuple(points[i+1][0])
            cv2.line(image, pt1, pt2, (0, 255, 0), 2)

def resize_image(image, width):
    aspect_ratio = width / image.shape[1]
    height = int(image.shape[0] * aspect_ratio)
    return cv2.resize(image, (width, height))

def main():
    input_image_path = "1.jpg"  # input image 
    display_width = 800  # display width 

    while True:
        # Read the input image
        image = cv2.imread(input_image_path)
        if image is None:
            print("Could not read the image.")
            break

        # Resize the image
        image = resize_image(image, display_width)

        # Display the image
        cv2.imshow("Image", image)

        # draw a rectangle over the object
        rect = cv2.selectROI("Image", image)
        if rect == (0, 0, 0, 0):
            print("ROI selection canceled.")
            continue
        x, y, w, h = rect

        # Crop the selected Region Of Interest (ROI)
        roi = image[y:y+h, x:x+w]

        # Convert ROI to RGBA format for rembg library
        rgba = cv2.cvtColor(roi, cv2.COLOR_BGR2RGBA)

        # rembg library to remove the background
        result = np.array(rembg.remove(rgba), dtype=np.uint8)

        # Convert the result back to BGR format
        result = cv2.cvtColor(result, cv2.COLOR_RGBA2BGR)

        # Find contours (outline points) in the result
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if at least one contour exists
        if len(contours) > 0:
            # Get the largest contour
            largest_contour = max(contours, key=cv2.contourArea)

            # Draw an outline over the ROI image
            cv2.drawContours(roi, [largest_contour], 0, (0, 255, 0), 2)

        # Overlay the object outline in the original image
        image[y:y+h, x:x+w] = roi

        # Show the output image
        cv2.imshow("Output", image)

        # Wait for user input
        key = cv2.waitKey(0) & 0xFF

        # Check if user wants to clear the outline
        if key == ord("c"):
            continue

        # Check if user wants to quit
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
