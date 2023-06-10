from flet import *
import cv2
import os
from datetime import datetime
import pyscreenshot as ImageGrab
import numpy as np

def main(page:Page):
	page.window_width = 400
	toparea = Text(0)
	leftarea = Text(0)

	def	takepicture(e):
		if not os.path.exists('images'):
		    os.makedirs('images')

		# Inisialisasi kamera
		cap = cv2.VideoCapture(0)
		cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('Camera', 300, 200)  # Ganti dengan lebar dan tinggi yang diinginkan

		while True:
		    # Membaca frame dari kamera
		    ret, frame = cap.read()
		    
		    # Menampilkan frame di jendela kamera
		    cv2.imshow('Camera', frame)
		    
		    # Menangkap tombol yang ditekan
		    key = cv2.waitKey(1)
		    
		    # Jika tombol 's' ditekan, simpan gambar
		    if key == ord('s'):
		        # Menyimpan gambar dengan nama 'capture.jpg' ke dalam folder 'images'
		        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
		        filename = f"capture_{timestamp}.jpg"
		        cv2.imwrite(os.path.join('images', filename), frame)
		        print("Gambar berhasil disimpan!")
		        myimage.src = f"images/{filename}"
		        page.update()
		        break
		    
		    # Jika tombol 'q' ditekan, keluar dari program
		    if key == ord('q'):
		        break

		# Menutup jendela kamera dan melepaskan sumber daya
		cap.release()
		cv2.destroyAllWindows()


	def changeposition(e:DragUpdateEvent):
		e.control.top = max(0,e.control.top + e.delta_y)
		e.control.left = max(0,e.control.left + e.delta_x)
		print(e.control.top,e.control.left)
		toparea.value = max(0,e.control.top + e.delta_y)
		leftarea.value = max(0,e.control.left + e.delta_x)
		page.update()


	def youchangesize(e):
		editphoto.content.width = e.control.value
		editphoto.content.height = e.control.value
		page.update()

	def cropmypicture(e):
		editphoto.content.visible = False
		page.update()
		top = int(page.window_top) +  int(toparea.value) + 5
		left =int(page.window_left) + int(leftarea.value) + 5
		width = changesize.value + 30
		height = changesize.value
		print(top,left)
		screenshot = ImageGrab.grab()
		image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
		cropped_image = image[top:top+height, left:left+width]
		timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
		filename = f"cropped_{timestamp}.jpg"
		cv2.imwrite(os.path.join('images', filename), cropped_image)
		print("Gambar berhasil dipotong!")
		myimage.src = f"images/{filename}"
		page.update()


	 

	myimage = Image(src="images/blank.jpg")
	
	editphoto = GestureDetector(
		drag_interval=10,
		top=10,
		left=10,
		mouse_cursor=MouseCursor.MOVE,
		on_pan_update=changeposition,
		content=Container(
			border=border.all(5,"white"),
			width=200,
			height=170,
			visible=True
			)
		)


	changesize = Slider(min=10,max=350,
		value=200,
		label="change size",
		on_change=youchangesize
		)

	page.add(
		Column([
			ElevatedButton("Take Camera",
				on_click=takepicture
				),
			Stack([myimage,editphoto]),
			ElevatedButton("crop picture",
				bgcolor="blue",color="white",
				on_click=cropmypicture
				),
			changesize,
			toparea,
			leftarea
			])
		)

flet.app(target=main,assets_dir="images")
