mjpg_streamer -i "input_uvc.so -d /dev/video0 -y -n -r 640x480 -f 15" -o "output_http.so -p 8000 -w /www/webcam" &
