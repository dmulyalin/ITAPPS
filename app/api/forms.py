location_create_form = {
      "labels": {
          "mandatory": ["Location"], 
          "optional": []
      },
      "properties": {
          "mandatory": [
              {"propertyName": "name", "propertyType": "string", "propertyValue": ""}, 
              {"propertyName": "address", "propertyType": "string", "propertyValue": ""}
          ], 
          "optional":[
              {"propertyName": "description", "propertyType": "string", "propertyValue": ""}
          ],
          "types": ["string", "integer", "boolean", "note", "list"]
      }  
    }