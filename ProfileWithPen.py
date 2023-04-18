# -- Make sure to have all these dependencies installed -- #
from PIL import Image
import requests, math
import urllib.request
import json, shutil
import os.path

USERNAME = "codeGIO"  # Change with your username and run the script

with open("Assets/IMG.chars.txt", 'r') as f:
    IMGchars = f.read().rsplit()

def saveThumbnail(url):
    urllib.request.urlretrieve(url, "Assets/thumbnail.png")

def savePFP(url):
    urllib.request.urlretrieve(url, "Assets/pfp.png")

def readThumbnail():
    img = Image.open("Assets/thumbnail.png").convert('RGB')
    size = img.size
    data = []
    for iy in range(size[1]):
        for ix in range(size[0]):
            col = img.getpixel((ix, iy))
            data.append(list(col))
    for i in range(len(data)):
        for j in range(3):
            data[i][j] = math.floor(data[i][j] / 4)
    temp = ""
    for i in data:
        for j in i:
            temp += IMGchars[j]
    return [size[0], size[1], temp]


def readPFP():
    img = Image.open("Assets/pfp.png").convert('RGB')
    size = img.size
    data = []
    for iy in range(size[1]):
        for ix in range(size[0]):
            col = img.getpixel((ix, iy))
            data.append(list(col))
    for i in range(len(data)):
        for j in range(3):
            data[i][j] = math.floor(data[i][j] / 4)
    temp = ""
    for i in data:
        for j in i:
            temp += IMGchars[j]
    return [size[0], size[1], temp]


def getUser(u):
    resp = requests.get(f"https://api.scratch.mit.edu/users/{u}").json()
    return resp


class User:
    def __init__(self, user):
        try:
            user = getUser(user)
            self.id = user['id']
            self.username = user['username']
            self.country = user['profile']['country']
            self.bio = user['profile']['bio']
            self.wiwo = user['profile']['status']
            self.img90 = user['profile']['images']["90x90"]
        except:
            raise Exception('DOESNOT EXIST')


def MakeTheProject(user):
    try:
        u = User(user)
    except Exception as e:
        print(e)
        return None
    data = [u.username, u.id, u.bio, u.wiwo]
    response = json.loads(requests.get(f"https://scratch.mit.edu/site-api/users/all/{user}/").text)
    if response["featured_project_label_id"] is None:
        data.append(0)
    else:
        data.append(int(1+response["featured_project_label_id"]))
    if response["featured_project_data"] is None:
        data.append("")
        data.append("")
    else:
        data.append(str(response["featured_project_data"]["title"]))
        data.append(str(response["featured_project_data"]["id"]))
    data.append(u.country)
    savePFP(u.img90)
    data.append(readPFP())
    if response["featured_project_data"] is None:
        data.append("")
    else:
        saveThumbnail(f"https://uploads.scratch.mit.edu/projects/thumbnails/{data[7]}.png")
        data.append(readThumbnail())
    for i in [2, 3, 5, 7]:
        data[i] = data[i].replace("\n", " ")
    with open("Assets/project.json", 'r', encoding="utf8") as f:
        project = json.load(f)
    project["targets"][0]["lists"]["9~zqgLe.//|w7zCkztM2"][1] = [u.username, str(u.id), data[2], data[3], data[4], data[5], data[6], u.country]
    project["targets"][0]["lists"][",9oQjL:4s(eK*^C5kii?"][1] = list(data[9])
    project["targets"][0]["lists"]["4lt40q3MZ|Ie{G$420_A"][1] = data[8]
    with open("ToExport/project.json", "w") as f:
        json.dump(project, f)
    src_path = "Assets/9af27a7ad39ec41b7cbfda3622d08a1a.svg"
    dst_path = "ToExport/9af27a7ad39ec41b7cbfda3622d08a1a.svg"
    shutil.copy(src_path, dst_path)
    src_path = "Assets/89e9c28db982688d9e408d4459ae4700.png"
    dst_path = "ToExport/89e9c28db982688d9e408d4459ae4700.png"
    shutil.copy(src_path, dst_path)
    src_path = "Assets/cd21514d0531fdffb22204e0ec5ed84a.svg"
    dst_path = "ToExport/cd21514d0531fdffb22204e0ec5ed84a.svg"
    shutil.copy(src_path, dst_path)
    archived = shutil.make_archive(base_name="Export", format='zip', root_dir='ToExport')
    if os.path.exists(f"Profile of {u.username}.sb3"):
        os.remove(f"Profile of {u.username}.sb3")
    os.rename("Export.zip", f"Profile of {u.username}.sb3")

MakeTheProject(USERNAME)
