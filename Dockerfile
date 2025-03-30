FROM python:3.10

# FFmpeg इंस्टॉल करो
RUN apt update && apt install -y ffmpeg

# वर्किंग डायरेक्ट्री सेट करो
WORKDIR /app

# बॉट की सभी फाइल्स कॉपी करो
COPY . .

# डिपेंडेंसी इंस्टॉल करो
RUN pip install --no-cache-dir -r requirements.txt

# स्टार्ट.sh को एक्सीक्यूटेबल बनाओ
RUN chmod +x start.sh

# बॉट रन करो
CMD ["bash", "start.sh"]
