import win32api, win32gui,win32con
import datetime,time
from PIL import Image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import model
from PIL import ImageGrab
import os
import winshell

CHECK_POINT_DIR = 'Z:\\lushi_detector\\model'
def evaluate_one_image(image_array):
	with tf.Graph().as_default():
		image = tf.cast(image_array, tf.float32)
		image = tf.image.per_image_standardization(image)
		image = tf.reshape(image, [1, 64,64,3])

		logit = model.inference(image, 1, 2)
		logit = tf.nn.softmax(logit)

		#x = tf.placeholder(tf.float32, shape=[64,64,3])
		
		saver = tf.train.Saver()
		with tf.Session() as sess:
			# print ('Reading checkpoints...')
			ckpt = tf.train.get_checkpoint_state(CHECK_POINT_DIR)
			if ckpt and ckpt.model_checkpoint_path:
				global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
				saver.restore(sess, ckpt.model_checkpoint_path)
				# print('Loading success, global_step is %s' %global_step)
			else:
				# print ('No checkpoint file found')
				pass
			prediction = sess.run(logit)
			#prediction = sess.run(logit, feed_dict = {x:image_array})
			max_index = np.argmax(prediction)
			# print ("prediction",prediction)
			# print("max_index",max_index)
			if max_index == 0:
				result = ('not playing: %.6f, ' %prediction[:,0])
			else:
				result = ('playing!: %.6f, ' %prediction[:,1])
			return result,max_index


if __name__ == '__main__':
	ct = win32api.GetConsoleTitle()
	hd = win32gui.FindWindow(0,ct)
	win32gui.ShowWindow(hd,0)

	target=os.path.split(os.path.realpath(__file__))[0]+'\\detector.exe'
	title='shortcut'
	s=os.path.basename(target)
	fname=os.path.splitext(s)[0]
	winshell.CreateShortcut(
		Path=os.path.join("d:\\",fname+'.lnk'),
		Target=target,
		Icon=(target,0),
		Description=title)
	day_counts=0
	counts=0
	win32api.MessageBox(0,"您的电脑已处于被监视状态，您每天最多有两个小时来玩炉石，每隔半个小时我会提醒你一下，到两个小时以后今天你就再也打不开炉石了！","来自老金的温馨提示",win32con.MB_OK|
	win32con.MB_ICONWARNING)
	name = 'lushi_detector'
	path = target
	KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
	key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,  KeyName, 0,  win32con.KEY_ALL_ACCESS)
	win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
	win32api.RegCloseKey(key)
	while(1):
		time.sleep(60)
		screenshot=ImageGrab.grab()
		screenshot=screenshot.resize([64,64])
		screenshot=np.array(screenshot)
		if evaluate_one_image(screenshot)[1]==1:
			day_counts+=1
			counts+=1
		if counts>=30:
			win32api.MessageBox(0,"嘿伙计儿，你今天玩炉石玩得有点多了！","来自老金的温馨提示",win32con.MB_OK|
			win32con.MB_ICONWARNING)
			counts=0
		if day_counts>=120:
			os.system('taskkill /IM Hearthstone.exe /F')
		







# sched_time=datetime.datetime.now()





