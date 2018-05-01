
from bokeh.models.widgets import Div

spinner_svg = """
<!-- By Sam Herbert (@sherb), for everyone. More @ http://goo.gl/7AJzbL -->
<svg width="38" height="38" viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg" stroke="#999">
    <g fill="none" fill-rule="evenodd">
        <g transform="translate(1 1)" stroke-width="2">
            <circle stroke-opacity=".5" cx="18" cy="18" r="18"/>
            <path d="M36 18c0-9.94-8.06-18-18-18">
                <animateTransform
                    attributeName="transform"
                    type="rotate"
                    from="0 18 18"
                    to="360 18 18"
                    dur="1s"
                    repeatCount="indefinite"/>
            </path>
        </g>
    </g>
</svg>
"""

# def get_spinner():
#     return Div(text=spinner_svg, width=50, height=50)


class Spinner(Div):
    __implementation__ = """
    import {Div} from "models/widgets/div"
    export class Spinner extends Div
        type: "Spinner"
    """

    def __init__(self, *args, **kwargs):
        kwargs['text'] = spinner_svg
        super().__init__(*args, **kwargs)
        self.show()

    def hide(self):
        self.style['visibility'] = 'hidden'

    
    def show(self):
        self.style['visibility'] = 'visible'

        