# Memeory Address

## What is a memory address?

A memory address is a unique identifier that represents a specific location in a computer's memory (RAM). It allows the CPU to access and manipulate data stored at that particular location. Memory addresses are used by programs and operating systems to organize and retrieve information efficiently.

<ins>***<font color="orange">Key points:</font>***</ins>
- **Unique identifier for a memory location**
- **Allows direct access to stored data**
- **Usually represented in hexadecimal format**
- **Essential for efficient data management in computer systems**

### How are memory addresses written?

Memory addresses are typically written in hexadecimal notation:

- Format: 0x[hexadecimal number]
- Example: 0x7FFF1234

The prefix *`0x`* indicates that the following number is in ***hexadecimal***. Each hexadecimal digit represents 4 bits, allowing for compact representation of large addresses.


## <ins><font color="Red">Why is so it important</font></ins>?

Understanding memory addresses is crucial for:

- Pointer manipulation in languages like C and C++
- <font color="blue">Debugging and memory management.</font>
- Optimizing code performance
- Working with low-level system operations

## Tools for Viewing Memory Addresses

Some common tools for viewing and manipulating memory addresses:

- Debuggers (e.g., GDB, Visual Studio Debugger)
- Memory editors (e.g., Cheat Engine)
- System monitoring tools (e.g., Process Explorer)

## Idea behind the project

Well, there isn't any great or ambitious idea behind this project. I just wanted to try out a new thing that I was curious about - <ins><font color="yellow">Cython</font></ins>.

And around the same time I was also looking if there's any pointers in `Python` like it is in `C` or `C++`. So I decided to make a package which can do that for python for myself.

Actuallt it is not a pointer but it can do the work of pointer for accessing the memory addresses, and besides I want to write a code for ***true multi-threading in Python*** (ofc I'll use C/C++ for that, lol).

## Installation
> :warning: **Warning:** Before donwloading and using, you should be cautious since playing around with memory addresses can be risky and can cause issues to your system or program to run.

I havn't uploaded it to the pypi yet so you cannot donwload it using `pip`. You can do either of these - 

- Clone the repository :-
  ```bash
  git clone https://github.com/yash-dk/memory-address.git
  ```
  -  and run - <br><br>

        ```bash
        pip install -r requirements.txt
        ```
   - After this you can make a `.pyd` fil by running - <br><br>
      ```bash
      python setup.py build_ext --inplace
      ```

- Or you can just download the `whl` file from the [releases](https://github.com/yash-dk/memory-address/releases) and run -
  <br>
  ```bash 
  pip install <path_to_whl_file>
  ```

> :bulb: **Tip:** Downloading and using the wheels would be much better and easier.
## Contributing

I was thinking of expanding its functionalities, but at my current level of knowledge, I don't think I'll be able to do it along, so anyone who's willing to contribute is welcome! Just send a pull request.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.