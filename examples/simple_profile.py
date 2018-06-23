from yuuki.dispatch import action
import os
import veri_flow as flow
import veri_group as group

@action(target="openc2:domain")
def deny(target, actuator, modifier):
    """
    Note: return values are sent as the response to an OpenC2 cmd
    """
    return "Denying domain {}".format(target['URI'])

@action(target="openc2:domain")
def allow(target, actuator, modifier):
    """
    Docstring for each openc2 action is used for QUERY openc2:openc2
    """
    return "Allowing domain {}".format(target['URI'])

@action(target="openc2:domain")
def store(target, actuator, modifier):
    """
    parm URI is the location where file is stored
    parm URL is ODL IP
    """
    command = "curl -X GET -H \"Content-Type: application/json\" -H \"Accept: application/json\" --user admin:admin http://" + target['URL'] + ":8181/restconf/operational/opendaylight-inventory:nodes/ | jq '.' > " + target['URI']
    os.popen(command).read() 
    return "success"

@action(target="openc2:user")
def deny(target, actuator, modifier):
    """Each instance of the multimethod can have a unique docstring"""
    return "Denying user {}".format(target['name'])


@action(target="openc2:user")
def allow(target, actuator, modifier):
    return "Allowing user {}".format(target['name'])


@action(target="openc2:file", actuator="openc2:chmod")
def mitigate(target, actuator, modifier):
    return "Mitigating file with chmod"


@action(target="openc2:file", actuator="openc2:rm")
def mitigate(target, actuator, modifier):
    return "Mitigating file by deleting it"


def foo():
    return "I am not an OpenC2 action"

@action(target="openc2:flow")
def add(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-flow:add-flow"
    print command
    os.popen(command).read() 
    return "success"

@action(target="openc2:flow")
def upadte(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-flow:update-flow"
    os.popen(command).read() 
    return "success"

@action(target="openc2:flow")
def remove(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-flow:remove-flow"
    os.popen(command).read() 
    return "success"

@action(target="openc2:veri_flow")
def add(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    ##addflow
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-flow:add-flow"
    os.popen(command).read() 
    
    ##end
    ##verification
    xdict = flow._xml2dict(target['URI'])
    ftable,count = flow._flow_data('ovs-ofctl dump-flows s1')
    fid = flow._flow_id(xdict, ftable, count)
    if fid == -1:
        return "error"
    result = flow._verification(xdict, ftable, fid)
    return result
    ##end

@action(target="openc2:veri_flow")
def update(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    ##updateflow
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-flow:update-flow"
    os.popen(command).read() 
    
    ##end
    ##verification
    xdict = flow._xml2dict(target['URI'])
    ftable,count = flow._flow_data('ovs-ofctl dump-flows s1')
    fid = flow._flow_id_u(xdict, ftable, count)
    if fid == -1:
        return "error"
    result = flow._verification_u(xdict, ftable, fid)
    return result
    ##end

@action(target="openc2:veri_flow")
def remove(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    ##removeflow
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-flow:remove-flow"
    os.popen(command).read() 
    
    ##end
    ##verification
    xdict = flow._xml2dict(target['URI'])
    ftable,count = flow._flow_data('ovs-ofctl dump-flows s1')
    if ftable == "":
        return "correct"
    fid = flow._flow_id(xdict, ftable, count)
    if fid == -1:
        return "correct"
    else:
        return "error"
    ##end

@action(target="openc2:group")
def add(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-group:add-group"
    os.popen(command).read() 
    return "success"

@action(target="openc2:group")
def update(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-group:update-group"
    os.popen(command).read() 
    return "success"

@action(target="openc2:group")
def remove(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-group:remove-group"
    os.popen(command).read() 
    return "success"

@action(target="openc2:veri_group")
def add(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-group:add-group"
    os.popen(command).read() 
    ##verification
    xdict = group._xml2dict(target['URI'])
    gtable,count = group._group_data('ovs-ofctl dump-groups s1 -O Openflow13')
    gid = group._group_id(xdict, gtable, count)
    if gid == -1:
        return "error"
    result = group._verification(xdict, gtable, gid)
    return result
    ##end

@action(target="openc2:veri_group")
def update(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-group:update-group"
    os.popen(command).read() 
    ##verification
    xdict = group._xml2dict(target['URI'])
    gtable,count = group._group_data('ovs-ofctl dump-groups s1 -O Openflow13')
    gid = group._group_id_u(xdict, gtable, count)
    if gid == -1:
        return "error"
    result = group._verification_u(xdict, gtable, gid)
    return result
    ##end

@action(target="openc2:veri_group")
def remove(target, actuator, modifier):
    """
    parm URI is the location where POST Body file is stored
    parm URL is ODL IP
    """
    command = "curl -X POST -H \"Content-Type: application/xml\" -d @" + target['URI'] + " --user admin:admin http://" + target['URL'] + ":8080/restconf/operations/sal-group:remove-group"
    os.popen(command).read() 
    ##verification
    xdict = group._xml2dict(target['URI'])
    gtable,count = group._group_data('ovs-ofctl dump-groups s1 -O Openflow13')
    if gtable == "":
        return "correct"
    gid = group._group_id(xdict, gtable, count)
    if gid == -1:
        return "correct"
    else:
        return "error"
    ##end

