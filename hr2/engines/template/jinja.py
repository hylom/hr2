import jinja2

class Renderer():
    has_lookup = False
    name = "jinja"
    
    def render(self, template, variables):
        renderer = jinja2.Template(template)
        content = renderer.render(variables)
        return content
