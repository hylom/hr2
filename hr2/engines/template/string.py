import string

class Renderer():
    has_lookup = False
    
    def render(self, template, variables):
        renderer = string.Template(template)
        content = renderer.safe_substitute(variables)
        return content

