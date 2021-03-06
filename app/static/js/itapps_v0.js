var MainApp = angular.module('MainApp', ['ngRoute', 'ngMaterial', 'ngMessages']);

MainApp.config(function($routeProvider) {
  $routeProvider.
    when('/frontpage/', {
      templateUrl: '/front_page.html',
      controller: 'frontPageController'
    }).
    when('/locations', {
      templateUrl: '/locations/list.html',
      controller: 'LocationsListCtrl'
    }).
    when('/locations/create', {
      templateUrl: '/locations/create.html',
      controller: 'LocationCreateCtrl'
    }).
    // MUST follow at the end as would match other URLs!!!!!
    when('/locations/:locationId', {
      templateUrl: '/locations/location.html',
      controller: 'LocationDetailCtrl'
    }).
    when('/devices/table', {
      templateUrl: '/devices/devices_table.html',
      controller: 'DevicesListCtrl'
    }).
    when('/devices/3d', {
      templateUrl: '/devices/devices_3d.html',
      controller: 'Devices3dCtrl'
    }).
    when('/devices/create', {
      templateUrl: '/devices/create.html',
      controller: 'DeviceCreateCtrl'
    }).
    when('/devices/import', {
      templateUrl: '/devices/import.html',
      controller: 'DeviceImportCtrl'
    }).
    // MUST follow at the end as would match other URLs!!!!!
    when('/devices/:deviceId', {
      templateUrl: '/devices/device.html',
      controller: 'DeviceDetailCtrl'
    }).
    otherwise({
      redirectTo: '/frontpage'
    });
});
   
// Customize colouring
MainApp.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue-grey')
    .accentPalette('grey')
    .warnPalette('red');
});
    
// custom directives
//
// File upload directives
MainApp.directive('addFile', function (FUNCTIONS) {
    return {
        restrict: "A",
        link: function ($scope, element, attr) {
            element.bind('change', function () {
                var formData = new FormData();
                formData.append(element[0].form.elements[0].name, element[0].form.elements[0].files[0]);
                // add files info to $scope
                $scope.device_node_model.config.files.push({
                    fileData: formData,
                    fileName: element[0].form.elements[0].files[0].name
                })
                //FUNCTIONS.upload(formData);
            });

        }
    };
});

// factory functions
MainApp.factory('FUNCTIONS', function($http){
  return {
    shared_data: {},
    upload: function (data) {
        $http({
            url: 'http://192.168.64.128:9000/api/misc/upload',
            method: "POST",
            data: data,
            headers: {
                'Content-Type': undefined,
                "Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"
            }
        }).then(function(response) {
          console.log("Success", response.status, response.data)
        }, function(response) {
          console.log("Error", response.status, response.data)
      });
    },
    list: function (callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/locations?brief=True',
        headers: {"Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"},
        cache: true
      }).then(callback, null);
    },
    list_devices: function (pagination, callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/devices?brief=True',
        headers: {
            "Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"
        },
        params: pagination,
        cache: true
      }).then(callback, null);
    },
    find: function(id, callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/locations/' + id,
        headers: {"Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"},
        cache: true
      }).then(callback);
    },
    find_device: function(id, callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/devices/' + id,
        headers: {"Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"},
        cache: true
      }).then(callback);
    },
    get_location_model: function(callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/locations/templates',
        headers: {"Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"},
        cache: true
      }).then(callback);
    },
    create_location: function(data) {
      $http({
        method: 'POST',
        url: 'http://192.168.64.128:9000/api/locations/create',
        headers: {
            "Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2",
            'Content-Type': 'application/json; charset=utf-8'
        },
        data: data
      }).then(function(response) {
          console.log("Success", response.status, response.data)
        }, function(response) {
          console.log("Error", response.status, response.data)
      });
    },
    delete_location: function(data) {
      $http({
        method: 'POST',
        url: 'http://192.168.64.128:9000/api/locations/delete',
        headers: {
            "Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2",
            'Content-Type': 'application/json; charset=utf-8'
        },
        data: data
      }).then(function(response) {
          console.log("Success", response.status, response.data)
        }, function(response) {
          console.log("Error", response.status, response.data)
      });
    },
    get_base_menu_data: function(callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/misc/base_menu',
        headers: {"Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"},
        cache: true
      }).then(callback);
    },
    get_device_template: function(template_name, callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/devices/templates?template_name=' + template_name,
        headers: {"Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"},
        cache: true
      }).then(callback);
    },
    get_device_templates: function(callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/devices/templates?template_name=_list_all_',
        headers: {"Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"},
        cache: true
      }).then(callback);
    },
    get_ttp_templates: function(callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/misc/ttp_templates?template_name=_list_all_',
        headers: {"Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"},
        cache: true
      }).then(callback);
    },
    create_device: function(data) {
      $http({
        method: 'POST',
        url: 'http://192.168.64.128:9000/api/devices/create',
        headers: {
            "Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2",
            'Content-Type': 'application/json; charset=utf-8'
        },
        data: data,
        cache: false
      }).then(function(response) {
          console.log("Success", response.status, response.data)
        }, function(response) {
          console.log("Error", response.status, response.data)
      });
    },
    delete_device: function(data, callback) {
      $http({
        method: 'POST',
        url: 'http://192.168.64.128:9000/api/devices/delete',
        headers: {
            "Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2",
            'Content-Type': 'application/json; charset=utf-8'
        },
        data: data,
        cache: false
      }).then(function(response) {
          console.log("Success", response.status, response.data)
        }, function(response) {
          console.log("Error", response.status, response.data)
      });
    },
    import_devices: function(data, callback) {
      $http({
        method: 'POST',
        url: 'http://192.168.64.128:9000/api/devices/import',
        headers: {
            "Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2",
            'Content-Type': 'application/json; charset=utf-8'
        },
        data: data,
        cache: false
      }).then(callback);
    },
    get_devices_graph: function (parameters, callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/devices/3d/graph_data',
        headers: {
            "Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2",
            'Content-Type': 'application/json; charset=utf-8'
        },
        params: parameters,
        cache: true
      }).then(callback, null);
    }
      
