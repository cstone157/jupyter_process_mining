from generator.tenlinesamplegenerator import *
from parser.tenlineparser import *

tmp = TenLineSampleGenerator(appendId=True)
fake_ten_line = tmp.generate_sample_data(100)

parser = TenLineParser()
results = parser.parse(fake_ten_line)

print(results[results["msg_cnt"] < 10])