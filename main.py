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
	def takepicture(e):
		# NOW I WILL OPEN CAMERA WITH OPENCV AND SAVE
		# YOU FACE IMAGE TO IMAGES FOLDER
		if not os.path.exists("images"):
			os.makedirs("images")

		cap = cv2.VideoCapture(0)
		# FOR WINDOW CAMERA
		cv2.namedWindow("YOU_FACE",cv2.WINDOW_NORMAL)
		cv2.resizeWindow("YOU_FACE",300,200)

		while True:
			ret,frame = cap.read()
			cv2.imshow("YOU_FACE",frame)

			key = cv2.waitKey(1)

			# NOW FOR SAVE YOU FACE IMAGE 
			# YOU MUST PRESS "s" FROM YOU KEYBORD TO WINDOW CAMERA
			if key == ord("s"):
				timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
				# SET FILE NAME
				filename = f"capture_{timestamp}.jpg"
				cv2.imwrite(os.path.join("images",filename),frame)
				print("YOU SUCCESS SAVED IMAGE")

				# AND SET TO IMAGE IF YOU SUCCES CROP
				myimage.src = f"images/{filename}"
				page.update()
				break
			# NOW IF YOU CLICK "q" from you keyboard
			# then window camera will close
			if key == ord("q"):
				break
		cap.release()
		cv2.destroyAllWindows()





	def cropmypicture(e):
		# NOW CROP PICTURE AND SAVE TO IMAGE FOLDER
		# NOW HIDE a border white container 
		editphoto.content.visible = False
		page.update()
		# DEFINE AREA YOU CROP PICTURE
		top = int(page.window_top) + int(toparea.value) + 20
		left = int(page.window_left) + int(toparea.value) + 20
		width = int(changesize.value) + 30
		height = int(changesize.value) 
		print(top,left)

		# NOW SCREENSHOt
		screenshot = ImageGrab.grab()
		image = cv2.cvtColor(np.array(screenshot),cv2.COLOR_RGB2BGR)
		cropped_image = image[top:top+height , left:left+width]

		# NOW RENAME WITH TIME YOU FILE IMAGE
		timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
		filename = f"cropped_{timestamp}.jpg"

		# NOW WRITE TO YOU LOCATION AND MAGE FILE
		cv2.imwrite(os.path.join("images",filename),cropped_image)
		print("image success crop")

		# AND SET IMAGE
		myimage.src = f"images/{filename}"
		page.update()








	def changeposition(e:DragUpdateEvent):
		e.control.top = max(0,e.control.top + e.delta_y)
		e.control.left = max(0,e.control.left + e.delta_x)
		print(e.control.top,e.control.left)
		toparea.value = max(0,e.control.top + e.delta_y)
		leftarea.value = max(0,e.control.left + e.delta_x)
		page.update()
		

	def changesize(e):
		editphoto.content.width = e.control.value
		editphoto.content.height = e.control.value
		page.update()

	# NOW CREATE SLIDER FOR CHANGE BORDER WHITE CROP
	changesize = Slider(
		min=10,max=350,
		value=200,label="change size",
		on_change=changesize
		)


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

	def cropagain(e):
		editphoto.content.visible = True
		page.update()

	page.add(
	Column([
		ElevatedButton("take you face",
			on_click=takepicture
			),
		Stack([myimage ,editphoto]),
		Row([
			ElevatedButton("Crop my picture",
			bgcolor="blue",color="white",
			on_click=cropmypicture
			),
			ElevatedButton("Crop again",
			bgcolor="red",color="white",
			on_click=cropagain
			),

			]),
		changesize,
		toparea,
		leftarea
		])

		)

flet.app(target=main,assets_dir="images")
