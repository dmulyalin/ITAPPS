"""
File to contain menu dictionaries used to build web gui menus and navigation bars
"""

# Main left sidenav menu:
main = [
    # Locations menu section
    {
        "name": "Geo",
        "submenu": [
            {
                "name": "Locations",
                "submenu": [],
                "url": "#!/locations"
            },
            {
                "name": "Racks",
                "submenu": [],
                "url": "#!/"
            }
        ],
        "url": "#!/"
    },
    
    # Hardware menu section
    {
        "name": "Hardware",
        "submenu": [
            {
                "name": "Devices",
                "submenu": [],
                "url": "#!/devices/table"
            },
            {
                "name": "Interfaces",
                "submenu": [
                    {
                        "name": "Ethernet",
                        "submenu": [
                            {
                                "name": "1G",
                                "url": "#!/"
                            },
                            {
                                "name": "10G",
                                "url": "#!/"
                            }
                        ],
                        "url": "#!/"
                    },
                    {
                        "name": "SDH",
                        "submenu": [],
                        "url": "#!/"
                    }
                ],
                "url": "#!/Interfaces"
            }
        ],
        "url": "#!/"
    }
]

# OLD menu:
old_menu = """
  <a class="navbar-brand" href="{{ url_for('home.homepage') }}">ITAPPS</a>

  <div class="collapse navbar-collapse">
    <ul class="navbar-nav mx-0">
      <!-- COmpanies dropdown menu -->
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Companies
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#">Organizations</a>
          <a class="dropdown-item" href="#">Departments</a>
          <a class="dropdown-item" href="#">Roles</a>
          <a class="dropdown-item" href="#">Persons</a>
        </div>
      </li>

      <!-- Geo dropdown menu -->
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Geo
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="{{ url_for('locations.locations_main_page') }}">Locations</a>
          <a class="dropdown-item" href="#">Racks</a>
        </div>
      </li>
      
      <!-- Hardware dropdown menu -->
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Hardware
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="{{ url_for('devices.list_devices') }}">Devices</a>
          <a class="dropdown-item" href="#">Vendors</a>
          <a class="dropdown-item" href="#">Licences</a>
          <a class="dropdown-item" href="#">Contracts</a>
        </div>
      </li>
        
      <!-- Switching dropdown menu -->
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Switching
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#">L2 Domains</a>
          <a class="dropdown-item" href="#">Vlans</a>
          <a class="dropdown-item" href="#">VXLAN</a>
          <a class="dropdown-item" href="#">VPLS</a>
          <a class="dropdown-item" href="#">PWE</a>
          <a class="dropdown-item" href="#">EVPN</a>
        </div>
      </li>
        
      <!-- Routing dropdown menu -->
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Routing
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#">L3 Domains</a>
          <a class="dropdown-item" href="#">VRF</a>
        </div>
      </li>
        
      <li class="nav-item">
        <a class="nav-link" href="{{ url_for('tools_import.tools_import') }}">Import</a>
      </li>   
    </ul>
      
    <!-- search form 
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
    -->

    <ul class="navbar-nav ml-auto">
      <!-- Admin dropdown menu -->
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Admin
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#">Users</a>
          <a class="dropdown-item" href="#">Roles</a>
        </div>
      </li>   
    
      <!-- logout link -->
      <li class="nav-item">
        <a class="nav-link" href="{{ url_for('auth.logout') }}">Logout</a>
      </li>   
    </ul>
  </div>
"""