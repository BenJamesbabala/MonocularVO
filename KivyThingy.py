#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Baseado no código disponivel em https://groups.google.com/forum/?hl=en#!topic/kivy-users/N18DmblNWb0
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from FileCapture import FileCapture
import cv2
from VisualOdometry import MonocularVO
from kivy.core.window import Window
class CameraApp(App):

    def build(self):
        Window.size = (300, 600)

        sv = ScrollView()
        self.img1 = Image(source='groundtruth_mav.jpg')
        self.vo = MonocularVO()
        self.capture = FileCapture()
        Clock.schedule_interval(self.update,
                                1.0 / 60.0)
        sv.add_widget(self.img1)
        return sv

    def update(self, dt):
        frame = self.capture.read_frame()
        cv2.imshow("Frame", frame)
        self.vo.update(frame)
        if self.vo.tracker.frame_idx > 1:
            x = int(self.vo.current_t[0][0])+2000
            y = int(self.vo.current_t[2][0])+2000
            cv2.circle(self.vo.trajectory, (x, y), 1, (0, 0, 255))
            frame = self.vo.trajectory
        print(self.vo.tracker.frame_idx)
        buf = frame.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img1.texture = texture1
        self.img1.size = (frame.shape[1], frame.shape[0])
        self.img1.keep_ratio = True
        self.img1.size_hint = (None, None)


if __name__ == '__main__':
    CameraApp().run()