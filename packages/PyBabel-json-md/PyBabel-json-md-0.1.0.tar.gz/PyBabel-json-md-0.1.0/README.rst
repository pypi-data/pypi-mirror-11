PyBabel-JSON-MD
===============

Release notes
-------------

- 0.1.0 - Initial Release

Pybabel-json-md is based loosely on pybabel-json which was written by Anton Bykov. Much of the logic is different in the way the parsing of the JSON file is handled as well as the handling of keys and the omission of the ngettext function, but, wanted to give credit to its predecessor. The code changes were significant enough to warrant a new version rather than attempt to make changes to the original.

The md portion of pybabel-json-md refers to MetaDef (i.e., Metadata Definitions) as described here:
`Openstack Metadata Definitions Catalog <http://specs.openstack.org/openstack/glance-specs/specs/juno/metadata-schema-catalog.html>`_

This Babel plugin is intended for use with Openstack Glance i18n efforts for Glance's Metadata Definitions Catalog.

Installation
------------
pip install pybabel-json-md

Usage
-----

- Add `[json_md: path/\*\*.json]` to a Babel config file (e.g., babel.cfg)

- Optionally, add in a 'name_list' to specify the names to filter with:

  name_list = display_name, description, title

- Run it with pybabel:

  pybabel extract -F babel.cfg -o sample.pot path-to-metadef-json-files

Key Features
------------

- By default the Value portion of all valid Key:Value pairs will be returned.

- Lists of strings are also supported.

- If you specify the 'name_list' option, the program will return just the string values associated with the key names supplied in name_list.

  In the Usage example above, the program will return string values associated with any occurrence of the keys 'display_name', 'description' and 'title'. The key name should be just the key immediately corresponding to the value or list (i.e., full path key names are not supported).

  The number of msgid's written out by babel when using the name_list option as given above, along with the sample JSON file below, is 1+22-3 occurrences. Note: the 22 is the number of matches returned by pybabel-json-md, but, the -3 is due to the fact that Version, Admin User and the Admin User description are each duplicated once and babel reports each as a single msgid. The 1 is the initial 'dummy' msgid written out by babel at the beginning of the pot file. 

Sample Metadef JSON File
------------------------

.. code-block:: json

  {
    "namespace": "OS::Software::Test",
    "display_name": "Test OS Software",
    "description": "Test software description (protected = false).",
    "visibility": "public",
    "protected": false,
    "resource_type_associations": [
        {
            "name": "OS::Glance::Image"
        },
        {
            "name": "OS::Cinder::Volume",
            "properties_target": "image"
        },
        {
            "name": "OS::Nova::Instance"
        }
    ],
    "objects": [
        {
            "name": "MySQL",
            "description": "MySQL software desc.",
            "properties": {
                "sw_database_mysql_version": {
                    "title": "Version",
                    "description": "The specific version of MySQL.",
                    "type": "string"
                },
                "sw_database_mysql_listen_port": {
                    "title": "Listen Port",
                    "description": "The configured TCP/IP port which MySQL listens...",
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 65535,
                    "default": 3606
                },
                "sw_database_mysql_admin": {
                    "title": "Admin User",
                    "description": "The primary user with privileges...",
                    "type": "string",
                    "default": "root"
                }
            }
        },
        {
            "name": "SQL Server",
            "description": "SQL Server is an RDBMS from MS.",
            "properties": {
                "sw_database_sqlserver_version": {
                    "title": "Version",
                    "description": "The specific version of Microsoft SQL Server.",
                    "type": "string"
                },
                "sw_database_sqlserver_edition": {
                    "title": "Edition",
                    "description": "SQL Server is available in multiple editions.",
                    "type": "string",
                    "default": "Express",
                    "enum": [
                        "Datacenter",
                        "Enterprise",
                        "Web",
                        "Express",
                        "Datawarehouse Appliance Edition"
                    ]
                },
                "sw_database_sqlserver_admin": {
                    "title": "Admin User",
                    "description": "The primary user with privileges...",
                    "type": "string",
                    "default": "sa"
                }
            }
        }
    ],
    "properties": {
        "guest_sockets": {
            "title": "vCPU Sockets",
            "description": "Preferred number of sockets to expose to the guest.",
            "type": "integer"
        },
        "guest_cores": {
            "title": "vCPU Cores",
            "description": "Preferred number of cores to expose to the guest.",
            "type": "integer"
        },
        "guest_threads": {
            "title": "vCPU Threads",
            "description": "Preferred number of threads to expose to the guest.",
            "type": "integer"
        }
    },
    "tags": [
        {"name": "tag1-test"},
        {"name": "tag2-test"}
    ]
  }
