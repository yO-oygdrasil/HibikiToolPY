import hou

class BasicFunc(object):

    @staticmethod
    def setWorldPos(objNode, x, y, z, fail_on_locked_parms = False):
        worldTrans = objNode.worldTransform()
        worldTrans.setAt(3, 0, x)
        worldTrans.setAt(3, 1, y)
        worldTrans.setAt(3, 2, z)
        objNode.setWorldTransform(worldTrans, fail_on_locked_parms)

    @staticmethod
    def getWorldPos(objNode):
        if objNode:
            worldTrans = objNode.worldTransform()
            return hou.Vector3(worldTrans.at(3,0),worldTrans.at(3,1),worldTrans.at(3,2))
        else:
            return None


    @staticmethod
    def alignWorldPos(node, target, fail_on_locked_parms = False):
        worldTrans = node.worldTransform()
        targetWorldTrans = target.worldTransform()
        worldTrans.setAt(3,0,targetWorldTrans.at(3,0))
        worldTrans.setAt(3,1,targetWorldTrans.at(3,1))
        worldTrans.setAt(3,2,targetWorldTrans.at(3,2))
        node.setWorldTransform(worldTrans, fail_on_locked_parms)

    # @staticmethod
    # def updateGeoPointAttr(freezeGeo, attrName, attribType,  ptnum, attrValue):
    #     if freezeGeo:
    #         attr = freezeGeo.findPointAttrib(attrName)
    #         if not attr:
    #             attr = freezeGeo.addAttrib(attribType, attrName, )


    @staticmethod
    def create_deleteAttr_after(node, pointAttr = '*', vertAttr='*', primAttr='*',detailAttr='*'):
        # type : (hou.Node, str, str,str,str)->hou.Node
        # node = hou.Node()
        deleteAttrNode = BasicFunc.create_node_after(node, 'attribdelete')
        #deleteAttrNode.parm('pt')
        return deleteAttrNode

    @staticmethod
    def create_node_after(sourceNode, newNodeTypeName, sourceOutputIndex = 0, newNodeInputIndex = 0, newNodeOutputIndex = 0):
        # type : (hou.Node,str,int,int,int)->hou.Node
        sourceOutputName = sourceNode.outputNames()[sourceOutputIndex]
        newNode = sourceNode.parent().createNode(newNodeTypeName)
        inputName = newNode.inputNames()[newNodeInputIndex]
        newNode.setNamedInput(inputName, sourceNode,sourceOutputName)
        newNodeOutputName = newNode.outputNames()[newNodeOutputIndex]
        for targetConnection in newNode.outputConnections():
            targetConnection.inputNode().setNamedInput(targetConnection.inputName(), newNode, newNodeOutputName)
        return newNode

    @staticmethod
    def connect_node(sourceNode, targetNode, sourceOutputIndex = 0, targetNodeInputIndex = 0):
        sourceOutputName = sourceNode.outputNames()[sourceOutputIndex]
        inputName = targetNode.inputNames()[targetNodeInputIndex]
        targetNode.setNamedInput(inputName, sourceNode, sourceOutputName)

    @staticmethod
    def create_null_at_obj(targetNode, nodeName = None):
        selfPos = BasicFunc.getWorldPos(targetNode)
        earth = targetNode.parent()
        # print earth
        ctl = earth.createNode('null')
        if nodeName is None:
            nodeName = 'ctl_' + targetNode.name()
        ctl.setName(nodeName)
        BasicFunc.set_transform_keeppos(ctl)
        BasicFunc.setWorldPos(ctl, selfPos[0], selfPos[1], selfPos[2])
        return ctl

    @staticmethod
    def get_look_at_matrix(selfPos, targetPos, upDirection):
        zaxis = hou.Vector3(targetPos - selfPos).normalized()
        xaxis = upDirection.cross(zaxis).normalized()
        yaxis = zaxis.cross(xaxis)
        resultMatrix = hou.Matrix4()
        resultMatrix.setAt(0, 0, xaxis.x())
        resultMatrix.setAt(0, 1, yaxis.x())
        resultMatrix.setAt(0, 2, zaxis.x())
        resultMatrix.setAt(0, 3, 0)
        resultMatrix.setAt(1, 0, xaxis.y())
        resultMatrix.setAt(1, 1, yaxis.y())
        resultMatrix.setAt(1, 2, zaxis.y())
        resultMatrix.setAt(1, 3, 0)
        resultMatrix.setAt(2, 0, xaxis.z())
        resultMatrix.setAt(2, 1, yaxis.z())
        resultMatrix.setAt(2, 2, zaxis.z())
        resultMatrix.setAt(2, 3, 0)
        resultMatrix.setAt(3, 0, 0)#-xaxis.dot(selfPos))
        resultMatrix.setAt(3, 1, 0)#-yaxis.dot(selfPos))
        resultMatrix.setAt(3, 2, 0)#-zaxis.dot(selfPos))
        resultMatrix.setAt(3, 3, 1)
        return resultMatrix


    @staticmethod
    def get_nodes_in_children(node, nodeTypeName):
        result = []
        for child in node.children():
            if child.type().name() == nodeTypeName:
                result.append(child)
        return result

    @staticmethod
    def get_node_in_children(node, nodeTypeName):
        for child in node.children():
            if child.type().name() == nodeTypeName:
                return child

    @staticmethod
    def set_transform_keeppos(node, keeppos = True):
        kpParm = node.parm('keeppos')
        if kpParm:
            kpParm.set(keeppos)

    @staticmethod
    def set_children_transform_keeppos(node, keeppos = True):
        outputs = node.outputs()
        if outputs:
            for child in outputs:
                BasicFunc.set_transform_keeppos(child, keeppos)

    @staticmethod
    def print_node(node):
        print "path:", node.path(), " type:"+node.type().name()

    @staticmethod
    def print_nodes(nodes):
        for node in nodes:
            BasicFunc.print_node(node)

    @staticmethod
    def print_parms(node):
        for parm in node.parms():
            print parm

    @staticmethod
    def print_inputs(node):
        for inputName in node.inputNames():
            print '['+inputName+'] from ('
        # for input in node.inputs():
        #     print input

    @staticmethod
    def print_outputs(node):
        for outputName in node.outputNames():
            print outputName

    @staticmethod
    def adjustLayout(node,relative_to_inputs=True, move_inputs=False, move_outputs=True, move_unconnected=False):
        node.moveToGoodPosition(relative_to_inputs,move_inputs,move_outputs,move_unconnected)

    @staticmethod
    def layoutChildren(parentNode, childrenNodes = (),horizonOffset = -1,verticalOffset = -1):

        parentNode.layoutChildren(childrenNodes, horizonOffset, verticalOffset)
