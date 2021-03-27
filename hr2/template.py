import os
import os.path
import re
import mimetypes

class TemplateNotFoundError(Exception):
    pass

class EngineNotAvailableError(Exception):
    def __init__(self, engine):
        self.message = "engine {} is not available".format(engine)

class RenderingError(Exception):
    def __init__(self, e):
        self.error = e

class Template():
    def __init__(self, engine, base_directories=[], default_engine=None):
        self.base_directories = base_directories
        self.engine = engine
        self.default_engine = default_engine
        self.allowed_content_types = ['text/html']

    def render(self, template_name, variables, content_type=None, engine=None):
        tmpl = self._find_template(template_name, content_type, engine)
        if not tmpl:
            raise TemplateNotFoundError()

        # if engine is not defined, use default engine
        if not tmpl.get('engine') and self.default_engine:
            tmpl['engine'] = self.default_engine

        # check if engine is available
        renderer = self.engine.get(tmpl["engine"], None)
        if not renderer:
            raise EngineNotAvailableError(tmpl["engine"])

        if renderer.has_lookup:
            tmpl["content"] = renderer(template_name, variables)
            return tmpl

        with open(tmpl["path"], 'r') as fp:
            content = fp.read()

        try:
            tmpl["content"] = renderer.render(content, variables)
        except Exception as e:
            raise RenderingError(e)

        return tmpl

    def _find_template(self, template_name, content_type, engine):
        candiate = {}
        for d in self.base_directories:
            r = self._find_template_file(d, template_name)
            for t in r:
                #print(t, content_type, engine)
                # check engine
                if engine and t["engine"] != engine:
                    continue
                # check content_type
                if content_type:
                    if t["content_type"] != content_type:
                        continue
                if t["content_type"]:
                    candiate[t["content_type"]] = t
                
        for ctype in self.allowed_content_types:
            if candiate[ctype]:
                return candiate[ctype]
        return None

    def _find_template_file(self, base_dir, template_name):
        # template_name is one of below format:
        # - "<relative directory>/<filename without extension>"
        # - "<filename without extension>"

        # if template_name starts with '/', remove it
        template_name = re.sub(r"^/+", '', template_name)

        target_dir = os.path.join(base_dir, os.path.dirname(template_name))
        name = os.path.basename(template_name)
        
        result = []
        with os.scandir(target_dir) as it:
            for entry in it:
                if entry.name.startswith('.') or entry.is_dir():
                    continue
                if entry.name.startswith(name):
                    parts = entry.name.split('.', 2)
                    if len(parts) == 3:
                        base, engine, ext = parts
                    elif len(parts) == 2:
                        base, engine, ext = (parts[0], '', parts[1])
                    elif len(parts) == 1:
                        base, engine, ext = (parts[0], '', '')
                    result.append({
                        "path": entry.path,
                        "engine": engine,
                        "content_type": mimetypes.types_map.get('.' + ext, None),
                        "ext": '.' + ext
                    })
        return result
                    
                    
                
        
        
        
        
