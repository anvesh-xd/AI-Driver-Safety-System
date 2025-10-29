import os
from ultralytics import YOLO

def main():
    
    # We use 'yolov8n.pt' 
    # This is the smallest, fastest model for prototype testing and easy to transfer to Pi
    print("Loading pre-trained YOLOv8n model...")
    model = YOLO('yolov8n.pt')

    # 'data' points to the .yaml file 
    # 'epochs' is how many times to train on the full dataset, we did 10 but 50-100 is preferred
    # 'imgsz' is the image size. 640 is a good default.
    data_yaml_path = os.path.join(os.path.dirname(__file__), 'data.yaml')
    
    print(f"Starting training with data from: {data_yaml_path}")
    
    # start training
    results = model.train(
        data=data_yaml_path,
        epochs=10,
        imgsz=640,
        project='training_runs',  # Creates a 'training_runs' folder for results
        name='first_run'          # Creates a subfolder 'first_run'
    )

# trained model is saved in training_runs/first_run/weights/best.pt
# trained model is best.pt

print(f"Training Completed")

if __name__ == '__main__':
    main()