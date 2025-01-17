import requests, json, time, os, datetime
from livestreamer import Livestreamer

model = 'AlexyaWonder'#enter model name

def get_data(model):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest',
	}
	data = [('method', 'getRoomData'), ('args[]', model)]
	r = requests.post('https://bongacams.com/tools/amf.php', headers=headers, data=data)
	return json.loads(r.text)

def stream(videoServerUrl, model):
	session = Livestreamer()
	session.set_option('http-headers', 'referer=https://bongacams.com/%s' % model)

	url = 'hlsvariant://https:%s/hls/stream_%s/playlist.m3u8' % (videoServerUrl, model)

	streams = session.streams(url)
	stream = streams['best']
	fd = stream.open()

	now = datetime.datetime.now()
	filePath = '%s/%s.mp4' % (model, model+now.strftime('%Y-%m-%d-%H-%M'))
	print(' - Start record stream')
	if not os.path.exists(model):
		os.makedirs(model)
	with open(filePath, 'wb') as f:
		while True:
			try:
				data = fd.read(1024)
				f.write(data)
			except:
				print(' - Error write record into file')
				f.close()
				return

if __name__ == '__main__':
	data = get_data(model)
	if 'videoServerUrl' in data['localData']:
		stream(data['localData']['videoServerUrl'], model)
	else:
		print(' - This model just now offline')
