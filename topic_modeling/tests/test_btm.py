import btm_module as btm
import utility_module as util

# folder_path = "./content"
# result_file_name = "result"
# util.combine_csv_file(folder_path, result_file_name)


##########################################
# 기능 : 한글 문자열을 유니코드 UTF-8로 인코딩하여 반환합니다
# 입력 예시 : '에스엠'
# 리턴값 예시 : '.EC.97.90.EC.8A.A4.EC.97.A0'
def convert_to_unicode(s):
    return '.' + '.'.join(['{:02X}'.format(byte) for byte in s.encode('utf-8')])

input_string = "에스엠"
result = convert_to_unicode(input_string)
print(result)