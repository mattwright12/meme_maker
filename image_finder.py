

from google_images_download import google_images_download

def get_image(title):
    response = google_images_download.googleimagesdownload()
    search = title + ' original'
    arguments = {"keywords":"{}".format(search),"limit":1,"print_urls":True}
    paths = response.download(arguments)
    image_path = paths[search]
    return image_path
    
