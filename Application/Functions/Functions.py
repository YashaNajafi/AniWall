#---------< Libs >----------
import json,os,requests,re
from contextlib import closing
#---------< Paths >---------
DataPath = os.path.join(".","BackgroundsData","BackgroundsData.json")
#---------< Functions >---------
def GetMainData():
    with open(DataPath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def GetDataOfWallpaper(SearchType: str, SearchValue: str = None):
    with open(DataPath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    backgrounds = data.get("Backgrounds", [])

    if SearchType == "ByName":
        if not SearchValue:
            raise ValueError("SearchValue is required for ByName search.")
        result = [bg for bg in backgrounds if bg["Name"].lower() == SearchValue.lower()]
        return result[0] if result else None

    elif SearchType == "ByCategory":
        if not SearchValue:
            raise ValueError("SearchValue is required for ByCategory search.")
        result = [bg for bg in backgrounds if SearchValue.lower() in bg["Categories"].lower()]
        return result

    else:
        raise TypeError(f"Type {SearchType} Not Defined!")

def GetCoversPath(WithFolder : bool=True):
    Index = 0
    CoversFolderPath = os.path.join(".","static","Images","Covers")
    CoversPath = os.listdir(CoversFolderPath)

    if WithFolder:
        for Item in CoversPath:

            PathStructure = "Images/Covers/"
            Item = PathStructure+Item
            CoversPath[Index] = Item
            Index+=1
    else:
        return CoversPath

    return CoversPath

def GetBackgrounds():
    with open(DataPath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def DownloadBackground(BackgroundName: str):
    BackgroundName += ".mp4"
    Link = f"https://raw.githubusercontent.com/YashaNajafi/AniWall/refs/heads/main/Wallpapers/{BackgroundName}"

    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(current_file))
    videos_dir = os.path.join(base_dir, "Videos")
    os.makedirs(videos_dir, exist_ok=True)

    try:
        with closing(requests.get(Link, stream=True)) as Response:
            Response.raise_for_status()
            file_path = os.path.join(videos_dir, BackgroundName)
            with open(file_path, 'wb') as file:
                for chunk in Response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        print("Download completed successfully.")
    except requests.exceptions.RequestException as e:
        print(f"File Download Error: {e}")

def CheckWallpaperExist(BackgroundName: str) -> bool:
    BackgroundName += ".mp4"

    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(current_file))
    videos_dir = os.path.join(base_dir, "Videos")

    file_path = os.path.join(videos_dir, BackgroundName)

    return os.path.isfile(file_path)

def GetCategory(CategorySTR : str):
    Match = re.search(r'\(([^()]*)\)', CategorySTR)
    if Match:
        return Match.group(1).strip()
    return CategorySTR.strip()

def GetMainCategory(CategorySTR: str):
    Match = re.search(r'^([^(]+)', CategorySTR)
    if Match:
        return Match.group(1).strip()
    return CategorySTR.strip()
