import requests
import json
import re
import angle
import flash
def ocr(filename):
    try:
        payload = {'apikey': 'fe5559db7c88957','scale': True,'language': 'eng'}
        with open(filename, 'rb') as f:
            response = requests.post('https://api.ocr.space/parse/image',files={filename: f},data=payload)
    except Exception as e:
        print(e)
        return('Server error','Contact Administrator')
    try:
        info = response.content.decode()
        jsonstr = json.loads(info)
        text = jsonstr["ParsedResults"][0]["ParsedText"]
    except Exception as e:
        print(e)
        return ('Network error', 'Try again')
    try:
        # Initializing cleaning of data
        text1 = []
        lines = text.split('\n')
        for lin in lines:
            s = lin.strip()
            s = s.rstrip()
            s = s.lstrip()
            xx = s.split('\n')
            if not ([w for w in xx if re.search('(INCOME| |TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA|PERMANENT|ACCOUNT|NUMBER|SIGNATURE|PERMA|NENT|ACCO|UNT|NUM|BER|SIGNA|TURE)$', w.upper())]):
                text1 = list(text1)
                text1.append(s)
        # Making tuples of data
        data = {}
        data['Name'] = re.sub('[^A-Z\s]', '', text1[0])
        data['Father Name'] = re.sub('[^A-Z\s]', '', text1[1])
        data['Date of Birth'] = re.sub('[^0-9/]', '', text1[2])
        data['PAN'] = re.sub('[^0-9A-Z]', '', text1[3])
        flh = ang = 0
        msg = ""
        try:
            flh = flash.flash(filename)
            ang = angle.angle(filename)
            if int(flh) > 2:
                msg = "There are reflections in the image, data might not be correct"
            elif int(ang) not in range(-3,3):
                msg = "Angle of the image is improper, data might not be correct"
        except Exception as e:
            print(e)
        f = open("details.txt", "a")
        f.write(str(data)+"\n")
        f.close()
        return data, msg
    except IndexError as e:
        print(e)
        if int(flh) > 2:
            return('There are reflections in the image', 'Try again')
        elif int(ang) not in range(-3,3):
            return('Keep the angle of the image proper', 'Try again')
        return('Blurred Image', 'Try again')
    except Exception as e:
        print(e)
        return ('Network Error', 'Try again')