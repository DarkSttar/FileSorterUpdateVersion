from pathlib import Path
from multiprocessing import Process, Manager,Semaphore
from time import time

#IMAGE
JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
PSD_IMAGES = [] 

#VIDEO
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []


#DOCUMENTS
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
HTM_DOCUMENTS = [] 
HTML_DOCUMENTS = [] 
#AUDIO
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []

#CODE
PYTHON_FILES = [] 
PYC_FILES = [] 
DLL_FILES = [] 
ADO_FILES = [] 

#OTHER
OTHER_FILES = []


REGISTER_EXTENTION = {
    
    ('IMAGES','JPEG') : JPEG_IMAGES,
    ('IMAGES','JPG') : JPG_IMAGES,
    ('IMAGES','PNG') : PNG_IMAGES, 
    ('IMAGES','SVG') : SVG_IMAGES,
    ('IMAGES','PSD') : PSD_IMAGES,
 
    ('VIDEO','AVI'): AVI_VIDEO, 
    ('VIDEO','MP4'): MP4_VIDEO, 
    ('VIDEO','MOV'): MOV_VIDEO,
    ('VIDEO','MKV'): MKV_VIDEO,
    
    ('DOCUMENTS','DOC'): DOC_DOCUMENTS, 
    ('DOCUMENTS','DOCX'): DOCX_DOCUMENTS, 
    ('DOCUMENTS','TXT'): TXT_DOCUMENTS, 
    ('DOCUMENTS','PDF') : PDF_DOCUMENTS, 
    ('DOCUMENTS','XLSX'): XLSX_DOCUMENTS,
    ('DOCUMENTS','PPTX'): PPTX_DOCUMENTS,
    ('DOCUMENTS','HTM') : HTM_DOCUMENTS,
    ('DOCUMENTS', 'HTML'):HTML_DOCUMENTS,
    ('AUDIO','MP3'):MP3_AUDIO,
    ('AUDIO','OGG'):OGG_AUDIO,
    ('AUDIO','WAV'):WAV_AUDIO,
    ('AUDIO','AMR'): AMR_AUDIO,
    
    ('CODE','PY'): PYTHON_FILES,
    ('CODE','PYC'): PYC_FILES,
    ('CODE','DLL'): DLL_FILES,
    ('CODE','ADO'): ADO_FILES,
    'OTHER':OTHER_FILES,
    'TYPES':['IMAGES','VIDEO','AUDIO','DOCUMENTS','CODE','OTHER_FILES_TYPE']
}

import os
from pathlib import Path
from threading import Thread, Semaphore
from multiprocessing import Process, Manager
from time import time

# Решта коду ...

class Sorter:
    def __init__(self, gargage: Path, sorting_path: Path):
        self.garbage = gargage
        self.sorting_path = sorting_path
        self.count_cpu = os.cpu_count()
        self.total_time = None
        self.count_files = 0
    def scan_directory(self,path):
        for item in path.iterdir():
            if item.is_dir():
                
                self.scan_directory(item)
            else:
                suffix = item.suffix
                suffix = suffix[1::].upper()
                self.get_files(item,suffix)
    def get_files(self,file,suffix):
        for key,value in REGISTER_EXTENTION.items():
            if suffix in key and suffix != '':
                value.append(file)
                return
        REGISTER_EXTENTION['OTHER'].append(file)


    def sorting_process(self):  
        processes = []
        for type in REGISTER_EXTENTION['TYPES']:            
            process = Process(target=self.sorting, args=(type,REGISTER_EXTENTION,self.count_files))
            processes.append(process)
        for item in processes:
            item.start()
        [th.join() for th in processes]
        return 'USE MULTIPROCESSING'
    

    def sorting(self,type,reg_ext,count_files):

           
        if type != 'OTHER_FILES_TYPE':
                for key,value in reg_ext.items():
                
                    if type in key:
                        
                        for file in reg_ext[key]:
                            current_path = Path(str(self.sorting_path) + '\\' + key[0] + '\\' + key[1])
                            current_path.mkdir(parents=True,exist_ok=True)
                            os.replace(file, Path(str(current_path) + '\\' + str(file.name)))
                            self.count_files += 1
        else:
            for file in reg_ext['OTHER']:
                current_folder = Path(str(self.sorting_path) + '\\' + 'OTHER')
                current_folder.mkdir(parents=True, exist_ok=True)
                os.replace(file,Path(str(current_folder) + '\\' + str(file.name)))
                    
                self.count_files += 1
            
        return self.count_files
    
    def print_result(self,type_app):
        print(f'{"*" * 100}')
        print('IMAGES ')
        print(f'JPEG ==> {len(JPEG_IMAGES)}')
        print(f'JPG  ==> {len(JPG_IMAGES)}' )
        print(f'PNG  ==> {len(PNG_IMAGES)}')
        print(f'SVG  ==> {len(SVG_IMAGES)}')
        print(f'PSD  ==> {len(PSD_IMAGES)}')
        print(f'{"*" * 100}')
        print(f'VIDEO ')
        print(f'AVI  ==> {len(AVI_VIDEO)}')
        print(f'MP4  ==> {len(MP4_VIDEO)}')
        print(f'MKV  ==> {len(MKV_VIDEO)}')
        print(f'MOV  ==> {len(MOV_VIDEO)}')
        print(f'{"*" * 100}')
        print('DOCUMENTS')
        print(f'DOC  ==> {len(DOC_DOCUMENTS)}')
        print(f'DOCX ==> {len(DOCX_DOCUMENTS)}')
        print(f'TXT  ==> {len(TXT_DOCUMENTS)}')
        print(f'PDF  ==> {len(PDF_DOCUMENTS)}')
        print(f'XLSX ==> {len(XLSX_DOCUMENTS)}')
        print(f'PPTX ==> {len(PPTX_DOCUMENTS)}')
        print(f'HTML ==> {len(HTML_DOCUMENTS)}')
        print(f'HTM  ==> {len(HTM_DOCUMENTS)}')
        print(f'{"*" * 100}')
        print('AUDIO')
        print(f'MP3  ==> {len(MP3_AUDIO)}')
        print(f'OGG  ==> {len(OGG_AUDIO)}')
        print(f'WAV  ==> {len(WAV_AUDIO)}')
        print(f'AMR  ==> {len(AMR_AUDIO)}')
        print(f'{"*" * 100}')
        print('CODE_FILES')
        print(f'PY  ==> {len(PYTHON_FILES)}')
        print(f'PYC ==> {len(PYC_FILES)}')
        print(f'DLL ==> {len(DLL_FILES)}')
        print(f'ADO ==> {len(ADO_FILES)}')
        print(f'OTHER FILES ==> {len(OTHER_FILES)}')
        print(f'TOTAL FILES ==> {self.count_files}')
        print(type_app)
    def start_sorting(self):
        start_time = time()
        self.scan_directory(self.garbage)
        self.print_result(self.sorting_process())
        end_time = time()
        self.total_time = end_time - start_time
        print(f'TOTAL TIME ==> {self.total_time}')
        

if __name__ == "__main__":
    garbage =  Path('C:\\Users\\DarkStar\\Desktop\\SortingFolder1')
    sorting_path = Path('C:\\Users\\DarkStar\\Desktop\\SortingFolder')
    sorter = Sorter(garbage,sorting_path)

    sorter.start_sorting()