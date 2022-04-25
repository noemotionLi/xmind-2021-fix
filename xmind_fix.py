# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:40:52 2022
此代码实质上是补充了在META-INF目录下的manifest.xml
原理： 打开xmind文件，获取目录，生成xml，添加目录文件META-INF/manifest.xml，大功告成
模块均为xml, tempfile, os, zipfile
函数 _get_filename 获取目录
xml_writer 生成文件
@author: 10291
"""

# 引入xml.dom模块
import xml.dom
import tempfile
import os
import zipfile

def _get_filename(file_name):
    '''
    用于获取xmind文件解压缩后的文件路径
    '''
    # 打开xmind文件，获取目录
    f = zipfile.ZipFile(file_name)

    # 需要按照父节点、子孙节点进行划分
    path_list = []
    for name in f.namelist():
        temp_list = name.split('/')
        # print(name)
        temp_str = ''
        for i in range(name.count('/')+1):
            temp_str += '/' + temp_list[i]
            temp = temp_str.replace('/','',1)
            path_list.append(temp)
    path_list = list(set(path_list))
    
    # not a valid XMind File 报错，就是因为没有以下路径
    path_list.insert(0,'META-INF')
    path_list.insert(1,'META-INF/manifest.xml')
    f.close()
    
    # 判别文件类型，将目录改变成需要的格式
    def type_check(file_path):
        if os.path.splitext(file_path)[1] == '.xml':
            type_media = 'text/xml'
        elif os.path.splitext(file_path)[1] == '.png':
            type_media = 'image/png'
        else : 
            type_media = ''
            file_path += '/'
        return type_media,file_path
    
    # 组装
    temp_list = []
    for wrong_path in path_list:
        media_type,file_path = type_check(wrong_path)
        # full_path = wrong_path.replace('\\','/')
        temp_list.append([media_type,file_path])
    return temp_list

def xml_writer(Attr_value):
    '''
    创建xml文件，将xmind目录写入
    未来可能需要修改的地方有password和xmlns，现已经写"死"
    '''
    # 获得DOMImplementation对象
    domImp = xml.dom.getDOMImplementation()
     
    # 通过DOMImplementation对象创建Document对象
    doc = domImp.createDocument(None, None, None)
     
    # 为Document对象添加root节点
    rootNode = doc.createElement("manifest")
    doc.appendChild(rootNode)
    
    # 创建属性并添加到节点
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
    # 文件名
    file_name = 'demo.xmind'
    
    # 调用_get_filename()获取xmind目录
    target_list = _get_filename(file_name)
    # 调用xml_writer构建xml文件
    xml_doc = xml_writer(target_list)
    
    # 创建一个临时文件夹
    directory_name = tempfile.mkdtemp()
    
    # 将xml_doc写入临时文件夹
    xml_path = os.path.join(directory_name,"manifest.xml")
    with open(os.path.join(xml_path), 'w', encoding='utf-8') as writer:
        xml_doc.writexml(writer, indent='\n', addindent="", newl="", encoding="utf-8")
    
    # 只需要将xml文件加入xmind中即可
    f = zipfile.ZipFile(file_name,'a')
    f.write(xml_path,'META-INF/manifest.xml')
    f.close()
