import os
import glob

# ============================================
'''
 dota开源数据集格式转数据堂标注平台格式
'''
# ============================================


# ================== 基础定义 ==================
# 输入文件夹
inputPath = r'D:\Datasets\DOTA-sample'

# 输出文件夹
outputPath = r'D:\ZTEST'

# Json模板
jsonHeader = '{"markResult": {"type": "FeatureCollection","features": ['
object_str = '{"type": "Feature","properties": {"objectId": %d,"content": {"label": "%s"},"generateMode": 2},' \
             '"geometry": {"type": "Square","coordinates": [[[%f,%f],[%f,%f],[%f,%f],[%f,%f],[%f,%f]]]}}'
jsonTail = ']}}'

# ================== 数据处理 ==================

# 设定工作目录
os.chdir(inputPath)

# 遍历包括子目录下的所有.txt文件
fileList = glob.glob('**/*.txt', recursive=True)

# 打印遍历到的.txt文件数量
print(f'发现了 {len(fileList)} 个文件')

fileCount = 1

# 循环读取原始文件，读一个处理生成一个JSON文件。
for file in fileList:
    # 原始文件的地址。例：D:\Datasets\DOTA-sample\P0000.txt
    fromFile = os.path.join(inputPath, file)

    # 生成的地址，例：D:\ZTEST\P0000.json 第一行直接通过字符串批量替换为JSON格式，注意，这个地方需要原始txt中没有json字样。
    toFile = os.path.join(outputPath, file.replace("txt", "json"))

    # 查看待生成的目录（尤其针对深层次目录的情况）是否存在，如果不存在则新建目录
    if not os.path.exists(os.path.dirname(toFile)):
        os.makedirs(os.path.dirname(toFile))

    # 打开输入的原始.txt文件，开始读取、写入JSON处理。
    with open(fromFile, "r+", encoding="utf-8") as ff:
        lines = ff.readlines()

        # 开始写入JSON文件。
        with open(toFile, "w+", encoding="utf-8") as tf:
            # 写JSON头部
            tf.write(jsonHeader)
            object_id = 1
            linesCount = len(lines)

            # 一行一行读入
            for line in lines:

                # dota特定的格式，不处理第一行和第二行。
                if line.startswith('image') or line.startswith('gsd'):
                    linesCount -= 1
                    continue
                else:
                    # 取到每一行后，按照空格分隔元素
                    element = line.split(" ")

                    # 对象json格式变量填入
                    object_i = object_str % (object_id, element[8], float(element[0]), float(element[1]),
                                             float(element[2]), float(element[3]), float(element[4]),
                                             float(element[5]), float(element[6]), float(element[7]),
                                             float(element[0]), float(element[1]))

                    # 最后一行不加
                    if object_id < linesCount:
                        tf.write(object_i + ',')
                    else:
                        tf.write(object_i)
                    object_id += 1
            # 写JSON尾部
            tf.write(jsonTail)
            print(f"第 {fileCount} 个文件处理完成")
            fileCount += 1

print(f'{len(fileList)} 个文件全部处理完成')
