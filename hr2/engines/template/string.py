import string

class Renderer():
    has_lookup = False
    name = "string_template"

    def render(self, template, variables):
        renderer = string.Template(template)
        content = renderer.safe_substitute(variables)
        return content

