from common_def import OUTPUT_FILE_SEPARATOR

class Event:
    def __init__(self, date, code,title, description):
        self.date = date
        self.code = code
        self.title = title
        self.description = description

    def output(self, fs, ida):
        if fs is None:
            return
        fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}\n".format(OUTPUT_FILE_SEPARATOR, ida, self.date, self.code, self.title, self.description))
