OpenVZ executor for Sloth CI app extension that replaces the default executor and runs actions inside a given OpenVZ container.

Extension params::

    # Use the sloth_ci.ext.openvz_exec module.
    module: openvz_exec

    # Container name.
    container_name: foo

    # Container ID.
    # container_id: 123

If name is provided, ID is ignored. If name is not provided, ID is mandatory.


