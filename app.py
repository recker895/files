











   
















   
   
    QS
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

# Standard MoviePy 1.0.3 imports
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip
)


class SimpleVideoAudioEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Video & Image Audio Overlay Editor")
        self.resize(900, 650)

        self.media_file = None
        self.media_type = None  # 'video' or 'image'
        self.audio_file = None

        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #181818;
                color: #FFFFFF;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2D2D2D;
                border: 1px solid #444;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3A3A3A;
            }
            QSpinBox {
                background-color: #2B2B2B;
                padding: 4px;
                border: 1px solid #444;
                border-radius: 4px;
                color: #00FF99;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #444;
            }
            QSlider::handle:horizontal {
                background: #00FF99;
                width: 14px;
                border-radius: 7px;
            }
        """)

        layout = QVBoxLayout(self)

        # Media Preview Area
        self.video_widget = QVideoWidget()
        self.image_label = QLabel("Select Video or Image to Start")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #000; font-size: 18px; border-radius: 6px;")

        layout.addWidget(self.video_widget)
        layout.addWidget(self.image_label)
        self.video_widget.hide()

        # Status Display
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #00FF99; font-size: 15px; font-weight: bold;")
        layout.addWidget(self.status_label)

        # Video Progress Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        layout.addWidget(self.slider)

        # Section 1: Media Load Controls
        media_btn_layout = QHBoxLayout()
        load_vid_btn = QPushButton("📷 / 🎥 Load Video or Image")
        load_vid_btn.clicked.connect(self.load_media)
        media_btn_layout.addWidget(load_vid_btn)

        # Image Duration SpinBox (Only used when an image is loaded)
        self.img_duration_label = QLabel("Image Duration:")
        self.img_duration_spin = QSpinBox()
        self.img_duration_spin.setRange(1, 3600)
        self.img_duration_spin.setValue(10)
        self.img_duration_spin.setSuffix(" sec")

        media_btn_layout.addWidget(self.img_duration_label)
        media_btn_layout.addWidget(self.img_duration_spin)
        self.img_duration_label.hide()
        self.img_duration_spin.hide()

        layout.addLayout(media_btn_layout)

        # Section 2: Audio File Controls
        audio_layout = QHBoxLayout()
        load_audio_btn = QPushButton("🎵 Load Background Music")
        load_audio_btn.clicked.connect(self.load_audio)

        self.audio_status_label = QLabel("No Audio Loaded")
        self.audio_status_label.setStyleSheet("color: #AAA;")

        audio_layout.addWidget(load_audio_btn)
        audio_layout.addWidget(self.audio_status_label)
        layout.addLayout(audio_layout)

        # Section 3: Playback Preview Controls
        preview_layout = QHBoxLayout()
        play_btn = QPushButton("Play Preview")
        pause_btn = QPushButton("Pause Preview")
        play_btn.clicked.connect(self.play_preview)
        pause_btn.clicked.connect(self.pause_preview)

        preview_layout.addWidget(play_btn)
        preview_layout.addWidget(pause_btn)
        layout.addLayout(preview_layout)

        # Section 4: Export Action Button
        export_btn = QPushButton("Export Final Video with Music")
        export_btn.setStyleSheet("""
            background-color: #00AA66;
            font-size: 18px;
            padding: 12px;
            font-weight: bold;
        """)
        export_btn.clicked.connect(self.export_video)
        layout.addWidget(export_btn)

        # ================= Media Player System =================
        self.video_player = QMediaPlayer()
        self.video_audio = QAudioOutput()
        self.video_player.setAudioOutput(self.video_audio)
        self.video_player.setVideoOutput(self.video_widget)

        self.music_player = QMediaPlayer()
        self.music_audio = QAudioOutput()
        self.music_player.setAudioOutput(self.music_audio)

        self.video_player.positionChanged.connect(self.slider.setValue)
        self.video_player.durationChanged.connect(lambda d: self.slider.setRange(0, d))
        self.slider.sliderMoved.connect(self.video_player.setPosition)

    # ================= Loader Handlers =================

    def load_media(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Video or Image", "", "Media Files (*.mp4 *.avi *.mov *.mkv *.png *.jpg *.jpeg)"
        )
        if not file_path:
            return

        self.media_file = file_path
        ext = file_path.lower().split('.')[-1]

        if ext in ['png', 'jpg', 'jpeg']:
            self.media_type = "image"
            self.video_widget.hide()
            self.image_label.show()

            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(800, 450, Qt.AspectRatioMode.KeepAspectRatio))

            self.img_duration_label.show()
            self.img_duration_spin.show()
            self.status_label.setText(f"Loaded Image: {file_path.split('/')[-1]}")

        else:
            self.media_type = "video"
            self.image_label.hide()
            self.video_widget.show()

            self.img_duration_label.hide()
            self.img_duration_spin.hide()

            self.video_player.setSource(QUrl.fromLocalFile(file_path))
            self.status_label.setText(f"Loaded Video: {file_path.split('/')[-1]}")

    def load_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Audio Track", "", "Audio Files (*.mp3 *.wav *.aac *.m4a)"
        )
        if file_path:
            self.audio_file = file_path
            self.music_player.setSource(QUrl.fromLocalFile(file_path))
            clean_name = file_path.replace("\\", "/").split("/")[-1]
            self.audio_status_label.setText(f"Selected Music: {clean_name}")

    # ================= Playback Controls =================

    def play_preview(self):
        if self.media_type == "video":
            self.video_player.play()
        if self.audio_file:
            self.music_player.play()
        self.status_label.setText("Playing Preview")

    def pause_preview(self):
        if self.media_type == "video":
            self.video_player.pause()
        if self.audio_file:
            self.music_player.pause()
        self.status_label.setText("Paused")

    # ================= Export Engine =================

    def export_video(self):
        if not self.media_file:
            QMessageBox.warning(self, "Missing Media", "Please select a Video or Image first.")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Exported Video", "output.mp4", "MP4 Files (*.mp4)"
        )
        if not output_path:
            return

        self.status_label.setText("Processing Video... Please Wait.")
        QApplication.processEvents()

        try:
            # 1. Load Primary Visual Clip
            if self.media_type == "video":
                visual_clip = VideoFileClip(self.media_file)
            else:
                duration = self.img_duration_spin.value()
                visual_clip = ImageClip(self.media_file, duration=duration)

            # 2. Process & Apply Audio
            if self.audio_file:
                audio_clip = AudioFileClip(self.audio_file)

                # Trim audio if it is longer than the visual clip
                if audio_clip.duration > visual_clip.duration:
                    audio_clip = audio_clip.subclip(0, visual_clip.duration)

                final_clip = visual_clip.set_audio(audio_clip)
            else:
                final_clip = visual_clip

            # 3. Write Output MP4 File
            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=24
            )

            # Clean up loaded resources
            final_clip.close()
            visual_clip.close()

            self.status_label.setText("✅ Export Complete!")
            QMessageBox.information(self, "Success", f"File rendered successfully to:\n{output_path}")

        except Exception as e:
            self.status_label.setText("❌ Export Failed")
            QMessageBox.critical(self, "Export Error", f"An error occurred during rendering:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleVideoAudioEditor()
    window.show()
    sys.exit(app.exec())


```
scores = []
for i, vec in enumerate(vectors):
    score = cosine_sim(q_vec, vec)
    scores.append({"text": chunks[i], "score": score})

scores.sort(key=lambda x: x["score"], reverse=True)

return jsonify(scores[:5])
```

if **name** == "**main**":
app.run(debug=True) 