// paste more functions ABOVE this line
  };
});
       
MainApp.controller('LocationsListCtrl', function ($scope, FUNCTIONS){
  FUNCTIONS.list(function(response) {
    $scope.locations = response.data.data;
    for (var i = 0; i < $scope.locations.length; i++) {
            $scope.locations[i].checkbox = false
        }      
    // save locations in shared data so that can access it from other controllers
    FUNCTIONS.shared_data.locations = $scope.locations
  });
  // function to set checkbox selected to all items in the table if header checkbox checkecd
  $scope.checkboxAll = function() {
    for (var i = 0; i < $scope.locations.length; i++) {
            $scope.locations[i].checkbox = $scope.locations.checkboxAll
        }        
  };
  // define search criterias section
  $scope.search_template = {
      labels: ["location"],
      properties: [],
      property_types: ["string", "integer", "boolean", "note", "list"]
  }
  $scope.addSearchProperty = function() {
      $scope.search_template.properties.push({"propertyName": "", "propertyType": "", "propertyValue": "", "chips": []})
  };
  $scope.removeSearchProperty = function(property) {
      var itemIndex = $scope.search_template.properties.indexOf(property)
      $scope.search_template.properties.splice(itemIndex, 1)
  };
});
    
MainApp.controller('LocationDetailCtrl', function ($scope, $routeParams, FUNCTIONS){
  FUNCTIONS.find($routeParams.locationId, function(location) {
    $scope.location = location.data.data;
  });
});
    
MainApp.controller('LocationCreateCtrl', function ($scope, $window, FUNCTIONS){
  //load location create form model from server
  FUNCTIONS.get_location_model(function(response) {
    $scope.form_data = response.data;
    // add empty chips list to form_data optional properties
    for (var i = 0; i < $scope.form_data.properties.optional.length; i++) {
        $scope.form_data.properties.optional[i].chips = []
    }
  });
  $scope.addOptionalProperty = function() {
      $scope.form_data.properties.optional.push({"propertyName": "", "propertyType": "", "propertyValue": "", "chips": []})
  };
  $scope.removeOptionalProperty = function(property) {
      var itemIndex = $scope.form_data.properties.optional.indexOf(property)
      $scope.form_data.properties.optional.splice(itemIndex, 1)
  };
  $scope.SubmitForm = function(form) {
      if (form.$valid) {
          FUNCTIONS.create_location($scope.form_data)
          // redirect to locations page and reload
          $window.location.href = "#!/locations"
          $window.location.reload()
      }
  };
});
    
MainApp.controller('pageControls', function ($scope, $window, FUNCTIONS){
  $scope.deleteLocationsItems = function() {
      var delete_list = [];
      for (var i = 0; i < FUNCTIONS.shared_data.locations.length; i++) {
          location_item = FUNCTIONS.shared_data.locations[i]
          if (location_item.checkbox == true) {
              delete_list.push(location_item)
          }
      }      
      FUNCTIONS.delete_location(delete_list)
      // redirect to locations page
      $window.location.href = "#!/locations"
      $window.location.reload()
  };    

  $scope.deleteDevicesItems = function() {
      var delete_list = [];
      for (var i = 0; i < FUNCTIONS.shared_data.devices.length; i++) {
          device_item = FUNCTIONS.shared_data.devices[i]
          if (device_item.checkbox == true) {
              delete_list.push(device_item)
          }
      }      
      FUNCTIONS.delete_device(delete_list)
      // redirect to locations page
      $window.location.href = "#!/devices"
      $window.location.reload()
  };   
    
});
    
