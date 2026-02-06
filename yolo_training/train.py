import os
from ultralytics import YOLO

def main():
    
    # I am currently using 'yolov8n.pt' instead of YOLOv11 to get a light pt file 
    print("Loading pre-trained YOLOv8n model...")
    model = YOLO('yolov8n.pt')

    # 'data' points to the .yaml file 
    # 'epochs' is how many times to train on the full dataset, we did 10 but 50-100 is preferred and we will go to 50
    # 'imgsz' is the image size. 640 is a good default that we are currently using 
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