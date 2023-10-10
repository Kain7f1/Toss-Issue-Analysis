import btm_module as btm
import utility_module as util

# content 폴더에 합칠걸 넣어주세요
folder_path = "./content"
util.create_folder(folder_path)
result_file_name = "crawling_result"

util.combine_csv_file(folder_path, result_file_name)