MainApp.controller('OverallCtrl', function ($scope, $mdSidenav, FUNCTIONS) {
  $scope.isSideNavOpen = false;
  $scope.menuIconVariable = "menu";
  $scope.menu_struct = [];
  //load base menu data
  FUNCTIONS.get_base_menu_data(function(response) {
    $scope.menu_struct = response.data;
    //console.log($scope.menu_struct)
    });
      
  $scope.toggleLeft = function() {
      // Uncomment to make navbar appear above content
      //$mdSidenav('left').toggle();
      $scope.isSideNavOpen = !$scope.isSideNavOpen;
      if ($scope.menuIconVariable == "menu") {
          $scope.menuIconVariable = "close";
      } else {
          $scope.menuIconVariable = "menu";
      };
    };
    
  $scope.onClick = function onClick(item) {
      //console.log(item);
    };
});

MainApp.controller('DevicesListCtrl', function ($scope, $window, FUNCTIONS){
  // table pagination section functions
  $scope.pagination = {
      rows_per_page: 10,
      rows_per_page_options: [5,10,15,30,50,80,100],
      page: 1,
      pages: [1,2,3,4,5,6],
      overall: 58,
      order_by: "hostname"
  };
  $scope.paginatePrev = function() {
      if ($scope.pagination.page != 1) {
          $scope.pagination.page -= 1 
          $scope.list_devices();
      } 
  }    
  $scope.paginateNext = function() {
      if  ($scope.pagination.page != $scope.pagination.pages.length) {
          $scope.pagination.page += 1 
          $scope.list_devices();
      }
  } 
  $scope.pageNumberSelector = function() {
      // reload devices list using new page value
      $scope.list_devices();
  }
  $scope.rowsPerPageSelector = function() {
      // reload devices list using rows per page value
      $scope.list_devices();
  }
    
  // function to list table content
  $scope.list_devices = function() {
    FUNCTIONS.list_devices($scope.pagination, function(response) {
      // console.log(response)
      $scope.devices = response.data.data;
      $scope.pagination.overall = response.data.meta.overall
      $scope.pagination.pages = response.data.meta.pages
      // console.log(response.data)
      for (var i = 0; i < $scope.devices.length; i++) {
              $scope.devices[i].checkbox = false
          }      
      // save Devices in shared data so that can access it from other controllers
      FUNCTIONS.shared_data.devices = $scope.devices
    });
  }
    
  // function to set checkbox selected to all items in the table if header checkbox checkecd
  $scope.checkboxAll = function() {
    for (var i = 0; i < $scope.devices.length; i++) {
            $scope.devices[i].checkbox = $scope.devices.checkboxAll
        }        
  };
    
  // search criterias section functions
  $scope.search_template = {
      labels: ["device"],
      properties: [],
      property_types: ["string", "integer", "boolean", "note", "list"]
  }
  $scope.addSearchProperty = function() {
      $scope.search_template.properties.push({"propertyName": "", "propertyType": "", "propertyValue": "", "chips": []})
  };
  $scope.removeSearchProperty = function(property) {
      var itemIndex = $scope.search_template.properties.indexOf(property)
      $scope.search_template.properties.splice(itemIndex, 1)
  };      
    
  // page init
  $scope.list_devices();
    
// end of this controller
});

MainApp.controller('Devices3dCtrl', function ($scope, $window, FUNCTIONS){
  $scope.parameters = [];
  $scope.gData = null;
  $scope.highlightNodes = [];
    
  $scope.show_3d_staff = function() {
    //query data from server
    FUNCTIONS.get_devices_graph($scope.parameters, function(response) {
      console.log(response)
      $scope.gData = response.data.data;
      console.log($scope.gData)
    //display graph 
    const Graph = ForceGraph3D()
      (document.getElementById('3d-graph'))
        .nodeLabel('hostname')
        .onNodeDragEnd(node => {
          node.fx = node.x;
          node.fy = node.y;
          node.fz = node.z;
        })
        .width(1000)
        .height(500)
        .nodeColor(node => $scope.highlightNodes.indexOf(node) === -1 ? 'rgba(0,255,255,0.6)' : 'rgb(255,0,0,1)')
        .onNodeClick(function(node) {
          if ($scope.highlightNodes.indexOf(node) === -1) {
              $scope.highlightNodes.push(node)
          }
          else {
              nodeIndex = $scope.highlightNodes.indexOf(node)
              $scope.highlightNodes.splice(nodeIndex, 1)
          }
          // trigger update of highlighted objects in scene
          Graph.nodeColor(Graph.nodeColor())
        })
        .graphData($scope.gData);
        
    });
  }
    
  // page init
  $scope.show_3d_staff();
    
// end of this controller
});


