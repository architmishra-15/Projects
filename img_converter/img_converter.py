from numpy import asarray, uint8
from PIL import Image
import h5py
import re
import os



class ImageConverter:
    
    formats = ['jpg', 'jpeg', 'png', 'tiff', 'tif', 'bmp', 'gif', 'webp', 'ppm', 'ico']
    
    def __init__(self):
        pass
        
    @staticmethod
    def valid_extension(filename: str) -> bool:
        '''
        Check if the file has a valid image extension.
        
        Args:
            filename: The name of the file to check.
        
        Returns:
            bool: True if valid, False otherwise.
        '''
        
        pattern = r'.*\.(jpg|jpeg|png|tiff|tif|bmp|gif|webp|ppm|ico)$'
        
        return bool(re.match(pattern, filename, re.IGNORECASE))


    def valid_formats(self):
        return f"Valid image formats are - {'\n'.join(format)}"
    
    
    def image_to_array(self, path: str, array_name: str = 'image_data', dataset:str = None)  -> None:
        '''
        This function will convert given file to HDF5 type file format.
        
        Args:
            path: Enter the path of the image.
            array_name: Enter the name of the file with which you want to save.
            dataset: Name of the dataset, by default it is set same as 'array_name'.
        
        Please note that the name of the file and dataset will be same for the easy of convinence
        '''
        # Remove the ".h5" extension if present in the given array_name 
        array_name = re.sub(r'\.h5$', '', array_name, flags=re.IGNORECASE)
        
        
        if dataset is None:
            dataset = array_name
            
        
        try:
            image = Image.open(path)
        
        except FileNotFoundError:
            return "Error! File not Found. Please enter a valid file destination"
        
        
        array = asarray(image)
        
        with h5py.File(f"{array_name}.h5", "w") as f:
            f.create_dataset(dataset, data=array, compression="gzip", compression_opts=9)
            print(f"HDF5 file '{array_name}.h5' saved successfully.")



    def array_to_image(self, path: str, dataset: str, img_name: str) -> None:
        
        '''
        This function converts HDF5 file to image file.
        
        Args:
            path: Location of HDF5 (.h5) file.
            dataset: Name of the dataset in which it is stored.
            img_name: The name by which the array that is converted to image is saved by.
        
        '''
        
        pattern = r'.*\.h5$'
        
        extention = bool(re.match(pattern, path, re.IGNORECASE))
        
        if extention:
            try:
        
                with h5py.File(path, 'r') as f:
                    if dataset not in f:
                        print(f"Dataset '{dataset}' not found in the HDF5 file.")
                        return
                    
                    data_set = f[dataset]
                    
                    image_array = data_set[:].astype(uint8)
                    
                image = Image.fromarray(image_array.astype(uint8))
                
                file_ext = os.path.splitext(img_name)[1].lower()[1:]  # Remove the dot from extension
                if not self.valid_extension(img_name):
                    valid_formats = ["jpg", "jpeg", "png", "tiff", "tif", "bmp", "gif", "webp", "ppm", "ico"]
                    print("Please enter a valid format")
                    print(f"Valid formats are {'\n'.join(valid_formats)}")
                    return
                
                try:
                    if file_ext == 'jpeg' or file_ext == 'jpg':
                        image.save(img_name, format='JPEG', quality=95)
                    elif file_ext == 'png':
                        image.save(img_name, format='PNG', compress_level=9)
                    elif file_ext == 'gif':
                        image.save(img_name, format='GIF')
                    elif file_ext == 'bmp':
                        image.save(img_name, format='BMP')
                    elif file_ext == 'tiff' or file_ext == 'tif':
                        image.save(img_name, format='TIFF')
                    elif file_ext == 'webp':
                        image.save(img_name, format='WEBP', quality=95)
                    elif file_ext == 'ppm':
                        image.save(img_name, format='PPM')
                    elif file_ext == 'ico':
                        image.save(img_name, format='ICO')
                    else:
                        print("Unsupported format")
                except Exception as e:
                    print(f"Error saving image: {e}")
                    
            except Exception as e:
                print(f"Error in reading file: {e}")
                
        else:
            return "Please give a valid HDF5 file location."
        

converter = ImageConverter()

# converter.image_to_array('264393624_880b15ac-11ab-43e2-a7e1-6a4507901280.jpg', 'output_array', 'output')

converter.array_to_image('output_array.h5', 'output', 'sample_image.png')