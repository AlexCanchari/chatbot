import requests

resp = requests.post('http://localhost:5000/predict',files={'file': open('causa_limena_31268_600_square.jpg','rb')})

print(resp.text)