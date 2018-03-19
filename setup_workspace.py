import requests
import json
import hcl
#User Configurable Vars
organization = "azc"
workspaceName = "CompanyXYZ-Application3"
ATLAS_TOKEN = "Bearer c6dlOIUOp9IPhA.atlasv1.e5KpWCdKJ8ZtIRdzzEmmHg3yiMzL2l866FLNblMtEd7CKDbayzXG7I5v6LPFfb5EFTg"

#Base configurations
headers = {'Authorization': ATLAS_TOKEN, 'Content-Type' : 'application/vnd.api+json'}
createWorkspaceURL = "https://app.terraform.io/api/v2/organizations/"+organization+"/workspaces"
createVariablesURL = "https://app.terraform.io/api/v2/vars"

#todo: 404 - workspace not found, 422 variables already present

def getoAuthToken(organization):
  r = requests.get('https://app.terraform.io/api/v2/organizations/'+organization+'/oauth-tokens', headers=headers)
  response = json.loads(r.text)
  return response['data'][0]['id']

def createVarPayload(varName,defaultVal,organization,workspaceName,category,sensitive):
  varPayload = {
  "data": {
    "type":"vars",
    "attributes": {
      "key":varName,
      "value":defaultVal,
      "category":category,
      "hcl":"false",
      "sensitive":sensitive
     }
  },
  "filter": {
    "organization": {
      "name":organization
    },
    "workspace": {
      "name":workspaceName
    }
  }
  }
  return varPayload

def createWorkspacePayload(vcsOrganization,vcsWorkspace,tfeWorkspaceName,workingDirectory,tfeOrganization):
  oAuthToken = getoAuthToken(tfeOrganization)
  workspacePayload = {
  "data": {
    "attributes": {
      "name":tfeWorkspaceName,
      "working-directory": workingDirectory,
      "vcs-repo": {
        "identifier": vcsOrganization+"/"+vcsWorkspace,
        "oauth-token-id": oAuthToken,
        "branch": "",
        "default-branch": "true"
      }
    },
    "type":"workspaces"
  }
  }
  print json.dumps(workspacePayload)  
  return workspacePayload

def createWorkspace():
  payload = createWorkspacePayload("AdamCavaliere","terraform-aws-examples",workspaceName,"application-config",organization)
  try:
    r = requests.post(createWorkspaceURL, headers=headers, data=json.dumps(payload))
  except:
    print r.raise_for_status()

def createVariables():
  with open('variables.tf', 'r') as fp:
      obj = hcl.load(fp)

  for k, v in obj['variable'].items():
    varName = k
    for k2, v2 in v.items():
      if k2 == 'default':
        defaultVal = v2
    try:
      defaultVal
    except:
      defaultVal = " "
    payload = createVarPayload(varName,defaultVal,organization,workspaceName,"terraform","false")
    try:
      r = requests.post(createVariablesURL, headers=headers, data=json.dumps(payload))
    except:
      print r.raise_for_status()

def setEnvVariables():
  with open('envVars.json', 'r') as fp:
    obj = json.load(fp)
    for k,v in obj['data'].items():  
      payload = createVarPayload(k,v['value'],organization,workspaceName,v['vartype'],v['sensitive'])
      try:
        r = requests.post(createVariablesURL, headers=headers, data=json.dumps(payload))
      except:
        print r.raise_for_status()

createWorkspace()
setEnvVariables()
createVariables()

