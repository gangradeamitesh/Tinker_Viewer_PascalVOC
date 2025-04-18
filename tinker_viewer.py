import os
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET

get_unknown = True
t1_classes_set = set([
    "aeroplane", "bicycle", "bird", "boat", "bus", "car",
    "cat", "cow", "dog", "horse", "motorbike", "sheep", "train",
    "elephant", "bear", "zebra", "giraffe", "truck", "person"
])

# --- Your annotation parsing function here ---
def parse_voc_annotation(xml_path, image_path,image_id):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        image = cv2.imread(image_path)
        height, width = image.shape[:2]

        instances = []
        for obj in root.findall("object"):
            label = obj.find("name").text
            bbox_xml = obj.find("bndbox")
            xmin = float(bbox_xml.find("xmin").text)
            ymin = float(bbox_xml.find("ymin").text)
            xmax = float(bbox_xml.find("xmax").text)
            ymax = float(bbox_xml.find("ymax").text)

            x = int(xmin)
            y = int(ymin)
            w = int(xmax - xmin)
            h = int(ymax - ymin)
            if get_unknown:
                instances.append({
                    "label": label if label in t1_classes_set else "unknown",
                    "bbox": [x, y, w, h]
                })
            else:
                instances.append({
                    "label": label,
                    "bbox": [x, y, w, h]
                })
    except:
        print("File not found :{xml_path}")
        return []
    if len(instances) > 2:
        print(instances)
        return instances
    return []

# --- GUI Class ---
class VOCViewer:
    def __init__(self, master, voc_base , grid_size):
        self.master = master
        self.voc_base = voc_base
        self.grid_size = grid_size  # Number of rows and columns in the grid
        self.num_images = grid_size[0] * grid_size[1]


        # Load image IDs
        val_file = os.path.join("") #set your path for image ids
        with open(val_file, "r") as f:
            self.image_ids = [line.strip() for line in f.readlines()]
        print(self.image_ids)
        self.index = 0

        # Setup canvas
        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack()
        self.canvas_labels = []
        for i in range(self.grid_size[0]):
            row = []
            for j in range(self.grid_size[1]):
                label = tk.Label(self.canvas_frame)
                label.grid(row=i, column=j, padx=5, pady=5)
                row.append(label)
            self.canvas_labels.append(row)

        # Control buttons
        btn_frame = tk.Frame(master)
        btn_frame.pack()

        tk.Button(btn_frame, text="<< Prev", command=self.prev_image).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Next >>", command=self.next_image).pack(side=tk.LEFT)

        self.load_image()

    def load_image(self):
        for i in range(self.num_images):
            idx = (self.index + i) % len(self.image_ids)
            image_id = self.image_ids[idx]
            print(image_id)
            xml_path = os.path.join(self.voc_base, "Annotations", f"{image_id}.xml")
            img_path = os.path.join(self.voc_base, "JPEGImages", f"{image_id}.jpg")
        
            instances = parse_voc_annotation(xml_path, img_path,image_id)
            if len(instances)==0:
                print("No instances found in the image. For Image Id : ",image_id)
                return
            image = cv2.imread(img_path)

        # Draw bounding boxes
            for inst in instances:
                x, y, w, h = inst["bbox"]
                label = inst["label"]
                if label=="unknown":
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                else:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            cv2.putText(image, f"Image ID: {image_id}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Convert image to displayable format
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = image.resize((600, 400))
            photo = ImageTk.PhotoImage(image)

            row, col = divmod(i, self.grid_size[1])
            self.canvas_labels[row][col].configure(image=photo)
            self.canvas_labels[row][col].image = photo  # Save a reference!

    def next_image(self):
        self.index = (self.index + 4) % len(self.image_ids)
        self.load_image()

    def prev_image(self):
        self.index = (self.index - 4) % len(self.image_ids)
        self.load_image()

# --- Run it ---
if __name__ == "__main__":
    print("Running the tinker viewer...")
    voc_base = ""  # <- set your path for annotations
    root = tk.Tk()
    root.title("Pascal VOC Viewer")
    app = VOCViewer(root, voc_base , grid_size=(2,2))
    root.mainloop()