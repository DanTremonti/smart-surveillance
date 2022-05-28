import os
import cloudinary.uploader
import twilio_mod.env as my_environ

cloudinary.config( 
            cloud_name = my_environ.env_keys['CLOUDINARY_CLOUD_NAME'], 
            api_key = my_environ.env_keys['CLOUDINARY_API_KEY'], 
            api_secret = my_environ.env_keys['CLOUDINARY_API_SECRET'] 
            )
def upload_cimage(path: str, name: str):
    return cloudinary.uploader.upload(
        path, 
        folder = 'smart-surveillance/' + os.getlogin(),
        public_id = name
        )