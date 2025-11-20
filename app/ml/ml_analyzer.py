from ultralytics import YOLO
import cv2
import numpy as np

class SmartImageAnalyzer:
    def __init__(self):
        self.yolo = YOLO('yolov8n.pt')  # Загружается один раз
        self.categories_map = {
            'person': 'clothes',
            'backpack': 'accessories',
            'sofa': 'furniture',
            'cell phone': 'electronics',
        }
    
    def analyze_image(self, image_path):
        # YOLO обнаружение
        results = self.yolo.predict(image_path)
        
        # Получаем обнаруженные объекты
        detected_classes = results[0].names
        
        # Определяем категорию
        category = self._get_category(detected_classes)
        
        # OpenCV анализ качества
        img = cv2.imread(image_path)
        condition = self._estimate_condition(img)
        
        return {
            "category": category,
            "condition": condition,
            "objects_detected": len(results[0].boxes)
        }
    
    def _get_category(self, classes):
        for cls in classes:
            if cls in self.categories_map:
                return self.categories_map[cls]
        return "other"
    
    def _estimate_condition(self, img):
        # Анализ контраста и резкости
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var()
        
        if sharpness > 500:
            return "excellent"
        elif sharpness > 300:
            return "good"
        else:
            return "fair"