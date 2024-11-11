import gradio as gr
import pandas as pd
import os
from ultralytics import YOLO
from PIL import Image, ImageDraw

# Load a pre-trained YOLO model (ensure the path is correct)
model = YOLO("models/mugie-grevys-plains-other-model-version-6.pt")  # Using YOLOv8 small pre-trained model

# Classes according to the YOLO model
categories = model.names

# Function to draw bounding boxes on the image
def draw_boxes(image, boxes, scores, classes, selected_classes):
    draw = ImageDraw.Draw(image)
    for box, score, cls in zip(boxes, scores, classes):
        class_name = categories[int(cls)]
        # If selected_classes is empty, include all classes
        if not selected_classes or class_name in selected_classes:
            # Draw bounding box
            draw.rectangle(((box[0], box[1]), (box[2], box[3])), outline="white", width=2)
            # Add label
            label = f"{class_name} ({score:.2f})"
            draw.text((box[0], box[1] - 10), label, fill="white")
    return image

# Function to generate report information
def generate_report(detections, total_images):
    # Convert the list of detections into a DataFrame
    df = pd.DataFrame(detections)

    # Calculate point count (number of objects per class)
    class_counts = df.groupby('class').size().reset_index(name='point_count')

    # Calculate max and min population (max/min objects per class in a single image)
    population_stats = df.groupby('class').agg(
        max_population=('image', 'size'),
        min_population=('image', 'size')
    ).reset_index()

    # Calculate the relative abundance (percentage of total detections)
    total_objects = len(df)
    class_counts['relative_abundance'] = (class_counts['point_count'] / total_objects) * 100

    # Merge point counts and population stats
    report_df = pd.merge(class_counts, population_stats, on='class')

    # Calculate images filtered (number of images where each class appears)
    image_count_per_class = df.groupby('class')['image'].nunique().reset_index(name='images_filtered')

    # Merge this data into the report
    report_df = pd.merge(report_df, image_count_per_class, on='class')

    return report_df

# Function to run YOLO detection and filter classes
def detect_objects_in_files(files, selected_classes):
    results_list = []
    images_with_boxes = []
    
    for file in files:
        img = Image.open(file.name)

        # Run YOLO detection
        results = model(img)

        # Parse the results
        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy()  # Bounding boxes
            scores = r.boxes.conf.cpu().numpy()  # Confidence scores
            classes = r.boxes.cls.cpu().numpy()  # Class labels

            # Draw bounding boxes on the image
            img_with_boxes = img.copy()
            img_with_boxes = draw_boxes(img_with_boxes, boxes, scores, classes, selected_classes)
            images_with_boxes.append(img_with_boxes)

            for box, score, cls in zip(boxes, scores, classes):
                class_name = categories[int(cls)]
                # Include detection based on selected_classes
                if not selected_classes or class_name in selected_classes:
                    results_list.append({
                        'image': os.path.basename(file.name),
                        'class': class_name,
                        'confidence': float(score),
                        'x_min': box[0],
                        'y_min': box[1],
                        'x_max': box[2],
                        'y_max': box[3]
                    })
    
    # Convert results into a dataframe
    df = pd.DataFrame(results_list)

    # Generate summary report
    report_df = generate_report(results_list, len(files))

    # Save the report dataframe to a CSV file
    csv_file = "detection_report.csv"
    report_df.to_csv(csv_file, index=False)

    return df, images_with_boxes, report_df, csv_file

# Gradio interface function
def process_files(files, selected_classes):
    # If no classes are selected, set selected_classes to None
    if not selected_classes:
        selected_classes = None
    # Process the uploaded files
    df, images_with_boxes, report_df, csv_file = detect_objects_in_files(files, selected_classes)
    return df, images_with_boxes, report_df, csv_file

# Create Gradio components
input_files = gr.File(
    file_count="multiple",
    label="Upload Images (Multiple Files Allowed)"
)

# CheckboxGroup for class selection with search and multi-select
class_selection = gr.CheckboxGroup(
    choices=list(categories.values()),
    label="Select Classes to Detect (Optional)",
    interactive=True
)

output_df = gr.Dataframe(
    label="Detection Results",
    headers=["image", "class", "confidence", "x_min", "y_min", "x_max", "y_max"]
)

output_images = gr.Gallery(
    label="Processed Images with Bounding Boxes",
    columns=2  # Adjust number of columns as needed
)

# Display the summary report on the screen
report_display = gr.Dataframe(
    label="Summary Report",
    headers=["class", "point_count", "max_population", "min_population", "relative_abundance", "images_filtered"]
)

# Add a downloadable CSV component for the summary report
output_csv = gr.File(label="Download Report as CSV")

# Launch Gradio interface
gr.Interface(
    fn=process_files,
    inputs=[input_files, class_selection],
    outputs=[output_df, output_images, report_display, output_csv],
    title="Animal Population Estimation on Camera Trap Images",
    allow_flagging="never").launch(share=True)# Adjust flagging settings as needed