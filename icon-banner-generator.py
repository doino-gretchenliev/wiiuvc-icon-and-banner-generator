import os
import sys
import urllib.request
from shutil import copyfile
from PIL import Image

base_url = "https://art.gametdb.com/wii"
cover_url = base_url + "/cover/{}/{}.png"
fall_back_cover_url = base_url + "/cover/{}/{}.png"
cover_full_url = base_url + "/cover3D/{}/{}.png"

game_dir = sys.argv[1]
cover_dir = game_dir

skip_cover_download = False

target_cover_image_width = 128
target_cover_image_hight = 128

target_fullcover_image_width = 1280
target_fullcover_image_hight = 720

substitude_id_map = {
    'R38X78': 'R38P78',
    'S2UP41': 'S2UE41'
}

languages = ["US", "EN", "FR"]


def get_image_url(game_id, full_cover=False):
    retry_map = []

    for language in languages:
        if full_cover:
            retry_map.append(cover_full_url.format(language, game_id))
        else:
            retry_map.append(cover_url.format(language, game_id))
            retry_map.append(fall_back_cover_url.format(language, game_id))

    if game_id in substitude_id_map:
        for language in languages:
            if full_cover:
                retry_map.append(cover_full_url.format(language, substitude_id_map[game_id]))
            else:
                retry_map.append(cover_url.format(language, substitude_id_map[game_id]))

    for image_url in retry_map:
        if is_server_image_available(image_url):
            return image_url

    raise Exception("No image found")


def is_server_image_available(image_url):
    try:
        urllib.request.urlopen(image_url)
        return True
    except:
        return False


def is_valid_image(image_url, image_file):
    image = urllib.request.urlopen(image_url)
    server_image_size = image.info()['Content-Length']

    image_file_size = os.stat(image_file).st_size
    return int(server_image_size) == int(image_file_size)


def prepare(image_file, width, height, resize=True):
    image_pil = Image.open(image_file)
    image_pil = image_pil.convert('RGBA')

    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height

    if not resize:
        resize_width = image_pil.width
        resize_height = image_pil.height
    else:
        resize_width = width
        resize_height = height

    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)

    if not resize:
        return background
    else:
        return image_resize


def image_resize(image_file, fullcover=False):
    basewidth = target_cover_image_width
    if fullcover:
        basewidth = target_fullcover_image_width

    img = Image.open(image_file)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(new_image_file)


def save_image(image, image_file):
    image.save(image_file, quality=100)


def main():
    if not os.path.exists(cover_dir):
        os.mkdir(cover_dir)

    games = []
    for r, direcotries, f in os.walk(game_dir):
        for directory in direcotries:
            game = {
                'name': directory[0:-9],
                'id': directory[-7:-1],
                'dir': directory,
                'full_path': os.path.join(game_dir, directory)
            }
            games.append(game)

    count = 0
    for game in games:
        count += 1
        print("[{}/{}] Processing game: [{}][{}]".format(count, len(games), game['name'], game['id']))

        game_cover_dir = os.path.join(cover_dir, game['dir'])
        game_cover_file = os.path.join(game_cover_dir, "cover.png")
        game_coverfull_file = os.path.join(game_cover_dir, "fullcover.png")

        if not os.path.exists(game_cover_dir):
            os.mkdir(game_cover_dir)

        if not skip_cover_download:
            download = False

            image_url = get_image_url(game['id'])

            if not os.path.exists(game_cover_file):
                download = True
            else:
                download = not is_valid_image(image_url, game_cover_file)

            if download:
                print("Downloading cover...")
                urllib.request.urlretrieve(image_url, game_cover_file)

            download = False

            image_url = get_image_url(game['id'], True)

            if not os.path.exists(game_coverfull_file):
                download = True
            else:
                download = not is_valid_image(image_url, game_coverfull_file)

            if download:
                print("Downloading full cover...")
                urllib.request.urlretrieve(image_url, game_coverfull_file)

        icon = prepare(game_cover_file, target_cover_image_width, target_cover_image_hight)
        banner = prepare(game_coverfull_file, target_fullcover_image_width, target_fullcover_image_hight, False)

        icon_file = save_image(icon, os.path.join(game_cover_dir, "icon.png"))
        banner_file = save_image(banner, os.path.join(game_cover_dir, "banner.png"))


if __name__ == "__main__":
    main()