MainApp.controller('DeviceDetailCtrl', function ($scope, $routeParams, FUNCTIONS){
  FUNCTIONS.find_device($routeParams.deviceId, function(device) {
    $scope.device = device.data.data;
  });
});

MainApp.controller('DeviceCreateCtrl', function ($scope, $window, FUNCTIONS){
  //load Device create form model from server
  FUNCTIONS.get_device_template(template_name="base", function(response) {
    $scope.form_data = response.data;
    // add empty chips list to form_data optional properties
    for (var i = 0; i < $scope.form_data.properties.optional.length; i++) {
        $scope.form_data.properties.optional[i].chips = []
    }
  });
  $scope.addOptionalProperty = function() {
      $scope.form_data.properties.optional.push({"propertyName": "", "propertyType": "", "propertyValue": "", "chips": []})
  };
  $scope.removeOptionalProperty = function(property) {
      var itemIndex = $scope.form_data.properties.optional.indexOf(property)
      $scope.form_data.properties.optional.splice(itemIndex, 1)
  };
  $scope.SubmitForm = function(form) {
      if (form.$valid) {
          FUNCTIONS.create_device($scope.form_data)
          // redirect to locations page and reload
          $window.location.href = "#!/devices"
          $window.location.reload()
      }
  };
});

MainApp.controller('DeviceImportCtrl', function ($scope, $window, FUNCTIONS) {    
  $scope.node_templates = [];
  $scope.node_template = "";
  $scope.device_node_model = {};
    
  // function to load all available device node templates from server
  $scope.get_node_csv_templates = function() {      
      FUNCTIONS.get_device_templates(function(response) {
          $scope.node_templates = response.data;
          $scope.node_template = $scope.node_templates[0]
          $scope.load_device_model(template_name=$scope.node_template);
        });
  };
    
  // function to load all available TTP templates from server
  $scope.get_ttp_templates = function() {      
      FUNCTIONS.get_ttp_templates(function(response) {
          $scope.ttp_templates = response.data["ttp_templates"];
          $scope.ttp_template = null;
        });
  };
    
  //function to load Device model from server, that model will be used to prefill csv form
  $scope.load_device_model = function(template_name) {
      FUNCTIONS.get_device_template(template_name=template_name, function(response) {
        $scope.device_node_model = response.data;
        $scope.device_node_model.csv={nodes:"", relationships:""};
        $scope.device_node_model.json={};
        $scope.device_node_model.config = {
            text: [""],
            files: []
        }
        $scope.device_node_model.ttp_template = ""
        var mandatoryProps = []; var optionalProps = [];
        // get mandatory properties:
        for (var i = 0; i < $scope.device_node_model.properties.mandatory.length; i++) {
            mandatoryProps.push($scope.device_node_model.properties.mandatory[i].propertyName);
        };
        // get optional properties:
        for (var i = 0; i < $scope.device_node_model.properties.optional.length; i++) {
            optionalProps.push($scope.device_node_model.properties.optional[i].propertyName);
        };
        // form comma separated string of properties names:
        $scope.device_node_model.csv.nodes = mandatoryProps.join() + "," + optionalProps.join();      
      });
  };    
    
  $scope.SubmitImportData = function(element) {
      // upload files if any
      for (var i = 0; i < $scope.device_node_model.config.files.length; i++) {
        FUNCTIONS.upload($scope.device_node_model.config.files[i]["fileData"])
        $scope.device_node_model.config.files[i]["fileData"] = ""
      };
      console.log($scope.device_node_model)
      FUNCTIONS.import_devices($scope.device_node_model, function(response) {
        // redirect to locations page and reload
        $window.location.href = "#!/devices"
        // log response to user
        $window.alert(JSON.stringify(response.data) + "  status:" + JSON.stringify(response.status))
        // reload current page to display new items
        //$window.location.reload()
      })
  };    
    
 //$scope.UploadButton = function($event) {
 //    var element = angular.element($event.target)
 //    var formData = new FormData();
 //    formData.append(element[0].form.elements[0].name, element[0].form.elements[0].files[0]);
 //    //FUNCTIONS.upload(formData);
 //    $scope.device_node_model.config.files.push(element[0].form.elements[0].files[0])
 //    //console.log($scope.device_node_model)
 // };    
    
  // controller initialization code:
  $scope.get_node_csv_templates();  
  $scope.get_ttp_templates()

// end of this controller
});


MainApp.controller('frontPageController', function ($scope, $window, FUNCTIONS) {    
// end of this controller
});