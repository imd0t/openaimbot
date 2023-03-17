import numpy as np
import cv2
import pyautogui
from queue import PriorityQueue
import keyboard
import tkinter as tk
from threading import Thread

class AimAssist:
    def __init__(self):
        self.interpolation_fps = "unlimited"
        self.confidence_threshold = 0.5
        self.strength = 1.0
        self.aiming_down_sights = False
        self.hipfire = True
        self.function_key_1 = False
        self.function_key_2 = False
        self.is_running = True

    def run(self):
        # Initialize the NVIDIA 20 series graphics card
        graphics_card = cv2.VideoCapture(0)

        while self.is_running:
            # Check function key status
            self.function_key_1 = keyboard.is_pressed('f1')
            self.function_key_2 = keyboard.is_pressed('f2')

            if self.function_key_1:
                self.aiming_down_sights = not self.aiming_down_sights
                self.hipfire = not self.hipfire

            # Capture the image from the graphics card
            ret, frame = graphics_card.read()
            if not ret:
                print("Error capturing video frame.")
                break

            # Convert the image to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Load the Fortnite character template
            fortnite_template = cv2.imread('fortnite_character.jpg', 0)

            # Match the template with the image
            result = cv2.matchTemplate(gray, fortnite_template, cv2.TM_CCOEFF_NORMED)

            # Get the confidence strength
            confidence_strength = np.amax(result)

            if confidence_strength >= self.confidence_threshold and self.function_key_2:
                # Get the coordinates of the characters
                loc = np.where(result >= confidence_strength)

                # Store characters in a priority queue based on distance
                characters = PriorityQueue()
                for pt in zip(*loc[::-1]):
                    # Get the distance of the character
                    distance = np.sqrt((pt[0] - frame.shape[1] / 2) ** 2 + (pt[1] - frame.shape[0] / 2) ** 2)
                    characters.put((distance, pt))

                # Get the second furthest character
                if characters.qsize() >= 2:
                    characters.get()
                    second_furthest = characters.get()[1]

                    # Adjust the interpolation fps
                    if self.interpolation_fps != "unlimited":
                        self.interpolation_fps = distance / 100

                    # Move the mouse to the character
                    if self.aiming_down_sights:
                        pyautogui.moveTo(second_furthest[0], second_furthest[1], self.interpolation_fps, _pause=False)
                    elif self.hipfire:
                        pyautogui.moveRel(second_furthest[0] * self.strength, second_furthest[1] * self.strength, _pause=False)

        graphics_card.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.is_running = False

def main():
    aim_assist = AimAssist()

    # Create a basic GUI window
    root = tk.Tk()
    root.title("Fortnite Aim Assist")

    def update_labels():
        aiming_down_sights_label.config(text=f"Aiming Down Sights: {aim_assist.aiming_down_sights}")
        hipfire_label.config(text=f"Hipfire: {aim_assist.hipfire}")

    def toggle_aiming_mode():
        aim_assist.aiming_down_sights = not aim_assist.aiming_down_sights
        aim_assist.hipfire = not aim_assist.hipfire
        update_labels()

    tk.Label(root, text="Fortnite Aim Assist", font=("Arial", 16, "bold")).pack(pady=10)
    
    aiming_down_sights_label = tk.Label(root, text="")
    aiming_down_sights_label.pack(pady=5)
    hipfire_label = tk.Label(root, text="")
    hipfire_label.pack(pady=5)

    toggle_aiming_mode_button = tk.Button(root, text="Toggle Aiming Mode (F1)", command=toggle_aiming_mode)
    toggle_aiming_mode_button.pack(pady=5)

    tk.Label(root, text="Press F2 to toggle Aim Assist On/Off", font=("Arial", 10)).pack(pady=10)

    # Add a button to close the application
    close_button = tk.Button(root, text="Close", command=root.quit)
    close_button.pack(pady=10)

    update_labels()

    # Start the AimAssist thread
    aim_assist_thread = Thread(target=aim_assist.run)
    aim_assist_thread.start()

    # Start the GUI main loop
    root.protocol("WM_DELETE_WINDOW", aim_assist.stop)
    root.mainloop()

    # Wait for the AimAssist thread to exit
    aim_assist_thread.join()

    if __name__ == "__main__":
    
        main()
