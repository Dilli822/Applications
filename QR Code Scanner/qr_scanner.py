import cv2
import time

def scan_qr_code():
    try:
        # Initialize the QRCode detector
        detector = cv2.QRCodeDetector()

        # Start video capture from the default camera
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise Exception("Could not access the camera. Please check if it is connected and available.")

        print("Waiting for QR code... (Press 'q' to quit)")

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Failed to grab frame from the camera. Retrying...")
                continue  # Skip this frame and try again

            # Detect and decode the QR code
            data, bbox, _ = detector.detectAndDecode(frame)

            # If a QR code is detected and data is found
            if bbox is not None and data:
                # Convert bbox points to proper format for cv2.line()
                bbox = bbox.astype(int)  # Ensure that bbox is an integer type
                bbox = bbox[0]  # bbox is nested in a list, we need the first level of data

                # Draw the bounding box around the QR code
                for i in range(len(bbox)):
                    cv2.line(frame, tuple(bbox[i]), tuple(bbox[(i + 1) % len(bbox)]), color=(0, 255, 0), thickness=2)

                # Display the decoded data near the QR code bounding box
                cv2.putText(frame, data, (bbox[0][0], bbox[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                # Display the frame with the bounding box and data
                cv2.imshow("QR Code Scanner", frame)

                print(f"QR Code detected: {data}")

                # Stay idle and show the QR code data for 6 seconds
                start_time = time.time()
                while time.time() - start_time < 6:
                    # Continue showing the frame without updating the capture
                    cv2.imshow("QR Code Scanner", frame)

                    # Check if 'q' is pressed during the idle period
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("Exiting QR code scanner.")
                        return

                print("Resuming scanning...")

            # Display the frame in idle mode while no QR code is detected
            cv2.imshow("QR Code Scanner", frame)

            # Press 'q' to quit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting QR code scanner.")
                break

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Always release the camera and close windows properly
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_qr_code()
