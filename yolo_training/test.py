import os
import cv2
from ultralytics import YOLO

def main():
    # Load Custom-Trained Model 
    model_path = os.path.join('training_runs', 'first_run', 'weights', 'best.pt')
    
    # Check if the model file exists
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return

    print(f"Loading custom model from: {model_path}")
    model = YOLO(model_path)

    # Set Test Image Path 
    image_name = '00005_00014_00005_png.rf.0e24dd3583d580dadb9d69e73a08e78c.jpg' 
    
    test_image_path = os.path.join('..', 'datasets', 'traffic-signs', 'test', 'images', image_name)

    # Check if the test image exists
    if not os.path.exists(test_image_path):
        print(f"Error: Test image not found at {test_image_path}")
        print(f"Please make sure '{image_name}' is a real file in that folder.")
        return

    print(f"Running inference on: {test_image_path}...")
    
    # Run Inference 
    results = model(test_image_path, conf=0.1)

    # Show the Results
    annotated_image = results[0].plot()

    print("Displaying results. Press any key in the new window to exit.")
    
    # Using OpenCV to display the image
    cv2.imshow("YOLOv8 Test Results", annotated_image)
    cv2.waitKey(0)  # Wait for a key to be pressed
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

#py -m venv venv
#source venv/Scripts/activate