nodes = { 
    
    "location_node_base": {
      "labels": {
          "mandatory": ["Location"], 
          "optional": []
      },
      "properties": {
          "mandatory": [
              {"propertyName": "name", "propertyType": "string", "propertyValue": "", "unique": True}, 
              {"propertyName": "address", "propertyType": "string", "propertyValue": ""}
          ], 
          "optional":[
              {"propertyName": "description", "propertyType": "string", "propertyValue": ""},
              {"propertyName": "postal code", "propertyType": "string", "propertyValue": "", "unique": True}
          ],
          "types": ["string", "integer", "boolean", "note", "list"]
      }  
    }
    
# next template here    
}

relatioships = {}

menu = {}