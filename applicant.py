from common_def import OUTPUT_FILE_SEPARATOR


class Applicant:
    def __init__(self, name, applicant_seq):
        self.name = name
        self.applicant_seq = applicant_seq

    def output(self, fs, ida):
        if fs is None:
            return
        fs.write("{1}{0}{2}{0}{3}\n".format(OUTPUT_FILE_SEPARATOR, ida, self.applicant_seq, self.name))
