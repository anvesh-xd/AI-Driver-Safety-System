import os
from ultralytics import YOLO
#not working fully currently will look into it further
def main():
    # Load Custom-Trained Model
    
    model_path = os.path.join('training_runs', 'first_run', 'weights', 'best.pt')

    # Check if the model file exists
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        print("Please make sure your 'first_run' folder exists.")
        return
    print(f"Loading custom model from: {model_path}")
    model = YOLO(model_path)
    model.export(format='saved_model')
    print(f"'best.tflite' is now saved in:")
    print(f"{os.path.join(os.getcwd(), model_path.replace('best.pt', ''))}")

if __name__ == '__main__':
    main()