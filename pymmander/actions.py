class Mkdir():
    def __init__(self, filemanager, src):
        self.fm = filemanager
        self.src = src
        self.exception_text = "File exists"
        self.success_text = "Directory created"

    def set_response(self, response):
        self.name = response

    def run(self):
        self.fm.mkdir(self.src, self.name)

class Rename():
    def __init__(self, filemanager, src):
        self.fm = filemanager
        self.src = src
        self.exception_text = "File exists"
        self.success_text = "Changed name"

    def set_response(self, response):
        self.name = response

    def run(self):
        self.fm.rename(self.src, self.name)

class Rm():
    def __init__(self, filemanager, src):
        self.fm = filemanager
        self.src = src
        self.exception_text = f"Not removing {src}"
        self.success_text = f"Removed {src}"

    def set_response(self, response):
        self.remove = response.lower() in ('y', 'yes', 'tak')

    def run(self):
        if self.remove:
            self.fm.rm(self.src)
        else:
            raise Exception()
    