import cv2
import easyocr
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# Function to handle the 'Upload Image' option
def upload_image_option():
    # Create a GUI window to select an image file
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select an image file
    image_path = filedialog.askopenfilename()

    # Check if the user canceled the file dialog
    if not image_path:
        print("No image selected. Exiting.")
    else:
        # Read the selected image
        img = cv2.imread(image_path)

        # Instance text detector
        reader = easyocr.Reader(['en'], gpu=False)

        # Detect text on the image
        text_ = reader.readtext(img)

        threshold = 0.25

        # Create a text file to write the detected text
        with open("detected_text.txt", "w") as text_file:
            for t_, t in enumerate(text_):
                bbox, text, score = t

                if score > threshold:
                    cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
                    cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

                    # Write the detected text to the text file
                    text_file.write(f"Text: {text}\n")

        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()

    print("Detected text has been written to 'detected_text.txt'.")

# Function to handle the 'Live Feed' option
def live_feed_option():
    # Create a GUI window to select an image file
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Initialize the video capture object (0 is typically the default camera)
    camera = cv2.VideoCapture(0)

    # Instance text detector
    reader = easyocr.Reader(['en'], gpu=False)

    detected_text = ""  # Initialize a variable to store detected text

    while True:
        # Read a frame from the camera
        ret, frame = camera.read()

        if not ret:
            print("Failed to capture a frame.")
            break

        # Detect text on the frame
        text_ = reader.readtext(frame)

        threshold = 0.25

        # Draw bounding boxes and text
        for t_, t in enumerate(text_):
            bbox, text, score = t

            if score > threshold:
                pt1 = tuple(map(int, bbox[0]))
                pt2 = tuple(map(int, bbox[2]))
                cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 5)
                cv2.putText(frame, text, pt1, cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

                # Append detected text to the variable
                detected_text += text + "\n"

        cv2.imshow('Text Detection', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    # Release the video capture object and close the OpenCV windows
    camera.release()
    cv2.destroyAllWindows()

    # Write the detected text to a file when 'q' is pressed
    if detected_text:
        with open("detected_text.txt", "w") as text_file:
            text_file.write(detected_text)

    print("Detected text has been written to 'detected_text.txt'.")

def main():
    # Create a GUI for the user to choose an option
    root = tk.Tk()
    root.title("Text Detection Options")

    label = tk.Label(root, text="Choose an option:")
    label.pack()

    button_upload = tk.Button(root, text="Upload Image", command=upload_image_option)
    button_upload.pack()

    button_live_feed = tk.Button(root, text="Live Feed", command=live_feed_option)
    button_live_feed.pack()

    root.mainloop()

if __name__ == "__main__":
    main()