import cv2
import time

import mysql.connector as mysql
from pyzbar import pyzbar

connection = mysql.connect(host="localhost",
                     user="root",
                     passwd="",
                     db="inventory")
def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    barcode_text = ""
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_text = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, barcode_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    return frame, barcode_text

def main(headless=False):
    barcode_text =""
    capture_duration = 30
    camera=None
    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("❌ Could not open camera.")
            return ""
        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not headless:
            print("📝 Instructions: Point camera at barcode or press ESC to exit")
        else:
            print("📝 Running in headless mode - scanning for barcode...")
    
    
        start_time = time.time()
        while True:

            ret, frame = camera.read()
            if not ret:
                print("❌ Failed to read from camera.")
                break
            frame, current_barcode = read_barcodes(frame)
            if current_barcode:
                barcode_text = current_barcode
                print(f"✅ Barcode detected: {barcode_text}")
            if headless:
                cv2.namedWindow("Barcode reader", cv2.WINDOW_NORMAL)
                cv2.moveWindow("Barcode reader", 300, 200)
                cv2.imshow('Barcode reader', frame)
                key = cv2.waitKey(1) & 0xFF
            else:
                key = -1  # No key input in headless mode
                time.sleep(0.1)
            if barcode_text:
                print("✅ Barcode read complete.")
                time.sleep(1)
                break
            if not headless and key == 27:
                print("🚫 ESC pressed, exiting scan.")
                break


            # if len(barcode_text) > 0:
            #     break

            if time.time() - start_time > capture_duration:
                print("⏱️ Scan timed out after 30 seconds.")
                break
    except Exception as e:
        print(f"❌ Camera/OpenCV error: {str(e)}")
        # Return empty string on error
        barcode_text = ""
        
    finally:
        # Always cleanup
        if camera is not None:
            camera.release()
        if not headless:
            cv2.destroyAllWindows()
        time.sleep(0.5)
    
    print(f"📦 Returning from scanner with: '{barcode_text}'")
    return barcode_text.strip() if barcode_text else ""



if __name__ == '__main__':
    scanned = main(headless=False)
    if scanned:
        print("✅ Final scanned barcode:", scanned)
    else:
        print("⚠️ No barcode detected.")