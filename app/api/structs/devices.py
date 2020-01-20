nodes = {
    
    "base" :{
      "labels": {
          "mandatory": ["Device"], 
          "optional": []
      },
      "properties": {
          "mandatory": [
              {"propertyName": "hostname", "propertyType": "string", 
               "propertyValue": "", "unique": True, "propertyInfo": "Unique name of device"}
          ], 
          "optional":[
              {"propertyName": "description", "propertyType": "string", 
               "propertyValue": "", "propertyInfo": "Description of this device"},
              {"propertyName": "vendor", "propertyType": "string", 
               "propertyValue": "", "propertyInfo": "Name of device Vendor"}
          ],
          "types": ["string", "integer", "boolean", "note", "list"]
      }  
    },
    
    "Cisco_CORE" :{
      "labels": {
          "mandatory": ["Device", "Core"], 
          "optional": []
      },
      "properties": {
          "mandatory": [
              {"propertyName": "hostname", "propertyType": "string", 
               "propertyValue": "", "unique": True, "propertyInfo": "Unique name of device"}
          ], 
          "optional":[
              {"propertyName": "description", "propertyType": "string", 
               "propertyValue": "", "propertyInfo": "Description of this device"},
              {"propertyName": "vendor", "propertyType": "string", 
               "propertyValue": "", "propertyInfo": "Name of device Vendor"},
              {"propertyName": "role", "propertyType": "string", 
               "propertyValue": "", "propertyInfo": "Role of this device"},              
          ],
          "types": ["string", "integer", "boolean", "note", "list"]
      }  
    }
    
# next template here    
}

relatioships = {

    "link_l1" :{
      "labels":  ["Link", "L1"],
      "source": "",
      "target": "",
      "properties": {
          "mandatory": [], 
          "optional": [],
          "types": ["string", "integer", "boolean", "note", "list"]
      }  
    }
 
# next template here   
}

menu = {}