from xml.dom import minidom
xmldoc = minidom.parse('testin.xml')
instance_node = xmldoc.getElementsByTagName('instance')[0]
contxt_node = instance_node.getElementsByTagName('context')[0]
print contxt_node.firstChild.nodeValue
print contxt_node.childNodes[0].data #use the first head, so surrounding texts are [0] and [2]
print contxt_node.childNodes[2].data
#head_node = contxt_node.getElementByTagName('head')[0]
