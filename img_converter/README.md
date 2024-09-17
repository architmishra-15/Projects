# Project


This project was made more as a side project/hobby type. I do not really plan on updating or maintaining it, lol.

Well, it's not like someone's really going to be using it either way.

- ## About 

This was made to convert any image to HDF5 file format and then get the image back from any HDF5 file type. *Just don't forget the dataset name* \:) (personal experience).


- ## Working

It works in a simple manner - you import it, you use it. I mean what else do you expect from a python package? You think these 3-4 y/o or 70-80 y/o be doing all the setting ups? Nah mate.

-   You can convert the image to HDF5 file, something like this -
  <br>
    ```python
    import img_converter

    converter = ImageConveter()

    converter.image_to_array(/path/to/image, file_name, dataset_name)
    ```
> Note :memo: **:** _If no filename is provided it'll take `image_data` as one by default. And if no `dataset_name` is provided, the filename will be the dataset name too._ 

-    And you can convert `.h5` files back to image files too -
        ```python
        import img_converter

        converter = ImageConverter()

        file = /path/to/HDF5_file

        converter.array_to_image(file, dataset_name, name_of_output_image)
        ```

> Note :memo: **:** To check the image formats you can export in type this command -

```python
print(converter.valid_formats())
```
<br>

- ## Installation

You can either download the [wheel file](), and type in this command

```bash
pip install <path to wheel file>
```

<center> <strong>OR</strong></center>

You can download it using pip -
```bash
pip install img_h5_converter
```


# Other Stuffs

Now, I know these all are pretty boring stuffs that no one wants to read (ofc me too). So I have kept it at last.
<br>

## What was the motivation behind this, or simply - `why?`

Well, there wasn't really some great or revolutionary idea behind this. I had recently come to know about some called `HDF5` file format (`.h5`). I was interested as what it was, why was it made.

**So here's a short summary of what it is from the internet -**

`Hierarchical Data Format, Version 5 (HDF5) is a file format and library for storing and managing large amounts of complex data. HDF5 is open source and uses a file directory-like structure to organize data. It's designed to store scientific data and to make it easier to share with others.`
`HDF5 files have a self-describing structure that makes it easy to navigate and find all the objects in the file.`
`It supports a variety of data types, including atomic datatypes, which are indivisible objects like numbers or strings, and composite datatypes, which are made up of multiple atomic datatypes. Users can also define their own datatypes.`

You can read more about it [here](https://docs.hdfgroup.org/hdf5/v1_14/_intro_h_d_f5.html). Or maybe [here with a nice and clean experience](https://www.neonscience.org/resources/learning-hub/tutorials/about-hdf5).

### But what does it meant to me?

Well, not much until a few days later a thought struck to my mind to share an image in the form of numpy array to my friend. But unfortunately, it was a `.png` image and numpy can't save 3-Dimenssional array to a text file. So that's when I begin to search and learn about `HDF5` file format. And hence this.

I thought this could be a nice and fun little project. And maybe I could encrypt it and then share it to somebody? Lol it'd be fun nice experiment. I think I'll add this encryption thing in the near future.

#### So yeah that all thanks for reading!