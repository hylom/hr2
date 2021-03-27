from mako.template import Template

class Renderer():
    has_lookup = False
    
    def render(self, template, variables):
        renderer = Template(template)
        content = renderer.render(**variables)
        return content
