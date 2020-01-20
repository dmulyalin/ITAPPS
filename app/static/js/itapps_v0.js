var MainApp = angular.module('MainApp', ['ngRoute', 'ngMaterial', 'ngMessages']);

MainApp.config(function($routeProvider) {
  $routeProvider.
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
    when('/devices', {
      templateUrl: '/devices/devices.html',
      controller: 'DevicesListCtrl'
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
      redirectTo: '/'
    });
});
   
// Customize colouring
MainApp.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue-grey')
    .accentPalette('grey')
    .warnPalette('red');
});
    
MainApp.factory('FUNCTIONS', function($http){
  return {
    shared_data: {},
    list: function (callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/locations?brief=True',
        headers: {"Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"},
        cache: true
      }).then(callback, null);
    },
    list_devices: function (callback){
      $http({
        method: 'GET',
        url: 'http://192.168.64.128:9000/api/devices?brief=True',
        headers: {"Authorization": "Bearer hmuWG750nIxTHEfTIjLtjviX6udcURR2"},
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
  FUNCTIONS.list_devices(function(response) {
    $scope.devices = response.data.data;
    for (var i = 0; i < $scope.devices.length; i++) {
            $scope.devices[i].checkbox = false
        }      
    // save Devices in shared data so that can access it from other controllers
    FUNCTIONS.shared_data.devices = $scope.devices
  });
  // function to set checkbox selected to all items in the table if header checkbox checkecd
  $scope.checkboxAll = function() {
    for (var i = 0; i < $scope.devices.length; i++) {
            $scope.devices[i].checkbox = $scope.devices.checkboxAll
        }        
  };
  // define search criterias section
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
  $scope.get_node_templates = function() {      
      FUNCTIONS.get_device_templates(function(response) {
          $scope.node_templates = response.data;
          $scope.node_template = $scope.node_templates[0]
          $scope.load_device_model(template_name=$scope.node_template);
        });
  };
    
  //function to load Device model from server, that model will be used to prefill csv form
  $scope.load_device_model = function(template_name) {
      FUNCTIONS.get_device_template(template_name=template_name, function(response) {
        $scope.device_node_model = response.data;
        $scope.device_node_model.csv={nodes:"", relationships:""};
        $scope.device_node_model.json={};
        $scope.device_node_model.config={};
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
    
  $scope.SubmitImportData = function() {
      FUNCTIONS.import_devices($scope.device_node_model, function(response) {
        // redirect to locations page and reload
        $window.location.href = "#!/devices"
        // log response to user
        $window.alert(JSON.stringify(response.data) + "  status:" + JSON.stringify(response.status))
        // reload current page to display new items
        $window.location.reload()
      })
  };
    
  // controller initialization code:
  $scope.get_node_templates();   

// end of this controller
});