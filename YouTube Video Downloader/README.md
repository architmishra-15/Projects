# About

In this project, I've tried to make a GUI based YouTube video downloader.

## How does it work 

- It'll look for the video you asked based on the link you provided.
- It'll download the video of the chosen quality.
- Video and audio would be downloaded separately.
- It'll merged in a single file using `ffmpeg` and would be exported by the provided name.

## Requirements

*I've attached a `requirements.txt` file, download the file from [here](requirements.txt) and enter the following code in the command prompt/ bash*

```commandline
pip install -r requirements.txt
```

### Additional requirements needed - 

- _Since ffmpeg does not come pre-installed, it needs to be downloaded._
    - **For Windows**
        - For windows  there are two methods, first is to download it from the [official website](sudo emerge media-video/ffmpeg).
      <center>OR</center>

        - Using `winget` -
            ```commandline
            winget install ffmpeg
            ```
    - **For macOS -**
        ```bash
        brew install ffmpeg
        ```
    - **For Debian based distros -**
        ```bash
        sudo apt update
        sudo apt install ffmpeg
        ```
    - **Using Yum (CentOS) -**
        ```bash
        sudo yum install ffmpeg
        ```
        <center>or</center>

        ```bash
        sudo dnf install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %rhel).noarch.rpm
        sudo dnf install ffmpeg
        ```
    - **openSUSE -**
        ```bash
        sudo zypper install ffmpeg
        ```
    - **Arch based distros-**
        ```bash
        sudo pacman -S ffmpeg
        ```
    - **Alpine -**
        ```bash
        sudo apk add ffmpeg
        ```
    - **Gentoo -**
        ```bash
        sudo emerge media-video/ffmpeg
        ```

## Executable

Instead of viewing, installing and running the code, you can directly install the exe file by [clicking here.](https://github.com/architmishra-15/Projects/releases/download/exe/Youtube-Downloader.exe) Please also copy the icon folder in case if you're donwloading the exe file. Keep the exe file inside the icon folder.
## License

_This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details._
