import os
import re
import csv

class MovieCollector:
    def __init__(self, pathList, showDuplicate):
        self.path_list = pathList
        self.showDuplicate = showDuplicate

    def createCSV(self, list):
        print('creating csv......')
        fileName = 'REPORT.csv'
        full_path = os.path.join(".", fileName)

        with open(full_path, 'w') as csvfile:
            fieldnames = ['company', 'id', 'path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for oneIndex, oneItem in enumerate(list):
                writer.writerow({
                    'company': oneItem['c'],
                    'id': oneItem['i'],
                    'path': oneItem['d']
                })

    def addToList(self, list, name, dir):
        regStr = "^[a-zA-Z]{3,7}(|-)[0-9]{3,5}"
        p = re.compile(regStr)
        if p.match(name):
            shortName = re.search(regStr, name).group(0)
            name_grp = re.split('(\d.*)', shortName)
            list.append({
                "c": name_grp[0],
                "i": name_grp[1],
                "d": dir
            })

    def change_format(self, str):
        str1 = str.replace("-", "")
        str2 = str1.lower()
        return str2

    def start(self):
        list = []
        for cwd in self.path_list:
            print('analysizing directory: %s ...' % (cwd))

            for root, dirs, files in os.walk(cwd):
                if len(dirs) < 1:
                    # normal folders
                    fanName0 = os.path.basename(root)
                    fanName = self.change_format(fanName0)
                    self.addToList(list, fanName, root)
                elif len(files) > 1 and len(dirs) > 0:
                    # files without parent folder
                    fanName = os.path.basename(root)
                    for oneFile in files:
                        fileName = os.path.splitext(oneFile)[0]
                        if fileName != '.DS_Store':
                            name = self.change_format(os.path.splitext(oneFile)[0])
                            self.addToList(list, name, root)


        list.sort(key=lambda x: x['c'] + x['i'])

        if self.showDuplicate:
            print("generating the duplication list: ")
            newResult = []
            end = len(list) - 1
            for oneIndex, oneItem in enumerate(list):
                if oneIndex < end and oneItem['c'] == list[oneIndex + 1]['c'] and oneItem['i'] == list[oneIndex + 1]['i']:
                    newResult.append(oneItem)
                    newResult.append(list[oneIndex + 1])
            print("create duplication list...")
            list = newResult

        self.createCSV(list)
        print('finished!')
        return list