from tkinter import ttk, LEFT


class IconedButton(ttk.Button):
    def __init__(self, *args, image=None, compound=LEFT, **kwargs):
        self._image = image
        super().__init__(*args, image=image, compound=compound, **kwargs)

    def config(self, *args, **kwargs):
        image = kwargs.get('image')

        if image is not None:
            self._image = image

        super().config(*args, **kwargs)

    configure = config
