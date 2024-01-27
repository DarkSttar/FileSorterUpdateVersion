from threading import Thread
from time import sleep,time
from pathlib import Path
from multiprocessing import Process
import shutil


class Sorter():
    def __init__(self, path, sortedPath) -> None:
        self.path = path
        self.sortedPath = sortedPath
        self.folders = [] # Записуються шляхи папок які є в директорії, які треба посортувати 
        self.format_list = [] #Записуються формати знайдених файлів
        self.total_time = None
        self.count_files = 0
        self.count_format = 0
    
    
    def thread_sorting(self, path): 
        start_time = time()
        for item in path.iterdir(): 
            if item.is_dir():
                self.folders.append(item)
                self.count_find_folders += 1
                pathx = Path(item)
                self.thread_sorting(pathx)
            else:
                pr = Thread(target=self.move_file, args=(item,))
                pr.start()
                self.count_files += 1
        end_time = time()
        self.total_time = end_time - start_time
        return 'Use Thread'
    
    def process_sorting(self, path): 
        start_time = time()
        for item in path.iterdir(): 
            if item.is_dir():
                self.folders.append(item)
                self.count_find_folders += 1
                pathx = Path(item)
                self.process_sorting(pathx)
            else:
                pr = Process(target=self.move_file, args=(item,))
                pr.start()
                self.count_files += 1
        end_time = time()
        self.total_time = end_time - start_time
        return 'Use MultiProcessing'
    

    def standart_sorting(self, path): 
        start_time = time()
        for item in path.iterdir(): 
            if item.is_dir():
                self.folders.append(item)
                pathx = Path(item)
                self.standart_sorting(pathx)
            else:
                self.move_file(item)
                self.count_files += 1
        end_time = time()
        self.total_time = end_time - start_time
        return 'Use Base'
    
    
    
    
    def move_file(self, file): 
        suffix = file.suffix
        if not suffix in self.format_list:
            self.format_list.append(suffix)
            self.count_format += 1
            
        currentFolder = Path(str(self.sortedPath) + '\\' + str(suffix))
        currentFolder.mkdir(parents=True, exist_ok=True)
        path = Path(str(currentFolder) + '\\' + str(file.name))
        
        shutil.move(file, path)
        print(path)

  

    def Start(self, path):
        self.print_result(self.standart_sorting(path))# тут вказати функцію за допомогою якої будуть сортвуватись файли
        #process_sorting(path)
        #thread_sorting(path)
        
        
        

    def print_result(self,type_app):
        sleep(5)
        print(f'{"*" * 100}')
        print(type_app)
        print(f'Total Time: {self.total_time}')
        print(f'Count Files: {self.count_files}')      
        print(f'Count Format: {self.count_format}')
        print(f'{"*" * 100}')
            


    

if __name__ == "__main__":
    folder_for_sorting = Path('C:\\Users\\DarkStar\\Desktop\\SortingFolder') # Папка в якій будуть сортуватися файли по форматам
    Garbage = Path('C:\\Users\\DarkStar\\Desktop\\SortingFolder1') # Папка зі сміттям
    sorter = Sorter(Garbage,folder_for_sorting)
    sorter.Start(Garbage)
    

