# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:40:52 2022

@author: 10291
"""

# 引入xml.dom模块
import xml.dom
import tempfile
import os
import zipfile

def _get_filename(file_name):
    # 打开xmind文件，获取目录
    f = zipfile.ZipFile(file_name)
    # path_list = f.namelist()
    # path_list.insert(0,'META-INF')
    # path_list.insert(1,'META-INF/manifest.xml')
    # f.close()
    
    # 重复步骤，可以删除
    path_list = []
    print(len(f.namelist()))
    for name in f.namelist():
        temp_list = name.split('/')
        # print(name)
        temp_str = ''
        for i in range(name.count('/')+1):
            temp_str += '/' + temp_list[i]
            temp = temp_str.replace('/','',1)
            path_list.append(temp)
    path_list = list(set(path_list))
    path_list.insert(0,'META-INF')
    path_list.insert(1,'META-INF/manifest.xml')
    f.close()
    
    # 将目录改变成需要的格式（）
    def type_check(file_path):
        if os.path.splitext(file_path)[1] == '.xml':
            type_media = 'text/xml'
        elif os.path.splitext(file_path)[1] == '.png':
            type_media = 'image/png'
        else : 
            type_media = ''
            file_path += '/'
        return type_media,file_path
    
    temp_list = []
    for wrong_path in path_list:
        media_type,file_path = type_check(wrong_path)
        # full_path = wrong_path.replace('\\','/')
        temp_list.append([media_type,file_path])
    return temp_list

def xml_writer(Attr_value):
    '''
    创建xml文件，将xmind目录写入
    未来可能需要修改的地方有password和xmlns，现已经写死
    '''
    # 获得DOMImplementation对象
    domImp = xml.dom.getDOMImplementation()
     
    # 通过DOMImplementation对象创建Document对象
    doc = domImp.createDocument(None, None, None)
     
    # 为Document对象添加root节点
    rootNode = doc.createElement("manifest")
    doc.appendChild(rootNode)
    
    # 创建属性并添加到节点
    # passwordAtt = doc.createAttribute("password-hint")
    # xmlnsAtt = doc.createAttribute("xmlns")
    # mediaAtt = doc.createAttribute("media-type")
    # pathAtt = doc.createAttribute("full-path")
    doc.createAttribute("password-hint")
    doc.createAttribute("xmlns")
    doc.createAttribute("media-type")
    doc.createAttribute("full-path")
    # 未来可能需要修改
    rootNode.setAttribute("password-hint","")
    rootNode.setAttribute("xmlns","urn:xmind:xmap:xmlns:manifest:1.0")
    
    # 遍历添加子节点
    def add_node(root, value):
        child = doc.createElement("file-entry")
        root.appendChild(child)
        child.setAttribute("media-type",value[0])
        child.setAttribute("full-path",value[1])
    for value in Attr_value:
        add_node(rootNode, value)
    return doc


if __name__ == "__main__":
    # 调用_get_filename()获取xmind目录
    file_name = '地圖概說.xmind'
    target_list = _get_filename(file_name)
    print(len(target_list))
    # 调用xml_writer构建xml文件
    xml_doc = xml_writer(target_list)
    
    # 创建一个临时文件夹
    directory_name = tempfile.mkdtemp()
    
    # 将xml_doc写入临时文件夹
    xml_path = os.path.join(directory_name,"manifest.xml")
    with open(os.path.join(xml_path), 'w', encoding='utf-8') as writer:
        xml_doc.writexml(writer, indent='\n', addindent="", newl="", encoding="utf-8")
    
    f = zipfile.ZipFile(file_name,'a')
    f.write(xml_path,'META-INF/manifest.xml')
    f.close()
