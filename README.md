# Jelly

## A Frameless, Transluscent, Modern, Draggable Dialog for PySide6

<img src="./icons/purple_vial_lg.png" alt="Jelly logo" align="right"></img>


This repository contains the source code for `Jelly`, a customizable, frameless dialog widget built with PySide6.
<br><br> 
There is also a **fully functional** example app called **QRJelly.py** you can have a look at for an idea on what it looks like.

### Features

* **Frameless Design:** Jelly removes the standard window frame, resulting in a sleek, modern aesthetic.
* **Draggable:** Users can easily drag the dialog around the screen by clicking and holding the title bar area.
* **Customizable Appearance:** You can modify the background color, button styles, and layout through CSS.
* **Minimize and Close Buttons:** Jelly includes pre-styled minimize and close buttons for user interaction.
* **Content Flexibility:** Add any QWidget to the dialog's content area using the `add_content_widget` method.


### Requirements

* Python 3.6+
* PySide6

**Note:** You'll also need an image for the window icon (`jelly_icon.png`) placed in a folder named `icons` within your project directory. You can raid the icons directory or make up your own.


### Usage

* Clone this repository or download the files. 
* Install requirements: (if I've missed anything let me know)
    ```bash
    pip install -r requirements.txt
    ```
*Python is not included in the requirements file. You can get that from your repository via your package manager.*
* Import the `Jelly` class in your Python script:

```python
from Jelly import Jelly

# Create a new Jelly instance
jelly_dialog = Jelly()

# Add your custom widgets to the content area
# ... (add_content_widget calls)

# Show the dialog
jelly_dialog.show()

# (Interact with the dialog as needed)
```

### Customizing Appearance

The `Jelly` class uses a CSS stylesheet to define its appearance. You can modify the stylesheet within the `__init__` method (`setStyleSheet`) to change the background color, button styles, and other visual elements.

### TODO

Jelly, for me, was just a different way of thinking about dialog windows. I was daydreaming about it one afternoon and said, "Why not see what it looks and feels like."
<br><br>
So, I've been working on this class as I get time, and have a few ideas for geometry tweaks. Also, something I miss, a basic title. Not neccessarily a bar, but something that resembles a standard title, but cooler. Possibly the missing green button that I simply didn't need on one of my other projects.  Might throw that back in there, too.

### Contributions

Clearly this class is a wee baby. But I see potential for it.
<br><br>
I don't typically collaborate, and have little experience with it on here, except with an old friend Robogod. But I'm not opposed to it if you have any noteworthy ideas.

### Thanks!

<p>Ryon Shane Hall</p>  

<a href="http://ryonshanehall.com" alt="RSH Homepage">my website</a>
