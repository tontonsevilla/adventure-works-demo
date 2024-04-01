from xml.dom import minidom

def getXmlString(list):
    root = minidom.Document()
    xml = root.createElement('purchases') 
    root.appendChild(xml)

    for idx, item in enumerate(list):
        # create child element
        itemElement = root.createElement('item')
        itemDict = dict(list[idx])

        for key in itemDict.keys():
            itemElement.setAttribute(key, str(itemDict[key]))

        xml.appendChild(itemElement)
    
    return root.toprettyxml(indent ="\t")